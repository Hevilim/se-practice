"""Smart Campus study room booking: availability decision for one room."""


def can_book(start, end, now, blocked, existing):
    """Return True if the requested slot [start, end) can be booked, else False.

    Times are integer minutes after midnight on a single date.
    `existing` holds (start, end) tuples of this room's active bookings.
    A start or end that is not an integer returns False (lab-report §9.2).
    Any other bad input also returns False instead of raising an error.
    No input is modified.
    """
    # Outside the contract (lab-report §9.2): reject non-integer times.
    for value in (start, end):
        if not isinstance(value, int) or isinstance(value, bool):
            return False

    try:
        # AC1: the slot lies within the day and has positive length.
        if not (0 <= start < end <= 1440):
            return False

        # AC1: the slot starts strictly in the future.
        if start <= now:
            return False

        # AC2: the duration is at most 120 minutes.
        if end - start > 120:
            return False

        # AC3: the room is not blocked.
        if blocked:
            return False

        # AC4: no overlap with any existing booking (half-open intervals).
        for booked_start, booked_end in existing:
            if start < booked_end and booked_start < end:
                return False
    except (TypeError, ValueError):
        # Outside the contract (lab-report §9.2): a bad now or existing never crashes.
        return False

    # AC5: every check passed.
    return True
