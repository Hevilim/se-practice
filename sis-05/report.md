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

A new Claude Code session (claude -p) in sis-05/project, model Claude Opus 5.5, in plan mode and with only the Read, Glob and Grep tools, so it could not edit files or run commands. It read AGENTS.md, README.md, booking.py, test_booking.py and original/booking_v1.py by itself. git status showed no change afterwards.

What you sent, exactly:

```text
Read AGENTS.md first, then README.md, booking.py, test_booking.py and original/booking_v1.py.

You are a read-only risk reviewer. Do not modify, create or delete any file, and do not run any command. Do not invent test results: you did not run the tests, so never say that a test passes or fails unless you only read it from the code, and say so.

Propose risks for this project in these categories: correctness, maintainability, security, dependency, agent operations. For each risk give: the category, the file and line, the evidence you read, how I can check it myself (a command or a test), and whether it is something you read in the code or only a guess. Use simple English.
```

The answer, pasted unedited:

```text
I read all five files and ran no commands, so none of the results below come from running the code or the tests. When I say what a call "returns", I worked it out by reading the code by hand.

The project folder has only: `booking.py`, `test_booking.py`, `original/booking_v1.py`, `original/.gitkeep`, `README.md`, `AGENTS.md`, `.gitignore`.

---

## Correctness

**C1. A room with `blocked=None` can be booked.**
- File: `booking.py:32`
- Evidence: `if blocked:` only checks whether `blocked` counts as true. `None`, `0` and `""` all count as false, so the check passes. AGENTS.md:21 says bad input returns `False`, but `blocked` is never type-checked. Reading the code, `can_book(660, 720, 540, None, [(600, 660)])` reaches `return True`. The opposite case also happens: `blocked="False"` (a string) counts as true, so the room is treated as blocked.
- Check: `python3 -c "from booking import can_book; print(can_book(660, 720, 540, None, [(600, 660)]))"`
- Source: read in code.

**C2. `now` is not type-checked, and `now=NaN` lets any slot through.**
- File: `booking.py:14-16, 24`
- Evidence: the type check only covers `(start, end)`. Any comparison with NaN is false, so `start <= float('nan')` is `False` and the "slot is in the future" check passes. A float `now` like `540.5` is also accepted. `now=None` is safe: it raises `TypeError`, which is caught.
- Check: `python3 -c "from booking import can_book; print(can_book(660, 720, float('nan'), False, []))"`
- Source: read in code.

**C3. Bad rows in `existing` can hide a real overlap.**
- File: `booking.py:36-38`
- Evidence: the code never checks that `booked_start < booked_end`, or that the values are integers. With a reversed row `(700, 600)`, a request for 620–680 gives `620 < 600` = False, so no overlap is found and the result is `True`. A NaN value behaves the same way.
- Check: `python3 -c "from booking import can_book; print(can_book(620, 680, 540, False, [(700, 600)]))"`
- Source: read in code. Whether bad rows can really reach this function is a guess.

**C4. The rule "never changes its inputs" is broken if `existing` is a generator.**
- File: `booking.py:36`, AGENTS.md:24
- Evidence: the `for` loop reads through the iterator, so the generator is empty afterwards. The tests at `test_booking.py:122-134` only use lists.
- Check: `python3 -c "from booking import can_book; g=iter([(600,660)]); can_book(700,720,540,False,g); print(list(g))"` (an empty list means the input was consumed)
- Source: read in code.

**C5. "Never raises an error" depends on only two exception types.**
- File: `booking.py:39`
- Evidence: only `TypeError` and `ValueError` are caught. An `existing` object whose iteration raises any other error (for example `RuntimeError`), or an `int` subclass with a broken `__lt__` or `__sub__`, would crash the call.
- Check: write a small test with a class whose `__iter__` raises `RuntimeError`.
- Source: guess (an edge case, not seen in real data).

## Maintainability

**M1. The broad `try/except` can hide future bugs.**
- File: `booking.py:18-41`
- Evidence: the whole decision is inside `try`. A future typo that raises `TypeError` would quietly return `False`. All the tests that expect `False` would still pass, so the bug could go unnoticed.
- Check: in a scratch copy, add a typo inside the `try` block, then run `python3 -m unittest -v`. Only the tests that expect `True` should fail.
- Source: read in code. The "future bug" part is a guess.

**M2. The AC labels in the tests do not match AGENTS.md.**
- File: `test_booking.py:121` compared with `AGENTS.md:20`
- Evidence: the test comment says "AC5: existing is never altered". AGENTS.md says AC5 is "return True only if every check passes". Also, the first six tests (`test_booking.py:10-32`) have no group comment, which AGENTS.md:55 asks for.
- Check: read the two lines side by side.
- Source: read in code.

**M3. Edge tests that AGENTS.md asks for are missing.**
- File: `test_booking.py`, `AGENTS.md:56`
- Evidence: AGENTS.md lists the limit `0`, but no test books `start=0` (for example `can_book(0, 60, -1, False, [])`). There are also no tests for `blocked=None`, a float or NaN `now`, reversed rows in `existing`, or a generator as `existing` (see C1–C4).
- Check: `grep -n "can_book(0," test_booking.py` (no output means no such test)
- Source: read in code (these tests are absent).

**M4. "lab-report §9.2" points to a document outside the project.**
- File: `booking.py:9, 13, 40`, `test_booking.py:136`
- Evidence: the project folder has no lab report. A search found the text in `../report.md`, one folder up. AGENTS.md:30 says to work only inside the project folder.
- Check: `ls ..; grep -n "9.2" ../report.md`
- Source: read (I only found where the text is, I did not open that file).

**M5. A second copy of the old code can drift or be copied back.**
- File: `original/booking_v1.py:12-30`
- Evidence: v1 has no type check and no `try`. So `can_book("600", 660, ...)` in v1 would raise `TypeError`, which breaks the current contract. Nothing stops anyone from editing it or copying it back.
- Check: `git log --oneline -- original/` and `git diff main -- original/`
- Source: read in code.

**M6. The magic numbers `1440` and `120` appear in the code and in two docs.**
- File: `booking.py:20, 28`, README.md:15-18, AGENTS.md:13-17
- Evidence: there are no named constants. If one rule changes, three places must be updated by hand.
- Check: `grep -n "1440\|120" booking.py README.md AGENTS.md`
- Source: read in code.

## Security

**S1. The checks let bookings through when inputs are bad, and `now` is fully trusted.**
- File: `booking.py:24, 32`
- Evidence: this is C1 and C2 seen as a security problem. If a caller ever takes `now` or `blocked` from the user's request, the user can send `now=-1` or `blocked=None` and get past the time check or the room block. The function cannot know who supplied the values.
- Check: look at how the caller builds `now` and `blocked`. There is no caller in this repo.
- Source: guess (depends on code I cannot see).

**S2. Secrets risk is low.**
- Evidence: there is no `.env` or config file in the project, and no I/O or imports in `booking.py`. I did not read `.gitignore`.
- Check: `cat .gitignore; git ls-files`
- Source: read (file list only).

## Dependency

**D1. "Python 3.10 or newer" is not enforced.**
- File: `AGENTS.md:27`, `README.md:24`
- Evidence: there is no `pyproject.toml` or version check. On macOS, `python3` may be Apple's older system Python. I saw no 3.10-only syntax in the code, so the rule may also be stricter than needed.
- Check: `python3 --version; which python3`
- Source: read (no version pin). The macOS part is a guess.

**D2. The tests import `booking` by bare name.**
- File: `test_booking.py:2`
- Evidence: `from booking import can_book` depends on the current folder or `sys.path`. If you run from another folder, the import fails, or a different `booking` module could be loaded instead.
- Check: `python3 -c "import booking; print(booking.__file__)"`
- Source: read in code. The shadowing part is a guess.

**D3. There is no CI.**
- Evidence: the project has no `.github/` or other CI config, so "tests pass" relies on someone running them by hand.
- Check: `ls -a; ls -a ../..`
- Source: read (file list).

## Agent operations

**A1. The git root is above the project, and there are many untracked files.**
- Evidence: the git status shows untracked `../../.DS_Store`, `../../SETUP.md`, `../../sis-02/` and `../../week-*`. `week-11` contains `node_modules`. A careless `git add -A` would stage all of it.
- Check: `git rev-parse --show-toplevel; git status --short`
- Source: read (git status snapshot).

**A2. The AGENTS.md rules are written but not enforced.**
- File: `AGENTS.md:58, 67, 12`
- Evidence: "never delete or weaken a test", "never push to main" and "do not edit original/" are only text. I can't see whether `main` has branch protection.
- Check: `git diff main -- test_booking.py original/`. For branch protection, look at the repo settings on GitHub.
- Source: the rules are read. That they are not enforced is a guess.

**A3. An agent could claim the tests passed without running them.**
- File: `AGENTS.md:52, 70`
- Evidence: there is no CI to confirm it. By my count from reading, `test_booking.py` has 35 test methods. Real output should end with `Ran 35 tests` and `OK`.
- Check: run `python3 -m unittest -v` yourself and compare the count.
- Source: the count is read. The risk is a guess.

**A4. A fix for C1/C2 changes behavior.**
- Evidence: making `blocked=None` or `now=NaN` return `False` is a behavior change. AGENTS.md:53 requires a new test for that, and you should decide on it yourself rather than let an agent do it alone.
- Source: read (AGENTS rule).

---

**Most important to check first:** C1 (`blocked=None` lets a booking through) and C2 (`now=NaN`). Both break the "bad input returns False" rule, and each takes a one-line command to confirm.

I did not create a plan file, because you asked me not to create any files.
```

