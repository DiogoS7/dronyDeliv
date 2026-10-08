"""Data types shared across dronyDeliv."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Header:
    """The header block at the top of every input and output file."""

    time: str  # e.g. "10h00"
    date: str  # e.g. "5-11-2019" (day-month-year)
    company: str
    scope: str  # "Drones", "Parcels" or "Timeline"

    @property
    def moment(self) -> datetime:
        return datetime.strptime(f"{self.date} {self.time}", "%d-%m-%Y %Hh%M")


@dataclass
class Drone:
    name: str
    zone: str
    max_weight: float  # kg
    max_distance: float  # metres from base, one way
    accumulated_distance: float  # km travelled so far
    autonomy: float  # km left before recharging
    available_at: datetime

    def can_deliver(self, order: Order) -> bool:
        """True if this drone is allowed and able to carry the order."""
        return (
            self.zone == order.zone
            and self.max_distance >= order.distance
            and self.max_weight >= order.weight
            and self.autonomy >= order.round_trip_km
        )


@dataclass
class Order:
    client: str
    zone: str
    requested_at: datetime
    distance: float  # metres from base, one way
    weight: float  # kg
    duration: int  # minutes for the full round trip

    @property
    def round_trip_km(self) -> float:
        return self.distance * 2 / 1000


@dataclass
class Delivery:
    order: Order
    drone_name: str
    departure: datetime


@dataclass
class Schedule:
    """Result of assigning drones to orders."""

    deliveries: list[Delivery] = field(default_factory=list)
    cancelled: list[Order] = field(default_factory=list)
    drones: list[Drone] = field(default_factory=list)
