#!/usr/bin/env python3
"""Remove class IDs and compact remaining IDs into a new annotation tree."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--remove", type=int, nargs="+", required=True)
    parser.add_argument("--class-count", type=int, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve() or args.output.exists():
        raise ValueError("Output must be a new, separate directory")
    removed = set(args.remove)
    remaining = [label for label in range(args.class_count) if label not in removed]
    mapping = {old: new for new, old in enumerate(remaining)}
    files = sorted(args.input.glob("subject*/scene*/*.csv"))
    for path in files:
        destination = args.output / path.relative_to(args.input)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with path.open(newline="", encoding="utf-8-sig") as source:
            rows = list(csv.DictReader(source))
        with destination.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=["begin", "end", "label"])
            writer.writeheader()
            for row in rows:
                label = int(row["label"])
                if label in mapping:
                    writer.writerow(
                        {"begin": int(row["begin"]), "end": int(row["end"]), "label": mapping[label]}
                    )
    print(f"Processed {len(files)} CSV files into {args.output}")
    print("mapping:", mapping)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
