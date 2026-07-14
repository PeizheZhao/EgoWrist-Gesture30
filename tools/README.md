# Tools

| Directory | Purpose |
|---|---|
| `acquisition/` | Capture two approximately synchronized RGB views and WT61C-TTL IMU data; check cameras; inspect IMU files. |
| `dataset/` | Convert, segment, summarize, resize, visualize, and render dataset records. |
| `review_web/` | Review generated gesture clips and export quality-control decisions. |
| `validation/` | Verify canonical annotations and externally distributed data. |

Every command provides `--help` and accepts explicit input and output paths. Operational examples are collected in [`../docs/USAGE.md`](../docs/USAGE.md), [`../docs/ACQUISITION.md`](../docs/ACQUISITION.md), and [`../docs/REVIEW.md`](../docs/REVIEW.md).
