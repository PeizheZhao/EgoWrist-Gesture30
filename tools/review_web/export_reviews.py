#!/usr/bin/env python3
"""Export Web review decisions from JSON to a stable CSV table."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviews", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite {args.output}; pass --force")
    with args.reviews.open(encoding="utf-8") as handle:
        reviews = json.load(handle)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["video", "status", "notes"])
        writer.writeheader()
        for video, review in sorted(reviews.items()):
            writer.writerow(
                {"video": video, "status": review.get("status", ""), "notes": review.get("notes", "")}
            )
    print(f"Exported {len(reviews)} reviews to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
