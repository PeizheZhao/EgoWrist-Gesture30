from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/dataset"))
from annotation_io import Annotation, load_csv  # noqa: E402


class AnnotationTests(unittest.TestCase):
    def test_inclusive_frame_count(self) -> None:
        self.assertEqual(Annotation(14, 27, 10).frame_count, 14)

    def test_all_csv_files_and_rows(self) -> None:
        paths = sorted((ROOT / "annotations/original/csv").glob("subject*/scene*/*.csv"))
        self.assertEqual(len(paths), 336)
        self.assertEqual(sum(len(load_csv(path)) for path in paths), 2751)

    def test_balanced_count(self) -> None:
        with (ROOT / "annotations/balanced/annotation_all_balance.json").open() as handle:
            data = json.load(handle)
        self.assertEqual(len(data["label_map"]), 30)
        self.assertEqual(len(data["database"]), 4255)


if __name__ == "__main__":
    unittest.main()
