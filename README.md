# EgoWrist-Gesture30

**A dual-view wrist-mounted RGB and IMU dataset for dynamic hand-gesture recognition.**

> 🌐 [中文说明](README.zh-CN.md)　·　📦 [Data Access](docs/DATA_ACCESS.md)　·　🚀 [Usage Guide](docs/USAGE.md)　·　📷 [Acquisition Guide](docs/ACQUISITION.md)

## Overview

EgoWrist-Gesture30 contains dynamic hand gestures captured from two complementary wrist-mounted RGB cameras together with a WT61C-TTL inertial measurement unit. The dataset covers 30 gesture classes, 13 participants, and 336 source recordings collected in indoor and outdoor environments with a right-wrist configuration.

The accompanying EgoWrist study evaluates the RGB modality. IMU measurements are retained in the complete dataset to support multimodal and sensor-fusion research. The two cameras are approximately synchronized in software; dataset IMU files do not support exact frame-level RGB–IMU alignment.

This GitHub repository distributes annotations, documentation, acquisition software, processing utilities, and validation tools. Recorded RGB frames and IMU files are distributed separately.

![Thirty dynamic gesture classes captured from the dorsal and palm wrist-camera views](docs/assets/gesture_overview.gif)

*Examples of all 30 gesture classes. Each panel presents synchronized dorsal and palm views from one annotated recording.*

## Dataset at a glance

| Property | Value |
|---|---:|
| Participants | 13 |
| Gesture classes | 30 |
| Source recordings | 336 |
| Canonical annotated intervals | 2,751 |
| Balanced derived segments | 4,255 |
| RGB streams | Dorsal and palm wrist-camera views |
| Nominal frame rate | 12 FPS |
| Inertial sensor | WT61C-TTL |
| Camera synchronization | Software-based, approximate |
| Official train/validation/test split | None |

The 2,751 original intervals form the canonical annotation set. The 4,255 balanced segments support class-balanced sampling without defining an evaluation split. Researchers can construct protocols appropriate to their tasks, with participant-disjoint partitions recommended for cross-user evaluation.

## Data Distribution

![Balanced gesture-label distribution](docs/assets/Gesture%20Label%20Occurrences_Balanced.png)

![Average balanced gesture duration](docs/assets/Average%20Duration%20Frames_Balanced.png)

The balanced annotation set contains 4,255 temporal segments across 30 gesture classes. The figures report the number of segments and mean segment duration for each class.

## Data organization

```text
EgoWrist-Gesture30/
├── annotations/                  # Canonical CSV and aggregate JSON annotations
├── data/                         # External data-access metadata
├── docs/                         # Dataset specification and operation guides
└── tools/                        # Acquisition, processing, review, and validation
```

Recorded data follow the annotation identity hierarchy:

```text
dataset-root/
└── subjectXX/sceneY/recording_id/
    ├── dorsal/*.jpg              # Dorsal wrist-camera view
    ├── palm/*.jpg                # Palm wrist-camera view
    └── sensor/sensor.csv         # WT61C-TTL measurements
```

Each original annotation file maps to one recording and contains inclusive frame intervals:

```csv
begin,end,label
14,27,10
```

Class IDs are zero-based from 0 to 29. The complete class vocabulary is available in [`annotations/classes.csv`](annotations/classes.csv), and the schemas are specified in [`docs/DATA_FORMAT.md`](docs/DATA_FORMAT.md).

## Modalities and hardware

- **RGB:** complementary dorsal and palm views captured by two HBVCAM-1466 V22 cameras with 160° fixed-focus, 1.66 mm lenses.
- **IMU:** WT61C-TTL acceleration, angular velocity, and Euler-angle measurements.
- **Synchronization:** the RGB streams use software-based approximate synchronization. Dataset IMU rows do not contain trustworthy wall-clock timestamps.

See [`docs/HARDWARE.md`](docs/HARDWARE.md) for the capture hardware and synchronization model.

## Documentation

| | Documentation |
|---:|---|
| 📐 | **[Data Format](docs/DATA_FORMAT.md)**<br><sub>Annotation schemas, interval semantics, RGB layout, and IMU columns</sub> |
| 📦 | **[Data Access](docs/DATA_ACCESS.md)**<br><sub>External recorded-data distribution and integrity metadata</sub> |
| 🚀 | **[Usage Guide](docs/USAGE.md)**<br><sub>Environment setup, annotation loading, validation, and processing</sub> |
| 📷 | **[Acquisition Guide](docs/ACQUISITION.md)**<br><sub>Dual-camera and WT61C-TTL collection workflow</sub> |
| 🔍 | **[Quality Review](docs/REVIEW.md)**<br><sub>Clip generation and local Web-based annotation review</sub> |
| 🔧 | **[Hardware and Synchronization](docs/HARDWARE.md)**<br><sub>Devices, measurement units, and synchronization limitations</sub> |

## Scope and responsible use

The repository does not contain recorded images, recorded sensor CSV files, generated videos, identity labels, predefined paper splits, training code, or model checkpoints.

The dataset is intended for gesture-recognition research. It should not be used for identity recognition, biometric profiling, or surveillance. Experimental reports should state the selected views, resolution, split protocol, and any RGB–IMU alignment assumptions.

## License

Repository tools are released under the [MIT License](LICENSE-CODE). Terms covering annotations and externally distributed recordings accompany the data distribution.
