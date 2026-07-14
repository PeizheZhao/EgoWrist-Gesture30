"""Read and validate EgoWrist temporal annotations."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Annotation:
    begin: int
    end: int
    label: int

    @property
    def frame_count(self) -> int:
        """Number of frames under the historical inclusive-boundary convention."""
        return self.end - self.begin + 1


def load_csv(path: str | Path) -> list[Annotation]:
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["begin", "end", "label"]:
            raise ValueError(f"Unexpected CSV schema in {path}: {reader.fieldnames}")
        annotations = [
            Annotation(begin=int(row["begin"]), end=int(row["end"]), label=int(row["label"]))
            for row in reader
        ]

    for item in annotations:
        if item.begin < 0 or item.end < item.begin:
            raise ValueError(f"Invalid interval in {path}: {item}")
        if not 0 <= item.label < 30:
            raise ValueError(f"Invalid label in {path}: {item.label}")
    return annotations
