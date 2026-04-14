#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DEFAULT_TIMEZONE = "America/Chicago"

MAJOR_PROMPTS = {
    "The Fool": "Begin cleanly. Courage is useful; recklessness is just noisy.",
    "The Magician": "Use what is already in your hands before asking for more.",
    "The High Priestess": "Let silence finish its sentence before you answer.",
    "The Empress": "Build the conditions where good things can actually grow.",
    "The Emperor": "Choose structure over mood. Discipline is the throne.",
    "The Hierophant": "Honor the practice. Wisdom gets stronger when repeated.",
    "The Lovers": "Align choice with value, not appetite.",
    "The Chariot": "Steer the force. Momentum without command is just drift.",
    "Strength": "Meet pressure with restraint. Soft control still counts.",
    "The Hermit": "Step back far enough to hear what is true.",
    "Wheel of Fortune": "Accept the turn. Your response is still yours.",
    "Justice": "Let the facts stand upright before you judge them.",
    "The Hanged Man": "Change the angle before forcing the outcome.",
    "Death": "Release what has already finished its work.",
    "Temperance": "Blend patience with action. Extremes are hungry liars.",
    "The Devil": "Name the chain plainly. That is where freedom starts.",
    "The Tower": "When false structure falls, do not rebuild the lie.",
    "The Star": "Protect hope by giving it a practical next step.",
    "The Moon": "Move carefully through uncertainty. Not every shadow is a sign.",
    "The Sun": "Let clarity make you generous, not careless.",
    "Judgement": "Answer the call without dragging every old version of yourself along.",
    "The World": "Complete the circle. Integration beats endless striving.",
}

SUIT_LENSES = {
    "Cups": "emotion, intuition, and clean-hearted attention",
    "Swords": "thought, truth, and disciplined judgment",
    "Wands": "will, courage, and directed energy",
    "Pentacles": "body, work, resources, and practical stewardship",
}

