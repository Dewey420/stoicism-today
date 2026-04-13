#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Primary source: metabismuth tarot dataset
SOURCE_URL = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/tarot.json"

def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    with urlopen(SOURCE_URL, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    # Normalize into your site's simpler format
    cards_out = []
    for card in payload:
        name = card.get("name", "").strip()
        arcana = "Major" if card.get("arcana") == "Major Arcana" else "Minor"

        # Try to extract useful meanings safely from available fields
        upright_parts = []
        if card.get("fortune_telling"):
            upright_parts.append(card["fortune_telling"][0])
        if card.get("meanings", {}).get("light"):
            upright_parts.append(card["meanings"]["light"][0])

        reversed_parts = []
        if card.get("meanings", {}).get("shadow"):
            reversed_parts.append(card["meanings"]["shadow"][0])

        upright = " ".join(upright_parts).strip() or "Meaning unavailable."
        reversed_meaning = " ".join(reversed_parts).strip() or "Reversed meaning unavailable."

        cards_out.append({
            "name": name,
            "arcana": arcana,
            "upright": upright,
            "reversed": reversed_meaning,
            "suit": card.get("suit"),
            "rank": card.get("rank"),
            "keywords": card.get("keywords", []),
        })

    out_path = DATA / "tarot_cards.json"
    out_path.write_text(
        json.dumps(cards_out, indent=2, ensure_ascii=False) + "\\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(cards_out)} cards to {out_path}")

if __name__ == "__main__":
    main()
