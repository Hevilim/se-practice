# Week 05 — Lab report

**Name:** Karim Aliyev
**Group:** Monday 16:00 - 19:00
**Date:** 07.10.2026

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant (tool) | Claude (claude.ai) |
| **Exact** model name | Claude Opus 5.5 |
| Language and version | Python 3.12.4 |
| Path | A |
| My Week 04 declaration for touching bookings | allowed |

---

## 2. Task 1 — the plan

**The assistant's plan, pasted unedited:**

```text
## Implementation plan for `can_book` (Python 3, no code yet)

**Approach:** a pure function with no side effects. It returns `False` as soon as any check fails, and returns `True` only if every check passes. It only reads `existing`: no sorting, appending or removing.

### Checks in order
1. **AC1, range and order:** `0 <= start < end <= 1440`. If this fails, return `False`.
2. **AC1, future start:** `start > now`, strictly. If this fails, return `False`.
3. **AC2, duration:** `end - start <= 120`. If this fails, return `False`. Step 1 already guarantees the duration is at least 1.
4. **AC3, blocked:** if `blocked` is true, return `False`.
5. **AC4, overlap:** for each `(s, e)` in `existing`, the slots overlap when `start < e and s < end` (half-open intervals). Any overlap means return `False`. Check every booking, never just the first one.
6. **AC5:** if nothing failed, return `True`.

Steps 1–4 are cheap, constant-time checks, so they come before the loop. The order doesn't change the result, because all checks must pass. But checking `start` and `end` first means the later steps only run on a sensible interval.

### Assumptions (taken from the contract, not added)
- `start` and `end` are integers but may be out of range. The function checks that; it doesn't check their types.
- `now` is valid (0–1439) and `blocked` is a Boolean, so neither is checked again.
- `existing` may be empty or unsorted. Each tuple is valid with `s < e`. Its order isn't assumed, and its bookings aren't assumed to be free of overlaps with each other.
- `end == 1440`, the end of the day, is allowed. `start == now` is rejected.
- There is no minimum duration beyond `start < end`, so a 1-minute booking is fine.
- Everything is on a single date, so bookings never wrap past midnight.

### Boundary cases that could expose bugs
Baseline: `now = 480`, `blocked = False`, `existing = [(600, 660)]` unless a case says otherwise.

| Case | Input (start, end) | Expected | Bug it catches |
|---|---|---|---|
| Start equals now | (480, 540) | False | `>=` used instead of `>` |
| Start one minute after now | (481, 541) | True | an off-by-one that is too strict |
| Negative start | (-10, 30) | False | missing lower-bound check |
| End at 1440 | (1380, 1440) | True | `< 1440` used instead of `<=` |
| End past the day | (1380, 1441) | False | missing upper-bound check |
| Zero length | (700, 700) | False | `<=` used instead of `<` |
| Reversed | (720, 700) | False | negative duration accepted |
| Exactly 120 min | (700, 820) | True | `<` used instead of `<=` |
| 121 min | (700, 821) | False | limit not enforced |
| Blocked but otherwise valid | (700, 760), blocked=True | False | AC3 ignored |
| Ends where a booking starts | (540, 600) | True | touching treated as overlap |
| Starts where a booking ends | (660, 720) | True | touching treated as overlap |
| One minute into the booking at the end | (540, 601) | False | overlap test too loose |
| One minute into the booking at the start | (659, 720) | False | overlap test too loose |
| Same slot as the booking | (600, 660) | False | only partial overlaps detected |
| Inside the booking | (610, 650) | False | only endpoint checks done |
| Wraps around the booking | (590, 670) | False | only checks whether endpoints fall inside a booking |
| Clash with the last of several unsorted bookings | existing=[(900,960),(600,660),(700,760)], request (720,780) | False | early `return True` inside the loop |
| Exact fit in a gap | existing=[(600,660),(720,780)], request (660,720) | True | touching on both sides rejected |
| No bookings | existing=[], request (700,760) | True | empty list mishandled |
| Latest possible now | now=1439, request (1439,1440) | False | `start > now` not checked |
| Input unchanged | copy `existing` before the call, compare after, for both True and False results | equal | sorting in place or appending (AC5) |

Two notes: `start = 0` can never be valid, because `now >= 0` and the start must be after `now`. Also, the first-hour booking test only works if `now` is earlier than the start. Ready to move to tests or code when you are.
```

