#!/usr/bin/env python3
"""Check an external RGB+IMU data tree against the canonical annotation CSV files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

IMU_FIELDS = {"accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ", "angleX", "angleY", "angleZ"}


def frame_exists(directory: Path, frame_id: int) -> bool:
    return (directory / f"{frame_id}.jpg").is_file() or (
        directory / f"{frame_id:06d}.jpg"
    ).is_file()


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_root", type=Path)
    parser.add_argument(
        "--annotations-root", type=Path, default=root / "annotations/original/csv"
    )
    parser.add_argument("--dorsal-name", default="dorsal")
    parser.add_argument("--palm-name", default="palm")
    parser.add_argument("--sensor-relative", default="sensor/sensor.csv")
    parser.add_argument("--max-errors", type=int, default=100)
    args = parser.parse_args()

    errors: list[str] = []
    recordings = intervals = checked_frames = sensor_files = 0
    annotation_paths = sorted(args.annotations_root.glob("subject*/scene*/*.csv"))
    for annotation_path in annotation_paths:
        recording = args.data_root / annotation_path.relative_to(args.annotations_root).with_suffix("")
        dorsal = recording / args.dorsal_name
        palm = recording / args.palm_name
        sensor = recording / args.sensor_relative
        recordings += 1
        if not dorsal.is_dir() or not palm.is_dir():
            errors.append(f"Missing RGB view directory in {recording}")
        if not sensor.is_file():
            errors.append(f"Missing IMU CSV: {sensor}")
        else:
            sensor_files += 1
            with sensor.open(newline="", encoding="utf-8-sig") as handle:
                fields = set(csv.DictReader(handle).fieldnames or [])
            missing = sorted(IMU_FIELDS - fields)
            if missing:
                errors.append(f"{sensor}: missing columns {', '.join(missing)}")

        with annotation_path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                intervals += 1
                begin, end = int(row["begin"]), int(row["end"])
                for frame_id in range(begin, end + 1):
                    checked_frames += 1
                    if not frame_exists(dorsal, frame_id):
                        errors.append(
                            f"Missing {args.dorsal_name} frame: {recording}/{args.dorsal_name}/{frame_id}.jpg"
                        )
                    if not frame_exists(palm, frame_id):
                        errors.append(
                            f"Missing {args.palm_name} frame: {recording}/{args.palm_name}/{frame_id}.jpg"
                        )
                    if len(errors) >= args.max_errors:
                        break
                if len(errors) >= args.max_errors:
                    break
        if len(errors) >= args.max_errors:
            break

    print(f"recordings checked: {recordings}")
    print(f"annotation intervals checked: {intervals}")
    print(f"annotated frame references checked: {checked_frames}")
    print(f"IMU files found: {sensor_files}")
    if errors:
        print(f"validation failed with at least {len(errors)} errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("external data validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