### 5.2 The findings, investigated

At least **five**, across at least **three** categories: `correctness`, `maintainability`, `security`,
`dependency`, `agent operations`. **Label:** `confirmed`, `plausible` or `unsupported`.

| # | Finding (short) | Category | What I opened or ran | Label | Evidence or why not |
| --- | --- | --- | --- | --- | --- |
| 1 | C1: blocked=None lets the room be booked | correctness | python3 -c "from booking import can_book; print(can_book(660, 720, 540, None, []))" | confirmed | It printed True. booking.py line 32 is if blocked |
| 2 | C2: now=NaN skips the start after now rule | correctness | python3 -c "...can_book(300, 360, float('nan'), False, [])" | confirmed | It printed True. Only start and end are type-checked (lines 14-16) |
| 3 | C3: a reversed row in existing hides a real overlap | correctness | python3 -c "...can_book(620, 680, 540, False, [(700, 600)])" | confirmed | It printed True |
| 4 | C4: a generator as existing is used up, so the input is changed | correctness | python3 -c "...g=iter([(600,660)]); can_book(700,720,540,False,g); print(list(g))" | confirmed | It printed [] |
| 5 | C5: an error other than TypeError or ValueError crashes the call | correctness | an existing object whose __iter__ raises RuntimeError | confirmed | RuntimeError: boom, the call raised instead of returning False |
| 6 | M1: the broad try/except can hide a future bug | maintainability | in a scratch copy I changed 120 to '120' inside the try block and ran python3 -m unittest | plausible | The TypeError was swallowed, but the suite still caught it: FAILED (failures=12). A bug that only affects False results could still hide |
| 7 | M2: the AC5 label in the tests does not match AGENTS.md | maintainability | test_booking.py line 121 and AGENTS.md line 20 | confirmed | The test says "AC5: existing is never altered", AGENTS.md says AC5 is "return True only if every check passes" |
| 8 | M4: "lab-report §9.2" points to a file outside the project | maintainability | grep -n "lab-report" booking.py | confirmed | Lines 9, 13 and 40; there is no lab report in project/ |
| 9 | M5: the old copy in original/booking_v1.py breaks the bad-input rule | maintainability | I imported booking_v1 and called can_book('600', 660, 540, False, []) | confirmed | TypeError: '<=' not supported between instances of 'int' and 'str' |
| 10 | S1: a caller could send now or blocked from the user and get past the checks | security | I looked for a caller | plausible | There is no caller in the project, so I cannot show who builds now and blocked |
| 11 | D1: "Python 3.10 or newer" is not enforced | dependency | python3 --version; ls -a | plausible | Python 3.15.2 here and no pyproject.toml. I did not try an older Python, and the code has no 3.10-only syntax |
| 12 | D3: there is no CI | agent operations | ls -a in project/ | confirmed | Only .gitignore, AGENTS.md, README.md, booking.py, original, test_booking.py. No .github folder |
| 13 | A1: the git root is above the project and has many untracked folders | agent operations | git rev-parse --show-toplevel; git status --short | confirmed | The root is se-practice, and week-01, week-08 (with node_modules) and others are untracked, so git add -A would stage them |

