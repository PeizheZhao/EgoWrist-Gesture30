#!/usr/bin/env python3
"""Local web interface for reviewing generated gesture clips."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REVIEW_OPTIONS = {
    "good": "Good quality",
    "blur": "Blurred",
    "label_error": "Label or temporal-boundary error",
    "capture_error": "Capture or gesture-execution error",
    "discuss": "Needs discussion",
}


def create_app(video_root: Path, review_file: Path):
    try:
        from flask import Flask, abort, jsonify, render_template, request, send_from_directory
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install -r requirements.txt") from exc
    app = Flask(__name__)
    video_root = video_root.resolve()
    review_file = review_file.resolve()

    def load_reviews() -> dict[str, dict[str, str]]:
        if not review_file.exists():
            return {}
        with review_file.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError("Review file must contain a JSON object")
        return data

    def save_reviews(reviews: dict[str, dict[str, str]]) -> None:
        review_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = review_file.with_suffix(review_file.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(reviews, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        temporary.replace(review_file)

    @app.get("/")
    def index():
        videos = sorted(
            path.relative_to(video_root).as_posix()
            for path in video_root.rglob("*")
            if path.suffix.lower() in {".mp4", ".avi", ".mov", ".webm"}
        )
        per_page = max(1, min(request.args.get("per_page", 12, type=int), 100))
        page = max(1, request.args.get("page", 1, type=int))
        total_pages = max(1, (len(videos) + per_page - 1) // per_page)
        page = min(page, total_pages)
        start = (page - 1) * per_page
        return render_template(
            "index.html",
            videos=videos[start : start + per_page],
            reviews=load_reviews(),
            options=REVIEW_OPTIONS,
            page=page,
            total_pages=total_pages,
            per_page=per_page,
            total_videos=len(videos),
        )

    @app.get("/video/<path:filename>")
    def video(filename: str):
        candidate = (video_root / filename).resolve()
        if video_root not in candidate.parents or not candidate.is_file():
            abort(404)
        return send_from_directory(video_root, filename)

    @app.post("/review")
    def review():
        filename = request.form.get("video", "")
        status = request.form.get("status", "")
        notes = request.form.get("notes", "").strip()
        if status not in REVIEW_OPTIONS:
            return jsonify(ok=False, message="Invalid review status"), 400
        if not (video_root / filename).is_file():
            return jsonify(ok=False, message="Unknown video"), 404
        reviews = load_reviews()
        reviews[filename] = {"status": status, "notes": notes}
        save_reviews(reviews)
        return jsonify(ok=True, message="Review saved")

    return app


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-root", required=True, type=Path)
    parser.add_argument("--review-file", type=Path, default=Path("reviews.json"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    if not args.video_root.is_dir():
        raise NotADirectoryError(args.video_root)
    create_app(args.video_root, args.review_file).run(
        host=args.host, port=args.port, debug=False
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