**What the plan invented or changed.** One row for every rule in the plan that is not in the
contract or in AC1–AC5, or that says something different from them. If you found none, write one
row saying which lines of the plan you checked against which AC.

| # | What the plan said | What the contract or the AC says | What I did |
| --- | --- | --- | --- |
| 1 | Six checks: day bounds, start after now, max 120 minutes, blocked, overlap, return True | AC1, AC2, AC3, AC4, AC5 | I checked every step. Each step comes from an AC. There are no new rules, no gap between bookings and no sorting. Nothing to drop. |
| 2 | The function only reads existing and does not sort or change it | AC5 says never alter existing | This is correct. I added tests that the list does not change. |
| 3 | now and blocked are not checked again | The contract says now is valid and blocked is a Boolean | This is correct. The plan does not check things the contract already promises. |
| 4 | The function does not check the types of start and end | The contract says times are integers, but it does not say what to do if they are not | This is correct for the contract. But I decided to return False for non-integer times, see 9.2. |

**Boundary cases the assistant suggested that I kept as tests:**

- start equal to now, start one minute after now, negative start (AC1)
- end at 1440, end at 1441, zero length, reversed times (AC1)
- exactly 120 minutes and 121 minutes (AC2)
- touching on both sides, inside, around and the same slot (AC4)
- several unsorted bookings, a slot between two bookings, no bookings (AC4)
- the list is the same after the call (AC5)

---

## 3. Task 2 — the first version (v1), read before it was run

v1 is saved as `code/original/booking_v1.<ext>`, exactly as the assistant returned it: yes

**AC map.** One row per condition in v1. Quote the line.

| # | Line in v1 | AC it implements | Correct as written? If not, why |
| --- | --- | --- | --- |
| 1 | if not (0 <= start < end <= 1440): return False | AC1 | Yes. It stops a negative start, zero length, reversed times and an end after 1440. An end at 1440 is allowed. |
| 2 | if start <= now: return False | AC1 | Yes. The start must be after now, so a start equal to now gives False. |
| 3 | if end - start > 120: return False | AC2 | Yes. 120 minutes is allowed, 121 is not. |
| 4 | if blocked: return False | AC3 | Yes. |
| 5 | if start < booked_end and booked_start < end: return False (inside a loop) | AC4 | Yes. Both signs are strict, so touching bookings are allowed. The loop checks every booking. |
| 6 | return True | AC5 | Yes. It runs only when all checks pass. The result is a real Boolean and the list is only read. |

Before running it I expected nothing in AC1 to AC5 to fail. I only expected a crash with TypeError on line 1 when start is "600" or None. I want False there, see 9.2.

**Anything in v1 that no AC asks for** (extra validation, a buffer between bookings, logging,
saving the booking, a different return type):

- Nothing. Only a docstring and comments.

---

## 4. Task 3 — my tests

Base input for every row unless the row says otherwise: `now=540, blocked=False, existing=[(600, 660)]`.

