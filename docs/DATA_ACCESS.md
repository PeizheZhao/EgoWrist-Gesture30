# Data access

The GitHub repository hosts annotations, documentation, and tools. Recorded dorsal-view RGB frames, palm-view RGB frames, and WT61C-TTL measurements are distributed as a separate data package because of their size.

Machine-readable access endpoints, archive versions, sizes, and SHA-256 checksums are maintained in [`../data/download_links.json`](../data/download_links.json). Recorded data should be extracted outside the Git repository.

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

After extraction, verify the data package as described in [USAGE.md](USAGE.md). Questions about data distribution may be sent to `zhaopeizhepro@outlook.com`.
