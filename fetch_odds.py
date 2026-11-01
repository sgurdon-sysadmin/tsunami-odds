"""Pull DraftKings/FanDuel odds from The Odds API and save a snapshot for Tsunami Bets.
Usage: python fetch_odds.py nba|nfl   (needs ODDS_API_KEY env var)
Credit cost per call = number of markets (all books below count as 1 region-group).
"""
import json, os, sys, datetime, urllib.request, urllib.parse

SPORTS = {"nba": "basketball_nba", "nfl": "americanfootball_nfl"}
BOOKS = "draftkings,fanduel,betmgm,caesars,espnbet,fanatics"   # <=10 books = 1 credit per market
GAME_MARKETS = "h2h,spreads,totals"
# Lean defaults fit the free 500-credit plan. Add markets via repo variables on a paid plan.
DEFAULT_PROPS = {"nba": "player_points", "nfl": "player_anytime_td"}

def get(path, **params):
    params["apiKey"] = os.environ["ODDS_API_KEY"]
    url = f"https://api.the-odds-api.com/v4{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        left = r.headers.get("x-requests-remaining")
        return json.load(r), left

def main(sport):
    key = SPORTS[sport]
    props = os.environ.get(f"{sport.upper()}_PROP_MARKETS") or DEFAULT_PROPS[sport]
    now = datetime.datetime.now(datetime.timezone.utc)
    games, left = get(f"/sports/{key}/odds", regions="us", bookmakers=BOOKS,
                      markets=GAME_MARKETS, oddsFormat="american")
    # Only this run's slate: games starting in the next 16 hours (saves credits)
    horizon = now + datetime.timedelta(hours=16)
    games = [g for g in games if now < datetime.datetime.fromisoformat(g["commence_time"].replace("Z", "+00:00")) < horizon]
    for g in games:
        try:
            ev, left = get(f"/sports/{key}/events/{g['id']}/odds", bookmakers=BOOKS,
                           markets=props, oddsFormat="american")
            g["props"] = ev.get("bookmakers", [])
        except Exception as e:  # keep going if one game fails
            g["props_error"] = str(e)
    out = {"sport": sport, "fetched_at": now.isoformat(), "credits_remaining": left,
           "books": BOOKS, "prop_markets": props, "games": games}
    os.makedirs("odds", exist_ok=True)
    with open(f"odds/{sport}_latest.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"{sport}: {len(games)} games, credits left {left}")

if __name__ == "__main__":
    main(sys.argv[1])