| # | Test name | Request (start, end) | What differs from the base input | Expected | AC | Result on v1 | Result on final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | test_touching_end_is_allowed | 660, 720 | none | True | AC4 | pass | pass |
| 2 | test_overlap_is_rejected | 630, 690 | none | False | AC4 | pass | pass |
| 3 | test_blocked_room_is_rejected | 660, 720 | blocked=True | False | AC3 | pass | pass |
| 4 | test_exactly_two_hours_is_allowed | 720, 840 | none | True | AC2 | pass | pass |
| 5 | test_over_two_hours_is_rejected | 720, 841 | none | False | AC2 | pass | pass |
| 6 | test_starts_now_is_rejected | 540, 570 | none | False | AC1 | pass | pass |
| 7 | test_zero_length_is_rejected | 700, 700 | none | False | AC1 | pass | pass |
| 8 | test_reversed_times_are_rejected | 720, 700 | none | False | AC1 | pass | pass |
| 9 | test_ends_exactly_at_end_of_day_is_allowed | 1380, 1440 | none | True | AC1 | pass | pass |
| 10 | test_ends_after_end_of_day_is_rejected | 1380, 1441 | none | False | AC1 | pass | pass |
| 11 | test_negative_start_is_rejected | -30, 30 | none | False | AC1 | pass | pass |
| 12 | test_start_one_minute_after_now_is_allowed | 541, 571 | none | True | AC1 | pass | pass |
| 13 | test_start_in_the_past_is_rejected | 500, 530 | none | False | AC1 | pass | pass |
| 14 | test_start_one_minute_after_midnight_now_is_allowed | 1, 61 | now=0 | True | AC1 | pass | pass |
| 15 | test_one_minute_booking_is_allowed | 720, 721 | none | True | AC2 | pass | pass |
| 16 | test_blocked_room_with_no_bookings_is_rejected | 660, 720 | blocked=True, no bookings | False | AC3 | pass | pass |
| 17 | test_touching_start_is_allowed | 570, 600 | none | True | AC4 | pass | pass |
| 18 | test_partial_overlap_over_start_is_rejected | 570, 630 | none | False | AC4 | pass | pass |
| 19 | test_inside_existing_is_rejected | 615, 645 | none | False | AC4 | pass | pass |
| 20 | test_contains_existing_is_rejected | 570, 690 | none | False | AC4 | pass | pass |
| 21 | test_identical_interval_is_rejected | 600, 660 | none | False | AC4 | pass | pass |
| 22 | test_empty_existing_is_allowed | 600, 660 | no bookings | True | AC4 | pass | pass |
| 23 | test_overlap_with_second_booking_is_rejected | 720, 780 | bookings 600-660 and 700-760 | False | AC4 | pass | pass |
| 24 | test_overlap_with_later_booking_in_unsorted_list_is_rejected | 610, 650 | bookings 900-960 and 600-660 | False | AC4 | pass | pass |
| 25 | test_fits_exactly_between_two_bookings_is_allowed | 660, 720 | bookings 600-660 and 720-780 | True | AC4 | pass | pass |
| 26 | test_free_slot_among_three_bookings_is_allowed | 760, 800 | bookings 600-660, 700-760, 800-860 | True | AC4 | pass | pass |
| 27 | test_existing_unchanged_after_accept | 780, 840 | bookings 900-960, 600-660, 700-760 | True and the list is the same | AC5 | pass | pass |
| 28 | test_existing_unchanged_after_reject | 610, 650 | bookings 900-960, 600-660, 700-760 | False and the list is the same | AC5 | pass | pass |
| 29 | test_string_start_returns_false | "600", 660 | one booking 700-760 | False | my rule from 9.2 | error | pass |
| 30 | test_fractional_start_returns_false | 600.5, 660 | one booking 700-760 | False | my rule from 9.2 | fail | pass |
| 31 | test_none_end_returns_false | 600, None | one booking 700-760 | False | my rule from 9.2 | error | pass |
| 32 | test_integer_subclass_times_are_allowed | Minutes(660), Minutes(720) | times are a subclass of int | True | AC5 | pass | pass |
| 33 | test_boolean_start_returns_false | True, 61 | now=0, no bookings | False | my rule from 9.2 | fail | pass |
| 34 | test_bad_now_returns_false | 660, 720 | now=None | False | my rule from 9.2 | error | pass |
| 35 | test_bad_existing_returns_false | 660, 720 | existing=[(600,)] | False | my rule from 9.2 | error | pass |

---

## 5. Task 4 — debugging with evidence

One row per defect you found — in v1, in a later version, or in your own tests. If v1 passed
everything, the row is the **new edge case you added**, with expected and actual equal, and the
cause column says why no change was needed.

| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | can_book(600.5, 660, 540, False, [(700, 760)]) | False (my rule from 9.2) | True | No line checks the type. The line if not (0 <= start < end <= 1440) works with a float. | A type check before all other checks | The assistant, in the debug answer |
| 2 | can_book("600", 660, 540, False, [(700, 760)]) | False (my rule from 9.2) | TypeError, the function crashes | 0 <= start cannot compare an int and a str | The same type check, before line 1 | Me |
| 3 | can_book(600, None, 540, False, [(700, 760)]) | False (my rule from 9.2) | TypeError, the function crashes | 600 < None cannot be compared | The same type check | Me |
| 4 | can_book(Minutes(660), Minutes(720), 540, False, [(600, 660)]) where Minutes is a subclass of int | True | False | My first check if type(start) is not int | Use isinstance(value, int), but still reject bool | The assistant, in the critique |
| 5 | can_book(660, 720, None, False, [(600, 660)]) and can_book(660, 720, 540, False, [(600,)]) | False (my rule from 9.2) | TypeError and ValueError, the function crashes | start <= now cannot compare an int and None, and for booked_start, booked_end in existing cannot unpack (600,) | Put the AC checks in try and return False on TypeError or ValueError | Me |

