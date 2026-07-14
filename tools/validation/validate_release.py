#!/usr/bin/env python3
"""Validate canonical EgoWrist-Gesture30 annotations."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {"labels": 30, "recordings": 336, "original": 2751, "balanced": 4255}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_csv_annotations() -> tuple[int, int, list[str], list[str]]:
    paths = sorted((ROOT / "annotations/original/csv").glob("subject*/scene*/*.csv"))
    rows = 0
    errors: list[str] = []
    warnings: list[str] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["begin", "end", "label"]:
                errors.append(f"{path}: unexpected columns {reader.fieldnames}")
                continue
            previous_end: int | None = None
            for line, row in enumerate(reader, 2):
                rows += 1
                try:
                    begin, end, label = int(row["begin"]), int(row["end"]), int(row["label"])
                except (KeyError, ValueError):
                    errors.append(f"{path}:{line}: non-integer annotation")
                    continue
                if begin < 0 or end < begin:
                    errors.append(f"{path}:{line}: invalid interval {begin}..{end}")
                if not 0 <= label < 30:
                    errors.append(f"{path}:{line}: label {label} is outside 0..29")
                if previous_end is not None and begin < previous_end:
                    warnings.append(f"{path}:{line}: interval begins before previous interval ends")
                previous_end = end
    return len(paths), rows, errors, warnings


def main() -> int:
    errors: list[str] = []
    recordings, original_rows, csv_errors, warnings = validate_csv_annotations()
    errors.extend(csv_errors)

    original = load_json(ROOT / "annotations/original/annotation_all.json")
    balanced = load_json(ROOT / "annotations/balanced/annotation_all_balance.json")
    label_map = load_json(ROOT / "annotations/original/label_map.json")

    actual = {
        "labels": len(label_map),
        "recordings": recordings,
        "original": original_rows,
        "balanced": len(balanced["database"]),
    }
    for key, expected in EXPECTED.items():
        if actual[key] != expected:
            errors.append(f"{key}: expected {expected}, got {actual[key]}")
    if original["label_map"] != label_map or balanced["label_map"] != label_map:
        errors.append("Label maps are inconsistent")
    if len(original["database"]) != original_rows:
        errors.append("Original JSON count does not match CSV row count")
    for name, data in (("original", original), ("balanced", balanced)):
        if any("subset" in entry for entry in data["database"].values()):
            errors.append(f"{name} annotations contain a predefined subset assignment")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Validation passed")
    for key in ("labels", "recordings", "original", "balanced"):
        print(f"- {key}: {actual[key]}")
    if warnings:
        print("Validation warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
