"""Render docs/example-timeline.svg from the example input files.

Run from the repository root:  PYTHONPATH=src python scripts/render_timeline.py
The chart is generated from the real scheduler output, so re-run this script
whenever the scheduling rules or the example files change.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from html import escape
from pathlib import Path

from dronydeliv.fileio import read_drones, read_orders
from dronydeliv.scheduler import assign

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
OUT = ROOT / "docs" / "example-timeline.svg"

LABEL_W, ROW_H, TOP, PX_PER_HOUR, PANEL_GAP = 120, 46, 70, 80, 48


def panels_for(deliveries) -> list[tuple[datetime, datetime]]:
    """One panel per calendar day, spanning that day's flights and order times.

    Panels snap to whole hours and are at least two hours wide.
    """
    events: list[datetime] = []
    for d in deliveries:
        events += [
            d.departure,
            d.departure + timedelta(minutes=d.order.duration),
            d.order.requested_at,
        ]
    days: dict = {}
    for moment in events:
        lo_h = moment.replace(minute=0)
        hi_h = lo_h + timedelta(hours=1 if moment.minute else 0)
        lo, hi = days.get(moment.date(), (lo_h, hi_h))
        days[moment.date()] = (min(lo, lo_h), max(hi, hi_h))
    panels = []
    for day in sorted(days):
        lo, hi = days[day]
        panels.append((lo, max(hi, lo + timedelta(hours=2))))
    return panels


def render() -> str:
    drones = read_drones(EXAMPLES / "drones10h00_2019y11m5.txt")
    orders = read_orders(EXAMPLES / "parcels10h00_2019y11m5.txt")
    schedule = assign(drones, orders)

    names = sorted(d.name for d in drones)
    zones = {d.name: d.zone for d in drones}
    panels = panels_for(schedule.deliveries)

    offsets, x = [], LABEL_W
    for lo, hi in panels:
        offsets.append(x)
        x += (hi - lo).total_seconds() / 3600 * PX_PER_HOUR + PANEL_GAP
    width = int(x - PANEL_GAP + 20)
    height = TOP + ROW_H * len(names) + 70

    def xpos(moment: datetime) -> float | None:
        for (lo, hi), off in zip(panels, offsets, strict=True):
            if lo <= moment <= hi:
                return off + (moment - lo).total_seconds() / 3600 * PX_PER_HOUR
        return None

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="system-ui, -apple-system, '
        f'Segoe UI, Helvetica, Arial, sans-serif" font-size="13">',
        "<style>"
        ".bg{fill:#ffffff}.ink{fill:#1f2328}.muted{fill:#59636e}.grid{stroke:#d1d9e0}"
        ".bar{fill:#0969da}.bar-text{fill:#ffffff}.req{fill:#bf8700}.lane{fill:#f6f8fa}"
        "@media (prefers-color-scheme: dark){.bg{fill:#0d1117}.ink{fill:#f0f6fc}"
        ".muted{fill:#9198a1}.grid{stroke:#3d444d}.bar{fill:#4493f8}.bar-text{fill:#0d1117}"
        ".req{fill:#d29922}.lane{fill:#151b23}}"
        "</style>",
        f'<rect class="bg" width="{width}" height="{height}" rx="8"/>',
    ]

    # Panel titles and hour grid
    for (lo, hi), off in zip(panels, offsets, strict=True):
        parts.append(
            f'<text class="ink" x="{off}" y="26" font-weight="600">'
            f"{lo:%a %d %b %Y}</text>"
        )
        hour = lo
        while hour <= hi:
            hx = xpos(hour)
            parts.append(
                f'<line class="grid" x1="{hx:.1f}" y1="{TOP - 12}" x2="{hx:.1f}" '
                f'y2="{TOP + ROW_H * len(names)}" stroke-width="1"/>'
            )
            parts.append(
                f'<text class="muted" x="{hx:.1f}" y="{TOP - 18}" '
                f'text-anchor="middle" font-size="11">{hour:%H:%M}</text>'
            )
            hour += timedelta(hours=1)

    # Drone lanes
    for i, name in enumerate(names):
        y = TOP + i * ROW_H
        parts.append(
            f'<rect class="lane" x="{LABEL_W}" y="{y + 4}" '
            f'width="{width - LABEL_W - 20}" height="{ROW_H - 8}" rx="4" opacity="0.6"/>'
        )
        parts.append(f'<text class="ink" x="16" y="{y + ROW_H / 2 - 2}" font-weight="600">'
                     f"{escape(name)}</text>")
        parts.append(f'<text class="muted" x="16" y="{y + ROW_H / 2 + 13}" font-size="11">'
                     f"{escape(zones[name])}</text>")

    # Deliveries
    for d in schedule.deliveries:
        y = TOP + names.index(d.drone_name) * ROW_H
        x1 = xpos(d.departure)
        x2 = xpos(d.departure + timedelta(minutes=d.order.duration))
        parts.append(
            f'<rect class="bar" x="{x1:.1f}" y="{y + 9}" width="{x2 - x1:.1f}" '
            f'height="{ROW_H - 18}" rx="4"><title>{escape(d.order.client)}: '
            f"{d.departure:%d %b %H:%M}, {d.order.duration} min</title></rect>"
        )
        parts.append(
            f'<text class="bar-text" x="{(x1 + x2) / 2:.1f}" y="{y + ROW_H / 2 + 4}" '
            f'text-anchor="middle" font-weight="600">{escape(d.order.client)}</text>'
        )
        rx = xpos(d.order.requested_at)
        if rx is not None and d.order.requested_at != d.departure:
            parts.append(f'<circle class="req" cx="{rx:.1f}" cy="{y + ROW_H / 2}" r="4"/>')

    # Legend and cancelled orders
    ly = TOP + ROW_H * len(names) + 30
    parts.append(f'<rect class="bar" x="{LABEL_W}" y="{ly - 10}" width="22" height="12" rx="3"/>')
    parts.append(f'<text class="muted" x="{LABEL_W + 30}" y="{ly}">round trip</text>')
    parts.append(f'<circle class="req" cx="{LABEL_W + 125}" cy="{ly - 4}" r="4"/>')
    parts.append(f'<text class="muted" x="{LABEL_W + 135}" y="{ly}">'
                 "order placed; drone left later</text>")
    if schedule.cancelled:
        names_c = ", ".join(f"{o.client} ({o.zone})" for o in schedule.cancelled)
        parts.append(f'<text class="muted" x="{LABEL_W}" y="{ly + 24}">'
                     f"Cancelled: {escape(names_c)}</text>")

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    OUT.write_text(render() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
