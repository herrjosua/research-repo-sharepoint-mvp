# Copilot test plan

Pass/fail check for whether Microsoft 365 Copilot can answer questions from the converted files in a
SharePoint library. Fictional data (study S-01, Meeting Room Booking Study).

## How to run
1. Upload the files in `library/` to a test library, and only those: not `docs/` (this file holds
   the answers) or `source/`. Add the metadata columns (see `sharepoint-profile.md`);
   `library-metadata.csv` has the values for each file.
2. Wait for indexing; run the questions again the next day, because indexing can lag.
3. Ask each question in Copilot Chat, in a new chat each time.
4. Record the result in the table at the bottom.

## Questions

| # | Question | Expected answer | Expected source | Tests |
|---|---|---|---|---|
| 1 | What were the main pain points users had when booking a meeting room? | Four: booked rooms sit empty (5 of 6), room size and equipment not shown (4 of 6), booking and calendar invite are separate steps (4 of 6), recurring bookings cannot be released one date at a time (3 of 6) | R-01, F-01 to F-04 | Summary across files |
| 2 | How are users getting around the problem of booked rooms being empty? | Look in the window, ping the booker in Teams, check the floor 3 tablet, take the room anyway; the office manager cancels by guessing | F-01, N-01 | Workarounds |
| 3 | What was the most interesting or unexpected insight? | People book rooms they may not need ("just in case") because getting one back is hard; 4 of 6 | F-05, R-01 | Insight |
| 4 | How many participants found a booked room empty? | 5 of 6 (all except P06, the new hire) | F-01, N-01 | Counting |
| 5 | What share of booked room hours went unused? | 31.0% (109 of 352 hours) | A-01, R-01 | Excel number |
| 6 | Which room had the highest share of unused booked hours? | Keel, 44.1% (then Anchor, 43.3%) | A-01 | Excel lookup |
| 7 | Why don't people cancel one date of a recurring booking? | It can only be cancelled as a whole series, so skipped dates stay booked ("If you cancel one week you cancel them all") | F-04 | Delivered as PDF |
| 8 | What did the new hire say about booking rooms? | Did not know how many people a room fit; books two rooms and cancels one because a colleague said rooms are hard to get | N-01, F-02, F-05 | Role-based retrieval |
| 9 | Does the usage data support what people said about empty rooms? | Yes: 31.0% of booked hours unused and 29.1% of bookings were no-shows, consistent with 5 of 6 finding a booked room empty | A-01, F-01 | Cross-file |
| 10 | Who ran the interviews and when? | Maya Alvarez, 2026-09-15 to 2026-09-17 | PL-01, N-01 | Metadata |
| 11 | How reliable are these findings? | Six interviews at one site: shows kinds of problems, not how common they are; usage data shows that rooms go unused, not why | F-01 Limits, R-01 slide 9 | Caveats |
| 12 | What did participants say about parking? | Nothing: parking is not covered in the study. A correct answer says so | None | Should not invent |
| 13 | Is the idea that empty bookings cause defensive booking proven? | No: it is our interpretation and was not tested | F-05 | Interpretation vs fact |

## Scoring
For each question record:
- **Correct** (yes / partly / no) against the expected answer
- **Right source cited** (yes / no)
- **Invented content** (yes / no); any invented fact is a fail
- **File format of the source** (Word, Excel, PowerPoint, PDF)

Also note: whether Copilot used the metadata columns, and whether the index workbook helped.

## Results
| # | Correct | Right source | Invented | Source format | Notes |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |
| 11 | | | | | |
| 12 | | | | | |
| 13 | | | | | |
