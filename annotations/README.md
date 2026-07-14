# Annotations

`original/` is the canonical temporal annotation set. It contains 336 CSV files and 2,751 gesture intervals across 30 labels. CSV columns are `begin,end,label`.

`balanced/annotation_all_balance.json` contains 4,255 derived samples produced by segmenting sufficiently long original intervals with an eight-frame target interval. This representation supports class-balanced sampling; the original annotations remain canonical, and no train/test split is prescribed.

See `docs/DATA_FORMAT.md` for interval semantics and JSON fields.
