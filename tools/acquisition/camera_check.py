#!/usr/bin/env python3
"""Preview two cameras and report their observed frame rates."""

from __future__ import annotations

import argparse
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera-a", type=int, default=0)
    parser.add_argument("--camera-b", type=int, default=1)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc

    cameras = [cv2.VideoCapture(args.camera_a), cv2.VideoCapture(args.camera_b)]
    for camera in cameras:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if not all(camera.isOpened() for camera in cameras):
        for camera in cameras:
            camera.release()
        raise RuntimeError("Could not open both cameras")

    counts = [0, 0]
    rates = [0.0, 0.0]
    started = time.monotonic()
    try:
        while True:
            for index, camera in enumerate(cameras):
                ok, frame = camera.read()
                if not ok:
                    continue
                counts[index] += 1
                cv2.putText(
                    frame,
                    f"Camera {index}: {rates[index]:.1f} FPS",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow(f"Camera {index}", frame)
            elapsed = time.monotonic() - started
            if elapsed >= 1.0:
                rates = [count / elapsed for count in counts]
                counts = [0, 0]
                started = time.monotonic()
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        for camera in cameras:
            camera.release()
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