---

## 6. Task 5 — risk register

### 6.1 The register

At least five risks, at least two `confirmed`. **Component:** a path in `project/`, or
`missing: <check>`. **Score = L × I.**

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification plan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | security | blocked comes in as None or 0 (unknown state) -> if blocked treats it as free -> a blocked room is booked | booking.py | finding 1: can_book(660, 720, 540, None, []) printed True | confirmed | 2 | 3 | 6 | accept blocked only when it is exactly False | Karim Aliyev | test_R1_none_blocked_is_rejected fails before and passes after the fix |
| R2 | correctness | now is not type-checked -> a NaN now makes start <= now False -> a slot in the past is booked | booking.py | finding 2: can_book(300, 360, float('nan'), False, []) printed True | confirmed | 2 | 3 | 6 | check now with the same integer check as start and end | Karim Aliyev | test_R2_nan_now_returns_false fails before and passes after the fix |
| R3 | correctness | a booking row in existing is reversed or NaN -> the overlap test is never true for it -> two bookings for one slot | booking.py | finding 3: can_book(620, 680, 540, False, [(700, 600)]) printed True | confirmed | 1 | 3 | 3 | reject existing rows that are not integer pairs with start < end | Karim Aliyev | a test test_R3_reversed_existing_row_returns_false |
| R4 | correctness | existing is a generator, or raises another error -> the loop uses it up or crashes -> the "no input is modified, never raises" rule breaks | booking.py | findings 4 and 5: list(g) printed [], and RuntimeError: boom | confirmed | 1 | 2 | 2 | copy existing to a tuple first and document that it must be a list | Karim Aliyev | a test with iter([...]) and a check that it is not empty afterwards |
| R5 | agent operations | there is no CI -> an agent says the tests pass without running them -> a broken change is merged | missing: CI that runs python3 -m unittest on every push | finding 12: no .github folder in project/ | plausible | 2 | 2 | 4 | a GitHub Actions job that runs the tests | Karim Aliyev | open a pull request and see the job run |
| R6 | maintainability | the old copy original/booking_v1.py has no bad-input handling -> someone edits or copies it back -> can_book raises errors again | original/booking_v1.py | finding 9: booking_v1 raised TypeError for start '600' | confirmed | 1 | 2 | 2 | delete the copy or mark it clearly as not used | Karim Aliyev | grep -rn booking_v1 shows no import, and the tests still pass |
| R7 | dependency | the Python version is not declared -> someone runs it on an old Python -> setup fails or behaves differently | missing: a declared Python version (pyproject.toml requires-python) | finding 11: no pyproject.toml, only a line in README.md | plausible | 1 | 1 | 1 | add a pyproject.toml with requires-python | Karim Aliyev | run the tests on the lowest declared version |

