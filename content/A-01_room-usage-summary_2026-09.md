---
id: A-01
title: Room Usage Summary, 2026-09-08 to 2026-09-19
type: analytics
study_id: S-01
status: final
valence: n/a
prevalence: n/a
author: Maya Alvarez
date: 2026-09-24
last_reviewed: 2026-10-05
related: [F-01, F-05, R-01]
data_file: data/A-01_room-usage.csv
---

# A-01 · Room Usage Summary, 2026-09-08 to 2026-09-19

| Field | Value |
|---|---|
| ID | A-01 |
| Type | Analytics summary |
| Study | S-01 Meeting Room Booking Study |
| Status | Final |
| Author | Maya Alvarez |
| Date | 2026-09-24 |
| Last reviewed | 2026-10-05 |
| Related | F-01, F-05, R-01 |
| Data | data/A-01_room-usage.csv (one row per room) |

*Fictional demo data.*

## Headline
Over 10 working days, **109 of 352 booked hours (31.0%) went unused**, and **78 of 268 bookings
(29.1%) were no-shows**. Small rooms were the worst: the three 4-seat rooms had **40.4%** of booked
hours unused.

## How the numbers were made
- **Source:** RoomBook bookings joined to door-sensor occupancy for all 8 rooms,
  2026-09-08 to 2026-09-19.
- **Booked hours:** hours booked in RoomBook.
- **Used hours:** booked hours in which the sensor detected someone in the room.
- **Unused hours:** booked hours minus used hours.
- **No-show booking:** a booking where no one was detected in the first 15 minutes.

## By room
| Room | Floor | Seats | Booked hours | Used hours | Unused hours | Unused % | Bookings | No-shows | No-show % |
|---|---|---|---|---|---|---|---|---|---|
| Harbor | 2 | 4 | 40 | 26 | 14 | 35.0% | 38 | 12 | 31.6% |
| Pier | 2 | 6 | 52 | 36 | 16 | 30.8% | 44 | 13 | 29.5% |
| Lighthouse | 2 | 10 | 58 | 41 | 17 | 29.3% | 36 | 9 | 25.0% |
| Anchor | 2 | 4 | 30 | 17 | 13 | 43.3% | 30 | 11 | 36.7% |
| Beacon | 3 | 12 | 52 | 39 | 13 | 25.0% | 28 | 6 | 21.4% |
| Mariner | 3 | 6 | 48 | 34 | 14 | 29.2% | 40 | 10 | 25.0% |
| Keel | 3 | 4 | 34 | 19 | 15 | 44.1% | 34 | 14 | 41.2% |
| Bridge | 3 | 16 | 38 | 31 | 7 | 18.4% | 18 | 3 | 16.7% |
| **All rooms** | | | **352** | **243** | **109** | **31.0%** | **268** | **78** | **29.1%** |

## By room size
| Size | Rooms | Booked hours | Unused hours | Unused % | No-show % |
|---|---|---|---|---|---|
| Small (4 seats) | Harbor, Anchor, Keel | 104 | 42 | 40.4% | 36.3% |
| Medium (6 seats) | Pier, Mariner | 100 | 30 | 30.0% | 27.4% |
| Large (10 to 16 seats) | Lighthouse, Beacon, Bridge | 148 | 37 | 25.0% | 22.0% |

## Highest and lowest
- Highest unused share: **Keel, 44.1%**, then Anchor, 43.3%.
- Lowest unused share: **Bridge, 18.4%**.

## Limits
Two working weeks at one site. The data shows that booked rooms go unused but not why. Sensors detect
presence, so a booking used by someone who stepped out counts as used. Interviews (N-01) are the
source for reasons.
