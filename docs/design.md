# Design notes

This is an English overview of how dronyDeliv works and why it is built the way it is. It covers both the original 2019 submission and the 2026 rewrite. The original implementation report (in Portuguese) is [`report-group16-pt.pdf`](report-group16-pt.pdf).

## The problem

A delivery company runs a fleet of drones spread across several zones. At regular intervals it receives two files: the current state of every drone, and a batch of new parcel orders. The program has to:

- assign each order to a suitable drone, or cancel it if none can do the job;
- produce a **timetable** saying when each drone leaves and for which client;
- produce an **updated drone file**, stamped 30 minutes later, that becomes the input to the next cycle.

Because the output drone file feeds the next run, mistakes compound. A wrong availability time or autonomy figure in one cycle skews every cycle after it. That is why correctness of the drone state mattered more than anything else in the rewrite.

## How a run works

```
drones file ──┐                          ┌──> updated drones file  (+30 min)
              ├─> validate ─> assign ──> ┤
parcels file ─┘                          └──> timetable file
```

1. **Validate.** Both file names encode a time and date (`drones10h00_2019y11m5.txt`). They must match each file's own header, and the two files must refer to the same moment. Mismatches are rejected before any work is done.
2. **Read** drones and orders into typed records (`Drone`, `Order`).
3. **Assign.** Each order is processed in the order it appears in the file (see below).
4. **Write** the two output files from the single `Schedule` that the assignment step returns.

## Choosing a drone

For each order, every drone is ranked by:

| Priority | Criterion | Reason |
|---|---|---|
| 1 | Operates in the order's zone | Drones cannot leave their zone |
| 2 | Earliest availability | Deliver as soon as possible |
| 3 | Most remaining autonomy | Spread battery use across the fleet |
| 4 | Least accumulated distance | Spread wear across the fleet |
| 5 | Name | Deterministic tie-break, so runs are reproducible |

The best-ranked drone that passes four hard checks gets the order. It must be in the order's zone, its maximum range must cover the distance, its weight capacity must cover the parcel, and its remaining autonomy must cover the round trip (twice the distance). If no drone passes, the order is cancelled.

The algorithm is **greedy**. Each order takes the best drone available at that moment, and later orders are never reconsidered. Orders are simply served in the order they appear in the file. That keeps the program easy to follow, which mattered for a first-year course. It is not globally optimal. An early, easy order can take a drone that a later, harder order needed.

## Time rules

- A drone departs at whichever is later: when it is free, or when the order was placed.
- Drones only fly between **08:00 and 20:00**. If a round trip would end after 20:00, the departure moves to 08:00 the next day. The `eva` order in the README example shows this.
- After a delivery, the drone's autonomy drops and its accumulated distance rises by the round-trip distance. It becomes free again when the trip ends.

## Code structure

| Module | Responsibility |
|---|---|
| `models.py` | Plain data types: `Drone`, `Order`, `Delivery`, `Schedule`, `Header` |
| `fileio.py` | Parsing, validation and writing; the only module that touches files |
| `scheduler.py` | The assignment algorithm; pure functions with no I/O |
| `cli.py` | Argument parsing and error reporting |

Keeping the scheduler free of file handling means it can be tested directly with small, hand-built fleets. Most of the test suite works this way.

## What changed from the 2019 version

The 2019 code worked on the course's test sets but had structural weaknesses. The 2026 rewrite keeps the same rules and fixes the following.

**Records as lists of strings.** Drones and orders were lists of text fields, indexed through constants such as `c.Autonomy = 5`. Every comparison had to convert types again (`float(drone[c.Autonomy])`), and a wrong index failed silently. These are now dataclasses with real numbers and `datetime` values.

**The month bug.** Dates were parsed with the format `%Y-%M-%d`, where `%M` means *minutes*, not month. Every date was effectively read as January. Sorting across months and next-day rollovers at month ends were wrong. Using real `datetime` values throughout removes the problem.

**Only three candidates.** The original looked only at the top three ranked drones. That crashed with `IndexError` when the fleet had fewer than three drones, and cancelled orders unnecessarily when the fourth-ranked drone could have taken them. The rewrite checks every drone.

**Timetable reconstructed after the fact.** The original report lists a known bug: the drone file and the timetable came out with different times depending on which was written first. The timetable writer tried to work out departure times again from the final drone states, and that loses information when a drone flies more than once. The rewrite records each departure at the moment the drone is assigned. Both files are written from that one record, so they always agree.

**File names validated by position.** Validation sliced characters at fixed positions, such as `droneFile[6:11]`. That broke when the path included a folder, or when the day had two digits instead of one. Names are now parsed with a regular expression applied to the file name only.

**No tests.** The original was checked by hand against the course test sets. The rewrite has unit tests for the scheduling rules and the bugs above, plus an end-to-end test against the example files. These run on every push through GitHub Actions.

## Possible extensions

- Accept CSV or JSON input alongside the course's text format.
- Add a `--dry-run` mode that prints the timetable without writing files.
- Explore a non-greedy assignment, such as matching all of a batch's orders at once, to reduce cancellations.