**The debug prompt I sent, and the assistant's answer** (leave the block empty if you did not use it):

````text
PROMPT (sent with the v1 code, the test test_fractional_start_returns_false and its failure output pasted below it):

The expected result is False, but I get True. Here are my code and failing test. Explain the cause and propose the smallest fix without changing the contract.

ANSWER:

## Why it returns True
Your function is behaving correctly under the contract. The test checks something the contract doesn't cover. Tracing `can_book(600.5, 660, 540, False, [(700, 760)])` through each check:

- **AC1 range:** `0 <= 600.5 < 660 <= 1440` holds.
- **AC1 future start:** `600.5 <= 540` is false, so the check passes.
- **AC2 duration:** `660 - 600.5 = 59.5`, which is not over 120.
- **AC3 blocked:** `blocked` is `False`.
- **AC4 overlap:** `600.5 < 760 and 700 < 660` is false, so there's no clash.
- **AC5:** the function returns `True`.

None of the checks looks at the *type* of the value. Python compares floats and ints without complaint, so `600.5` gets through every rule. The test's own comment says it's "outside the contract": the contract says times are integer minutes. So the contract doesn't define what should happen with `600.5`, and returning `True` doesn't break any AC.

## Option A: no code change (closest to the stated scope)
Treat the test as out of scope. Remove it, or mark it `@unittest.skip("outside contract: times are integers")`. Then the function stays exactly AC1–AC5. Choose this if the lab report doesn't actually require handling bad input.

## Option B: smallest code fix (if lab-report §9.2 is a real requirement)
I can't see §9.2. I only have the scenario, contract and ACs. If it really requires "non-integer time returns False", add one guard as the first check:

```python
    # Outside the contract (lab-report §9.2): reject non-integer times.
    if type(start) is not int or type(end) is not int:
        return False
```

How this fits:
- **Contract unchanged:** the signature stays the same, and every valid integer input gets the same result as before. The guard only gives a defined answer to input the contract never allowed.
- **It must come first:** a value like `"600"` would otherwise raise `TypeError` in the AC1 comparison. Putting the guard first also covers "never crashes".
- **Why `type(...) is int` and not `isinstance(..., int)`:** `bool` is a subclass of `int`. With `isinstance`, a `start` of `True` would be accepted as `1`.
- **What it doesn't touch:** `now`, `blocked` and `existing` stay unchecked, because the contract guarantees they're valid.

One thing to decide: Option B goes beyond AC1–AC5. If you take it, write it down as an extra rule from §9.2 so the test and code agree, rather than treating it as part of the original acceptance criteria. If you want, I can draft that wording for the lab report.
````

---

## 6. Task 5 — the critique

**The assistant's critique, pasted unedited:**

```text
## Review against the contract and AC1–AC5

I found **two issues**, both caused by the extra type guard. I didn't make up more to reach five. Everything that implements AC1–AC5 checks out.

### Issue 1: the guard can reject input the contract allows
> `if type(start) is not int or type(end) is not int:`

- **Concerns:** AC5 ("Return True only when AC1–AC4 hold", which also means it must return True when they do) and the contract line "Times are integer minutes after midnight".
- **Problem:** `type(x) is int` accepts only the exact `int` class, so it rejects other integer types, such as a subclass of `int`. A slot that meets AC1–AC4 can then get `False`.
- **Note:** this only matters if callers can pass integer types other than a plain `int`. Excluding `bool` on purpose is fine.

### Issue 2: a rule outside the contract is mixed in with AC1–AC5
> `# Outside the contract (lab-report §9.2): reject non-integer times.`

- **Concerns:** the rule to "Use only these" (the scenario, contract and AC1–AC5) and the feature scope.
- **Problem:** this check comes from §9.2, not from any AC. The code comment says so, but the docstring still describes only the contract. A reader of the docstring wouldn't know non-integer times are rejected.
- **Decide:** keep it as a documented extra rule (add it to the docstring and the lab report), or remove it to stay strictly within AC1–AC5.

