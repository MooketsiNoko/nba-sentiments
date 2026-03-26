import anthropic
import os
import requests
from dotenv import load_dotenv

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_team_news(team_name: str):
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={team_name} NBA&sortBy=publishedAt&pageSize=5"
        f"&language=en&apiKey={news_api_key}"
    )
    response = requests.get(url)
    data = response.json()

    articles = []
    for article in data.get("articles", []):
        if article.get("title") and article.get("description"):
            articles.append({
                "title": article["title"],
                "description": article.get("description", "")
            })
    return articles


def analyze_sentiment(team_name: str, articles: list, stats: dict):
    if not articles:
        return "No news available for sentiment analysis."

    headlines_text = "\n".join(
        [f"- {a['title']}: {a['description']}" for a in articles]
    )

    prompt = f"""You are an NBA analyst. Analyze the following news headlines and team stats
for the {team_name} and give a short, punchy sentiment report.

TEAM STATS:
- Record: {stats.get('wins', 0)}W - {stats.get('losses', 0)}L
- Win Rate: {stats.get('winPercent', 0)}
- Points Per Game (season total): {stats.get('pointsFor', 0)}
- Points Allowed (season total): {stats.get('pointsAgainst', 0)}

RECENT NEWS:
{headlines_text}

Give your response in EXACTLY this format:
SENTIMENT: <LOCKED IN (dominant/thriving), MID SEASON (average/inconsistent), or COOKED (struggling/falling apart)>
CONFIDENCE: <HIGH, MEDIUM, or LOW>
OUTLOOK: <2-3 punchy sentences max. Be direct, no fluff.>
KEY FACTOR: <The single most important thing affecting this team right now in one sentence.>
"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


if __name__ == "__main__":
    team = "Oklahoma City Thunder"
    stats = {"wins": 57, "losses": 16, "winPercent": 0.781,
             "pointsFor": 8658, "pointsAgainst": 7857}

    print(f"Fetching news for {team}...\n")
    articles = get_team_news(team)

    print(f"Found {len(articles)} articles. Analyzing sentiment...\n")
    result = analyze_sentiment(team, articles, stats)

    print("=== SENTIMENT ANALYSIS ===\n")
    print(result)