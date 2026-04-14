#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DEFAULT_SOURCE_URL = (
    "https://raw.githubusercontent.com/metabismuth/tarot-json/master/tarot-images.json"
)
IMAGE_BASE_URL = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards"
EXPECTED_CARD_COUNT = 78


def load_json_source(source: str) -> dict:
    if source.startswith(("http://", "https://")):
        request = Request(source, headers={"User-Agent": "Stoicism-Today/1.0"})
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    return json.loads(Path(source).read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "card"


def normalize_card(card: dict, index: int) -> dict:
    for field in ("name", "number", "arcana"):
        if field not in card:
            raise ValueError(f"Card #{index + 1} is missing required field: {field}")

    name = str(card["name"]).strip()
    number = str(card["number"]).strip()
    arcana = str(card["arcana"]).strip()
    suit = card.get("suit")
    image_name = card.get("img")

    if not name:
        raise ValueError(f"Card #{index + 1} has a blank name")
    if arcana not in {"Major Arcana", "Minor Arcana"}:
        raise ValueError(f"Card {name!r} has unexpected arcana: {arcana!r}")
    if arcana == "Minor Arcana" and not suit:
        raise ValueError(f"Minor Arcana card {name!r} is missing a suit")

    card_id = Path(image_name).stem if image_name else slugify(name)
    normalized = {
        "id": card_id,
        "sourceIndex": index,
        "name": name,
        "number": number,
        "arcana": arcana,
        "suit": str(suit).strip() if suit else None,
    }

    if image_name:
        normalized["image"] = {
            "filename": str(image_name),
            "url": f"{IMAGE_BASE_URL}/{image_name}",
        }

    return normalized


def normalize_deck(raw: dict, source_url: str) -> dict:
    cards = raw.get("cards")
    if not isinstance(cards, list):
        raise ValueError("Tarot source did not include a top-level cards array")

    normalized_cards = [normalize_card(card, index) for index, card in enumerate(cards)]
    if len(normalized_cards) != EXPECTED_CARD_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_CARD_COUNT} tarot cards, got {len(normalized_cards)}"
        )

    names = [card["name"] for card in normalized_cards]
    ids = [card["id"] for card in normalized_cards]
    if len(set(names)) != len(names):
        raise ValueError("Tarot source contains duplicate card names")
    if len(set(ids)) != len(ids):
        raise ValueError("Tarot source contains duplicate card ids")

    return {
        "description": "Normalized Rider-Waite-Smith tarot deck for Stoicism Today.",
        "source": {
            "name": "metabismuth/tarot-json",
            "url": source_url,
            "license": "MIT",
            "imageBaseUrl": IMAGE_BASE_URL,
        },
        "cardCount": len(normalized_cards),
        "cards": normalized_cards,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync the Stoicism Today tarot deck from an external JSON source."
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE_URL,
        help="Tarot JSON source URL or local file path.",
    )
    parser.add_argument(
        "--output",
        default=str(DATA / "tarot_cards.json"),
        help="Destination path for the normalized tarot deck.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)

    try:
        raw = load_json_source(args.source)
        deck = normalize_deck(raw, args.source)
        save_json(output, deck)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"Tarot sync failed: {exc}", file=sys.stderr)
        return 1

    print(f"Synced {deck['cardCount']} tarot cards to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
