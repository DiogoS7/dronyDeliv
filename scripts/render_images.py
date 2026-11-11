"""Render the README images from a real run on the example files.

    pip install playwright && playwright install chromium
    PYTHONPATH=src python scripts/render_images.py

Writes, into docs/:
    how-it-works.png      what goes in, what dronyDeliv decides, what comes out
    example-schedule.png  which drone flies each order, on a timeline
    social-preview.png    repo banner (upload it in Settings > Social preview)

Each image is an HTML template in scripts/images/ filled with data from the
scheduler, so re-run this script whenever the rules or the examples change.
"""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

from dronydeliv.fileio import read_drones, read_header, read_orders
from dronydeliv.scheduler import CLOSING, OPENING, assign

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
TEMPLATES = ROOT / "scripts" / "images"
DOCS = ROOT / "docs"

DRONES_FILE = EXAMPLES / "drones10h00_2019y11m5.txt"
ORDERS_FILE = EXAMPLES / "parcels10h00_2019y11m5.txt"

# template name -> (output file, viewport width, device scale factor)
IMAGES = {
    "how_it_works": ("how-it-works.png", 1000, 2),
    "schedule": ("example-schedule.png", 1000, 2),
    "social_preview": ("social-preview.png", 1280, 1),
}


def _minutes(moment) -> int:
    """Minutes since midnight of the run's first day."""
    return moment.hour * 60 + moment.minute


def _km(metres: float) -> str:
    return f"{metres / 1000:g} km"


def _cancel_reason(order, drones) -> str:
    local = [d for d in drones if d.zone == order.zone]
    if not local:
        return f"no drone is based in {order.zone}"
    if not any(d.max_weight >= order.weight for d in local):
        return "too heavy for every drone there"
    if not any(d.max_distance >= order.distance for d in local):
        return "too far for every drone there"
    return "no drone has enough battery left"


def build_data() -> dict:
    header = read_header(DRONES_FILE)
    drones = read_drones(DRONES_FILE)
    orders = read_orders(ORDERS_FILE)
    schedule = assign(drones, orders)
    run_day = header.moment.date()
    after = {d.name: d for d in schedule.drones}

    def day_offset(moment) -> int:
        return (moment.date() - run_day).days

    deliveries = []
    for d in schedule.deliveries:
        back = d.departure + timedelta(minutes=d.order.duration)
        deliveries.append(
            {
                "client": d.order.client,
                "zone": d.order.zone,
                "drone": d.drone_name,
                "ordered": d.order.requested_at.strftime("%H:%M"),
                "ordered_min": _minutes(d.order.requested_at),
                "ordered_day": day_offset(d.order.requested_at),
                "departs": d.departure.strftime("%H:%M"),
                "back": back.strftime("%H:%M"),
                "start_min": _minutes(d.departure),
                "end_min": _minutes(back),
                "day": day_offset(d.departure),
                "next_day": d.departure.date() > d.order.requested_at.date(),
            }
        )
    deliveries.sort(key=lambda x: (x["day"], x["start_min"]))

    return {
        "company": header.company,
        "date": header.moment.strftime("%A %d %B %Y").replace(" 0", " "),
        "opening": OPENING.strftime("%H:%M"),
        "closing": CLOSING.strftime("%H:%M"),
        "opening_min": OPENING.hour * 60 + OPENING.minute,
        "closing_min": CLOSING.hour * 60 + CLOSING.minute,
        "drones": [
            {
                "name": d.name,
                "zone": d.zone,
                "max_weight": f"{d.max_weight:g} kg",
                "range": _km(d.max_distance),
                "battery_before": d.autonomy,
                "battery_after": after[d.name].autonomy,
                "free_from": d.available_at.strftime("%H:%M"),
                "free_again": after[d.name].available_at.strftime("%H:%M"),
                "free_again_day": day_offset(after[d.name].available_at),
            }
            for d in sorted(drones, key=lambda d: d.name)
        ],
        "orders": [
            {
                "client": o.client,
                "zone": o.zone,
                "ordered": o.requested_at.strftime("%H:%M"),
                "distance": _km(o.distance),
                "weight": f"{o.weight:g} kg",
                "minutes": o.duration,
            }
            for o in orders
        ],
        "deliveries": deliveries,
        "cancelled": [
            {
                "client": o.client,
                "zone": o.zone,
                "ordered": o.requested_at.strftime("%H:%M"),
                "ordered_min": _minutes(o.requested_at),
                "reason": _cancel_reason(o, drones),
            }
            for o in schedule.cancelled
        ],
    }


def main() -> None:
    data = json.dumps(build_data())
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for template, (out_name, width, scale) in IMAGES.items():
            page = browser.new_page(
                viewport={"width": width, "height": 640}, device_scale_factor=scale
            )
            page.add_init_script(f"window.DATA = {data};")
            page.goto((TEMPLATES / f"{template}.html").as_uri())
            page.evaluate("document.fonts.ready")
            page.locator("#card").screenshot(path=str(DOCS / out_name))
            page.close()
            print(f"Wrote docs/{out_name}")
        browser.close()


if __name__ == "__main__":
    main()
