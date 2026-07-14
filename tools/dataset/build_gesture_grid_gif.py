#!/usr/bin/env python3
"""Build a labeled dual-view GIF containing one example of every gesture."""

from __future__ import annotations

import argparse
import json
import math
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


@dataclass(frozen=True)
class Sample:
    label_id: int
    label_name: str
    recording: str
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start + 1


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def recording_from_key(key: str) -> str:
    recording, separator, index = key.rpartition("_")
    if not separator or not index.isdigit():
        raise ValueError(f"Unexpected annotation key: {key}")
    return recording


def interval_is_complete(sample: Sample, frames_root: Path, views: tuple[str, str]) -> bool:
    recording_root = frames_root / sample.recording
    for view in views:
        view_root = recording_root / view
        if not view_root.is_dir():
            return False
        for frame_id in range(sample.start, sample.end + 1):
            if not (view_root / f"{frame_id}.jpg").is_file():
                return False
    return True


def choose_samples(
    annotations: Path,
    frames_root: Path,
    views: tuple[str, str],
    target_length: int,
) -> list[Sample]:
    with annotations.open(encoding="utf-8") as handle:
        data = json.load(handle)

    candidates: dict[int, list[Sample]] = {int(label_id): [] for label_id in data["label_map"]}
    for key, entry in data["database"].items():
        annotation = entry["annotations"]
        label_id = int(annotation["label"])
        candidates[label_id].append(
            Sample(
                label_id=label_id,
                label_name=data["label_map"][str(label_id)],
                recording=recording_from_key(key),
                start=int(annotation["start_frame"]),
                end=int(annotation["end_frame"]),
            )
        )

    selected: list[Sample] = []
    for label_id in sorted(candidates):
        ranked = sorted(
            candidates[label_id],
            key=lambda sample: (abs(sample.length - target_length), sample.recording, sample.start),
        )
        match = next((sample for sample in ranked if interval_is_complete(sample, frames_root, views)), None)
        if match is None:
            raise FileNotFoundError(f"No complete dual-view interval found for label {label_id}")
        selected.append(match)
    return selected


def sampled_frame_ids(sample: Sample, frame_count: int) -> list[int]:
    if frame_count == 1:
        return [(sample.start + sample.end) // 2]
    return [
        round(sample.start + index * (sample.end - sample.start) / (frame_count - 1))
        for index in range(frame_count)
    ]


def fit_frame(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        rgb = source.convert("RGB")
        return ImageOps.fit(rgb, size, method=Image.Resampling.LANCZOS)


def draw_label(
    draw: ImageDraw.ImageDraw,
    sample: Sample,
    x: int,
    y: int,
    width: int,
    header_height: int,
    font: ImageFont.ImageFont,
    id_font: ImageFont.ImageFont,
) -> None:
    draw.rounded_rectangle((x + 7, y + 7, x + 35, y + 35), radius=7, fill="#2563EB")
    identifier = f"{sample.label_id:02d}"
    box = draw.textbbox((0, 0), identifier, font=id_font)
    draw.text((x + 21 - (box[2] - box[0]) / 2, y + 21 - (box[3] - box[1]) / 2), identifier, font=id_font, fill="white")

    words = sample.label_name.replace("_", " ")
    lines = textwrap.wrap(words, width=31, break_long_words=True)[:2]
    line_height = 15
    block_height = len(lines) * line_height
    text_y = y + max(6, (header_height - block_height) // 2)
    for line in lines:
        draw.text((x + 43, text_y), line, font=font, fill="#0F172A")
        text_y += line_height


def build_gif(
    samples: list[Sample],
    frames_root: Path,
    output: Path,
    views: tuple[str, str],
    columns: int,
    animation_frames: int,
    duration_ms: int,
) -> None:
    tile_width, tile_height = 300, 138
    header_height = 46
    margin, gutter = 8, 6
    view_width = (tile_width - margin * 2 - gutter) // 2
    view_height = tile_height - header_height - margin
    rows = math.ceil(len(samples) / columns)
    canvas_size = (columns * tile_width, rows * tile_height)
    font = load_font(13)
    id_font = load_font(12, bold=True)
    view_font = load_font(11, bold=True)
    timelines = {sample.label_id: sampled_frame_ids(sample, animation_frames) for sample in samples}

    frames: list[Image.Image] = []
    for animation_index in range(animation_frames):
        canvas = Image.new("RGB", canvas_size, "#E2E8F0")
        draw = ImageDraw.Draw(canvas)
        for grid_index, sample in enumerate(samples):
            column = grid_index % columns
            row = grid_index // columns
            x, y = column * tile_width, row * tile_height
            draw.rectangle((x + 1, y + 1, x + tile_width - 2, y + tile_height - 2), fill="white", outline="#CBD5E1", width=2)
            draw_label(draw, sample, x, y, tile_width, header_height, font, id_font)

            frame_id = timelines[sample.label_id][animation_index]
            for view_index, view in enumerate(views):
                image_x = x + margin + view_index * (view_width + gutter)
                image_y = y + header_height
                frame_path = frames_root / sample.recording / view / f"{frame_id}.jpg"
                frame = fit_frame(frame_path, (view_width, view_height))
                canvas.paste(frame, (image_x, image_y))
                badge = "DORSAL" if view_index == 0 else "PALM"
                badge_width = 58 if view_index == 0 else 43
                draw.rounded_rectangle((image_x + 4, image_y + 4, image_x + badge_width, image_y + 22), radius=4, fill="#0F172A")
                draw.text((image_x + 8, image_y + 6), badge, font=view_font, fill="white")
        frames.append(canvas)

    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )


def write_manifest(samples: list[Sample], path: Path, views: tuple[str, str]) -> None:
    payload = {
        "views": list(views),
        "samples": [
            {
                "label_id": sample.label_id,
                "label_name": sample.label_name,
                "recording": sample.recording,
                "start_frame": sample.start,
                "end_frame": sample.end,
            }
            for sample in samples
        ],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("frames_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--dorsal-name", default="dorsal", help="Dorsal-view directory name")
    parser.add_argument("--palm-name", default="palm", help="Palm-view directory name")
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--frames", type=int, default=18)
    parser.add_argument("--duration-ms", type=int, default=110)
    parser.add_argument("--target-length", type=int, default=24)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.columns < 1 or args.frames < 2 or args.duration_ms < 20:
        parser.error("columns must be positive, frames >= 2, and duration-ms >= 20")

    views = (args.dorsal_name, args.palm_name)
    samples = choose_samples(args.annotations, args.frames_root, views, args.target_length)
    build_gif(samples, args.frames_root, args.output, views, args.columns, args.frames, args.duration_ms)
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        write_manifest(samples, args.manifest, views)
    print(f"Wrote {args.output} with {len(samples)} gestures in a {args.columns}-column grid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
