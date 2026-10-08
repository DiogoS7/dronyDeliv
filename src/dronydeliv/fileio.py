"""Reading and writing dronyDeliv text files.

Every file starts with a seven-line header followed by one record per line,
fields separated by ", "::

    Time:
    10h00
    Day:
    5-11-2019
    Company:
    iQueue
    Drones:
    drone1, Lisbon, 5.0, 3000, 120.5, 40.0, 2019-11-05, 09:30

File names encode the same time and date as the header, e.g.
``drones10h00_2019y11m5.txt`` and ``parcels10h00_2019y11m5.txt``.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path

from .models import Drone, Header, Order, Schedule

FILENAME_RE = re.compile(
    r"^(?P<scope>[a-z]+)(?P<hour>\d{2})h(?P<minute>\d{2})"
    r"_(?P<year>\d{4})y(?P<month>\d{1,2})m(?P<day>\d{1,2})\.txt$"
)

DRONE_FIELDS = 8
ORDER_FIELDS = 7


class InputFileError(ValueError):
    """An input file is missing, malformed or inconsistent."""


def _format_date(moment: datetime) -> str:
    return f"{moment.day}-{moment.month:02d}-{moment.year}"


def _format_time(moment: datetime) -> str:
    return moment.strftime("%Hh%M")


# ---------------------------------------------------------------- reading


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise InputFileError(f"File not found: {path}") from None


def read_header(path: Path) -> Header:
    lines = _read_lines(path)
    if len(lines) < 7:
        raise InputFileError(f"{path.name}: header is incomplete")
    return Header(
        time=lines[1].strip(),
        date=lines[3].strip(),
        company=lines[5].strip(),
        scope=lines[6].strip().rstrip(":"),
    )


def _records(path: Path, expected_fields: int) -> list[list[str]]:
    records = []
    for number, line in enumerate(_read_lines(path)[7:], start=8):
        if not line.strip():
            continue
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != expected_fields:
            raise InputFileError(
                f"{path.name}, line {number}: expected {expected_fields} "
                f"fields, found {len(fields)}"
            )
        records.append(fields)
    return records


def _when(date: str, hour: str) -> datetime:
    return datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H:%M")


def read_drones(path: Path) -> list[Drone]:
    try:
        return [
            Drone(
                name=name,
                zone=zone,
                max_weight=float(weight),
                max_distance=float(distance),
                accumulated_distance=float(accumulated),
                autonomy=float(autonomy),
                available_at=_when(date, hour),
            )
            for name, zone, weight, distance, accumulated, autonomy, date, hour in _records(
                path, DRONE_FIELDS
            )
        ]
    except ValueError as error:
        if isinstance(error, InputFileError):
            raise
        raise InputFileError(f"{path.name}: {error}") from None


def read_orders(path: Path) -> list[Order]:
    try:
        return [
            Order(
                client=client,
                zone=zone,
                requested_at=_when(date, hour),
                distance=float(distance),
                weight=float(weight),
                duration=int(duration),
            )
            for client, zone, date, hour, distance, weight, duration in _records(
                path, ORDER_FIELDS
            )
        ]
    except ValueError as error:
        if isinstance(error, InputFileError):
            raise
        raise InputFileError(f"{path.name}: {error}") from None


# ------------------------------------------------------------- validation


def validate(path: Path, expected_scope: str) -> Header:
    """Check that a file's name agrees with its header; return the header."""
    match = FILENAME_RE.match(path.name)
    if not match:
        raise InputFileError(
            f"{path.name}: name must look like "
            f"{expected_scope}HHhMM_YYYYyMMmDD.txt"
        )
    header = read_header(path)
    try:
        name_moment = datetime(
            int(match["year"]),
            int(match["month"]),
            int(match["day"]),
            int(match["hour"]),
            int(match["minute"]),
        )
        header_moment = header.moment
    except ValueError as error:
        raise InputFileError(f"{path.name}: invalid date or time ({error})") from None

    if (
        match["scope"] != expected_scope
        or header.scope.lower() != expected_scope
        or name_moment != header_moment
    ):
        raise InputFileError(f"{path.name}: name and header are inconsistent")
    return header


def validate_pair(drone_path: Path, parcel_path: Path) -> Header:
    drones = validate(drone_path, "drones")
    parcels = validate(parcel_path, "parcels")
    if drones.moment != parcels.moment:
        raise InputFileError(
            f"{drone_path.name} and {parcel_path.name} are for different times"
        )
    return drones


# ---------------------------------------------------------------- writing


def output_name(scope: str, moment: datetime) -> str:
    return f"{scope}{moment:%Hh%M}_{moment.year}y{moment.month:02d}m{moment.day}.txt"


def _header_lines(moment: datetime, company: str, scope: str) -> list[str]:
    return [
        "Time:",
        _format_time(moment),
        "Day:",
        _format_date(moment),
        "Company:",
        company,
        f"{scope}:",
    ]


def write_drones(schedule: Schedule, header: Header, out_dir: Path) -> Path:
    """Write the updated fleet, valid 30 minutes after the input files."""
    moment = header.moment + timedelta(minutes=30)
    drones = sorted(
        schedule.drones,
        key=lambda d: (d.available_at, -d.autonomy, d.name),
    )
    lines = _header_lines(moment, header.company, "Drones")
    lines += [
        ", ".join(
            [
                d.name,
                d.zone,
                _fmt(d.max_weight),
                _fmt(d.max_distance),
                f"{d.accumulated_distance:.1f}",
                f"{d.autonomy:.1f}",
                d.available_at.strftime("%Y-%m-%d"),
                d.available_at.strftime("%H:%M"),
            ]
        )
        for d in drones
    ]
    path = out_dir / output_name("drones", moment)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_timetable(schedule: Schedule, header: Header, out_dir: Path) -> Path:
    """Write cancelled orders (by client name) then deliveries (by departure)."""
    lines = _header_lines(header.moment, header.company, "Timeline")
    for order in sorted(schedule.cancelled, key=lambda o: o.client):
        lines.append(
            f"{order.requested_at:%Y-%m-%d}, {order.requested_at:%H:%M}, "
            f"{order.client}, cancelled"
        )
    for delivery in sorted(
        schedule.deliveries, key=lambda d: (d.departure, d.order.client)
    ):
        lines.append(
            f"{delivery.departure:%Y-%m-%d}, {delivery.departure:%H:%M}, "
            f"{delivery.order.client}, {delivery.drone_name}"
        )
    path = out_dir / output_name("timetable", header.moment)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _fmt(value: float) -> str:
    """Format a number the way the input files do: 3000 or 120.5."""
    return str(int(value)) if value.is_integer() else f"{value:.1f}"
