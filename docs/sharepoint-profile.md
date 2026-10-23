# SharePoint profile

How the Markdown in `content/` is written so it still works after conversion to Word, Excel,
PowerPoint and PDF files in a SharePoint library that Microsoft 365 Copilot searches. This profile
exists because Copilot sees SharePoint files as documents, not as a repository: it does not follow
relative links or folder paths, and it may not treat YAML frontmatter as structured fields.

## Rules

| Rule | Why |
|---|---|
| Every file has an ID prefix and a descriptive name: `F-01_booked-rooms-sit-empty_2026-09` | The name is the one piece of context that always travels with the file |
| Every file opens with a header table (ID, type, study, valence, prevalence, status, author, dates, related) | Frontmatter may not be indexed as fields; the table is body text, so it is |
| Frontmatter is kept alongside the table | It is the source for the SharePoint metadata columns below |
| Cross-references use ID and title ("F-04 Recurring bookings..."), never relative paths or `[[wiki]]` links | Copilot cannot follow links between files |
| Each record restates its own context (study, dates, method, participant count) | Copilot retrieves pieces of files, not whole folders |
| Prevalence is written as text ("5 of 6 participants (83%)") | Charts and images are not read reliably |
| Quotes are inline, with participant ID | Evidence has to be in the file to be cited |
| Each finding has a Limits section | Lets Copilot answer "how reliable is this" from the source |
| Interpretation is labeled as ours, separate from what participants said | Keeps answers from presenting inference as fact |

## Metadata columns

These become SharePoint site columns, attached through one content type for all records.

| Column | Type | Source field | Values |
|---|---|---|---|
| ID | Single line of text | `id` | `F-01`, `A-01`, ... |
| Title | Single line of text | `title` | |
| Record type | Choice | `type` | plan, notes, finding, analytics, readout, index |
| Study | Single line of text | `study_id` | `S-01` |
| Status | Choice | `status` | draft, final |
| Valence | Choice | `valence` | pain-point, insight, n/a |
| Prevalence | Single line of text | `prevalence` | "5 of 6 participants" |
| Author | Single line of text | `author` | |
| Date | Date | `date` | |
| Last reviewed | Date | `last_reviewed` | |
| Related | Single line of text | `related` | `F-04, F-05, A-01` |

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
- **PDF:** needs a real text layer. Treat it as a distribution copy of a Word file.

## How this differs from the full research repo

The full repo (`agentic-repo`) relies on git, relative links, per-folder indexes and frontmatter
queried by tooling. This profile is the same content with the structure moved into file names, body
text and SharePoint columns. It assumes no git and no scripts on the client side.
