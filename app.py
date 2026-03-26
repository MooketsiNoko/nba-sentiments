import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from teams import get_standings, get_recent_games
from analysis import analyze_team_performance, get_team_stats
from sentiment import get_team_news, analyze_sentiment

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="NBA Sentiment Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Design System ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0a;
    color: #e8e8e8;
}
.main .block-container {
    padding: 2.5rem 3rem;
    max-width: 1400px;
}

/* ── Typography ── */
h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.04em;
}

/* ── Header ── */
.dash-header {
    border-bottom: 1px solid #2a0a0a;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}
.dash-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    letter-spacing: 0.06em;
    color: #ffffff;
    margin: 0;
    line-height: 1;
}
.dash-subtitle {
    color: #999;
    font-size: 0.85rem;
    margin-top: 0.4rem;
    font-weight: 300;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.red-accent {
    color: #c41230;
}

/* ── Section Labels ── */
.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.08em;
    color: #ffffff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #2a0a0a, transparent);
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #1a0505;
    border: 1px solid #1a0505;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 2.5rem;
}
.metric-card {
    background: #0f0f0f;
    padding: 1.4rem 1.6rem;
}
.metric-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #888;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #ffffff;
    letter-spacing: 0.04em;
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.78rem;
    color: #c41230;
    margin-top: 0.3rem;
    font-weight: 500;
}

/* ── Standings Table ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1a1a1a;
    border-radius: 4px;
    overflow: hidden;
}
[data-testid="stDataFrame"] table {
    background: #0f0f0f;
}

/* ── Charts ── */
[data-testid="stBarChart"] {
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-radius: 4px;
    padding: 1rem;
}

/* ── Multiselect Override ── */
[data-baseweb="tag"] {
    background-color: #1a0505 !important;
    border: 1px solid #c41230 !important;
    border-radius: 2px !important;
}
[data-baseweb="tag"] span {
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
}
[data-baseweb="select"] {
    background: #0f0f0f !important;
    border: 1px solid #1f1f1f !important;
}
[data-baseweb="popover"] {
    background: #111 !important;
}

/* ── Button ── */
[data-testid="baseButton-primary"] {
    background: #c41230 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    padding: 0.6rem 2rem !important;
    transition: background 0.2s ease !important;
}
[data-testid="baseButton-primary"]:hover {
    background: #8b0000 !important;
}

/* ── Sentiment Cards ── */
.s-card {
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-top: 3px solid #c41230;
    border-radius: 4px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.s-card.locked-in { border-top-color: #c41230; }
.s-card.mid-season { border-top-color: #8b3a3a; }
.s-card.cooked     { border-top-color: #3a0a0a; }

.s-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.s-team-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.05em;
    color: #ffffff;
}
.s-badge {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 2px;
}
.badge-locked  { background: #c41230; color: #fff; }
.badge-mid     { background: #3a1a1a; color: #c47070; border: 1px solid #5a2a2a; }
.badge-cooked  { background: #1a0505; color: #664444; border: 1px solid #2a0a0a; }

.s-outlook {
    color: #c8c8c8;
    font-size: 0.92rem;
    line-height: 1.7;
    margin-bottom: 0.8rem;
    font-weight: 300;
}
.s-keyfactor {
    font-size: 0.8rem;
    color: #888;
    padding-top: 0.8rem;
    border-top: 1px solid #1a1a1a;
}
.s-keyfactor strong {
    color: #c41230;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.72rem;
}
.s-stats {
    font-size: 0.75rem;
    color: #777;
    margin-top: 0.6rem;
    letter-spacing: 0.04em;
}
.s-confidence {
    font-size: 0.72rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Divider ── */
hr {
    border-color: #1a0505 !important;
    margin: 2rem 0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0f0f0f !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 4px !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    color: #777 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #c41230 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <p class="dash-title">NBA <span class="red-accent">Sentiment</span> Dashboard</p>
    <p class="dash-subtitle">Live standings · AI-powered team analysis · Performance analytics</p>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    df = get_standings()
    df = analyze_team_performance(df)
    return df

with st.spinner("Pulling live NBA data..."):
    df = load_data()

# ─── Metric Cards ──────────────────────────────────────────
best_record  = df.iloc[0]
best_offense = df.loc[df["ppg"].idxmax()]
best_defense = df.loc[df["opp_ppg"].idxmin()]
best_diff    = df.loc[df["point_diff"].idxmax()]

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Best Record</div>
        <div class="metric-value">{best_record['team'].replace(' ', '<br>')}</div>
        <div class="metric-sub">{int(best_record['wins'])}W — {int(best_record['losses'])}L</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Best Offense</div>
        <div class="metric-value">{best_offense['team'].replace(' ', '<br>')}</div>
        <div class="metric-sub">{best_offense['ppg']} PPG</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Best Defense</div>
        <div class="metric-value">{best_defense['team'].replace(' ', '<br>')}</div>
        <div class="metric-sub">{best_defense['opp_ppg']} OPP PPG</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Best Differential</div>
        <div class="metric-value">{best_diff['team'].replace(' ', '<br>')}</div>
        <div class="metric-sub">+{best_diff['point_diff']} per game</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Standings ─────────────────────────────────────────────
st.markdown('<div class="section-label">Full Standings</div>', unsafe_allow_html=True)

display_df = df[["team", "wins", "losses", "winPercent",
                 "ppg", "opp_ppg", "point_diff", "tier"]].copy()
display_df.columns = ["Team", "W", "L", "Win%", "PPG", "OPP PPG", "DIFF", "Tier"]

st.dataframe(display_df, use_container_width=True, hide_index=False, height=380)

st.divider()

# ─── Charts ────────────────────────────────────────────────
st.markdown('<div class="section-label">Performance Charts</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.caption("TOP 10 — POINT DIFFERENTIAL")
    top10_diff = df.nlargest(10, "point_diff")[["team", "point_diff"]].set_index("team")
    st.bar_chart(top10_diff, color="#c41230")

with chart_col2:
    st.caption("TOP 10 — POINTS PER GAME")
    top10_ppg = df.nlargest(10, "ppg")[["team", "ppg"]].set_index("team")
    st.bar_chart(top10_ppg, color="#8b0000")

st.divider()

# ─── Sentiment ─────────────────────────────────────────────
st.markdown('<div class="section-label">Team Sentiment Reports</div>',
            unsafe_allow_html=True)
st.caption("POWERED BY CLAUDE AI  ·  LIVE NEWS + TEAM STATS")

all_teams = df["team"].tolist()
default_teams = ["Oklahoma City Thunder", "Los Angeles Lakers", "Boston Celtics"]

selected_teams = st.multiselect(
    "Select teams:",
    options=all_teams,
    default=default_teams,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

if selected_teams:
    if st.button("Run Analysis", type="primary"):
        for team_name in selected_teams:
            stats = get_team_stats(df, team_name)
            if not stats:
                continue

            with st.spinner(f"Analyzing {team_name}..."):
                articles = get_team_news(team_name)
                sentiment_text = analyze_sentiment(team_name, articles, stats)

            # Parse
            sentiment = "MID SEASON"
            card_class = "mid-season"
            badge_class = "badge-mid"

            if "LOCKED IN" in sentiment_text:
                sentiment = "LOCKED IN"
                card_class = "locked-in"
                badge_class = "badge-locked"
            elif "COOKED" in sentiment_text:
                sentiment = "COOKED"
                card_class = "cooked"
                badge_class = "badge-cooked"

            outlook, key_factor, confidence = "", "", ""
            for line in sentiment_text.strip().split("\n"):
                if line.startswith("OUTLOOK:"):
                    outlook = line.replace("OUTLOOK:", "").strip()
                elif line.startswith("KEY FACTOR:"):
                    key_factor = line.replace("KEY FACTOR:", "").strip()
                elif line.startswith("CONFIDENCE:"):
                    confidence = line.replace("CONFIDENCE:", "").strip()

            st.markdown(f"""
            <div class="s-card {card_class}">
                <div class="s-card-header">
                    <span class="s-team-name">{team_name}</span>
                    <div>
                        <span class="s-badge {badge_class}">{sentiment}</span>
                    </div>
                </div>
                <p class="s-confidence">Confidence: {confidence}</p>
                <p class="s-outlook">{outlook}</p>
                <div class="s-keyfactor">
                    <strong>Key Factor</strong> — {key_factor}
                </div>
                <div class="s-stats">
                    {int(stats['wins'])}W-{int(stats['losses'])}L
                    &nbsp;·&nbsp; PPG: {stats['ppg']}
                    &nbsp;·&nbsp; DIFF: {stats['point_diff']:+.1f}
                    &nbsp;·&nbsp; {stats['tier']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            recent = get_recent_games(team_name)
            if recent:
                with st.expander(f"{team_name} — Recent Games"):
                    for g in recent:
                        st.write(f"**{g['matchup']}** · {g['status']}")
                        for t, s in g['scores'].items():
                            st.write(f"  {t}: {s}")

st.divider()
st.caption("DATA: ESPN API + NEWSAPI  ·  ANALYSIS: ANTHROPIC CLAUDE  ·  BUILT BY MOOKETSI NOKO")