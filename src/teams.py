import requests
import pandas as pd

def get_standings():
    url = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"
    response = requests.get(url)
    data = response.json()

    teams = []
    for conference in data.get("children", []):
        for entry in conference.get("standings", {}).get("entries", []):
            team = entry["team"]
            stats = {s["name"]: s.get("value", s.get("displayValue", 0)) for s in entry.get("stats", [])}
            teams.append({
                "team": team["displayName"],
                "abbreviation": team["abbreviation"],
                "wins": int(stats.get("wins", 0)),
                "losses": int(stats.get("losses", 0)),
                "winPercent": round(float(stats.get("winPercent", 0)), 3),
                "pointsFor": round(float(stats.get("pointsFor", 0)), 1),
                "pointsAgainst": round(float(stats.get("pointsAgainst", 0)), 1),
            })

    df = pd.DataFrame(teams)
    df = df.sort_values("winPercent", ascending=False).reset_index(drop=True)
    df.index += 1  # rank starts at 1
    return df


def get_recent_games(team_name: str):
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    response = requests.get(url)
    data = response.json()

    games = []
    for event in data.get("events", []):
        competitors = event["competitions"][0]["competitors"]
        team_names = [c["team"]["displayName"] for c in competitors]

        if team_name in team_names:
            scores = {c["team"]["displayName"]: c["score"] for c in competitors}
            status = event["status"]["type"]["description"]
            games.append({
                "matchup": " vs ".join(team_names),
                "scores": scores,
                "status": status
            })

    return games


if __name__ == "__main__":
    print("=== NBA STANDINGS ===\n")
    df = get_standings()
    print(df[["team", "wins", "losses", "winPercent", "pointsFor", "pointsAgainst"]].to_string())

    print("\n=== OKC RECENT GAMES ===\n")
    games = get_recent_games("Oklahoma City Thunder")
    if games:
        for g in games:
            print(f"{g['matchup']} — {g['status']}")
            for team, score in g['scores'].items():
                print(f"  {team}: {score}")
    else:
        print("No recent games found.")