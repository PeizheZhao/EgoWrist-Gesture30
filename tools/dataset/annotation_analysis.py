#!/usr/bin/env python3
"""Plot balanced-label counts and average interval durations."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def analyze(data: dict) -> tuple[dict[str, int], dict[str, float], int]:
    label_count: dict[str, int] = defaultdict(int)
    label_duration: dict[str, list[int]] = defaultdict(list)

    for entry in data["database"].values():
        annotation = entry["annotations"]
        label_name = data["label_map"][annotation["label"]]
        label_count[label_name] += 1
        start = int(annotation["start_frame"])
        end = int(annotation["end_frame"])
        label_duration[label_name].append(end - start + 1)

    ordered_names = list(data["label_map"].values())
    counts = {name: label_count[name] for name in ordered_names}
    averages = {
        name: sum(label_duration[name]) / len(label_duration[name])
        for name in ordered_names
    }
    return counts, averages, len(data["database"])


def plot_counts(counts: dict[str, int], total: int, output: Path) -> None:
    figure, axes = plt.subplots(figsize=(12, 6))
    bars = axes.bar(counts.keys(), counts.values(), color="skyblue")
    axes.set_xlabel("Gesture Labels")
    axes.set_ylabel("Occurrences")
    axes.set_title("Gesture Label Occurrences (Balanced)")
    axes.tick_params(axis="x", rotation=45)
    for label in axes.get_xticklabels():
        label.set_horizontalalignment("right")
    axes.bar_label(bars, fmt="%d", padding=2)
    axes.text(0, 0, f"Total Number: {total}", fontsize=12, transform=axes.transAxes)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def plot_duration(averages: dict[str, float], output: Path) -> None:
    figure, axes = plt.subplots(figsize=(12, 6))
    bars = axes.bar(averages.keys(), averages.values(), color="lightgreen")
    axes.set_xlabel("Gesture Labels")
    axes.set_ylabel("Average Duration Frames (Balanced)")
    axes.set_title("Average Duration of Gestures")
    axes.tick_params(axis="x", rotation=45)
    for label in axes.get_xticklabels():
        label.set_horizontalalignment("right")
    axes.bar_label(bars, labels=[f"{value:.1f}" for value in averages.values()], padding=2)
    figure.tight_layout()
    figure.savefig(output, dpi=160)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Balanced aggregate annotation JSON")
    parser.add_argument("output", type=Path, help="Directory for the two PNG figures")
    args = parser.parse_args()

    with args.input.open(encoding="utf-8") as handle:
        data = json.load(handle)
    counts, averages, total = analyze(data)
    args.output.mkdir(parents=True, exist_ok=True)
    plot_counts(counts, total, args.output / "Gesture Label Occurrences_Balanced.png")
    plot_duration(averages, args.output / "Average Duration Frames_Balanced.png")
    print(f"Wrote two figures for {len(counts)} labels and {total} balanced segments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
