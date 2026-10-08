"""Command-line entry point: ``dronydeliv DRONES_FILE PARCELS_FILE``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .fileio import (
    InputFileError,
    read_drones,
    read_orders,
    validate_pair,
    write_drones,
    write_timetable,
)
from .scheduler import assign


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dronydeliv",
        description=(
            "Assign delivery drones to parcel orders and write an updated "
            "drone list and a delivery timetable."
        ),
    )
    parser.add_argument("drones", type=Path, help="drones file, e.g. drones10h00_2019y11m5.txt")
    parser.add_argument("parcels", type=Path, help="parcels file, e.g. parcels10h00_2019y11m5.txt")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="where to write results (default: the drones file's folder)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = args.output_dir or args.drones.parent
    try:
        header = validate_pair(args.drones, args.parcels)
        schedule = assign(read_drones(args.drones), read_orders(args.parcels))
        out_dir.mkdir(parents=True, exist_ok=True)
        drones_out = write_drones(schedule, header, out_dir)
        timetable_out = write_timetable(schedule, header, out_dir)
    except InputFileError as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 1

    print(
        f"{len(schedule.deliveries)} delivered, {len(schedule.cancelled)} cancelled\n"
        f"Wrote {drones_out}\nWrote {timetable_out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