### 6.2 The top two for action

Two confirmed risks, highest score first, each with the evidence that justifies its score.

1. **R1** — score 6. My run showed a blocked room with blocked=None is booked, and a wrong yes is the worst result for this rule.
2. **R2** — score 6. My run showed a NaN current time lets a slot in the past be booked, the same serious wrong yes.

---

## 7. Task 6 — agent-readiness audit

### 7.1 The rows

`yes` or `no`, and the evidence (README §10).

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Tests, one command | yes | python3 -m unittest -v runs all tests (output in 2.3 and 8.3) |
| 1b | Lint or type check | no | ruff, flake8 and mypy are not installed or configured; only python3 -m py_compile, which is a syntax check |
| 1c | Build or run from a clean copy | yes | no install step; the import command from README.md printed True, py_compile exit code 0 |
| 1d | Pinned dependencies | yes | no third-party dependencies at all, only the standard library |
| 2a | README accurate | yes | project/README.md: the three commands in it work as written (8.3) |
| 2b | Reproducible setup | yes | README.md says Python 3.10 or newer and no packages; nothing else is needed |
| 2c | `AGENTS.md` with safe commands and forbidden actions | yes | project/AGENTS.md, headings Safe commands and Forbidden actions |
| 3a | CI | no | no .github folder or other CI config |
| 3b | Logging an agent can read | no | can_book returns only False and prints nothing; the reason for a rejection is lost |
| 3c | Security safeguards | no | no secret scanning or dependency audit; input checks only for start, end and now |
| 3d | Review gate before merge | yes | AGENTS.md: "A human reviews and merges every change" and "Never push to main or merge your own changes" |

