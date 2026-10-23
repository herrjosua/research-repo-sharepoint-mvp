# research-repo-sharepoint-mvp

A small proof of concept: can Microsoft 365 Copilot answer questions about UX research kept as
Word, Excel, PowerPoint and PDF files in SharePoint, with no git, no scripts and no custom app on
the client side?

It is the low-tech counterpart to [`agentic-repo`](https://github.com/herrjosua/agentic-repo), a
git and Markdown research knowledge base queried by an AI agent. This repo keeps a deliberately
small subset of that idea (one study, nine records) and rewrites it so it survives as plain
SharePoint documents.

All data in this repository is **fictional**. The company (Harborview Group), the internal app
(RoomBook), the researcher and all participants are invented.

## Status

| Part | State |
|---|---|
| Study content (Markdown source) | Drafted |
| SharePoint conventions | Documented in [`docs/sharepoint-profile.md`](docs/sharepoint-profile.md) |
| Copilot test questions | Drafted in [`docs/copilot-test-plan.md`](docs/copilot-test-plan.md) |
| Conversion to Office files and PDF | Working: `python3 scripts/build.py` |
| Test in a SharePoint library with Copilot | Not started |

## The study

S-01, the Meeting Room Booking Study: 6 interviews and a two-week room usage pull at a fictional
company's headquarters. It was written to give Copilot three kinds of question to answer: what the
pain points were, how people work around them, and what the unexpected insight was. The remaining
test questions cover counting, spreadsheet lookups, cross-file answers, caveats and a question the
data cannot answer.

## Layout

```
content/    One Markdown file per record, flat. Source for the Office files.
  _index.md   Master index (becomes an Excel workbook)
  PL-01_...   Research plan
  N-01_...    Interview notes (6 sessions)
  F-01_...    Findings F-01 to F-05
  A-01_...    Room usage summary
  R-01_...    Readout (slide-structured, becomes the PowerPoint)
data/       CSV behind the analytics summary (A-01_room-usage.csv)
docs/       SharePoint profile and the Copilot test plan
scripts/    Build scripts (Markdown to Word, Excel, PowerPoint, PDF) and the verifier
build/      Generated output, git-ignored
```

Records are flat on purpose. In SharePoint the file name and the metadata columns carry the
context that folders carry in git.

## Conventions

Markdown here is written differently from `agentic-repo`: every file has a header table in the body
as well as frontmatter, cross-references use IDs and titles instead of relative links, and every
record restates its own context. The full rules and the SharePoint metadata columns are in
[`docs/sharepoint-profile.md`](docs/sharepoint-profile.md).

File names follow `<ID>_<short-title>_<yyyy-mm>.md`. ID prefixes: `PL` plan, `N` notes,
`F` finding, `A` analytics, `R` readout.

## Output formats

Markdown stays the source and Office files are generated from it. Edit the Markdown, not the
generated files. One finding (F-04) is deliberately delivered as PDF so Copilot's handling of each
format can be compared. The mapping is the `FORMAT` table in `scripts/common.py`.

| Record | Format |
|---|---|
| PL-01, N-01, F-01, F-02, F-03, F-05 | Word (.docx) |
| F-04 | PDF, exported from Word |
| A-01 | Excel (.xlsx) |
| Content index | Excel (.xlsx), `INDEX_content-index.xlsx` |
| R-01 | PowerPoint (.pptx) |

## Build

Requirements: Python 3.10 or later, [pandoc](https://pandoc.org/), and LibreOffice (`soffice` on
the PATH, used for the PDF step).

```
pip install -r requirements.txt
python3 scripts/build.py
```

The script lints the Markdown, clears `build/`, builds every file, then runs `scripts/verify.py`
(skip it with `--no-verify`). Output:

| Path | Contents |
|---|---|
| `build/sharepoint/` | The 10 files to upload to the library |
| `build/metadata.csv` | One row per file with the values for each SharePoint metadata column; paste into the library's grid view to apply them in bulk |
| `build/work/` | Intermediate files (the Word file behind the PDF, a LibreOffice profile) |

How each format is made:

- **Word:** pandoc converts the body of each Markdown file (frontmatter removed). A python-docx pass
  then sets column widths, borders, repeating header rows, landscape orientation for wide tables,
  and the document properties (title, author, subject).
- **Excel:** `openpyxl` builds formatted Excel Tables plus a README sheet. Derived columns such as
  unused percent are written as values, not formulas, so they can be read without recalculation.
- **PowerPoint:** `python-pptx` builds one slide per `## Slide N:` section in R-01. The slide title
  is a real title placeholder, tables carry alt text, and the full wording goes in the speaker notes.
- **PDF:** LibreOffice converts the Word file, requesting a tagged PDF.

`scripts/verify.py` reopens every output and checks headings, tables, list items, slide titles and
notes, the PDF text layer, that the spreadsheet numbers match the Markdown, and that
`metadata.csv` lists exactly the delivered files. Passing it does not check how the files look in
Word or PowerPoint: open them before uploading.

## Testing

Run the questions in [`docs/copilot-test-plan.md`](docs/copilot-test-plan.md) against a test
SharePoint library with the metadata columns applied, and record the results in that file.

## License

MIT, as in [`LICENSE`](LICENSE).

## AI-assisted development

This repository was developed with AI assistance (Claude). The study content is fictional and was
written for this proof of concept.
