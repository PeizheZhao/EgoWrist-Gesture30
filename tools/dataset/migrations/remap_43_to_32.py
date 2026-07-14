#!/usr/bin/env python3
"""Historical 43-to-32 label migration; always writes to a separate output tree."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

DELETE = {0, 14, 16, 17, 21, 34, 35}
MERGE = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 23: 15, 24: 15}
REMAP = {
    7: 3, 8: 4, 9: 5, 10: 6, 11: 7, 12: 8, 13: 9, 15: 10,
    18: 11, 19: 12, 20: 13, 22: 14, 25: 16, 26: 17, 27: 18,
    28: 19, 29: 20, 30: 21, 31: 22, 32: 23, 33: 24, 36: 25,
    37: 26, 38: 27, 39: 28, 40: 29, 41: 30, 42: 31,
}


def convert(path: Path, destination: Path) -> None:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    converted = []
    for row in rows:
        label = int(row["label"])
        if label in DELETE:
            continue
        label = MERGE.get(label, REMAP.get(label, label))
        converted.append({"begin": int(row["begin"]), "end": int(row["end"]), "label": label})
    merged = []
    for row in converted:
        if merged and row["label"] != 10 and merged[-1]["label"] == row["label"]:
            merged[-1]["end"] = row["end"]
        else:
            merged.append(row)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["begin", "end", "label"])
        writer.writeheader()
        writer.writerows(merged)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve() or args.output.exists():
        raise ValueError("Output must be a new, separate directory")
    files = sorted(args.input.glob("subject*/scene*/*.csv"))
    for path in files:
        convert(path, args.output / path.relative_to(args.input))
    print(f"Converted {len(files)} CSV files into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
