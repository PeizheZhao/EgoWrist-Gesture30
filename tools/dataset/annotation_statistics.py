#!/usr/bin/env python3
"""Report per-class counts and inclusive frame durations from aggregate JSON annotations."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    with args.annotations.open(encoding="utf-8") as handle:
        data = json.load(handle)
    counts: dict[str, int] = defaultdict(int)
    durations: dict[str, list[int]] = defaultdict(list)
    for entry in data["database"].values():
        annotation = entry["annotations"]
        label = str(annotation["label"])
        counts[label] += 1
        durations[label].append(int(annotation["end_frame"]) - int(annotation["start_frame"]) + 1)
    result = {
        "total": len(data["database"]),
        "classes": [
            {
                "label_id": int(label),
                "name": data["label_map"][label],
                "count": counts[label],
                "mean_frames": sum(durations[label]) / len(durations[label]),
            }
            for label in sorted(data["label_map"], key=int)
        ],
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Total samples: {result['total']}")
        print("ID  Count  Mean frames  Class")
        for item in result["classes"]:
            print(f"{item['label_id']:>2}  {item['count']:>5}  {item['mean_frames']:>11.2f}  {item['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
