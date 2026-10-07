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
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |
| 11 | | | | | | | |

---

## 5. Task 4 — debugging with evidence

One row per defect you found — in v1, in a later version, or in your own tests. If v1 passed
everything, the row is the **new edge case you added**, with expected and actual equal, and the
cause column says why no change was needed.

| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |

**The debug prompt I sent, and the assistant's answer** (leave the block empty if you did not use it):

```text
```

---

## 6. Task 5 — the critique

**The assistant's critique, pasted unedited:**

```text
(paste here)
```

| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | | | |

---

## 8. Evidence — real output

### 8.1 My suite, final run

Paste the **complete** terminal output. For Python: everything `python -m unittest -v` printed.

```text
(paste here)
```

### 8.2 The checker, final run

Paste the **complete** output of `python tests/check_booking.py`. Paste it **last**: if you edit
this file afterwards, run the checker again and paste again.

```text
(paste here)
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
| | |

### 9.2 Outside the contract

The contract says times are integers. It does not say what `can_book` does when one is not —
`600.5`, or the string `"600"`. What does **your** function do, and why is that the right call?

-

### 9.3 A bound that never decides

One of the bounds written in AC1 can never be the *only* reason a request is rejected. Which one,
and why?

-

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
