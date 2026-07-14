#!/usr/bin/env python3
"""Build a canonical aggregate JSON file from the annotation CSV tree."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_root", type=Path)
    parser.add_argument("label_map", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite {args.output}; pass --force to replace it")

    with args.label_map.open(encoding="utf-8") as handle:
        label_map = json.load(handle)
    database: dict[str, dict] = {}
    for path in sorted(args.csv_root.glob("subject*/scene*/*.csv")):
        relative = path.relative_to(args.csv_root).with_suffix("").as_posix()
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["begin", "end", "label"]:
                raise ValueError(f"Unexpected CSV schema in {path}: {reader.fieldnames}")
            for index, row in enumerate(reader):
                database[f"{relative}_{index}"] = {
                    "annotations": {
                        "label": str(int(row["label"])),
                        "start_frame": str(int(row["begin"])),
                        "end_frame": str(int(row["end"])),
                    },
                }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump({"label_map": label_map, "database": database}, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Wrote {len(database)} annotations to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
