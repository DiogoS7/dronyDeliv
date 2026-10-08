"""Assigns drones to parcel orders."""

from __future__ import annotations

import copy
from datetime import datetime, time, timedelta

from .models import Delivery, Drone, Order, Schedule

#: Drones only fly between these hours. A delivery that would end after
#: CLOSING moves to OPENING on the next day.
OPENING = time(8, 0)
CLOSING = time(20, 0)


def _priority(drone: Drone, order: Order) -> tuple:
    """Sort key: preferred drones come first.

    Same zone as the order, then earliest available, then most autonomy,
    then least distance travelled, then alphabetical name.
    """
    return (
        drone.zone != order.zone,
        drone.available_at,
        -drone.autonomy,
        drone.accumulated_distance,
        drone.name,
    )


def departure_time(drone: Drone, order: Order) -> datetime:
    """When the drone leaves for this order, respecting opening hours."""
    departure = max(drone.available_at, order.requested_at)
    if departure.time() < OPENING:
        departure = datetime.combine(departure.date(), OPENING)
    finish = departure + timedelta(minutes=order.duration)
    closing = datetime.combine(departure.date(), CLOSING)
    if finish > closing:
        departure = datetime.combine(departure.date() + timedelta(days=1), OPENING)
    return departure


def assign(drones: list[Drone], orders: list[Order]) -> Schedule:
    """Assign each order, in file order, to the best available drone.

    Orders no drone can handle are cancelled. The input lists are not
    modified; updated drone states are returned in ``Schedule.drones``.
    """
    fleet = copy.deepcopy(drones)
    schedule = Schedule()

    for order in orders:
        candidates = sorted(fleet, key=lambda d: _priority(d, order))
        drone = next((d for d in candidates if d.can_deliver(order)), None)
        if drone is None:
            schedule.cancelled.append(order)
            continue

        departure = departure_time(drone, order)
        drone.autonomy = round(drone.autonomy - order.round_trip_km, 1)
        drone.accumulated_distance = round(
            drone.accumulated_distance + order.round_trip_km, 1
        )
        drone.available_at = departure + timedelta(minutes=order.duration)
        schedule.deliveries.append(Delivery(order, drone.name, departure))

    schedule.drones = fleet
    return schedule
