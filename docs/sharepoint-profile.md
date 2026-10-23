# SharePoint profile

How the records in `library/` are written so Microsoft 365 Copilot can use them from a SharePoint
library. The records are Word, Excel, PowerPoint and PDF files, edited directly. This profile exists
because Copilot sees SharePoint files as documents, not as a repository: it does not follow links or
folder paths, and it may not index metadata columns as searchable fields.

## Rules

| Rule | Why |
|---|---|
| Every file has an ID prefix and a descriptive name: `F-01_booked-rooms-sit-empty_2026-09` | The name is the one piece of context that always travels with the file |
| Every file opens with a header table (ID, type, study, valence, prevalence, status, author, dates, related) | Metadata columns may not be indexed as fields; the table is body text, so it is |
| The same values go in the SharePoint metadata columns below | Columns make the library filterable; `docs/library-metadata.csv` has the values for each file |
| Cross-references use ID and title ("F-04 Recurring bookings..."), never file paths or links | Copilot cannot follow links between files |
| Each record restates its own context (study, dates, method, participant count) | Copilot retrieves pieces of files, not whole folders |
| Prevalence is written as text ("5 of 6 participants (83%)") | Charts and images are not read reliably |
| Quotes are inline, with participant ID | Evidence has to be in the file to be cited |
| Each finding has a Limits section | Lets Copilot answer "how reliable is this" from the source |
| Interpretation is labeled as ours, separate from what participants said | Keeps answers from presenting inference as fact |

## Metadata columns

These become SharePoint site columns, attached through one content type for all records.

| Column | Type | Header table row | Values |
|---|---|---|---|
| ID | Single line of text | ID | `F-01`, `A-01`, ... |
| Title | Single line of text | (document title) | |
| Record type | Choice | Type | plan, notes, finding, analytics, readout, index |
| Study | Single line of text | Study | `S-01` |
| Status | Choice | Status | draft, final |
| Valence | Choice | Valence | pain-point, insight, n/a |
| Prevalence | Single line of text | Prevalence | "5 of 6 participants" |
| Author | Single line of text | Author | |
| Date | Date | Date | |
| Last reviewed | Date | Last reviewed | |
| Related | Single line of text | Related | `F-04, F-05, A-01` |

## ID prefixes

| Prefix | Record |
|---|---|
| PL | Research plan |
| N | Interview notes |
| F | Finding (pain point, workaround or insight) |
| A | Analytics summary |
| R | Readout |

## Format-specific rules (for the converted files)

- **Word:** real Heading styles, not bold text. The header table stays at the top. One record per
  file.
- **Excel:** formatted Tables with one header row, no merged cells, a README sheet describing
  columns.
- **PowerPoint:** a descriptive sentence as each slide title; the full wording in the speaker notes;
  alt text on any chart.
- **PDF:** needs a real text layer. Treat it as a distribution copy of a Word file; the Word original
  is in `source/`.

## Keeping the files consistent

There is no build step, so the same fact is typed in several files. After changing one, update the
others.

| Fact | Lives in |
|---|---|
| Who raised what (counts out of 6) | N-01 matrix, the findings F-01 to F-05, R-01 slide 4, the index workbook |
| Booked, used and unused hours; no-show rates | A-01 workbook, F-01, F-05, R-01 slides 3 and 7 |
| Quotes | N-01 and the finding that uses them |
| Titles, dates, status | Each file's header table, the index workbook, `docs/library-metadata.csv` |

## How this differs from the full research repo

The full repo (`agentic-repo`) relies on git, relative links, per-folder indexes and frontmatter
queried by tooling. This profile is the same content with the structure moved into file names, body
text and SharePoint columns. It assumes no git, no scripts and no Python on the client side.
