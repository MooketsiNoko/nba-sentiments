# NBA Sentiment Dashboard

A live NBA analytics dashboard that combines real-time standings, 
pandas-powered performance analysis, and AI-generated team sentiment 
reports — all in a clean Streamlit web interface.

## What it does

- Pulls live NBA standings and scores via ESPN's API
- Calculates per-game stats and classifies all 30 teams into 
  performance tiers using pandas
- Fetches team-specific news via NewsAPI
- Uses Claude (Anthropic) to generate a sentiment report and 
  confidence rating per team
- Visualizes everything in a dark-themed Streamlit dashboard 
  with bar charts, a full standings table, and sentiment cards

## Tech Stack

- **Python** — core logic
- **pandas** — performance calculations and team tier classification
- **Streamlit** — interactive web dashboard
- **Anthropic Claude API** — sentiment analysis and team outlook generation
- **ESPN API** — live standings and scores (no key required)
- **NewsAPI** — team-specific news headlines

## Setup

1. Clone the repo
```bash
   git clone https://github.com/MooketsiNoko/nba-sentiment-dashboard.git
   cd nba-sentiment-dashboard
```

2. Create a virtual environment and install dependencies
```bash
   python -m venv venv
   venv\Scripts\activate
   pip install requests pandas python-dotenv anthropic streamlit
```

3. Create a `.env` file with your API keys
```
   NEWS_API_KEY=your_news_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
```

4. Run the dashboard
```bash
   streamlit run app.py
```

## Project Structure
```
nba-sentiment-dashboard/
├── src/
│   ├── teams.py        # ESPN API — live standings and scores
│   ├── analysis.py     # pandas — performance metrics and tier classification
│   ├── sentiment.py    # NewsAPI + Claude — sentiment analysis
│   └── main.py         # terminal version
├── app.py              # Streamlit dashboard
├── .env                # API keys (not committed)
└── README.md
```

## Dashboard Sections

**League Snapshot** — four headline metrics: best record, best offense, 
best defense, best point differential

**Full Standings** — sortable table of all 30 teams with win%, PPG, 
OPP PPG, point differential, and tier classification

**Performance Charts** — top 10 teams by point differential and PPG

**Team Sentiment Reports** — select any teams and run AI analysis. 
Each card shows a LOCKED IN / MID SEASON / COOKED rating, confidence 
level, AI-written outlook, and key factor driving the team's trajectory
