import unittest
from datetime import datetime

from dronydeliv.models import Drone, Order
from dronydeliv.scheduler import assign, departure_time


def drone(name="d1", zone="Lisbon", autonomy=40.0, at="2019-11-05 09:00", **kw):
    return Drone(
        name=name,
        zone=zone,
        max_weight=kw.get("max_weight", 5.0),
        max_distance=kw.get("max_distance", 3000.0),
        accumulated_distance=kw.get("accumulated", 0.0),
        autonomy=autonomy,
        available_at=datetime.fromisoformat(at),
    )


def order(client="ana", zone="Lisbon", at="2019-11-05 10:00", **kw):
    return Order(
        client=client,
        zone=zone,
        requested_at=datetime.fromisoformat(at),
        distance=kw.get("distance", 1000.0),
        weight=kw.get("weight", 1.0),
        duration=kw.get("duration", 30),
    )


class AssignTests(unittest.TestCase):
    def test_works_with_fewer_than_three_drones(self):
        # The 2019 version crashed with IndexError here.
        result = assign([drone()], [order()])
        self.assertEqual(len(result.deliveries), 1)

    def test_works_with_no_drones(self):
        result = assign([], [order()])
        self.assertEqual(len(result.cancelled), 1)

    def test_prefers_earliest_available_drone_in_zone(self):
        drones = [
            drone("late", at="2019-11-05 09:50"),
            drone("early", at="2019-11-05 09:10"),
            drone("porto", zone="Porto", at="2019-11-05 08:00"),
        ]
        result = assign(drones, [order()])
        self.assertEqual(result.deliveries[0].drone_name, "early")

    def test_ties_broken_by_autonomy_then_name(self):
        drones = [drone("b", autonomy=30), drone("c", autonomy=40), drone("a", autonomy=40)]
        result = assign(drones, [order()])
        self.assertEqual(result.deliveries[0].drone_name, "a")

    def test_looks_beyond_first_three_candidates(self):
        weak = [drone(f"w{i}", max_weight=0.5, at="2019-11-05 08:00") for i in range(3)]
        strong = drone("strong", at="2019-11-05 09:00")
        result = assign(weak + [strong], [order()])
        self.assertEqual(result.deliveries[0].drone_name, "strong")

    def test_cancels_when_no_drone_can_carry(self):
        result = assign([drone(max_weight=1.0)], [order(weight=2.0)])
        self.assertEqual(result.cancelled[0].client, "ana")
        self.assertEqual(result.deliveries, [])

    def test_cancels_when_autonomy_too_low(self):
        result = assign([drone(autonomy=1.5)], [order(distance=1000)])  # needs 2 km
        self.assertEqual(len(result.cancelled), 1)

    def test_updates_drone_state(self):
        result = assign([drone(autonomy=40.0)], [order(distance=1500, duration=30)])
        updated = result.drones[0]
        self.assertEqual(updated.autonomy, 37.0)
        self.assertEqual(updated.accumulated_distance, 3.0)
        self.assertEqual(updated.available_at, datetime(2019, 11, 5, 10, 30))

    def test_does_not_mutate_input(self):
        fleet = [drone(autonomy=40.0)]
        assign(fleet, [order()])
        self.assertEqual(fleet[0].autonomy, 40.0)

    def test_same_drone_reused_for_later_order(self):
        result = assign([drone()], [order("a"), order("b", at="2019-11-05 10:10")])
        departures = [d.departure for d in result.deliveries]
        # second order waits for the drone to return at 10:30
        self.assertEqual(departures, [datetime(2019, 11, 5, 10, 0), datetime(2019, 11, 5, 10, 30)])


class DepartureTimeTests(unittest.TestCase):
    def test_rolls_over_to_next_morning_after_closing(self):
        dep = departure_time(drone(), order(at="2019-11-05 19:45", duration=30))
        self.assertEqual(dep, datetime(2019, 11, 6, 8, 0))

    def test_rollover_across_month_end(self):
        # The 2019 version used %M (minutes) instead of %m (month) for dates,
        # so this produced the wrong month.
        dep = departure_time(
            drone(at="2019-11-30 19:00"), order(at="2019-11-30 19:45", duration=30)
        )
        self.assertEqual(dep, datetime(2019, 12, 1, 8, 0))

    def test_waits_for_opening_hours(self):
        dep = departure_time(drone(at="2019-11-05 06:00"), order(at="2019-11-05 06:30"))
        self.assertEqual(dep, datetime(2019, 11, 5, 8, 0))


if __name__ == "__main__":
    unittest.main()
