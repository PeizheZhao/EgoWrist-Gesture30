#!/usr/bin/env python3
"""Regenerate balanced annotations without modifying the canonical input."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


def split_intervals(data: dict, interval: int = 8) -> dict:
    result = copy.deepcopy(data)
    source = data["database"]
    output = result["database"]
    for key, value in list(source.items()):
        start = int(value["annotations"]["start_frame"])
        end = int(value["annotations"]["end_frame"])
        length = end - start
        if length <= interval * 2:
            continue
        del output[key]
        parts = int(length / interval)
        for index in range(parts):
            part_start = start + index * interval
            part_end = end if index == parts - 1 else part_start + interval
            output[f"{key}-{index}"] = {
                "annotations": {
                    "label": value["annotations"]["label"],
                    "start_frame": str(part_start),
                    "end_frame": str(part_end),
                },
            }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--interval", type=int, default=8)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite {args.output}; pass --force to replace it")
    with args.input.open(encoding="utf-8") as handle:
        data = json.load(handle)
    result = split_intervals(data, args.interval)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Wrote {len(result['database'])} balanced samples to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