RANK_PROMPTS = {
    "1": "Start with one clear intention.",
    "2": "Choose deliberately; split attention weakens the day.",
    "3": "Let the right alliance strengthen the work.",
    "4": "Stabilize before you expand.",
    "5": "Treat friction as information, not identity.",
    "6": "Restore balance through a concrete act.",
    "7": "Hold your ground without turning rigid.",
    "8": "Practice the skill in front of you.",
    "9": "Notice what your effort has earned, then guard it wisely.",
    "10": "Finish the cycle without making the burden sacred.",
    "11": "Stay curious. Beginner energy can still be disciplined.",
    "12": "Move with devotion, but keep your hands on the reins.",
    "13": "Lead with mature care, not performance.",
    "14": "Master yourself first; the rest can follow.",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def select_next_playlist_track():
    playlist_path = DATA / "playlist.json"
    playlist = load_json(playlist_path)
    tracks = playlist["tracks"]
    if not tracks:
        raise ValueError("playlist.json must include at least one track")

    idx = (playlist.get("lastSelectedIndex", -1) + 1) % len(tracks)
    playlist["lastSelectedIndex"] = idx
    return tracks[idx], playlist


def briefing_now() -> datetime:
    timezone_name = os.getenv("BRIEFING_TIMEZONE", DEFAULT_TIMEZONE)
    try:
        return datetime.now(ZoneInfo(timezone_name))
    except ZoneInfoNotFoundError:
        return datetime.now().astimezone()


def format_pretty_date(value: datetime) -> str:
    try:
        return value.strftime("%B %-d, %Y")
    except ValueError:
        return value.strftime("%B %d, %Y").replace(" 0", " ")


def stable_index(seed: str, item_count: int) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % item_count


def draw_tarot_card(date_key: str) -> dict:
    tarot_path = DATA / "tarot_cards.json"
    if not tarot_path.exists():
        raise FileNotFoundError(
            "Missing data/tarot_cards.json. Run python scripts/sync_tarot_source.py first."
        )

    deck = load_json(tarot_path)
    cards = deck.get("cards", [])
    if not cards:
        raise ValueError("data/tarot_cards.json does not contain any cards")

    return cards[stable_index(f"Stoicism Today tarot {date_key}", len(cards))]


def tarot_prompt(card: dict) -> str:
    if card.get("arcana") == "Major Arcana":
        return MAJOR_PROMPTS.get(
            card["name"],
            "Meet the symbol with discipline, then choose the next right act.",
        )

    rank = RANK_PROMPTS.get(str(card.get("number")), "Choose the next disciplined move.")
    lens = SUIT_LENSES.get(card.get("suit"), "the work immediately in front of you")
    return f"{rank} Apply it through {lens}."


def format_tarot(card: dict) -> str:
    if card.get("suit"):
        detail = f"{card['suit']} • {card['arcana']} • {card['number']}"
    else:
        detail = f"{card['arcana']} • {card['number']}"

    return f"{card['name']}\n{detail}\n→ {tarot_prompt(card)}"


def tarot_question(card: dict) -> str:
    if card.get("arcana") == "Major Arcana":
        return f"Where is {card['name']} asking me for a cleaner, braver response today?"

    suit_questions = {
        "Cups": "What feeling needs discipline instead of drama today?",
        "Swords": "What thought needs to be tested against reality today?",
        "Wands": "Where should I aim my fire instead of scattering it?",
        "Pentacles": "What practical responsibility deserves my best attention today?",
    }
    return suit_questions.get(card.get("suit"), "What requires my disciplined attention today?")


def format_music(track: dict) -> str:
    note = track.get("note", "Auto-rotated from your playlist source.")
    return f"From your playlist:\n🎵 “{track['title']}” — {track['artist']}\n→ {note}"


def ensure_briefing_defaults(briefing: dict) -> None:
    briefing.setdefault("mode", "🏛️ The Daily Practice")
    briefing.setdefault("tagline", "Discipline. Clarity. Small moves.")
    briefing.setdefault("holidays", "📝 Holiday source pending.")
    briefing.setdefault("moon", "🌑 Moon source pending.")
    briefing.setdefault("current", "☽ Daily current pending.")
    briefing.setdefault("sigil", {"glyph": "☽", "meaning": "→ Observe. Reflect. Do not force."})
    briefing.setdefault("directive", "Notice what is yours to govern.")
    briefing.setdefault("action", "📝 Choose one disciplined act and do it cleanly.")
    briefing.setdefault("persona", "🏛️ PERSONA — THE PRACTITIONER\nClear eyes\nSteady hands\nNo wasted motion")
    briefing.setdefault(
        "quote",
        "“You have power over your mind—not outside events. Realize this, and you will find strength.”\n— Marcus Aurelius",
    )


def build_widget_payload(briefing: dict) -> dict:
    return {
        "gv_holidays": briefing["holidays"],
        "gv_moon": briefing["moon"],
        "gv_tarot": briefing["tarot"],
        "gv_music": briefing["music"],
        "gv_directive": briefing["directive"],
        "gv_action": briefing["action"],
        "gv_quote": briefing["quote"],
        "gv_question": briefing["question"],
    }


def main():
    briefing_path = DATA / "briefing.json"
    briefing = load_json(briefing_path)
    ensure_briefing_defaults(briefing)

    today = briefing_now()
    date_key = today.strftime("%Y-%m-%d")
    pretty = format_pretty_date(today)
    tarot_card = draw_tarot_card(date_key)
    track, playlist = select_next_playlist_track()

    briefing["date"] = today.strftime("%Y-%m-%d")
    briefing["weekday"] = today.strftime("%A")
    briefing["title"] = f"🏛️🌅 STOICISM TODAY // {pretty.upper()}"
    briefing["tarot"] = format_tarot(tarot_card)
    briefing["tarotCard"] = tarot_card
    briefing["music"] = format_music(track)
    briefing["question"] = tarot_question(tarot_card)

    save_json(briefing_path, briefing)
    save_json(DATA / "widget_fields.json", build_widget_payload(briefing))
    save_json(DATA / "playlist.json", playlist)

if __name__ == "__main__":
    main()