### 7.2 The level and the missing evidence

**Level:** 0

**Missing evidence for the next level:**

<!-- Name the rows and what would have to exist. -->
- Level 1 has 3 of 4 rows (75%, less than 80%), so the project is level 0. Row 1b is missing: a lint or type check, for example ruff or mypy, written in AGENTS.md and passing.
- Level 2 rows are all yes, but they do not count until Level 1 is reached.
- For Level 3: CI that runs the tests (3a), a reason for each rejection that an agent can read (3b), and secret scanning plus full input checks (3c).

---

## 8. Task 7 — two mitigations and verification

### 8.1 The first mitigation

**Risk:** R1

**What I changed, and what I rejected from the assistant's proposal:** I changed if blocked to if blocked is not False, so only an exact False lets the booking go on, and added test_R1_none_blocked_is_rejected. I took this from Claude Code's patch (exchange 4) after reading it. I rejected its claim that the suite would have "35 tests (33 old and 2 new)": there were 35 old tests, and the real run after both fixes shows 37.

The test that fails before the fix (or why a test is not feasible):

```text
$ python3 -m unittest -v test_booking.BookingTests.test_R1_none_blocked_is_rejected
test_R1_none_blocked_is_rejected (test_booking.BookingTests.test_R1_none_blocked_is_rejected) ... FAIL

======================================================================
FAIL: test_R1_none_blocked_is_rejected (test_booking.BookingTests.test_R1_none_blocked_is_rejected)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/hevilim/Developer/se-practice/sis-05/project/test_booking.py", line 81, in test_R1_none_blocked_is_rejected
    self.assertIs(result, False)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

The diff (`git diff`):

```text
diff --git a/sis-05/project/booking.py b/sis-05/project/booking.py
index e5c5394..ab9eb96 100644
--- a/sis-05/project/booking.py
+++ b/sis-05/project/booking.py
@@ -29,7 +29,7 @@ def can_book(start, end, now, blocked, existing):
             return False
 
         # AC3: the room is not blocked.
-        if blocked:
+        if blocked is not False:
             return False
 
         # AC4: no overlap with any existing booking (half-open intervals).
diff --git a/sis-05/project/test_booking.py b/sis-05/project/test_booking.py
index 9d56aa1..647c3ea 100644
--- a/sis-05/project/test_booking.py
+++ b/sis-05/project/test_booking.py
@@ -76,6 +76,10 @@ class BookingTests(unittest.TestCase):
         result = can_book(660, 720, 540, True, [])
         self.assertIs(result, False)
 
