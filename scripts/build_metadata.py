"""Write build/metadata.csv: one row per delivered file, columns match the SharePoint site columns.

Paste the columns into the library's "Edit in grid view" to apply metadata in bulk.
"""
from __future__ import annotations

import csv
from pathlib import Path

from common import INDEX_OUT_NAME, METADATA_COLUMNS, Record, display


def build_metadata(records: list[Record], out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["File name"] + [label for label, _ in METADATA_COLUMNS])
        for r in records:
            w.writerow([r.out_name] + [display(r.meta.get(key)) for _, key in METADATA_COLUMNS])
        w.writerow([INDEX_OUT_NAME, "INDEX", "Content Index", "index", "S-01", "final", "n/a", "n/a", "", "", "2026-10-05", ""])
    return out
