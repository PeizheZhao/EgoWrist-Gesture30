# Data access

The GitHub repository hosts annotations, documentation, and tools. Recorded dorsal-view RGB frames, palm-view RGB frames, and WT61C-TTL measurements are distributed as a separate data package because of their size.

## Request access

Submit the [EgoWrist Gesture 30 Dataset Access Request](https://forms.office.com/r/EqiJNLWgtF) to request the recorded data package. The form asks for your name, institution or affiliation, contact email address, confirmation that the dataset and derived data will be used exclusively for non-commercial academic and scientific research, and agreement not to redistribute the dataset.

Access is reviewed based on the submitted information. Approved requesters receive the recorded-data distribution instructions separately. The machine-readable registry in [`../data/download_links.json`](../data/download_links.json) records the access-request URL and any published archive version, size, and SHA-256 metadata. Extract recorded data outside the Git repository.

The data package follows this hierarchy:

```text
dataset-root/
└── subjectXX/
    └── sceneY/
        └── recording_id/
            ├── dorsal/*.jpg
            ├── palm/*.jpg
            └── sensor/sensor.csv
```

After receiving and extracting the package, verify it as described in [USAGE.md](USAGE.md). Questions about an access request or data distribution may be sent to `zhaopeizhepro@outlook.com`.