+    def test_R1_none_blocked_is_rejected(self):
+        result = can_book(660, 720, 540, None, [])
+        self.assertIs(result, False)
+
     # AC4: the other overlap relationships
     def test_touching_start_is_allowed(self):
         result = can_book(570, 600, 540, False, [(600, 660)])
```

### 8.2 The second mitigation

**Risk:** R2

**What I changed, and what I rejected from the assistant's proposal:** I added now to the integer check that start and end already use, changed the docstring to say "a start, end or now", and added test_R2_nan_now_returns_false. The patch is the one from exchange 4. Nothing in the code was rejected, but I checked its side effect myself: a float now like 540.0 now returns False, and no existing test uses a float now.

The test that fails before the fix (or why a test is not feasible):

```text
$ python3 -m unittest -v test_booking.BookingTests.test_R2_nan_now_returns_false
test_R2_nan_now_returns_false (test_booking.BookingTests.test_R2_nan_now_returns_false) ... FAIL

======================================================================
FAIL: test_R2_nan_now_returns_false (test_booking.BookingTests.test_R2_nan_now_returns_false)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/hevilim/Developer/se-practice/sis-05/project/test_booking.py", line 171, in test_R2_nan_now_returns_false
    self.assertIs(result, False)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

The diff (`git diff`):

```text
diff --git a/sis-05/project/booking.py b/sis-05/project/booking.py
index ab9eb96..26a2e40 100644
--- a/sis-05/project/booking.py
+++ b/sis-05/project/booking.py
@@ -6,12 +6,12 @@ def can_book(start, end, now, blocked, existing):
 
     Times are integer minutes after midnight on a single date.
     `existing` holds (start, end) tuples of this room's active bookings.
-    A start or end that is not an integer returns False (lab-report §9.2).
+    A start, end or now that is not an integer returns False (lab-report §9.2).
     Any other bad input also returns False instead of raising an error.
     No input is modified.
     """
     # Outside the contract (lab-report §9.2): reject non-integer times.
-    for value in (start, end):
+    for value in (start, end, now):
         if not isinstance(value, int) or isinstance(value, bool):
             return False
 
diff --git a/sis-05/project/test_booking.py b/sis-05/project/test_booking.py
index 647c3ea..14531ca 100644
--- a/sis-05/project/test_booking.py
+++ b/sis-05/project/test_booking.py
@@ -165,3 +165,7 @@ class BookingTests(unittest.TestCase):
     def test_bad_existing_returns_false(self):
         result = can_book(660, 720, 540, False, [(600,)])
         self.assertIs(result, False)
+
+    def test_R2_nan_now_returns_false(self):
+        result = can_book(300, 360, float('nan'), False, [])
+        self.assertIs(result, False)
```

### 8.3 The final checks

The real output of the final test run (and any other check you ran):

```text
$ python3 -m unittest -v
test_R1_none_blocked_is_rejected (test_booking.BookingTests.test_R1_none_blocked_is_rejected) ... ok
test_R2_nan_now_returns_false (test_booking.BookingTests.test_R2_nan_now_returns_false) ... ok
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
Ran 37 tests in 0.001s

OK
$ python3 -m py_compile booking.py test_booking.py; echo "exit code $?"
exit code 0
$ python3 -c "from booking import can_book; print(can_book(660, 720, 540, False, [(600, 660)]))"
True
```

Tests and checks I did not run, and why:

<!-- Write below this line. "None" only if it is true. -->

- Lint and type check: no tool is installed, and installing one is a dependency change (row 1b).
- The tests on Python 3.10, the lowest version the README names: I only have Python 3.15.2.
- CI: there is none (R5).
- Tests for R3, R4 and R6: those risks are not fixed yet, so I did not add tests for them.

