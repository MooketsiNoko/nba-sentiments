import pandas as pd
from teams import get_standings, get_recent_games
from analysis import analyze_team_performance, get_team_stats, print_analysis
from sentiment import get_team_news, analyze_sentiment

# Teams to analyze — customize this
WATCHLIST = [
    "Oklahoma City Thunder",
    "Los Angeles Lakers",
    "Charlotte Hornets"
]


def run_dashboard():
    print("⏳ Fetching NBA standings...\n")
    df = get_standings()
    df = analyze_team_performance(df)

    print_analysis(df)

    print("=" * 60)
    print("🔍 TEAM SENTIMENT REPORTS")
    print("=" * 60)

    for team_name in WATCHLIST:
        stats = get_team_stats(df, team_name)
        if not stats:
            print(f"\n❌ Could not find stats for {team_name}")
            continue

        print(f"\n📍 {team_name} ({stats['tier']})")
        print(f"   Record: {int(stats['wins'])}W-{int(stats['losses'])}L  |  "
              f"PPG: {stats['ppg']}  |  DIFF: {stats['point_diff']:+.1f}")
        print("-" * 60)

        articles = get_team_news(team_name)
        sentiment = analyze_sentiment(team_name, articles, stats)
        print(sentiment)

        recent = get_recent_games(team_name)
        if recent:
            print("\n🏀 RECENT GAMES:")
            for g in recent:
                print(f"  {g['matchup']} — {g['status']}")
                for t, s in g['scores'].items():
                    print(f"    {t}: {s}")

        print()


if __name__ == "__main__":
    run_dashboard()