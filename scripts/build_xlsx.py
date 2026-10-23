"""Excel workbooks: the A-01 usage summary and the content index.

Derived columns are written as static values computed here (not formulas) so the numbers are
readable without recalculation, which matters for anything that reads the file without Excel.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from common import DATA, CONTENT, METADATA_COLUMNS, Record, display, parse_md_table

DISCLAIMER = "Fictional demo data."


def _size(capacity: int) -> str:
    return "Small" if capacity <= 4 else "Medium" if capacity <= 6 else "Large"


def _add_table(ws, name: str, header: list[str], rows: list[list], wrap_cols: tuple[int, ...] = ()) -> None:
    ws.append(header)
    for r in rows:
        ws.append(r)
    ref = f"A1:{get_column_letter(len(header))}{len(rows) + 1}"
    tab = Table(displayName=name, ref=ref)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(tab)
    ws.freeze_panes = "A2"
    for i, h in enumerate(header, start=1):
        width = max(len(str(h)), *(len(str(r[i - 1])) for r in rows)) + 2
        ws.column_dimensions[get_column_letter(i)].width = min(width, 60)
    for c in ws[1]:
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in ws.iter_rows(min_row=2):
        for c in r:
            c.alignment = Alignment(wrap_text=(c.column - 1) in wrap_cols, vertical="top")


def _readme_sheet(wb: Workbook, rec_lines: list[tuple[str, str]], guide: list[tuple[str, str]], note: str) -> None:
    ws = wb.active
    ws.title = "README"
    for k, v in rec_lines:
        ws.append([k, v])
    ws.append([])
    ws.append([note])
    ws.append([])
    ws.append(["Column or sheet", "Meaning"])
    start = ws.max_row  # the header row just added
    for k, v in guide:
        ws.append([k, v])
    ref = f"A{start}:B{ws.max_row}"
    tab = Table(displayName="Guide", ref=ref)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(tab)
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 90
    first_guide_row = start
    for row in ws.iter_rows():
        for c in row:
            # wrap only the Meaning column and the guide table; titles and the note run across
            wrap = c.column == 2 or c.row >= first_guide_row
            c.alignment = Alignment(wrap_text=wrap, vertical="top")
    ws["A1"].font = Font(bold=True, size=14)
    for r in range(1, len(rec_lines) + 1):
        ws.cell(r, 1).font = Font(bold=True, size=14 if r == 1 else 11)


def build_usage(rec: Record, out: Path) -> Path:
    src = DATA / "A-01_room-usage.csv"
    with open(src, newline="", encoding="utf-8") as f:
        raw = list(csv.DictReader(f))

    rooms = []
    for r in raw:
        b, u = int(r["booked_hours"]), int(r["used_hours"])
        bk, ns = int(r["bookings"]), int(r["no_show_bookings"])
        rooms.append({
            "id": r["room_id"], "name": r["room_name"], "floor": int(r["floor"]),
            "cap": int(r["capacity"]), "size": _size(int(r["capacity"])),
            "b": b, "u": u, "bk": bk, "ns": ns,
        })

    def pct(a, b):
        return round(100 * a / b, 1)

    tb = sum(r["b"] for r in rooms); tu = sum(r["u"] for r in rooms)
    tbk = sum(r["bk"] for r in rooms); tns = sum(r["ns"] for r in rooms)

    wb = Workbook()
    _readme_sheet(
        wb,
        [("A-01 Room Usage Summary, 2026-09-08 to 2026-09-19", ""),
         ("Study", "S-01 Meeting Room Booking Study"),
         ("Author", str(rec.meta.get("author", ""))),
         ("Date", display(rec.meta.get("date"))),
         ("Source", "RoomBook bookings joined to door-sensor occupancy, 8 rooms, 10 working days. "
                    "Written up in the Word/Markdown record A-01 and used in readout R-01.")],
        [("Summary", "Headline totals: booked, used and unused hours, bookings and no-shows."),
         ("By size", "The same measures grouped by room size: Small (4 seats), Medium (6), Large (10 to 16)."),
         ("By room", "One row per room."),
         ("Booked hours", "Hours booked in RoomBook."),
         ("Used hours", "Booked hours in which the sensor detected someone in the room."),
         ("Unused hours", "Booked hours minus used hours."),
         ("Unused %", "Unused hours as a percent of booked hours."),
         ("No-show bookings", "Bookings where no one was detected in the first 15 minutes."),
         ("No-show %", "No-show bookings as a percent of bookings.")],
        f"{DISCLAIMER} Derived columns are computed when the file is built and stored as values.",
    )

    ws = wb.create_sheet("Summary")
    _add_table(ws, "Headline", ["Metric", "Value", "Unit"], [
        ["Booked hours", tb, "hours"],
        ["Used hours", tu, "hours"],
        ["Unused hours", tb - tu, "hours"],
        ["Unused share of booked hours", pct(tb - tu, tb), "percent"],
        ["Bookings", tbk, "bookings"],
        ["No-show bookings", tns, "bookings"],
        ["No-show share of bookings", pct(tns, tbk), "percent"],
    ])

    ws = wb.create_sheet("By size")
    rows = []
    for size, label in (("Small", "Small (4 seats)"), ("Medium", "Medium (6 seats)"), ("Large", "Large (10 to 16 seats)")):
        g = [r for r in rooms if r["size"] == size]
        b = sum(r["b"] for r in g); u = sum(r["u"] for r in g)
        bk = sum(r["bk"] for r in g); ns = sum(r["ns"] for r in g)
        rows.append([label, ", ".join(r["name"] for r in g), b, u, b - u, pct(b - u, b), bk, ns, pct(ns, bk)])
    _add_table(ws, "BySize", ["Size", "Rooms", "Booked hours", "Used hours", "Unused hours",
                              "Unused %", "Bookings", "No-show bookings", "No-show %"], rows)

    ws = wb.create_sheet("By room")
    rows = [[r["id"], r["name"], r["floor"], r["cap"], r["size"], r["b"], r["u"], r["b"] - r["u"],
             pct(r["b"] - r["u"], r["b"]), r["bk"], r["ns"], pct(r["ns"], r["bk"])] for r in rooms]
    _add_table(ws, "ByRoom", ["Room ID", "Room", "Floor", "Seats", "Size", "Booked hours", "Used hours",
                              "Unused hours", "Unused %", "Bookings", "No-show bookings", "No-show %"], rows)

    p = wb.properties
    p.title = rec.title
    p.creator = str(rec.meta.get("author", ""))
    p.subject = "S-01 Meeting Room Booking Study"
    p.keywords = rec.id
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


def build_index(records: list[Record], out: Path) -> Path:
    # One-line summaries live in content/_index.md; everything else comes from each record's frontmatter.
    idx_text = (CONTENT / "_index.md").read_text(encoding="utf-8")
    summaries = {}
    for row in parse_md_table([l for l in idx_text.splitlines() if l.startswith("|")])[1:]:
        summaries[row[0]] = row[5]

    header = [label for label, _ in METADATA_COLUMNS] + ["Summary", "File"]
    rows = []
    for r in records:
        rows.append([display(r.meta.get(key)) for _, key in METADATA_COLUMNS]
                    + [summaries.get(r.id, ""), r.out_name])

    wb = Workbook()
    _readme_sheet(
        wb,
        [("Content index", ""),
         ("Study", "S-01 Meeting Room Booking Study"),
         ("Records", str(len(records)))],
        [("Index", "One row per record. Columns match the SharePoint metadata columns, plus Summary and File."),
         ("ID", "Record ID. Prefixes: PL plan, N notes, F finding, A analytics, R readout."),
         ("Valence", "pain-point, insight, or n/a."),
         ("Prevalence", "How many of the 6 interview participants raised it, as text."),
         ("File", "File name of the delivered copy in the library.")],
        f"{DISCLAIMER} Generated from the Markdown frontmatter and content/_index.md.",
    )
    ws = wb.create_sheet("Index")
    _add_table(ws, "ContentIndex", header, rows, wrap_cols=(1, len(header) - 2))
    p = wb.properties
    p.title = "Content Index"
    p.subject = "S-01 Meeting Room Booking Study"
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out