### 8.4 Updated scores and what remains

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 2 | 3 | 6 | 1 | 3 | 3 | test_R1_none_blocked_is_rejected failed before and passes now; any blocked value except False rejects. Impact stays 3 if a caller sends False by mistake |
| R2 | 2 | 3 | 6 | 1 | 3 | 3 | test_R2_nan_now_returns_false failed before and passes now; a non-integer now returns False. A wrong integer now from the caller is still trusted |

**Remaining limitations and trade-offs:**

<!-- Write below this line -->

Both fixes make the function stricter: blocked=0 and a float now like 540.0 are now rejected, which is a behaviour change for callers that used them. A wrong but valid integer now or blocked=False from the caller is still trusted. R3 (bad rows in existing), R4 (generators and other errors) and R6 (the old copy) are still open, and there is still no lint and no CI.

---

## 9. Tasks 8–9 — background-agent safeguards and the release decision

### 9.1 A hypothetical background-agent task

| Safeguard | For this project |
| --- | --- |
| The task | Fix R3: make can_book return False for rows in existing that are not integer pairs with start < end, and add test_R3_reversed_existing_row_returns_false |
| Isolation (branch or worktree) | a new git worktree on a branch agent/r3-existing-rows made from sis-05, never main |
| Allowed files | only sis-05/project/booking.py and sis-05/project/test_booking.py; not original/, AGENTS.md or anything outside project/ |
| Commands | only python3 -m unittest -v, python3 -m py_compile booking.py test_booking.py, git status, git diff and git commit on its own branch |
| Time limit | 30 minutes of work and at most 5 test runs; after that it stops and reports what it has |
| Prohibited operations | no git push, no merge, no pip install or other dependency change, no rm -rf or git reset --hard, no deleting or weakening tests, no network access, no secrets |
| Required artifacts | a change summary, the git diff, the full unittest output before and after (the R3 test failing first), the py_compile result, and notes on any new risk |
| Human approval, failure and rollback | I read the diff and run the tests myself before I merge anything. If tests fail or the agent touches another file, I delete the branch and worktree (git worktree remove) and main stays unchanged |

### 9.2 Release decision

**Decision:** CONDITIONAL

<!-- Keep one word above. GO is not allowed while any confirmed risk still scores 6 or more.
     Then 80-150 words: the test evidence, the register, the readiness level. Name at least two
     risk IDs. -->

<!-- Write your justification below this line -->

The two highest confirmed risks, R1 and R2, were fixed. Their tests failed before the fix, and the final run shows all 37 tests passing, so no confirmed risk still scores 6 or more. GO is allowed by the rule, but I do not choose it. The project is only readiness level 0, because there is no lint or type check, and there is no CI (R5). R3, a reversed booking row that can hide an overlap, is confirmed with score 3 and still open, and R4 and R6 are also open. The conditions: callers must pass integer times, blocked as a real boolean and well-formed existing rows. I own R3 as the next fix, with the background-agent task in 9.1 and a failing test first. A human reviews every merge, as AGENTS.md says.

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

I used Claude Code with the model Claude Opus 5.5 (claude-opus-5-5). Every exchange was a new session in plan mode with only read tools, so it could not change files. It got the project files, and after Task 2 every prompt told it to read AGENTS.md first, because Claude Code does not load AGENTS.md by itself.

The most useful suggestion was C1 in the risk review: blocked=None lets a blocked room be booked. I ran the command, it printed True, and test_R1_none_blocked_is_rejected failed before the fix. C2 about a NaN current time was also real. A weak part was M1: the reviewer said a typo inside the try block could go unnoticed, but when I put a typo in a scratch copy, 12 tests failed. The patch answer also said there would be 35 tests with 33 old ones, which was wrong: there were 35 old tests and 37 at the end.

I checked every finding myself with a command or a scratch test before I gave it a label. The tests changed my decisions. Because R1 and R2 had failing tests, I could fix them first and prove the fix. I left R3 for the next step. The readiness rows showed the project is only level 0, so I chose CONDITIONAL, not GO.

