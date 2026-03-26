import pandas as pd


def analyze_team_performance(df: pd.DataFrame):
    """Add derived analytics columns to the standings dataframe."""

    # Point differential per game (standings totals, ~73 games played)
    df["games_played"] = df["wins"] + df["losses"]
    df["ppg"] = (df["pointsFor"] / df["games_played"]).round(1)
    df["opp_ppg"] = (df["pointsAgainst"] / df["games_played"]).round(1)
    df["point_diff"] = (df["ppg"] - df["opp_ppg"]).round(1)

    # Tier classification
    def classify_tier(row):
        if row["winPercent"] >= 0.650:
            return "🔥 Elite"
        elif row["winPercent"] >= 0.500:
            return "💪 Playoff Contender"
        elif row["winPercent"] >= 0.380:
            return "😬 Bubble"
        else:
            return "💀 Cooked"

    df["tier"] = df.apply(classify_tier, axis=1)

    return df


def get_team_stats(df: pd.DataFrame, team_name: str):
    """Pull a single team's stats as a dict."""
    row = df[df["team"] == team_name]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def print_analysis(df: pd.DataFrame):
    """Print a clean terminal breakdown."""
    print("=== NBA PERFORMANCE ANALYSIS ===\n")

    for tier in ["🔥 Elite", "💪 Playoff Contender", "😬 Bubble", "💀 Cooked"]:
        tier_df = df[df["tier"] == tier]
        if tier_df.empty:
            continue
        print(f"{tier}")
        print("-" * 60)
        for _, row in tier_df.iterrows():
            print(
                f"  {row['team']:<30} "
                f"{int(row['wins'])}W-{int(row['losses'])}L  "
                f"PPG: {row['ppg']}  "
                f"DIFF: {row['point_diff']:+.1f}"
            )
        print()


if __name__ == "__main__":
    from teams import get_standings

    df = get_standings()
    df = analyze_team_performance(df)
    print_analysis(df)

    print("\n=== OKC DEEP DIVE ===\n")
    stats = get_team_stats(df, "Oklahoma City Thunder")
    if stats:
        for key, value in stats.items():
            print(f"  {key}: {value}")