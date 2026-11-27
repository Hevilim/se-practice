# Study room booking check

A small Python module from the Smart Campus course project. It decides if one study room can be
booked for a requested time slot. It does not save bookings.

## Files

- `booking.py` has one function, `can_book(start, end, now, blocked, existing)`. It returns `True`
  or `False`.
- `test_booking.py` has the unit tests (Python `unittest`).
- `original/booking_v1.py` is the first version of `can_book`, kept for comparison. Nothing imports it.

## The rule

Times are whole minutes after midnight on one day (0 to 1440). A slot can be booked when:

1. `0 <= start < end <= 1440`, and `start` is after `now`;
2. it is at most 120 minutes long;
3. the room is not blocked;
4. it does not overlap any booking in `existing` (touching ends is allowed).

## Setup and commands

You need Python 3.10 or newer. There are no third-party packages.

```text
python3 -m unittest -v          # run the tests
python3 -m py_compile booking.py test_booking.py   # syntax check
```

Use it from Python:

```text
python3 -c "from booking import can_book; print(can_book(660, 720, 540, False, [(600, 660)]))"
```