AGENTS.md helped. The assistant used its safe commands, and the patch kept the rule that can_book returns only True or False. Its first draft copied a reference to a file that is not in the project, so I had to fix it. Next time I would add a lint tool and CI first, so an agent could prove its claims.

---

## 11. AI evidence appendix

At least **three** complete exchanges.

### 11.1 Exchange 1

| | |
| --- | --- |
| Tool and date | Claude Code (claude -p, plan mode, read tools only), 27.11.2026 |
| Exact model | Claude Opus 5.5 (claude-opus-5-5) |
| Prompt (summary) | Draft an AGENTS.md for this project with seven headings (Purpose, Architecture, Setup, Safe commands, Coding conventions, Test expectations, Forbidden actions), only commands that work, and the four forbidden actions. Do not modify files |
| Output I used | The whole draft became project/AGENTS.md |
| Problems I found in it | It copied the reference "lab-report §9.2" from booking.py three times, but that file is not in the project |
| Changes I made | I removed the three references and kept the rest |
| How I verified it | I ran every safe command it lists (unittest, one test, py_compile, the import example); all worked. git status showed no change from the assistant |

### 11.2 Exchange 2

| | |
| --- | --- |
| Tool and date | Claude Code (claude -p, plan mode, read tools only), 27.11.2026 |
| Exact model | Claude Opus 5.5 (claude-opus-5-5) |
| Prompt (summary) | Would Strategy (each rule as a function in a list) make the chain of checks in booking.py lines 18-41 easier to change, or only longer? Apply it or not warranted |
| Output I used | Its reasons for not warranted: only four short fixed checks, more parts for the same behaviour, the order and the one try block are easier together |
| Problems I found in it | Its claim that original/booking_v1.py is "not a real duplicate" is weak: finding 9 shows the copy behaves differently and is a risk (R6) |
| Changes I made | I chose not warranted and did not take its extra suggestion of named constants, so the code stayed the same |
| How I verified it | I ran python3 -m unittest and py_compile again after the decision (4.4): 35 tests OK |

### 11.3 Exchange 3

| | |
| --- | --- |
| Tool and date | Claude Code (claude -p, plan mode, read tools only), 27.11.2026 |
| Exact model | Claude Opus 5.5 (claude-opus-5-5) |
| Prompt (summary) | Read-only risk review: read AGENTS.md and the files, do not modify anything, do not invent test results, give risks in the five categories with file, line, evidence and how to check |
| Output I used | Findings C1 to C5, M1, M2, M4, M5, S1, D1, D3 and A1, which became findings 1-13 in 5.2 and risks R1 to R7 |
| Problems I found in it | M1 said a typo bug could go unnoticed, but my scratch test showed 12 tests fail for such a typo. S1 depends on a caller that does not exist in the project |
| Changes I made | I labelled M1, S1 and D1 plausible, not confirmed, and set my own L and I scores |
| How I verified it | I ran each check command it gave (outputs in 5.2) and git status showed no change |

Exchange 4 (the mitigations):

| | |
| --- | --- |
| Tool and date | Claude Code (claude -p, plan mode, read tools only), 27.11.2026 |
| Exact model | Claude Opus 5.5 (claude-opus-5-5) |
| Prompt (summary) | Propose the smallest patch for R1 (blocked=None) and R2 (now=NaN) as diffs, with a test per risk named test_R1_ or test_R2_ that fails before the fix |
| Output I used | Both code changes (if blocked is not False, and now in the integer check) and both tests |
| Problems I found in it | It said both tests fail without running them, and it counted "35 tests (33 old and 2 new)", but there were 35 old tests and 37 in the end |
| Changes I made | I added each test first, ran it, saw it fail, then applied the fix, in two separate commits |
| How I verified it | The failing runs are in 8.1 and 8.2, and the final run in 8.3 shows Ran 37 tests, OK |

### 11.4 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | |
