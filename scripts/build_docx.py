"""Markdown -> Word (.docx) with pandoc, then tidy tables and set document properties."""
from __future__ import annotations

import subprocess
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from common import Record


def _set_borders(table) -> None:
    tbl_pr = table._tbl.tblPr
    old = tbl_pr.find(qn("w:tblBorders"))
    if old is not None:
        tbl_pr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "808080")
        borders.append(el)
    look = tbl_pr.find(qn("w:tblLook"))
    if look is not None:
        look.addprevious(borders)  # keep schema order
    else:
        tbl_pr.append(borders)


def _mark_header_row(table) -> None:
    """Repeat the first row on each page and flag it as a header row (accessibility)."""
    row = table.rows[0]
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:tblHeader")) is None:
        tr_pr.append(OxmlElement("w:tblHeader"))
    for cell in row.cells:
        tc_pr = cell._tc.get_or_add_tcPr()
        if tc_pr.find(qn("w:shd")) is None:
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), "E7E6E6")
            # schema order inside tcPr: tcW, gridSpan, vMerge, tcBorders, shd, ..., vAlign
            anchor = tc_pr.find(qn("w:tcBorders"))
            if anchor is None:
                anchor = tc_pr.find(qn("w:tcW"))
            if anchor is not None:
                anchor.addnext(shd)
            else:
                tc_pr.insert(0, shd)
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True


def _set_col_widths(table, widths_in: list[float]) -> None:
    """Write an explicit grid (pandoc leaves tblGrid empty) and matching cell and table widths."""
    table.autofit = False
    tbl = table._tbl
    grid = tbl.tblGrid
    for gc in list(grid):
        grid.remove(gc)
    for w in widths_in:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w * 1440)))
        grid.append(gc)
    tbl_w = tbl.tblPr.find(qn("w:tblW"))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_w.set(qn("w:w"), str(int(sum(widths_in) * 1440)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_in):
            cell.width = Inches(w)


def _auto_widths(table, total_in: float) -> list[float]:
    """Column widths in proportion to cell text, never narrower than the longest word.

    Wide tables cap the text-length preference so short columns are not starved.
    """
    ncols = len(table.rows[0].cells)
    cap = 16 if ncols >= 6 else 40
    weights = []
    for c in range(ncols):
        texts = [row.cells[c].text for row in table.rows]
        longest_cell = max(len(t) for t in texts)
        longest_word = max(len(w) for t in texts for w in t.split() or [""])
        weights.append(max(longest_word + 3, min(longest_cell, cap)))
    scale = total_in / sum(weights)
    return [w * scale for w in weights]


def _tidy(doc: Document, rec: Record) -> None:
    wide = any(len(t.rows[0].cells) >= 7 for t in doc.tables)
    sec = doc.sections[0]
    # pandoc's output has no explicit page setup: set US Letter with 1 inch margins
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)
    if wide:  # landscape for documents with a wide matrix
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
    text_width = (sec.page_width - sec.left_margin - sec.right_margin) / 914400  # inches

    for table in doc.tables:
        _set_borders(table)
        _mark_header_row(table)
        ncols = len(table.rows[0].cells)
        header = [c.text.strip() for c in table.rows[0].cells]
        if header == ["Field", "Value"]:
            _set_col_widths(table, [1.7, text_width - 1.7])
        else:
            _set_col_widths(table, _auto_widths(table, text_width))
        if ncols >= 5:  # smaller text so wide tables fit
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(9)

    cp = doc.core_properties
    cp.title = rec.title
    cp.author = str(rec.meta.get("author", ""))
    cp.subject = f"{rec.meta.get('study_id', '')} {rec.meta.get('type', '')}".strip()
    cp.keywords = rec.id
    cp.comments = "Fictional demo data. Generated from Markdown by scripts/build_docx.py."


def build_docx(rec: Record, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "docx", "-o", str(out)],
        input=rec.body.encode("utf-8"),
        check=True,
    )
    doc = Document(str(out))
    _tidy(doc, rec)
    doc.save(str(out))
    return out
