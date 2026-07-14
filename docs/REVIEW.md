# Annotation quality review

The review workflow converts annotated dual-view frame intervals into clips, presents them in a local Web interface, and exports quality-control decisions. The interface records review results separately and does not edit annotations.

## Generate clips

```bash
python tools/dataset/frames_to_video.py \
  --annotations annotations/original/csv/subject01/scene1/1.csv \
  --dorsal /path/to/dataset-root/subject01/scene1/1/dorsal \
  --palm /path/to/dataset-root/subject01/scene1/1/palm \
  --output /tmp/egowrist-clips/subject01/scene1/1 \
  --fps 12
```

## Start the review interface

```bash
python tools/review_web/app.py \
  --video-root /tmp/egowrist-clips \
  --review-file /tmp/egowrist-reviews.json
```

Open `http://127.0.0.1:5000`. Available states are good quality, blur, label or boundary error, capture or gesture error, and needs discussion.

## Export decisions

```bash
python tools/review_web/export_reviews.py \
  /tmp/egowrist-reviews.json \
  /tmp/egowrist-reviews.csv
```

Approved corrections should be applied to the affected original CSV files. Regenerate aggregate JSON files and run the repository validator after every correction.
