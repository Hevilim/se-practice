# SIS #05 — Report

**Name:** Karim Aliyev
**Group:** Monday 16:00 - 19:00
**Date:** 27.11.2026

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup and the project

| | |
| --- | --- |
| Project (name, and what it does in one line) | Study room booking check: can_book decides if one study room can be booked for a time slot |
| Language and stack | Python 3 (standard library only), tests with unittest |
| Where it comes from (my own / Smart Campus / other: say what) | Smart Campus: my own Python version of the booking rule from SIS 03 (sis-03/code). Nothing is copied from my Week 10 or Week 11 worksheets |
| Baseline commit — the project brought in unchanged (§3 of the README) | dcb636e |
| Assistant (tool) | Claude Code (the claude command in the terminal) |
| Exact model (with its version, or `not displayed`) | Claude Opus 5.5 (claude-opus-5-5) |
| Where I ran the commands (my computer / Codespace / Bolt terminal / …) | my computer (macOS, Python 3.15.2) |

---

## 2. Task 1 — baseline and context

### 2.1 Repository map

Real paths in `project/`.

| Part | Where (paths) and what it does |
| --- | --- |
| Entry points | project/booking.py: the function can_book(start, end, now, blocked, existing). There is no command line program; it is used by import |
| Modules | project/booking.py: the booking rule (AC1 to AC4 checks, bad input returns False). project/original/booking_v1.py: the first version of can_book, kept for comparison, nothing imports it |
| Dependencies (and where they are declared) | None. Only the Python standard library. There is no requirements.txt or pyproject.toml, and the Python version is not declared anywhere |
| Tests | project/test_booking.py: 35 unittest tests in the class BookingTests |
| Build / run scripts | None. There is no build step, no script and no Makefile. Tests run with python3 -m unittest |

### 2.2 Commands

At least three. **Kind:** `test`, `lint`, `type`, `build` or `run`. **Exists:** `yes` / `no`.
**Result:** `pass`, `fail`, `missing` or `not run` (say why in the note).

| Command | Kind | Exists | Result | Note |
| --- | --- | --- | --- | --- |
| `python3 -m unittest -v` | test | yes | pass | Ran 35 tests, OK. Output in 2.3 |
| `python3 -m py_compile booking.py test_booking.py` | build | yes | pass | exit code 0. Only a syntax check, there is no real build |
| `ruff check .` / `flake8` | lint | no | missing | No lint tool is configured or installed (ruff not found, flake8 not found) |
| `mypy booking.py` | type | no | missing | No type checker, and booking.py has no type hints (No module named mypy) |
| `python3 booking.py` | run | yes | pass | exit code 0, but it prints nothing: the file only defines a function |

### 2.3 Baseline output

The **real** output of the baseline test run (or of running the program, if there were no tests):

