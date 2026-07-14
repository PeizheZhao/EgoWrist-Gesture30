"""Minimal WT61C-TTL serial protocol reader.

The device emits 11-byte WitMotion packets. This module decodes the packet
types used by EgoWrist: acceleration (0x51), angular velocity (0x52), and
Euler angles (0x53). A combined sample is emitted after a valid angle packet.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import BinaryIO

PACKET_SIZE = 11
HEADER = 0x55


def _int16(low: int, high: int) -> int:
    value = (high << 8) | low
    return value - 65536 if value >= 32768 else value


class WT61Decoder:
    """Incrementally decode WT61C-TTL byte streams."""

    def __init__(self) -> None:
        self._buffer = bytearray()
        self._latest: dict[str, float | int] = {}

    def feed(self, data: bytes, timestamp_ns: int | None = None) -> list[dict[str, float | int]]:
        """Decode bytes and return zero or more complete combined samples."""
        self._buffer.extend(data)
        samples: list[dict[str, float | int]] = []

        while len(self._buffer) >= PACKET_SIZE:
            if self._buffer[0] != HEADER:
                del self._buffer[0]
                continue

            packet = self._buffer[:PACKET_SIZE]
            if sum(packet[:10]) & 0xFF != packet[10]:
                del self._buffer[0]
                continue

            del self._buffer[:PACKET_SIZE]
            packet_type = packet[1]
            if packet_type == 0x51:
                self._decode_acceleration(packet)
            elif packet_type == 0x52:
                self._decode_gyroscope(packet)
            elif packet_type == 0x53:
                self._decode_angles(packet)
                required = {
                    "accX",
                    "accY",
                    "accZ",
                    "gyroX",
                    "gyroY",
                    "gyroZ",
                    "angleX",
                    "angleY",
                    "angleZ",
                }
                if required.issubset(self._latest):
                    sample = dict(self._latest)
                    sample["timestamp_ns"] = timestamp_ns or time.time_ns()
                    samples.append(sample)

        return samples

    def _decode_acceleration(self, packet: bytes) -> None:
        scale = 16.0 / 32768.0
        self._latest.update(
            accX=round(_int16(packet[2], packet[3]) * scale, 4),
            accY=round(_int16(packet[4], packet[5]) * scale, 4),
            accZ=round(_int16(packet[6], packet[7]) * scale, 4),
        )
        raw_temperature = _int16(packet[8], packet[9])
        self._latest["temperature"] = round(raw_temperature / 32768.0 * 96.38 + 36.53, 2)

    def _decode_gyroscope(self, packet: bytes) -> None:
        scale = 2000.0 / 32768.0
        self._latest.update(
            gyroX=round(_int16(packet[2], packet[3]) * scale, 4),
            gyroY=round(_int16(packet[4], packet[5]) * scale, 4),
            gyroZ=round(_int16(packet[6], packet[7]) * scale, 4),
        )

    def _decode_angles(self, packet: bytes) -> None:
        scale = 180.0 / 32768.0
        self._latest.update(
            angleX=round(_int16(packet[2], packet[3]) * scale, 3),
            angleY=round(_int16(packet[4], packet[5]) * scale, 3),
            angleZ=round(_int16(packet[6], packet[7]) * scale, 3),
        )


class WT61Serial:
    """Context-managed serial reader for WT61C-TTL."""

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 0.2) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial: BinaryIO | None = None
        self._decoder = WT61Decoder()

    def __enter__(self) -> "WT61Serial":
        try:
            import serial
        except ImportError as exc:
            raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc
        self._serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        return self

    def __exit__(self, *_: object) -> None:
        if self._serial is not None:
            self._serial.close()
            self._serial = None

    def samples(self) -> Iterator[dict[str, float | int]]:
        if self._serial is None:
            raise RuntimeError("WT61Serial must be used as a context manager")
        while True:
            data = self._serial.read(64)
            if data:
                yield from self._decoder.feed(data, timestamp_ns=time.time_ns())
