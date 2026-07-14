#!/usr/bin/env python3
"""Resize a frame tree into a separate output directory without changing source images."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        raise ValueError("Input and output directories must be different")
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc
    files = sorted(args.input.rglob("*.jpg"))

    def resize(path: Path) -> None:
        destination = args.output / path.relative_to(args.input)
        if destination.exists() and not args.force:
            raise FileExistsError(f"Refusing to overwrite {destination}; pass --force")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(path) as image:
            image.resize((args.width, args.height), Image.Resampling.LANCZOS).save(destination)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        list(executor.map(resize, files))
    print(f"Resized {len(files)} images into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
