# Marvel Rivals Rank Tracker

Track player rank changes in Marvel Rivals using the tracker.gg API. Sends Discord alerts when a player moves up or down in tier/division.

## Features
- Tracks specific IGN usernames
- Checks for tier/division changes only (not rank point shifts)
- Sends alerts to a Discord channel
- Fully automated and customizable

## Setup
1. Clone the repo and install Python if needed.
2. Copy `private_config.py.example` to `private_config.py` and fill in:
   - `TRACKER_API_KEY`
   - `DISCORD_WEBHOOK_URL`
3. Add IGN usernames to `tracked_players.json` like this:

```json
{
  "Miyagz": {
    "last_rank": "Unknown",
    "last_updated": "2025-04-19T00:00:00Z"
  }
}