### Checked, no issues
| Line | Criterion | Verdict |
|---|---|---|
| `if not (0 <= start < end <= 1440):` | AC1 range, start < end | Correct. `end == 1440` is allowed; zero-length and reversed slots are rejected. |
| `if start <= now:` | AC1 `start > now` | Correct, strict. |
| `if end - start > 120:` | AC2 | Correct. 120 is allowed, 121 is rejected. |
| `if blocked:` | AC3 | Correct. The contract guarantees a Boolean. |
| `if start < booked_end and booked_start < end:` | AC4, half-open intervals | Correct. Touching endpoints are allowed; partial, inside, wrapping and exact-match overlaps are caught. Every booking is checked, so order doesn't matter. |
| `return True` | AC5 | Reached only when every check passes. |
| (whole function) | AC5 "never alter existing", contract "Keep all inputs unchanged" | `existing` is only read; no input is changed. |

**Verdict:** for valid `int` inputs, the function meets AC1–AC5 and the contract. The only things left to decide are about the extra §9.2 guard.
```

| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | Issue 1: the check type(start) is not int rejects a subclass of int | accept | AC5 says True when AC1 to AC4 hold. A subclass of int is still an integer. I checked it and the old code really gave False. | 33 tests, OK |
| 2 | Issue 2: the docstring does not say anything about the extra rule | accept | No AC changes, but a reader should see the rule. I added one line to the docstring. | 33 tests, OK |
| 3 | Issue 2: or remove the type check | reject | Without it "600" crashes again. The contract says return True or False. | no change |

---

## 7. Change log — v1 to final

| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | Before: no type check. After: if type(start) is not int or type(end) is not int: return False | v1 gave True for 600.5 and crashed on "600" and None (section 5, rows 1 to 3) | test_fractional_start_returns_false, test_string_start_returns_false and test_none_end_returns_false went from fail or error to ok |
| 2 | Before: type(...) is not int. After: not isinstance(value, int) or isinstance(value, bool) | Critique issue 1 (section 5, row 4) | test_integer_subclass_times_are_allowed went from False to ok |
| 3 | Added one line to the docstring about non-integer times | Critique issue 2 | No test changed, 33 tests OK |
| 4 | Before: no try. After: the AC checks are inside try, and except (TypeError, ValueError) returns False | A bad now or existing crashed the function (section 5, row 5) | test_bad_now_returns_false and test_bad_existing_returns_false went from error to ok |

---

## 8. Evidence — real output

### 8.1 My suite, final run

Paste the **complete** terminal output. For Python: everything `python -m unittest -v` printed.

```text
$ cd code && python3 -m unittest -v
test_bad_existing_returns_false (test_booking.BookingTests.test_bad_existing_returns_false) ... ok
test_bad_now_returns_false (test_booking.BookingTests.test_bad_now_returns_false) ... ok
test_blocked_room_is_rejected (test_booking.BookingTests.test_blocked_room_is_rejected) ... ok
test_blocked_room_with_no_bookings_is_rejected (test_booking.BookingTests.test_blocked_room_with_no_bookings_is_rejected) ... ok
test_boolean_start_returns_false (test_booking.BookingTests.test_boolean_start_returns_false) ... ok
test_contains_existing_is_rejected (test_booking.BookingTests.test_contains_existing_is_rejected) ... ok
test_empty_existing_is_allowed (test_booking.BookingTests.test_empty_existing_is_allowed) ... ok
test_ends_after_end_of_day_is_rejected (test_booking.BookingTests.test_ends_after_end_of_day_is_rejected) ... ok
test_ends_exactly_at_end_of_day_is_allowed (test_booking.BookingTests.test_ends_exactly_at_end_of_day_is_allowed) ... ok
test_exactly_two_hours_is_allowed (test_booking.BookingTests.test_exactly_two_hours_is_allowed) ... ok
test_existing_unchanged_after_accept (test_booking.BookingTests.test_existing_unchanged_after_accept) ... ok
test_existing_unchanged_after_reject (test_booking.BookingTests.test_existing_unchanged_after_reject) ... ok
test_fits_exactly_between_two_bookings_is_allowed (test_booking.BookingTests.test_fits_exactly_between_two_bookings_is_allowed) ... ok
test_fractional_start_returns_false (test_booking.BookingTests.test_fractional_start_returns_false) ... ok
test_free_slot_among_three_bookings_is_allowed (test_booking.BookingTests.test_free_slot_among_three_bookings_is_allowed) ... ok
test_identical_interval_is_rejected (test_booking.BookingTests.test_identical_interval_is_rejected) ... ok
test_inside_existing_is_rejected (test_booking.BookingTests.test_inside_existing_is_rejected) ... ok
test_integer_subclass_times_are_allowed (test_booking.BookingTests.test_integer_subclass_times_are_allowed) ... ok
test_negative_start_is_rejected (test_booking.BookingTests.test_negative_start_is_rejected) ... ok
test_none_end_returns_false (test_booking.BookingTests.test_none_end_returns_false) ... ok
test_one_minute_booking_is_allowed (test_booking.BookingTests.test_one_minute_booking_is_allowed) ... ok
test_over_two_hours_is_rejected (test_booking.BookingTests.test_over_two_hours_is_rejected) ... ok
test_overlap_is_rejected (test_booking.BookingTests.test_overlap_is_rejected) ... ok
test_overlap_with_later_booking_in_unsorted_list_is_rejected (test_booking.BookingTests.test_overlap_with_later_booking_in_unsorted_list_is_rejected) ... ok
test_overlap_with_second_booking_is_rejected (test_booking.BookingTests.test_overlap_with_second_booking_is_rejected) ... ok
test_partial_overlap_over_start_is_rejected (test_booking.BookingTests.test_partial_overlap_over_start_is_rejected) ... ok
test_reversed_times_are_rejected (test_booking.BookingTests.test_reversed_times_are_rejected) ... ok
test_start_in_the_past_is_rejected (test_booking.BookingTests.test_start_in_the_past_is_rejected) ... ok
test_start_one_minute_after_midnight_now_is_allowed (test_booking.BookingTests.test_start_one_minute_after_midnight_now_is_allowed) ... ok
test_start_one_minute_after_now_is_allowed (test_booking.BookingTests.test_start_one_minute_after_now_is_allowed) ... ok
test_starts_now_is_rejected (test_booking.BookingTests.test_starts_now_is_rejected) ... ok
test_string_start_returns_false (test_booking.BookingTests.test_string_start_returns_false) ... ok
test_touching_end_is_allowed (test_booking.BookingTests.test_touching_end_is_allowed) ... ok
test_touching_start_is_allowed (test_booking.BookingTests.test_touching_start_is_allowed) ... ok
test_zero_length_is_rejected (test_booking.BookingTests.test_zero_length_is_rejected) ... ok

