# AGENTS.md

## Purpose
This is a small Python module from the Smart Campus course project. It checks if one
study room can be booked for a time slot. It does not save bookings. The only public
function is `can_book(start, end, now, blocked, existing)`, which returns `True` or `False`.

## Architecture
- `booking.py` holds `can_book`. It has no imports and no side effects.
- `test_booking.py` holds the `unittest` tests (class `BookingTests`).
- `original/booking_v1.py` is the first version, kept only to compare against.
  Nothing imports it. Do not edit it.
- Times are whole minutes after midnight on one day (0 to 1440). Slots are half-open
  `[start, end)`, so two bookings that only touch at one end do not overlap.
- The rules, checked in this order:
  1. `0 <= start < end <= 1440` and `start > now` (AC1)
  2. the slot is at most 120 minutes (AC2)
  3. the room is not blocked (AC3)
  4. the slot does not overlap anything in `existing` (AC4)
  5. return `True` only if every check passes (AC5)
- Bad input returns `False` and never raises an error. This
  includes a `start` or `end` that is not an `int`, or is a `bool`. `int`
  subclasses are allowed.
- `can_book` never changes its inputs.

## Setup
- You need Python 3.10 or newer.
- There are no third-party packages, no `requirements.txt`, and no virtual
  environment. Nothing needs to be installed.
- Run every command from the project folder (the one with `booking.py`).

## Safe commands
    python3 -m unittest -v                                        # run all tests
    python3 -m unittest -v test_booking.BookingTests.test_overlap_is_rejected   # run one test
    python3 -m py_compile booking.py test_booking.py              # syntax check
    python3 -c "from booking import can_book; print(can_book(660, 720, 540, False, [(600, 660)]))"
    git status
    git diff
No lint, formatter, or type checker is installed. Do not run `flake8`, `black`,
`ruff`, `mypy`, or `pytest`.

## Coding conventions
- Use only the Python standard library.
- Use 4-space indents, `snake_case` names, and keep lines short.
- Keep the docstring and the short `# ACn:` comment above each check.
- Return `True` or `False`. Never raise an error, and never return `None` or any
  other value.
- Never change the inputs, including the `existing` list.
- Keep changes small. Do not change the function signature unless asked.

## Test expectations
- `python3 -m unittest -v` must pass with no failures before you hand over a change.
- Add a test for every behavior change or bug fix.
- Name tests `test_<what_happens>` and check results with `self.assertIs(result, True/False)`.
- Group tests under a comment that names the rule (AC1 to AC5, or bad input).
- Test edges: exact limits (0, 1440, 120 minutes, `start == now`), slots that touch,
  and bad input.
- Never delete or weaken a test just to make the tests pass.

## Forbidden actions
- Never commit secrets such as passwords, tokens, keys, or `.env` files.
- Never deploy to production.
- Never run destructive commands, for example `rm -rf`, `git reset --hard`,
  `git clean -fd`, `git push --force`, or rewriting git history.
- Never add, remove, or upgrade dependencies without human review. This includes
  running `pip install`.
- Never push to `main` or merge your own changes.

**A human reviews and merges every change.** Your job is to prepare a change on a
branch, show that the tests pass, and explain what you changed.
