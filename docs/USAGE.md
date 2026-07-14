# Usage guide

This guide covers repository validation, annotation loading, external-data validation, and dataset utilities. Acquisition and quality-review workflows are documented separately in [ACQUISITION.md](ACQUISITION.md) and [REVIEW.md](REVIEW.md).

## Environment

Annotation inspection and repository validation require Python 3.10 or later and the standard library. Image, serial-device, and Web utilities use the optional packages in `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Validate the repository

Run these commands from the repository root:

```bash
python tools/validation/validate_release.py
python -m unittest discover -s tools/validation/tests
```

The canonical counts are 30 labels, 336 recordings, 2,751 original intervals, and 4,255 balanced segments.

## Load an annotation file

```python
from pathlib import Path
import csv

annotation_file = Path("annotations/original/csv/subject01/scene1/1.csv")
with annotation_file.open(newline="", encoding="utf-8-sig") as handle:
    intervals = list(csv.DictReader(handle))

for interval in intervals:
    begin = int(interval["begin"])
    end = int(interval["end"])
    label = int(interval["label"])
    frame_ids = range(begin, end + 1)  # inclusive boundaries
    print(label, list(frame_ids))
```

The canonical source is `annotations/original/csv/`. The aggregate file `annotations/original/annotation_all.json` represents the same intervals in one document. `annotations/balanced/annotation_all_balance.json` contains derived segments and does not define train, validation, or test subsets.

## Inspect annotation statistics

```bash
python tools/dataset/annotation_statistics.py \
  annotations/original/annotation_all.json

python tools/dataset/annotation_statistics.py \
  annotations/balanced/annotation_all_balance.json
```

## Obtain and validate recorded data

Data endpoints and integrity metadata are listed in `data/download_links.json`. Extract the recorded data outside the Git repository, then validate it:

```bash
python tools/validation/validate_external_data.py /path/to/dataset-root \
  --dorsal-name dorsal \
  --palm-name palm \
  --sensor-relative sensor/sensor.csv
```

The validator checks the recording hierarchy, both RGB views, every frame referenced by the annotations, IMU file presence, and required sensor columns.

## Resolve intervals to recorded files

```python
from pathlib import Path

data_root = Path("/path/to/dataset-root")
subject, scene, recording = "subject01", "scene1", "1"
begin, end = 14, 27

recording_root = data_root / subject / scene / recording
dorsal_frames = [recording_root / "dorsal" / f"{i}.jpg" for i in range(begin, end + 1)]
palm_frames = [recording_root / "palm" / f"{i}.jpg" for i in range(begin, end + 1)]
sensor_csv = recording_root / "sensor" / "sensor.csv"
```

## Regenerate aggregate annotations

Regenerate aggregate files in a separate directory before updating canonical annotations:

```bash
python tools/dataset/csv_to_json.py \
  annotations/original/csv \
  annotations/original/label_map.json \
  /tmp/annotation_all.json

python tools/dataset/build_balanced_annotations.py \
  /tmp/annotation_all.json \
  /tmp/annotation_all_balance.json
```

Both utilities refuse accidental overwrite unless `--force` is supplied. Run repository validation after any annotation change.

## Other utilities

```bash
# Build side-by-side review clips
python tools/dataset/frames_to_video.py --help

# Resize an image hierarchy into a separate destination
python tools/dataset/resize_images.py --help

# Generate balanced-annotation distribution figures
python tools/dataset/annotation_analysis.py \
  annotations/balanced/annotation_all_balance.json \
  docs/assets

# Generate the 30-class dorsal/palm overview animation
python tools/dataset/build_gesture_grid_gif.py \
  annotations/original/annotation_all.json \
  /path/to/dataset-root \
  docs/assets/gesture_overview.gif
```

Version-conversion utilities are provided under `tools/dataset/migrations/`. They are intended only for explicitly versioned annotation migrations and are not part of the standard 30-class workflow.
