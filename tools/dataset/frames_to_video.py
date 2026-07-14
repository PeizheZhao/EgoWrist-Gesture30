#!/usr/bin/env python3
"""Render annotated dual-view frame intervals as reviewable MP4 clips."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def resolve_frame(directory: Path, frame_id: int) -> Path:
    for name in (f"{frame_id}.jpg", f"{frame_id:06d}.jpg"):
        path = directory / name
        if path.is_file():
            return path
    raise FileNotFoundError(f"Missing frame {frame_id} in {directory}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path, help="one recording CSV")
    parser.add_argument("--dorsal", required=True, type=Path)
    parser.add_argument("--palm", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--fps", type=float, default=12.0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc
    args.output.mkdir(parents=True, exist_ok=True)

    with args.annotations.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    for index, row in enumerate(rows):
        begin, end, label = int(row["begin"]), int(row["end"]), int(row["label"])
        output = args.output / f"clip_{index:03d}_label_{label:02d}.mp4"
        if output.exists() and not args.force:
            raise FileExistsError(f"Refusing to overwrite {output}; pass --force")
        frames = []
        for frame_id in range(begin, end + 1):
            dorsal = cv2.imread(str(resolve_frame(args.dorsal, frame_id)))
            palm = cv2.imread(str(resolve_frame(args.palm, frame_id)))
            if dorsal is None or palm is None:
                raise FileNotFoundError(f"Missing frame {frame_id} in one or both views")
            frames.append(cv2.hconcat([dorsal, palm]))
        height, width = frames[0].shape[:2]
        writer = cv2.VideoWriter(
            str(output), cv2.VideoWriter_fourcc(*"mp4v"), args.fps, (width, height)
        )
        if not writer.isOpened():
            raise RuntimeError(f"Could not create {output}")
        for frame in frames:
            writer.write(frame)
        writer.release()
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
