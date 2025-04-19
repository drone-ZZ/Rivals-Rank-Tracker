# Marvel Rivals Rank Tracker Bot (Tracker.gg + Discord)

import requests
import json
import time
from datetime import datetime

# === Load from private config ===
try:
    from private_config import TRACKER_API_KEY, DISCORD_WEBHOOK_URL
except ImportError:
    TRACKER_API_KEY = "your_tracker_gg_api_key_here"
    DISCORD_WEBHOOK_URL = "your_discord_webhook_url_here"

PLAYER_LIST_FILE = "tracked_players.json"
PLATFORM = "steam"  # or 'battle', 'xbl', 'psn' etc.

HEADERS = {
    "TRN-Api-Key": TRACKER_API_KEY
}

# === FUNCTIONS ===

def load_players():
    try:
        with open(PLAYER_LIST_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_players(data):
    with open(PLAYER_LIST_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def fetch_player_rank(username):
    url = f"https://public-api.tracker.gg/v2/marvel-rivals/standard/profile/{PLATFORM}/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        try:
            segments = data['data']['segments']
            for seg in segments:
                if seg['type'] == 'overview':
                    return seg['stats']['rank']['metadata']['tierName']
        except (KeyError, TypeError):
            print(f"[!] Couldn't find rank for {username}")
            return None
    else:
        print(f"[!] API Error for {username}: {response.status_code}")
        return None

def send_discord_alert(username, old_rank, new_rank):
    direction = "📈 up" if new_rank > old_rank else "📉 down"
    data = {
        "content": f"🎮 **{username}** ranked {direction}: **{old_rank} → {new_rank}**"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def check_all_players():
    players = load_players()
    for username, info in players.items():
        print(f"[Checking] {username}...")
        old_rank = info.get("last_rank", "Unknown")
        new_rank = fetch_player_rank(username)

        # Only send update if tier name changed
        if new_rank and new_rank != old_rank:
            old_tier = old_rank.split()[0] if old_rank != "Unknown" else None
            new_tier = new_rank.split()[0]
            old_division = old_rank.split()[1] if old_rank != "Unknown" and len(old_rank.split()) > 1 else None
            new_division = new_rank.split()[1] if len(new_rank.split()) > 1 else None

            if old_tier != new_tier or old_division != new_division:
                print(f"[Update] {username} rank changed: {old_rank} → {new_rank}")
                send_discord_alert(username, old_rank, new_rank)
                players[username]["last_rank"] = new_rank
                players[username]["last_updated"] = datetime.utcnow().isoformat()

    save_players(players)

# === MAIN ===
if __name__ == "__main__":
    check_all_players()
