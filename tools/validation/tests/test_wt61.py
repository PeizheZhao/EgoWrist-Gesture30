from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/acquisition"))
from wt61 import WT61Decoder  # noqa: E402


def packet(kind: int, values: tuple[int, int, int, int]) -> bytes:
    body = bytearray([0x55, kind])
    for value in values:
        body.extend(int(value).to_bytes(2, "little", signed=True))
    body.append(sum(body) & 0xFF)
    return bytes(body)


class WT61Tests(unittest.TestCase):
    def test_three_packet_sample(self) -> None:
        decoder = WT61Decoder()
        stream = b"".join(
            [
                packet(0x51, (16384, 0, -16384, 0)),
                packet(0x52, (16384, 0, -16384, 0)),
                packet(0x53, (16384, 0, -16384, 0)),
            ]
        )
        samples = decoder.feed(stream, timestamp_ns=123)
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0]["timestamp_ns"], 123)
        self.assertEqual(samples[0]["accX"], 8.0)
        self.assertEqual(samples[0]["gyroX"], 1000.0)
        self.assertEqual(samples[0]["angleZ"], -90.0)


if __name__ == "__main__":
    unittest.main()