----------------------------------------------------------------------
Ran 35 tests in 0.001s

OK
```

### 8.2 The checker, final run

Paste the **complete** output of `python tests/check_booking.py`. Paste it **last**: if you edit
this file afterwards, run the checker again and paste again.

```text
$ python3 tests/check_booking.py
Week 05 - can_book: the function, your tests, the evidence   (Path A)

PASS   F1   the six cases from the task table           6 of 6 cases
PASS   F2   AC1 time order and day bounds               5 of 5 cases
PASS   F3   AC1 the start is in the future              5 of 5 cases
PASS   F4   AC2 at most 120 minutes                     3 of 3 cases
PASS   F5   AC3 a blocked room accepts nothing          2 of 2 cases
PASS   F6   AC4 every kind of overlap is rejected       5 of 5 cases
PASS   F7   AC4 touching endpoints are allowed          3 of 3 cases
PASS   F8   AC4 every existing booking is checked       4 of 4 cases
PASS   F9   AC5 the result is a real Boolean            3 of 3 cases
PASS   F10  AC5 the inputs are left unchanged           2 of 2 cases
PASS   O1   the assistant's first version is kept       v1 kept (33 lines)
PASS   S1   your suite has at least 11 tests            35 tests
PASS   S2   your suite is green on your own code        35 tests, OK
PASS   M1   your tests catch a fault in AC1             caught by test_starts_now_is_rejected
PASS   M2   your tests catch a fault in AC1             caught by test_ends_after_end_of_day_is_rejected
PASS   M3   your tests catch a fault in AC1             caught by test_zero_length_is_rejected
PASS   M4   your tests catch a fault in AC2             caught by test_exactly_two_hours_is_allowed
PASS   M5   your tests catch a fault in AC3             caught by test_blocked_room_is_rejected, test_blocked_room_with_no_bookings_is_rejected
PASS   M6   your tests catch a fault in AC4             caught by test_fits_exactly_between_two_bookings_is_allowed, test_free_slot_among_three_bookings_is_allowed, test_integer_subclass_times_are_allowed and 2 more
PASS   M7   your tests catch a fault in AC4             caught by test_existing_unchanged_after_reject, test_overlap_with_later_booking_in_unsorted_list_is_rejected, test_overlap_with_second_booking_is_rejected
PASS   M8   your tests catch a fault in AC4             caught by test_contains_existing_is_rejected
PASS   M9   your tests catch a fault in AC5             caught by test_existing_unchanged_after_accept
PASS   M10  your tests catch a fault in AC5             caught by test_existing_unchanged_after_accept, test_existing_unchanged_after_reject
PASS   L1   report 1: tool, model and language          tool, model and language recorded
PASS   L2   report 2: the plan, and what you corrected  plan pasted, 26 row(s) on what you corrected or verified
PASS   L3   report 3: v1 mapped to AC1-AC4              6 conditions mapped, AC1-AC4 all present
PASS   L4   report 4: at least 11 of your tests listed  35 tests listed
PASS   L5   report 5: debugging evidence                5 row(s) of input / expected / actual
PASS   L6   report 6: the critique, each point judged   critique pasted, 5 points judged
PASS   L7   report 7: change log                        4 change-log row(s)
PASS   L8   report 8.1: real output of your suite       suite output pasted
PASS   L9   report 10: conclusion of 120-180 words      179 words
------------------------------------------------------------------------------
v1 (code/original/booking_v1.py): passes F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 - fails nothing - identical to your final: no
Not counted for M - these fail on a can_book that follows the contract exactly, so they
test what the contract leaves open or contradict an AC: test_bad_existing_returns_false, test_bad_now_returns_false, test_boolean_start_returns_false, test_fractional_start_returns_false, test_none_end_returns_false, test_string_start_returns_false
SUMMARY pass=32 fail=0 error=0   (32 checks)
Behaviour and shape are clean. This says nothing about the quality of your review.
```

### 8.3 Path B only — three faults I planted myself

Break your own function on purpose, one line at a time, run your suite, restore the line.

| # | Line I changed (before → after) | AC it breaks | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

The three failing runs (Path A students leave this block empty):

```text
```

---

## 9. What still fails, and what the contract does not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | The last checker run has no FAIL and no ERROR. |

### 9.2 Outside the contract

The contract says times are integers. It does not say what `can_book` does when one is not —
`600.5`, or the string `"600"`. What does **your** function do, and why is that the right call?

My function returns False if start or end is not an integer, for example 600.5, "600", None or True. It also returns False if now or existing is bad, for example now=None. It never crashes. The contract says the function returns True or False, and a crash is neither of them. Saying True for a time like 600.5 is also wrong. These checks do not change the answer for normal inputs, and F1 to F10 still pass.

### 9.3 A bound that never decides

One of the bounds written in AC1 can never be the *only* reason a request is rejected. Which one,
and why?

It is 0 <= start. The value of now is always 0 or more. So if start is below 0, it is also below now, and the rule start > now already gives False. These two rules always reject it together.

---

## 10. Conclusion (120–180 words)

<!-- Answer all three, in your own words, without the assistant:
     (a) Explain the overlap condition in your final code — why those two comparisons, and why
         they let touching bookings through.
     (b) Which fault did your tests miss the longest, and what did the missing test have in common
         with the ones you already had?
     (c) What did you have to decide that neither the contract nor the assistant decided for you?
     Worthless: "the AI made a mistake and I fixed it."
     Worth everything: "F7 failed on can_book(570, 600, ...): v1 compared with <= on the start
     side, so a booking that ends exactly when another begins was rejected." -->

<!-- Write your conclusion below this line -->

(a) My overlap check is start < booked_end and booked_start < end. Two bookings overlap only when each one starts before the other one ends. Both signs are strict. For can_book(660, 720, 540, False, [(600, 660)]) we get 660 < 660, which is False, so the touching booking is allowed and the result is True.

(b) M9 was missed the longest. After the six table tests M2, M3, M7, M8, M9 and M10 passed all my tests. M9 breaks AC5, and only test_existing_unchanged_after_accept catches it. All my first tests had the same problem: they checked only the return value and never looked at existing after the call.

(c) I had to decide what happens when a time is not an integer. v1 returned True for can_book(600.5, 660, 540, False, [(700, 760)]) and crashed with TypeError on can_book("600", 660, ...). I made the function return False for these, but a subclass of int is still allowed. I also made it return False and not crash when now or existing is bad.