```text
$ python3 -m unittest -v
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

### 2.4 Weaknesses and missing checks

At least three. **Evidence:** a file and line, or a command and its output. **Kind:** `fact` (you saw
it) or `assumption` (not yet shown).

| # | Weakness or missing check | Evidence | Kind |
| --- | --- | --- | --- |
| 1 | The room is treated as free when blocked is not a real boolean. blocked=None (an unknown state) gives True | booking.py line 32: if blocked. My run: can_book(660, 720, 540, None, []) printed True | fact |
| 2 | now is never checked. A NaN current time skips the "start after now" rule | booking.py line 24: start <= now is False for NaN. My run: can_book(300, 360, float('nan'), False, []) printed True | fact |
| 3 | The code points to a document that is not in the project | booking.py lines 9, 13 and 40 say "lab-report §9.2"; there is no lab-report in project/ | fact |
| 4 | No lint or type check exists | ruff not found, flake8 not found, No module named mypy (2.2) | fact |
| 5 | The same rule is copied in two files, so a fix in one can be forgotten in the other | original/booking_v1.py lines 11-30 repeat booking.py lines 19-38 | fact |
| 6 | The broad except (TypeError, ValueError) can hide a real bug inside the checks | booking.py lines 39-41. I did not find a case that hides a bug yet | assumption |

### 2.5 Acceptance criteria

Three to five things that must still be true after every change, and how you check each one.

| ID | Must remain true | How I check it (a test, a command, a step) |
| --- | --- | --- |
| AC1 | A slot is booked only if 0 <= start < end <= 1440 and start is after now | tests test_zero_length_is_rejected, test_ends_after_end_of_day_is_rejected, test_starts_now_is_rejected, test_start_one_minute_after_now_is_allowed |
| AC2 | A slot longer than 120 minutes is rejected, 120 minutes is allowed | tests test_exactly_two_hours_is_allowed, test_over_two_hours_is_rejected |
| AC3 | A blocked room is always rejected | tests test_blocked_room_is_rejected, test_blocked_room_with_no_bookings_is_rejected |
| AC4 | A slot that overlaps a booking is rejected; touching ends is allowed | tests test_overlap_is_rejected, test_touching_end_is_allowed, test_touching_start_is_allowed |
| AC5 | can_book returns only True or False, never raises an error and never changes existing | tests test_existing_unchanged_after_accept, test_bad_existing_returns_false, and the full run of python3 -m unittest |

---

## 3. Task 2 — agent instructions

### 3.1 The file and how the assistant reads it

| | |
| --- | --- |
| File (`project/AGENTS.md` or `project/CLAUDE.md`) | project/AGENTS.md |
| Created or improved? | created (the project had none). Claude Code drafted it (exchange 1); I removed three references to "lab-report §9.2", a file that is not in the project |
| Does the assistant load it by itself? (`yes` / `no, I pasted it` / `not sure, I pasted it`) | no, I pasted it: Claude Code reads CLAUDE.md, not AGENTS.md, so every prompt after it was written told the assistant to read AGENTS.md first |

### 3.2 What it covers

Where each topic is in the file (the heading, or the line).

| Topic | Where in the file |
| --- | --- |
| Purpose | ## Purpose |
| Architecture | ## Architecture |
| Setup | ## Setup |
| Safe commands | ## Safe commands (python3 -m unittest -v, one test, py_compile, the import example, git status, git diff) |
| Coding conventions | ## Coding conventions |
| Test expectations | ## Test expectations |
| Forbidden actions | ## Forbidden actions (secrets, production deploys, destructive commands, dependency changes without human review, pushing to main) |

---

## 4. Task 3 — a focused pattern decision

### 4.1 The maintainability problem

<!-- One problem: the file and lines, and why it makes the code harder to change. Write below this line -->

In project/booking.py lines 18-41, can_book checks all rules in one chain of if statements inside one try block. The limits 1440 and 120 are written inside the conditions (lines 20 and 28). The same chain is copied in project/original/booking_v1.py lines 11-30. To add a new rule, for example opening hours, you must edit the middle of this function.

### 4.2 The pattern I evaluated

<!-- Strategy, Adapter, or another you can name; what it would change for this problem. Write below this line -->

Strategy: each rule becomes its own small function with the same five arguments, kept in a list, and can_book runs the list in order and returns False at the first rule that fails. A new rule would then be a new function added to the list. I asked Claude Code about it (exchange 2).

### 4.3 My decision, before and after

**Decision:** not warranted

<!-- Why, and the structure before and after (functions, modules, or a diagram in a code block). Write below this line -->

There are only four checks, each one or two lines, and nothing adds or changes rules while the program runs. Strategy would add five functions, a list and a loop, so the code gets longer but not easier to change: a new rule is still one edit in one file. The order of the checks also matters, and the one try block is simpler with the checks together. The copy in original/booking_v1.py is only for comparison, so a pattern would not remove it. Claude Code also suggested named constants for 1440 and 120; I did not do it, because the README already names both limits and I keep the code unchanged here.

```text
Before:  booking.py -> can_book() with 4 checks (AC1-AC4) in one try block
After:   the same. No file in project/ was changed by this decision.
```

### 4.4 The acceptance criteria still hold

The real output of the same checks, run after the decision:

```text
$ python3 -m unittest
...................................
----------------------------------------------------------------------
Ran 35 tests in 0.000s

