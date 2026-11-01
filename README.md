🌊 Tsunami Bets

Automated sports betting research for NFL and NBA. It finds plus-money bets backed by real information, scores them, builds parlays, and sends the report to Notion and email.

Research only. The system never places bets, logs in to sportsbooks, or submits forms. Nothing is guaranteed; all risk is mine.

How it works
GitHub Action (this repo)          Claude scheduled task               You
─────────────────────────          ─────────────────────               ───
Pulls odds from The Odds API  ──►  Reads the odds file, researches  ──►  Email summary
~25 min before each report         stats, injuries and models,          + full Notion page
Saves odds/{nba|nfl}_latest.json   scores bets, builds parlays
Odds pull (GitHub). fetch_odds.py runs on a schedule, gets game lines and player props from DraftKings, FanDuel, BetMGM, ESPN BET and others, and commits the snapshot to odds/.
Report (Claude). A scheduled task clones this repo, reads the snapshot, does the research, and scores every bet.
Delivery. A full report is added as a sub-page of Tsunami Bets Reports in Notion, and a short phone-friendly summary is emailed.
Schedule (Eastern Time)
What	When	Odds pull	Report
NBA	Every day	5:15 p.m.	5:40 p.m.
NFL Sunday	Sundays	10:15 a.m.	10:40 a.m.
NFL Monday / Thursday night	Mon & Thu	7:15 p.m.	7:40 p.m.
Credit check	Wednesdays	—	8:47 p.m.

No games = no report and no credits used.

Reading the report
The three boards
Board	What qualifies	Use it for
Plus board (main)	Odds +100 or longer, Edge ≥ +4, Hit % ≥ 30%, backed by a model or 2+ stats	Main bets
Long shot board	Odds +300 or longer, Edge ≥ +5, Hit % ≥ 15%	Small, high-payout bets
Anchors	Minus odds, Hit % ≥ 70%, Edge ≥ 0	Parlay pieces only, never alone
Key numbers
Hit %: estimated chance the bet wins. Starts from a model (Dimers, ESPN/Mike Clay, FTN, numberFire) or the no-vig line, then research adjustments (max ±5), injury boost (shown separately) and external factors (max ±3).
Implied %: chance the odds imply. −X → X/(X+100); +X → 100/(X+100).
Edge: Hit % − Implied %. Positive = the price looks better than the risk.
Hit freq (last 20): how often the player cleared this exact line, e.g. 13/20. Shown for context only; it does not change Hit %.
🔺 Injury boost: a teammate is out and this player gains volume.
"Line has caught up": 5+ straight hits and the book has already raised the line.
Parlays
Grouped by start time (NFL: Sunday early / Sunday late / weekday; NBA: early / middle / late).
Every parlay is priced at one book only (DraftKings first). Never mix books.
Combined Hit % = legs' Hit % multiplied together.
Other sections
Near misses: bets that almost qualified and what news would change them.
Lines needed: good matchups with no verified price. Paste the line to Claude and it will score it ("user-provided").
Fun bet (NFL): Patriots and fantasy roster parlay, labeled "fun only".
Run notes: when odds were pulled and which sources failed. Check this first.
Before you bet: checklist
Read Run notes. If the odds file was stale or missing, re-check prices in the app.
Re-check injury status for every leg. News can drop after the report runs.
Confirm the price in DraftKings still matches (or beats) the report.
Treat Anchors as parlay pieces only.
Common tasks
I want to…	Do this
Run a report now	In Claude, ask to run the Tsunami Bets NFL or NBA scheduled task.
Pull fresh odds by hand	GitHub → Actions → Fetch odds → Run workflow → type nba or nfl.
Change which props are pulled	GitHub → Settings → Secrets and variables → Actions → Variables. Set NBA_PROP_MARKETS or NFL_PROP_MARKETS (comma-separated, e.g. player_points,player_rebounds). Delete to go back to defaults.
Score lines I found myself	Paste them into Claude with the player, line, odds and book.
Pause everything	Turn off the scheduled tasks in Claude and disable the workflow in GitHub Actions.
Change the rules or prompt	Ask Claude to update the Tsunami Bets prompts; copies live in the Fun Side Projects project (tsunami-bets/).
Odds API credits
Free plan: 500 credits/month. Game lines = 3 credits per pull; props = 1 credit per game per prop type.
Defaults: NBA points props, NFL anytime-TD props. Estimated ~420 credits/month with both sports.
The weekly credit check logs usage to Odds API credit log in Notion and emails if credits run low, run out, or a pull is missed.
If credits run out, reports still run and fall back to web-searched lines (flagged in Run notes). GitHub also emails when a pull fails.
Season	Suggested prop types
Nov–Mar (both sports)	Defaults
NBA playoffs (mid Apr–Jun)	player_points,player_rebounds,player_assists
NFL only (Sep–Oct)	player_anytime_td,player_reception_yds,player_receptions,player_rush_yds
Rules the system always follows
Plus-money bets backed by real information come first. Risk is fine when the research supports it.
No prediction markets or exchanges (Kalshi, Polymarket, Novig, etc.) for odds or probabilities.
DraftKings preferred; every price is labeled with its book. No-vig math always uses both sides from the same book.
Real stats and real lines only. Estimates are labeled ESTIMATE. Small samples (under 2 games) are flagged.
All math is done in code.
Maintenance calendar
Mid-December: NFL adds Saturday games → add a Saturday odds pull and report.
March 8 (daylight saving): GitHub runs on UTC, so odds pulls shift an hour later → move the times in .github/workflows/odds.yml back an hour.
Start of each month: read the credit summary email and adjust prop types if needed.
Repo files
File	Purpose
fetch_odds.py	Pulls odds from The Odds API and saves a snapshot.
.github/workflows/odds.yml	The pull schedule and manual Run workflow button.
odds/nba_latest.json, odds/nfl_latest.json	Latest snapshots (history kept in git).
Secret ODDS_API_KEY	API key, stored in GitHub Secrets. Never commit it.
