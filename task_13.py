"""Task 13: Room booking scheduler; adjacent intervals are allowed."""

from datetime import datetime

class BookingScheduler:
    def __init__(self):
        self.bookings = []
        self.booking_ids = set()

    def add_booking(self, room, start, end, booking_id):
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise TypeError("start and end must be datetime objects")
        if end <= start:
            return False, "End time must be later than start time"
        if booking_id in self.booking_ids:
            return False, "Duplicate booking ID"

        for booking in self.bookings:
            if booking["room"] == room:
                # Half-open intervals: touching endpoints do not overlap.
                overlaps = start < booking["end"] and booking["start"] < end
                if overlaps:
                    return False, f"Conflicts with booking {booking['booking_id']}"

        self.bookings.append({
            "room": room, "start": start, "end": end, "booking_id": booking_id
        })
        self.booking_ids.add(booking_id)
        self.bookings.sort(key=lambda b: (b["room"], b["start"]))
        return True, "Booking accepted"


if __name__ == "__main__":
    scheduler = BookingScheduler()
    fmt = "%Y-%m-%d %H:%M"
    dt = lambda value: datetime.strptime(value, fmt)
    print(scheduler.add_booking("A", dt("2026-11-07 09:00"),
                                dt("2026-11-07 10:00"), "B1"))
    print(scheduler.add_booking("A", dt("2026-11-07 10:00"),
                                dt("2026-11-07 11:00"), "B2"))
    print(scheduler.add_booking("A", dt("2026-11-07 09:30"),
                                dt("2026-11-07 10:30"), "B3"))
