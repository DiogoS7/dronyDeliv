"""Render docs/example-timeline.svg from the example input files.

Run from the repository root:  PYTHONPATH=src python scripts/render_timeline.py
The chart is generated from the real scheduler output, so re-run this script
whenever the scheduling rules or the example files change.

The SVG is drawn at the width GitHub displays README images (about 800px),
so its text appears at its real size.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from html import escape
from pathlib import Path

from dronydeliv.fileio import read_drones, read_orders
from dronydeliv.models import Delivery
from dronydeliv.scheduler import CLOSING, assign

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
OUT = ROOT / "docs" / "example-timeline.svg"

WIDTH = 800
LABEL_W = 112  # drone names column
RIGHT_PAD = 20
GAP = 76  # space between days ("overnight")
HEADER_H = 64
ROW_H = 60
BAR_H = 28

STYLE = (
    ".bg{fill:#ffffff}.ink{fill:#1f2328}.muted{fill:#59636e}.grid{stroke:#d1d9e0}"
    ".lane{fill:#f6f8fa}.bar{fill:#0969da}.bar-text{fill:#ffffff}"
    ".note{fill:#9a6700}.bad{fill:#cf222e}"
    "@media (prefers-color-scheme: dark){"
    ".bg{fill:#0d1117}.ink{fill:#f0f6fc}.muted{fill:#9198a1}.grid{stroke:#3d444d}"
    ".lane{fill:#151b23}.bar{fill:#4493f8}.bar-text{fill:#0d1117}"
    ".note{fill:#d29922}.bad{fill:#ff7b72}}"
)


def _floor_hour(moment: datetime) -> datetime:
    return moment.replace(minute=0, second=0, microsecond=0)


def _ceil_hour(moment: datetime) -> datetime:
    floored = _floor_hour(moment)
    return floored if floored == moment else floored + timedelta(hours=1)


def day_windows(deliveries: list[Delivery]) -> list[tuple[datetime, datetime]]:
    """One window per day with flights, from the first take-off to the last
    landing, rounded out to whole hours and at least two hours wide."""
    days: dict = {}
    for d in deliveries:
        start = d.departure
        end = d.departure + timedelta(minutes=d.order.duration)
        lo, hi = days.get(start.date(), (start, end))
        days[start.date()] = (min(lo, start), max(hi, end))
    windows = []
    for day in sorted(days):
        lo, hi = _floor_hour(days[day][0]), _ceil_hour(days[day][1])
        windows.append((lo, max(hi, lo + timedelta(hours=2))))
    return windows


def _cancel_reason(order, drones) -> str:
    if not any(dr.zone == order.zone for dr in drones):
        return f"no drone works in {order.zone}"
    return "no drone could carry it that far or that heavy"


def render() -> str:
    drones = read_drones(EXAMPLES / "drones10h00_2019y11m5.txt")
    orders = read_orders(EXAMPLES / "parcels10h00_2019y11m5.txt")
    schedule = assign(drones, orders)

    names = sorted(d.name for d in drones)
    zones = {d.name: d.zone for d in drones}
    windows = day_windows(schedule.deliveries)

    total_hours = sum((hi - lo).total_seconds() / 3600 for lo, hi in windows)
    px_per_hour = (WIDTH - LABEL_W - RIGHT_PAD - GAP * (len(windows) - 1)) / total_hours
    offsets, x = [], float(LABEL_W)
    for lo, hi in windows:
        offsets.append(x)
        x += (hi - lo).total_seconds() / 3600 * px_per_hour + GAP

    def xpos(moment: datetime) -> float:
        for (lo, hi), off in zip(windows, offsets, strict=True):
            if lo <= moment <= hi:
                return off + (moment - lo).total_seconds() / 3600 * px_per_hour
        raise ValueError(f"{moment} is outside the chart")

    lanes_bottom = HEADER_H + ROW_H * len(names)
    footer_lines = len(schedule.cancelled)
    height = lanes_bottom + 24 + footer_lines * 24 + 12

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
        f'width="{WIDTH}" height="{height}" font-size="14" '
        'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif">',
        f"<style>{STYLE}</style>",
        f'<rect class="bg" width="{WIDTH}" height="{height}" rx="10"/>',
    ]

    # Day headings and hour grid
    for (lo, hi), off in zip(windows, offsets, strict=True):
        out.append(
            f'<text class="ink" x="{off:.0f}" y="24" font-weight="600" font-size="15">'
            f"{lo:%A} {lo.day} {lo:%b}</text>"
        )
        hour = lo
        while hour <= hi:
            hx = xpos(hour)
            out.append(
                f'<line class="grid" x1="{hx:.1f}" y1="{HEADER_H - 8}" x2="{hx:.1f}" '
                f'y2="{lanes_bottom}" stroke-width="1"/>'
            )
            out.append(
                f'<text class="muted" x="{hx:.1f}" y="{HEADER_H - 16}" '
                f'text-anchor="middle" font-size="12">{hour:%H:%M}</text>'
            )
            hour += timedelta(hours=1)

    # Overnight divider between days
    for i in range(1, len(windows)):
        gx = offsets[i] - GAP / 2
        out.append(
            f'<line class="grid" x1="{gx:.1f}" y1="{HEADER_H - 8}" x2="{gx:.1f}" '
            f'y2="{lanes_bottom + 4}" stroke-width="1.5" stroke-dasharray="4 4"/>'
        )
        out.append(
            f'<text class="muted" x="{gx:.1f}" y="{lanes_bottom + 16}" text-anchor="middle" '
            'font-size="11" font-style="italic">overnight</text>'
        )

    # Drone lanes
    for i, name in enumerate(names):
        y = HEADER_H + i * ROW_H
        out.append(
            f'<rect class="lane" x="{LABEL_W - 8}" y="{y + 4}" '
            f'width="{WIDTH - LABEL_W - RIGHT_PAD + 16}" height="{ROW_H - 8}" rx="6"/>'
        )
        out.append(
            f'<text class="ink" x="16" y="{y + 27}" font-weight="600">{escape(name)}</text>'
        )
        out.append(
            f'<text class="muted" x="16" y="{y + 45}" font-size="12">'
            f"{escape(zones[name])}</text>"
        )

    # Flights
    for d in schedule.deliveries:
        y = HEADER_H + names.index(d.drone_name) * ROW_H
        end = d.departure + timedelta(minutes=d.order.duration)
        x1, x2 = xpos(d.departure), xpos(end)
        bar_y = y + (ROW_H - BAR_H) / 2
        out.append(
            f'<rect class="bar" x="{x1:.1f}" y="{bar_y:.0f}" width="{x2 - x1:.1f}" '
            f'height="{BAR_H}" rx="5"><title>{escape(d.order.client)}: '
            f"leaves {d.departure:%H:%M}, back {end:%H:%M}</title></rect>"
        )
        out.append(
            f'<text class="bar-text" x="{(x1 + x2) / 2:.1f}" y="{bar_y + 19:.0f}" '
            'text-anchor="middle" font-weight="600" font-size="13">'
            f"{escape(d.order.client)}</text>"
        )
        out.append(
            f'<text class="muted" x="{x2 + 8:.1f}" y="{bar_y + 19:.0f}" font-size="12">'
            f"{d.departure:%H:%M}–{end:%H:%M}</text>"
        )
        if d.departure.date() > d.order.requested_at.date():
            # Explain the overnight move at the end of the previous day.
            day_start = next(
                off for (lo, _), off in zip(windows, offsets, strict=True)
                if lo.date() == d.departure.date()
            )
            out.append(
                f'<text class="note" x="{day_start - GAP - 8:.1f}" y="{bar_y + 19:.0f}" '
                'text-anchor="end" font-size="12">'
                f"ordered {d.order.requested_at:%H:%M}, too late for today →</text>"
            )

    # Cancelled orders
    for i, order in enumerate(sorted(schedule.cancelled, key=lambda o: o.client)):
        y = lanes_bottom + 30 + i * 24
        out.append(
            f'<text class="bad" x="16" y="{y}" font-weight="600">✕ {escape(order.client)} '
            'cancelled</text>'
        )
        out.append(
            f'<text class="muted" x="170" y="{y}">'
            f"{escape(_cancel_reason(order, drones))}</text>"
        )

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    OUT.write_text(render() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
