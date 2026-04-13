#!/usr/bin/env python3
from __future__ import annotations
import json
import requests
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def get_moon():
    try:
        res = requests.get("https://api.farmsense.net/v1/moonphases/?d=0")
        data = res.json()[0]
        phase = data["Phase"]
        illumination = round(float(data["Illumination"]) * 100)
        return f"🌑 {phase}\n🌕 Illumination: {illumination}%\n→ Flow with the cycle."
    except:
        return "🌑 Moon data unavailable"

def draw_tarot():
    cards = [
        ("The Magician", "You already have the tools. Use them."),
        ("The Fool", "A new path opens. Step forward."),
        ("The Hermit", "Seek inward clarity."),
        ("The Emperor", "Take control. Build structure."),
        ("The High Priestess", "Trust your intuition.")
    ]
    card = random.choice(cards)
    return f"{card[0]}\n→ {card[1]}"
def get_stoic_quote():
    quotes = [
        "“You have power over your mind—not outside events. Realize this, and you will find strength.”\\n— Marcus Aurelius",
        "“First say to yourself what you would be; and then do what you have to do.”\\n— Epictetus",
        "“Wherever there is a human being, there is an opportunity for kindness.”\\n— Seneca",
        "“The soul becomes dyed with the color of its thoughts.”\\n— Marcus Aurelius",
        "“Luck is what happens when preparation meets opportunity.”\\n— Seneca"
    ]
    return random.choice(quotes)
    def get_holidays(today):
    holiday_map = {
        (4, 13): [
            "🍑 National Peach Cobbler Day",
            "🔤 National Scrabble Day",
            "🥪 Make Lunch Count Day"
        ],
        (4, 14): [
            "🌿 National Gardening Day",
            "🧀 National Pecan Day"
        ],
        (4, 15): [
            "💸 Tax Day",
            "🎨 World Art Day"
        ]
    }

    items = holiday_map.get((today.month, today.day), ["📝 No holidays entered yet"])
    return "\\n".join(items)
def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def rotate_playlist():
    playlist_path = DATA / "playlist.json"
    playlist = load_json(playlist_path)
    tracks = playlist["tracks"]
    idx = (playlist.get("lastSelectedIndex", -1) + 1) % len(tracks)
    playlist["lastSelectedIndex"] = idx
    save_json(playlist_path, playlist)
    return tracks[idx]

def main():
    briefing_path = DATA / "briefing.json"
    briefing = load_json(briefing_path)
    track = rotate_playlist()
    today = datetime.now(timezone.utc).astimezone()
    try:
        pretty = today.strftime("%B %-d, %Y")
    except ValueError:
        pretty = today.strftime("%B %d, %Y").replace(" 0", " ")
    briefing["date"] = today.strftime("%Y-%m-%d")
    briefing["weekday"] = today.strftime("%A")
    briefing["title"] = f"🏛️🌅 STOICISM TODAY // {pretty.upper()}"
    briefing["tagline"] = "Auto-updated shell active."
    briefing["holidays"] = get_holidays(today)
    briefing["moon"] = get_moon()
    briefing["tarot"] = draw_tarot()
    briefing["quote"] = get_stoic_quote()
    briefing["music"] = f"From your playlist:\n🎵 “{track['title']}” — {track['artist']}\n→ Auto-rotated from your playlist source."
    briefing["question"] = "What requires my disciplined attention today?"
    save_json(briefing_path, briefing)
    widget = {
        "gv_holidays": briefing["holidays"],
        "gv_moon": briefing["moon"],
        "gv_tarot": briefing["tarot"],
        "gv_music": briefing["music"],
        "gv_directive": briefing["directive"],
        "gv_action": briefing["action"],
        "gv_quote": briefing["quote"],
        "gv_question": briefing["question"],
    }
    save_json(DATA / "widget_fields.json", widget)

if __name__ == "__main__":
    main()
