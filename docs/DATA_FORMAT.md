# Data format

## Recording identity

Recordings use the hierarchy:

```text
subjectXX/sceneY/recording_id/
```

Annotation CSV files mirror this hierarchy. The external recording package contains two RGB directories and one IMU CSV.

## Original temporal annotations

Each CSV has three integer columns:

```csv
begin,end,label
14,27,10
```

- `begin`: first annotated frame.
- `end`: last annotated frame.
- `label`: zero-based class ID in the range 0 through 29.

Both boundaries are inclusive. A segment therefore contains `end - begin + 1` frames. Data loaders must preserve this convention unless the annotations and loader are jointly converted to half-open intervals.

`annotations/original/annotation_all.json` mirrors the CSV content. Label and frame values are stored as strings for compatibility with the dataset processing tools.

## Balanced samples

`annotations/balanced/annotation_all_balance.json` contains 4,255 derived samples. Long original intervals are divided into shorter segments using an eight-frame target interval. The original 2,751 intervals remain canonical.

## RGB frames

Frame files use integer filenames such as `0.jpg`, `1.jpg`, and so on. Dorsal-view frames are stored under `dorsal/`, and palm-view frames are stored under `palm/`. Both views use the same frame index within a recording.

## IMU CSV

The IMU table contains:

| Column | Meaning | Unit |
|---|---|---|
| unnamed first column | row index | none |
| `accX`, `accY`, `accZ` | acceleration | g |
| `gyroX`, `gyroY`, `gyroZ` | angular velocity | deg/s |
| `angleX`, `angleY`, `angleZ` | Euler angles | deg |

The row index is not a wall-clock timestamp. The dataset does not provide exact RGB-to-IMU alignment.
