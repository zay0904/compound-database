"""
Export the entire SQLite database to a JSON file that your static
website can load with fetch(). Run this any time the data changes.

Usage:
    python export_json.py
    # writes compounds.json to the current directory
"""
from __future__ import annotations

import json
from pathlib import Path

from src.queries import search


def main() -> None:
    rows = search("", limit=10000)
    out = Path("compounds.json")
    out.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"✓ Wrote {len(rows)} compounds to {out.resolve()}")


if __name__ == "__main__":
    main()