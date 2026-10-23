#!/usr/bin/env python3
"""Build the SharePoint upload set from content/*.md.

Usage:  python3 scripts/build.py            # build everything and verify
        python3 scripts/build.py --no-verify

Output:
  build/sharepoint/   files to upload to the library
  build/metadata.csv  metadata column values, one row per file
  build/work/         intermediate files (the Word file behind the PDF, LibreOffice profile)
Requires: pandoc and LibreOffice (soffice) on PATH; pip install -r requirements.txt
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

from build_docx import build_docx
from build_metadata import build_metadata
from build_pdf import build_pdf
from build_pptx import build_pptx
from build_xlsx import build_index, build_usage
from common import BUILD, FORMAT, INDEX_OUT_NAME, OUT, WORK, lint_markdown, load_records


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-verify", action="store_true", help="skip the verification pass")
    args = ap.parse_args()

    for tool in ("pandoc", "soffice"):
        if not shutil.which(tool):
            print(f"error: '{tool}' not found on PATH", file=sys.stderr)
            return 2

    records = load_records()
    problems = lint_markdown(records)
    if problems:
        print("Markdown problems:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    if BUILD.exists():
        shutil.rmtree(BUILD)
    OUT.mkdir(parents=True)
    WORK.mkdir(parents=True)

    for rec in records:
        fmt = FORMAT[rec.id]
        if fmt == "docx":
            build_docx(rec, OUT / rec.out_name)
        elif fmt == "pdf":
            docx = build_docx(rec, WORK / f"{rec.path.stem}.docx")
            build_pdf(docx, OUT / rec.out_name, WORK / "lo-profile")
        elif fmt == "xlsx":
            build_usage(rec, OUT / rec.out_name)
        elif fmt == "pptx":
            build_pptx(rec, OUT / rec.out_name)
        print(f"built {rec.out_name}")
    build_index(records, OUT / INDEX_OUT_NAME)
    print(f"built {INDEX_OUT_NAME}")
    build_metadata(records, BUILD / "metadata.csv")
    print("built metadata.csv")

    if args.no_verify:
        return 0
    return subprocess.call([sys.executable, str(__file__).replace("build.py", "verify.py")])


if __name__ == "__main__":
    sys.exit(main())
