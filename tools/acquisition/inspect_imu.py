#!/usr/bin/env python3
"""Print a concise summary of a historical or newly captured IMU CSV."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

FIELDS = ("accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ", "angleX", "angleY", "angleZ")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    values = {field: [] for field in FIELDS}
    rows = 0
    with args.csv_file.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(FIELDS) - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"Missing IMU columns: {', '.join(missing)}")
        for row in reader:
            rows += 1
            for field in FIELDS:
                value = float(row[field])
                if math.isfinite(value):
                    values[field].append(value)
    print(f"file: {args.csv_file}")
    print(f"rows: {rows}")
    for field in FIELDS:
        series = values[field]
        print(f"{field}: min={min(series):.4f} max={max(series):.4f} mean={sum(series)/len(series):.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
