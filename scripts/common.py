"""Shared loading and constants for the build scripts."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DATA = ROOT / "data"
BUILD = ROOT / "build"
WORK = BUILD / "work"          # intermediate files, not uploaded
OUT = BUILD / "sharepoint"     # the set to upload to the SharePoint library

# Delivered format per record. F-04 is a PDF on purpose, to compare formats in Copilot.
FORMAT = {
    "PL-01": "docx",
    "N-01": "docx",
    "F-01": "docx",
    "F-02": "docx",
    "F-03": "docx",
    "F-04": "pdf",
    "F-05": "docx",
    "A-01": "xlsx",
    "R-01": "pptx",
}
INDEX_OUT_NAME = "INDEX_content-index.xlsx"

# Order and labels of the SharePoint metadata columns (docs/sharepoint-profile.md).
METADATA_COLUMNS = [
    ("ID", "id"),
    ("Title", "title"),
    ("Record type", "type"),
    ("Study", "study_id"),
    ("Status", "status"),
    ("Valence", "valence"),
    ("Prevalence", "prevalence"),
    ("Author", "author"),
    ("Date", "date"),
    ("Last reviewed", "last_reviewed"),
    ("Related", "related"),
]

_FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


@dataclass
class Record:
    id: str
    path: Path
    meta: dict
    body: str

    @property
    def title(self) -> str:
        return str(self.meta["title"])

    @property
    def out_name(self) -> str:
        return f"{self.path.stem}.{FORMAT[self.id]}"


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = _FM.match(text)
    if not m:
        raise ValueError("file has no YAML frontmatter")
    return yaml.safe_load(m.group(1)), m.group(2).lstrip("\n")


def load_records() -> list[Record]:
    records = []
    for path in sorted(CONTENT.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
        rec = Record(id=str(meta["id"]), path=path, meta=meta, body=body)
        if rec.id not in FORMAT:
            raise ValueError(f"{path.name}: no output format configured for {rec.id}")
        if not path.name.startswith(rec.id + "_"):
            raise ValueError(f"{path.name}: file name must start with {rec.id}_")
        records.append(rec)
    missing = set(FORMAT) - {r.id for r in records}
    if missing:
        raise ValueError(f"configured records with no Markdown file: {sorted(missing)}")
    return records


def parse_md_table(lines: list[str]) -> list[list[str]]:
    """Rows of a pipe table (separator row dropped), cells stripped."""
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.fullmatch(r"\|[\s:|-]+\|", line):
            continue
        rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def display(value) -> str:
    """Metadata value as plain text for a spreadsheet or CSV cell."""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    if value is None:
        return ""
    return str(value)


def lint_markdown(records: list["Record"]) -> list[str]:
    """Problems that would silently change how pandoc renders the file."""
    problems = []
    for rec in records:
        lines = rec.body.split("\n")
        for i in range(1, len(lines)):
            if re.match(r"^(- |\d+\. )", lines[i]):
                prev = lines[i - 1]
                if prev.strip() and not re.match(r"^(- |\d+\. |#|\s{2,}|\|)", prev):
                    problems.append(
                        f"{rec.path.name}: list item needs a blank line before it (body line {i + 1}): {prev[:50]!r}")
    return problems
