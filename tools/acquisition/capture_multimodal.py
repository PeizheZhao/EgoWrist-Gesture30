#!/usr/bin/env python3
"""Capture approximately synchronized dual-view RGB frames and WT61C-TTL IMU data."""

from __future__ import annotations

import argparse
import csv
import threading
import time
from pathlib import Path

from wt61 import WT61Serial


class LatestFrame:
    def __init__(self, camera_index: int, width: int, height: int) -> None:
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError(
                "Install dependencies with: pip install -r requirements.txt"
            ) from exc
        self.cv2 = cv2
        self.capture = cv2.VideoCapture(camera_index)
        if not self.capture.isOpened():
            raise RuntimeError(f"Cannot open camera {camera_index}")
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._lock = threading.Lock()
        self._frame = None
        self._timestamp_ns = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            ok, frame = self.capture.read()
            if not ok:
                continue
            timestamp_ns = time.time_ns()
            with self._lock:
                self._frame = frame
                self._timestamp_ns = timestamp_ns

    def latest(self):
        with self._lock:
            if self._frame is None:
                return None, 0
            return self._frame.copy(), self._timestamp_ns

    def close(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)
        self.capture.release()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True, help="e.g. subject14")
    parser.add_argument("--scene", required=True, help="e.g. scene1")
    parser.add_argument("--recording", required=True, help="e.g. 1")
    parser.add_argument("--palm-camera", type=int, default=0)
    parser.add_argument("--dorsal-camera", type=int, default=1)
    parser.add_argument("--imu-port", required=True, help="e.g. /dev/ttyUSB0 or COM15")
    parser.add_argument("--imu-baudrate", type=int, default=115200)
    parser.add_argument("--fps", type=float, default=12.0)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--duration", type=float, default=10.0, help="seconds")
    parser.add_argument("--output", type=Path, default=Path("captures"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.output / args.subject / args.scene / args.recording
    if root.exists():
        raise FileExistsError(f"Refusing to overwrite existing recording: {root}")
    palm_dir = root / "palm"
    dorsal_dir = root / "dorsal"
    sensor_dir = root / "sensor"
    palm_dir.mkdir(parents=True)
    dorsal_dir.mkdir(parents=True)
    sensor_dir.mkdir(parents=True)

    stop = threading.Event()
    sensor_error: list[BaseException] = []
    sensor_fields = [
        "timestamp_ns",
        "accX",
        "accY",
        "accZ",
        "gyroX",
        "gyroY",
        "gyroZ",
        "angleX",
        "angleY",
        "angleZ",
        "temperature",
    ]

    def collect_imu() -> None:
        try:
            with (sensor_dir / "sensor.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=sensor_fields)
                writer.writeheader()
                with WT61Serial(args.imu_port, args.imu_baudrate) as imu:
                    for sample in imu.samples():
                        writer.writerow(sample)
                        if stop.is_set():
                            break
        except BaseException as exc:  # propagate hardware-thread failures to the main thread
            sensor_error.append(exc)
            stop.set()

    palm = LatestFrame(args.palm_camera, args.width, args.height)
    dorsal = LatestFrame(args.dorsal_camera, args.width, args.height)
    cv2 = palm.cv2
    imu_thread = threading.Thread(target=collect_imu, daemon=True)
    palm.start()
    dorsal.start()
    imu_thread.start()

    frame_period = 1.0 / args.fps
    deadline = time.monotonic() + args.duration
    next_poll = time.monotonic()
    frame_id = 0

    try:
        with (root / "frames.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                ["frame_id", "poll_timestamp_ns", "palm_timestamp_ns", "dorsal_timestamp_ns", "offset_ns"]
            )
            while time.monotonic() < deadline and not stop.is_set():
                delay = next_poll - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
                poll_timestamp_ns = time.time_ns()
                palm_frame, palm_timestamp_ns = palm.latest()
                dorsal_frame, dorsal_timestamp_ns = dorsal.latest()
                if palm_frame is not None and dorsal_frame is not None:
                    cv2.imwrite(str(palm_dir / f"{frame_id:06d}.jpg"), palm_frame)
                    cv2.imwrite(str(dorsal_dir / f"{frame_id:06d}.jpg"), dorsal_frame)
                    writer.writerow(
                        [
                            frame_id,
                            poll_timestamp_ns,
                            palm_timestamp_ns,
                            dorsal_timestamp_ns,
                            abs(palm_timestamp_ns - dorsal_timestamp_ns),
                        ]
                    )
                    frame_id += 1
                next_poll += frame_period
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        palm.close()
        dorsal.close()
        imu_thread.join(timeout=2)

    if sensor_error:
        raise RuntimeError("IMU collection failed") from sensor_error[0]
    print(f"Saved {frame_id} approximate frame pairs to {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