OK
$ python3 -m py_compile booking.py test_booking.py; echo "exit code $?"
exit code 0
```

---

## 5. Task 4 — read-only AI risk review

### 5.1 The review

How you made sure the assistant could not modify files, and what it was given:

<!-- Write below this line -->

What you sent, exactly:

```text
(paste here)
```

The answer, pasted unedited:

```text
(paste here)
```

### 5.2 The findings, investigated

At least **five**, across at least **three** categories: `correctness`, `maintainability`, `security`,
`dependency`, `agent operations`. **Label:** `confirmed`, `plausible` or `unsupported`.

| # | Finding (short) | Category | What I opened or ran | Label | Evidence or why not |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

---

## 6. Task 5 — risk register

### 6.1 The register

At least five risks, at least two `confirmed`. **Component:** a path in `project/`, or
`missing: <check>`. **Score = L × I.**

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification plan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | | | | | | | | | | | |
| R2 | | | | | | | | | | | |
| R3 | | | | | | | | | | | |
| R4 | | | | | | | | | | | |
| R5 | | | | | | | | | | | |

### 6.2 The top two for action

Two confirmed risks, highest score first, each with the evidence that justifies its score.

1. **R?** —
2. **R?** —

---

## 7. Task 6 — agent-readiness audit

### 7.1 The rows

`yes` or `no`, and the evidence (README §10).

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Tests, one command | | |
| 1b | Lint or type check | | |
| 1c | Build or run from a clean copy | | |
| 1d | Pinned dependencies | | |
| 2a | README accurate | | |
| 2b | Reproducible setup | | |
| 2c | `AGENTS.md` with safe commands and forbidden actions | | |
| 3a | CI | | |
| 3b | Logging an agent can read | | |
| 3c | Security safeguards | | |
| 3d | Review gate before merge | | |

### 7.2 The level and the missing evidence

**Level:** (0, 1, 2 or 3 — by the 80% rule)

**Missing evidence for the next level:**

<!-- Name the rows and what would have to exist. -->
-

---

## 8. Task 7 — two mitigations and verification

### 8.1 The first mitigation

**Risk:** R?

**What I changed, and what I rejected from the assistant's proposal:**

The test that fails before the fix (or why a test is not feasible):

```text
(paste here)
```

The diff (`git diff`):

```text
(paste here)
```

### 8.2 The second mitigation

**Risk:** R?

**What I changed, and what I rejected from the assistant's proposal:**

The test that fails before the fix (or why a test is not feasible):

```text
(paste here)
```

The diff (`git diff`):

```text
(paste here)
```

### 8.3 The final checks

The real output of the final test run (and any other check you ran):

```text
(paste here)
```

Tests and checks I did not run, and why:

<!-- Write below this line. "None" only if it is true. -->

### 8.4 Updated scores and what remains

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |
| | | | | | | | |

**Remaining limitations and trade-offs:**

<!-- Write below this line -->

---

## 9. Tasks 8–9 — background-agent safeguards and the release decision

### 9.1 A hypothetical background-agent task

| Safeguard | For this project |
| --- | --- |
| The task | |
| Isolation (branch or worktree) | |
| Allowed files | |
| Commands | |
| Time limit | |
| Prohibited operations | |
| Required artifacts | |
| Human approval, failure and rollback | |

### 9.2 Release decision

**Decision:** GO / CONDITIONAL / NO-GO

<!-- Keep one word above. GO is not allowed while any confirmed risk still scores 6 or more.
     Then 80-150 words: the test evidence, the register, the readiness level. Name at least two
     risk IDs. -->

<!-- Write your justification below this line -->

---

## 10. AI reflection

<!-- 200-300 words, in your own words, without the assistant. Answer all four:
     1. Which assistant and model did you use, and what context did it receive?
     2. One useful AI suggestion, and one inaccurate, weak or unverified one.
     3. What did you personally check, and how did the tests change your decisions?
     4. Did AGENTS.md improve the process? What should improve next?
     Worthless: "The AI was very helpful and saved me a lot of time."
     Worth everything: "Claude (claude-sonnet-5-5) got the README, AGENTS.md and the diff. Its R1,
     eval on the shares field, was right: test_R1 failed before the fix. Its claim that the tests
     were flaky was unsupported: ten runs, ten passes." -->

<!-- Write your reflection below this line -->

---

## 11. AI evidence appendix

At least **three** complete exchanges.

### 11.1 Exchange 1

| | |
| --- | --- |
| Tool and date | |
| Exact model | |
| Prompt (summary) | |
| Output I used | |
| Problems I found in it | |
| Changes I made | |
| How I verified it | |

### 11.2 Exchange 2

| | |
| --- | --- |
| Tool and date | |
| Exact model | |
| Prompt (summary) | |
| Output I used | |
| Problems I found in it | |
| Changes I made | |
| How I verified it | |

### 11.3 Exchange 3

| | |
| --- | --- |
| Tool and date | |
| Exact model | |
| Prompt (summary) | |
| Output I used | |
| Problems I found in it | |
| Changes I made | |
| How I verified it | |

### 11.4 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |
