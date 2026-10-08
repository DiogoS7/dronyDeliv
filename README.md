# dronyDeliv

[![CI](https://github.com/DiogoS7/dronyDeliv/actions/workflows/ci.yml/badge.svg)](https://github.com/DiogoS7/dronyDeliv/actions/workflows/ci.yml)

A command-line scheduler for a drone delivery company. Given the current state of a drone fleet and a list of parcel orders, it decides which drone delivers each parcel, cancels orders no drone can handle, and writes out the updated fleet and a delivery timetable.

Originally built in 2019 as the group project for **Programação 1** (LTI) and refactored in 2026 into a tested, installable package.

## Results

What happens when you run it on the sample files: **4 drones, 6 orders, on Tuesday 5 November 2019.**

> ✅ **5 delivered** &nbsp;·&nbsp; 🌙 **1 moved to the next morning** &nbsp;·&nbsp; ❌ **1 cancelled**

![Timeline of the example run: which drone flew which order, and when](docs/example-timeline.svg)

### What happened to each order

- ✅ **ana** gets her parcel from **alpha** at 10:00. It's the first Lisbon drone free.
- ✅ **bruno** gets his from **charlie** at 10:15. It's the only drone in Porto.
- ✅ **carla** gets hers from **bravo** at 10:30. alpha is still out delivering to ana.
- ✅ **filipe** gets his from **delta** at 12:00. His 9 kg parcel is 5.5 km away, and only delta is strong enough with the range to get there.
- 🌙 **eva** gets hers from **alpha** at 08:00 the next morning. She ordered at 19:30, and the 45-minute trip wouldn't be back before drones stop flying at 20:00.
- ❌ **duarte**'s order is cancelled. He's in Faro, and no drone works there.

### The fleet afterwards

Every run also saves each drone's new state, ready for the next batch of orders.

| Drone | Battery range left | Free again |
|---|---|---|
| alpha | 31 km (was 40) | Wed 6 Nov, 08:45 |
| bravo | 22.6 km (was 25) | Tue 5 Nov, 11:00 |
| charlie | 52 km (was 60) | Tue 5 Nov, 11:15 |
| delta | 1 km (was 12), nearly empty | Tue 5 Nov, 13:30 |

<details>
<summary>See the raw output files</summary>

`timetable10h00_2019y11m5.txt`, with cancelled orders first, then each departure in time order:

```
2019-11-05, 11:00, duarte, cancelled
2019-11-05, 10:00, ana, alpha
2019-11-05, 10:15, bruno, charlie
2019-11-05, 10:30, carla, bravo
2019-11-05, 12:00, filipe, delta
2019-11-06, 08:00, eva, alpha
```

`drones10h30_2019y11m5.txt`, the updated fleet:

```
bravo, Lisbon, 2, 1500, 82.4, 22.6, 2019-11-05, 11:00
charlie, Porto, 8, 5000, 18.0, 52.0, 2019-11-05, 11:15
delta, Lisbon, 10, 6000, 11.0, 1.0, 2019-11-05, 13:30
alpha, Lisbon, 5, 3000, 129.5, 31.0, 2019-11-06, 08:45
```

Both files also start with a short header (time, date, company). The full files are in [`examples/expected/`](examples/expected).

</details>

Want the details? [How drones are chosen](#how-drones-are-chosen) explains the rules, and the [design notes](docs/design.md) explain how the program is built.

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/DiogoS7/dronyDeliv.git
cd dronyDeliv
pip install -e .

dronydeliv examples/drones10h00_2019y11m5.txt examples/parcels10h00_2019y11m5.txt -o out/
```

```
5 delivered, 1 cancelled
Wrote out/drones10h30_2019y11m5.txt
Wrote out/timetable10h00_2019y11m5.txt
```

You can also run it without installing: `PYTHONPATH=src python -m dronydeliv DRONES PARCELS`.

## How drones are chosen

Orders are processed in the order they appear in the parcels file. For each one, every drone that can take it is ranked by:

1. operating in the same zone as the order,
2. earliest availability,
3. most remaining autonomy,
4. least accumulated distance,
5. name, alphabetically.

A drone *can take* an order when it is in the order's zone, its range covers the delivery distance, it can carry the weight, and it has enough autonomy for the round trip. If no drone qualifies, the order is cancelled.

The drone departs at whichever is later: when it becomes free or when the order was placed. Drones fly between 08:00 and 20:00. A delivery that would finish after 20:00 is moved to 08:00 the next morning.

## File formats

Every file starts with the same seven-line header, followed by one record per line with fields separated by `, `.

**Input files** must be named `dronesHHhMM_YYYYyMMmD.txt` and `parcelsHHhMM_YYYYyMMmD.txt`. The time and date in the name must match the header, and both files must be for the same moment.

```
Time:
10h00
Day:
5-11-2019
Company:
iQueue
Drones:
alpha, Lisbon, 5, 3000, 120.5, 40.0, 2019-11-05, 09:30
```

| File | Fields |
|---|---|
| Drones | name, zone, max weight (kg), max distance (m), accumulated distance (km), autonomy (km), available date, available time |
| Parcels | client, zone, order date, order time, distance from base (m), weight (kg), round-trip duration (min) |

**Output files:**

- `drones…txt` is the updated fleet, stamped 30 minutes after the input. Drones are sorted by availability, then by autonomy.
- `timetable…txt` lists cancelled orders first (`date, time, client, cancelled`), then deliveries by departure time (`date, time, client, drone`).

See [`examples/`](examples) for a complete input set and the expected output.

## Project layout

```
src/dronydeliv/
  cli.py        command-line interface
  fileio.py     reading, validating and writing files
  scheduler.py  the assignment algorithm
  models.py     Drone, Order, Delivery and Schedule types
tests/          unit and end-to-end tests
examples/       sample input files and expected output
scripts/        regenerates the results chart
docs/           design notes, results chart, original report (Portuguese)
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

CI runs the tests and linter on Python 3.10–3.13 for every push.

## What changed since the 2019 submission

The code as originally submitted is preserved under the [`v1.0-submission`](https://github.com/DiogoS7/dronyDeliv/tree/v1.0-submission) tag. Version 2.0 is a rewrite of the same program that fixes these problems:

- **Dates.** Dates were parsed with `%M` (minutes) instead of `%m` (month), so sorting and next-day rollovers ignored the month.
- **Small fleets.** The program crashed when fewer than three drones were available, because it only ever considered the top three candidates. It now considers every drone.
- **Timetable times.** The original report mentions a known bug: the drone file and the timetable gave different times depending on which was written first. The timetable is now built directly from the assignment results, so the two always agree.
- **File names.** File names were validated by slicing fixed character positions, so a folder path or a two-digit day broke validation. Names are now parsed with a regular expression.
- **Cleanup.** The release adds clear error messages for malformed input, a test suite, sample data, packaging and CI. It also removes compiled caches and a duplicate zip from version control.

## Authors

- **Diogo Santos** – time utilities, input validation
- **José Almeida** – file reading and writing, assignment logic
