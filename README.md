# research-repo-sharepoint-mvp

A small proof of concept: can Microsoft 365 Copilot answer questions about UX research kept as
Word, Excel, PowerPoint and PDF files in SharePoint, with no git, no scripts and no custom app on
the client side?

It is the low-tech counterpart to [`agentic-repo`](https://github.com/herrjosua/agentic-repo), a
git and Markdown research knowledge base queried by an AI agent. This repo keeps a deliberately
small subset of that idea (one study, nine records) as plain SharePoint documents. The Office and
PDF files are the source of truth and are edited directly. There is no build step, and nothing here
needs Python or any other tooling.

All data in this repository is **fictional**. The company (Harborview Group), the internal app
(RoomBook), the researcher and all participants are invented.

## Status

| Part | State |
|---|---|
| Study files (Word, Excel, PowerPoint, PDF) | Done |
| SharePoint conventions | Documented in [`docs/sharepoint-profile.md`](docs/sharepoint-profile.md) |
| Copilot test questions | Drafted in [`docs/copilot-test-plan.md`](docs/copilot-test-plan.md) |
| Test in a SharePoint library with Copilot | Not started |

## The study

S-01, the Meeting Room Booking Study: 6 interviews and a two-week room usage pull at a fictional
company's headquarters. It was written to give Copilot three kinds of question to answer: what the
pain points were, how people work around them, and what the unexpected insight was. The remaining
test questions cover counting, spreadsheet lookups, cross-file answers, caveats and a question the
data cannot answer.

## Layout

```
library/   The files to upload to the SharePoint library (10 files)
source/    Word original of the one PDF in library/
docs/      SharePoint profile, Copilot test plan, metadata values (library-metadata.csv)
```

Only `library/` goes into SharePoint. `docs/` holds the answer key for the test, so it stays out of
the library.

| Record | File in `library/` | Format |
|---|---|---|
| PL-01 Research plan | `PL-01_research-plan_room-booking_2026-09.docx` | Word |
| N-01 Interview notes | `N-01_interview-notes_room-booking_2026-09.docx` | Word |
| F-01 Booked rooms often sit empty | `F-01_booked-rooms-sit-empty_2026-09.docx` | Word |
| F-02 Room size and equipment not shown | `F-02_room-details-missing_2026-09.docx` | Word |
| F-03 Booking and invite are separate steps | `F-03_booking-and-calendar-separate_2026-09.docx` | Word |
| F-04 Recurring bookings are all-or-nothing | `F-04_recurring-bookings-all-or-nothing_2026-09.pdf` | PDF |
| F-05 People book defensively (insight) | `F-05_people-book-defensively_2026-09.docx` | Word |
| A-01 Room usage summary | `A-01_room-usage-summary_2026-09.xlsx` | Excel |
| R-01 Readout | `R-01_readout_room-booking_2026-10.pptx` | PowerPoint |
| Content index | `INDEX_content-index.xlsx` | Excel |

F-04 is a PDF on purpose, so Copilot's handling of each format can be compared.

## Conventions

Every file has an ID prefix and a descriptive name, opens with a header table, restates its own
context, and refers to other records by ID and title instead of links. File names follow
`<ID>_<short-title>_<yyyy-mm>`. ID prefixes: `PL` plan, `N` notes, `F` finding, `A` analytics,
`R` readout. The full rules and the SharePoint metadata columns are in
[`docs/sharepoint-profile.md`](docs/sharepoint-profile.md).

## Using it

1. Create a test SharePoint library.
2. Add the metadata columns listed in `docs/sharepoint-profile.md`.
3. Upload the contents of `library/`.
4. Apply the metadata: open the library in grid view and paste the columns from
   `docs/library-metadata.csv`. Its first column is the file name.
5. Run the questions in `docs/copilot-test-plan.md`, again the next day because indexing can lag,
   and record the results in that file.

## Editing

Edit the Office files directly. The same facts appear in several files, for example the unused-hours
figures in A-01, F-01, F-05 and R-01, so the "Keeping the files consistent" table in
`docs/sharepoint-profile.md` lists where to update.

F-04 is the exception. Edit the Word original in `source/`, then export it to PDF into `library/`,
with "Document structure tags for accessibility" ticked in the Save As PDF options so the PDF keeps
its structure.

An earlier variant of this repo, with Markdown sources and a Python script that generated these
files, is in the git history (commit `3aea093`).

## License

MIT, as in [`LICENSE`](LICENSE).

## AI-assisted development

This repository was developed with AI assistance (Claude). The study content is fictional and was
written for this proof of concept.
