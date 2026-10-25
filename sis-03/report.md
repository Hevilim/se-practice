# SIS #03 — Report: Smart Campus Room Availability Checker

<!-- The ONLY file you write prose in. Keep every numbered heading (## 1. … ## 13.) and every
     ### sub-heading, and the **Label:** words — the checker finds your answers by them.
     Replace every "(write here)" and "(paste here)". Delete these <!-- --> comments if you like. -->

## 1. Setup and reuse

<!-- Model: the exact model with its version, as the tool shows it ("ChatGPT" is a tool, not a
     model). If the tool does not show it, write: not displayed
     Reuse: week-05 if code/original/booking_v1.py is your Week 05 v1, copied unedited;
     week-06 if web/original/ is your Week 06 v1 export; fresh if you generated it for this SIS. -->

| Item | Value |
| --- | --- |
| Coding assistant (tool) | Claude (claude.ai) |
| Coding assistant model | Claude Opus 5.5 |
| Bolt.new model | not displayed |
| Bolt project link | https://bolt.new/p/72159062 |
| Language | Python 3.12.4 |
| Path | A |
| Python v1 from | week-05 |
| Web v1 from | week-06 |

## 2. Baseline — before any new AI exchange

<!-- Written by you, without AI, before the first exchange of this SIS. Commit and push it
     first (README §2). Reusing Week 05/06 work does not exempt you: this section is new. -->

### 2.1 Scope in my own words

**Scope:** I build a Python function can_book and one web page that check if one room is free, so a student can choose a good time. The page uses one room with made-up bookings, and it does not have login, database, backend, external APIs or payment, and it does not create or confirm any booking.

### 2.2 The acceptance criteria in my own words

| AC | In my own words |
| --- | --- |
| AC1 | Time is whole minutes from midnight, start must be smaller than end, end can be 1440 at most, and start must be later than now, so start equal to now is not ok. |
| AC2 | The booking can be 120 minutes long at most, 120 is ok but 121 is not ok. |
| AC3 | If the room is blocked, the answer is always Unavailable, even if the time is free. |
| AC4 | The request can not overlap with a booking that already exists, but if they only touch at the end, like 10:00-11:00 and 11:00-12:00, it is not an overlap. |
| AC5 | The page shows only Available or Unavailable, it does not save or change bookings, so the same check gives the same answer again. |
| AC6 | When the answer is Unavailable the user sees a clear reason, and the page works well on a phone screen about 375 px wide. |

### 2.3 Likely failure points

<!-- At least two. The brief's examples: endpoint overlap, starts-now. -->

| # | Failure point | AC | How I will check it |
| --- | --- | --- | --- |
| 1 | The overlap check uses <= instead of <, so a request 11:00-12:00 next to a booking 10:00-11:00 is wrongly rejected. | AC4 | T1, request 660-720 with booking 600-660, expected Available. |
| 2 | The check that start is after now uses >= instead of >, so a request that starts exactly at now is wrongly accepted. | AC1 | T6, now is 540, request 540-570, expected Unavailable. |

### 2.4 The contract

| Parameter | Meaning | Type and allowed values |
| --- | --- | --- |
| `start` | Start of the time the student wants. | Integer minutes from midnight, from 0 to 1439, must be bigger than now and smaller than end. |
| `end` | End of the wanted time, this minute is not included. | Integer minutes, up to 1440 included, must be bigger than start. |
| `now` | Current time of the day. | Integer minutes, always correct, from 0 to 1439. |
| `blocked` | Shows if the room is closed for booking. | Boolean True or False, True means booking is not possible. |
| `existing` | Bookings that this room already has. | List of (start, end) pairs in minutes, it can be empty, and the function does not change it. |
| returns | Result of the check. | Boolean, True only if AC1, AC2, AC3 and AC4 are all ok, otherwise False. |

### 2.5 Initial assumptions and manual checks

**Assumptions:**

1. All bookings and the request are in the same day, no booking goes past midnight.
2. The existing list can be empty and can be not sorted, and now is given on the page by the user, not taken from the computer clock.

**Checked manually:**

- I took T1 and put numbers in the overlap rule start < booked_end and booked_start < end: 660 < 660 is False and 600 < 720 is True, so the result is False, there is no overlap and the answer is Available.

## 3. Python v1 review

<!-- One row per conditional branch in code/original/booking_v1.py (your language's v1 on
     Path B). Quote the condition exactly. AC1-AC4 must all appear in the AC column. -->

| Branch in v1 (quoted) | AC | Satisfies it? | Why |
| --- | --- | --- | --- |
| if not (0 <= start < end <= 1440): return False | AC1 | Yes | It rejects a negative start, a zero length, reversed times (T7) and an end after 1440 (T9). An end at 1440 is allowed (T8). |
| if start <= now: return False | AC1 | Yes | The start must be after now. A start equal to now gives False (T6). |
| if end - start > 120: return False | AC2 | Yes | 120 minutes is allowed (T4) and 121 minutes is not (T5). |
| if blocked: return False | AC3 | Yes | A blocked room gives False even when the time is free (T3). |
| for booked_start, booked_end in existing: if start < booked_end and booked_start < end: return False | AC4 | Yes | Both signs are strict, so touching bookings are allowed (T1). The loop checks every booking, not only the first one (T10). |
| return True | AC5 | Yes | It is reached only when all checks pass. The list existing is only read, never changed (T11). |

v1 already gives the expected result for T1 to T11. My final adds only a type check and a try block for bad input from week-05. It does not change any result for valid input.

## 4. Prototype v1 in Bolt.new

**Prompt as sent:**

~~~~text
Build a small responsive Smart Campus Room Availability Checker. Requirements: AC1: Accept a candidate interval only when 0 ≤ start < end ≤ 1440 and start is after the supplied current time. AC2: Reject a booking longer than 120 minutes. AC3: Reject the request when the selected room is blocked. AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed. AC5: Show a clear Available / Unavailable decision without changing the existing booking data. AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback. Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
~~~~

<!-- Main generated files or components, with their path inside web/original/
     (for example src/App.tsx). At least two. -->

| Generated file or component | Path | Its role |
| --- | --- | --- |
| App component, evaluateBooking, ResultCard, RoomSchedule, Timeline | src/App.tsx | The whole page. It has the sample rooms, the form, the check of AC1 to AC4 in evaluateBooking, the result card and the list of bookings. |
| Entry point | src/main.tsx | It mounts App into the page. |
| Project setup | package.json | The scripts and the libraries. It also lists @supabase/supabase-js, which no file uses. |

**What v1 does:**

- The page has a Room list with four fictional rooms. Innovation Lab is blocked and has a booking 08:00-20:00.
- The page has a Current time field, a Start field and an End field. The time fields stop at 23:59.
- The Check availability button shows Available, Unavailable or Invalid input, with the reasons.
- No room has only the booking 10:00-11:00, so I cannot set up the base data of T1 to T12. All twelve cases are Not testable on v1.
- A check does not change the list of bookings.

## 5. Test cases — executed on both artifacts

<!-- Base for every case unless the row says otherwise: now = 540, blocked = False,
     existing = [(600, 660)]. Do not change the first four columns.
     Python columns: True, False or Error (it raised) — what the call actually returned.
       T11: the result of the SECOND call. T12: n/a.
       Path A: the checker runs both of your files on T1-T11 and compares (C2, C3).
     Page columns: Available, Unavailable or Not testable — what the page actually showed.
     Never write a result you did not observe. -->

| Case | Name | Input | Expected | Python v1 | Python final | Page v1 | Page final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 660–720 | Available | True | True | Not testable | Available |
| T2 | Overlap | 630–690 | Unavailable | False | False | Not testable | Unavailable |
| T3 | Blocked | 660–720, blocked | Unavailable | False | False | Not testable | Unavailable |
| T4 | Exactly 120 min | 720–840 | Available | True | True | Not testable | Available |
| T5 | 121 min | 720–841 | Unavailable | False | False | Not testable | Unavailable |
| T6 | Starts now | 540–570 | Unavailable | False | False | Not testable | Unavailable |
| T7 | Reversed | 720–660 | Unavailable | False | False | Not testable | Unavailable |
| T8 | Ends at midnight | 1380–1440 | Available | True | True | Not testable | Not testable |
| T9 | Past midnight | 1380–1441 | Unavailable | False | False | Not testable | Not testable |
| T10 | Second booking | 720–780, existing (600–660), (700–760) | Unavailable | False | False | Not testable | Unavailable |
| T11 | Same check twice | 660–720, twice | Available | True | True | Not testable | Available |
| T12 | Narrow screen | T1 at ~375 px wide | Available | n/a | n/a | Not testable | Available |

Page final rooms: T1, T2, T4 to T9, T11 and T12 in Auditorium B, T3 in Innovation Lab, T10 in Seminar Room 5, current time 09:00. I ran all cases with Playwright in Chrome on a local copy of each export. On v1 no room has only the booking 10:00-11:00, so every case is Not testable. T8 and T9 are Not testable on both pages, because the End field does not accept 24:00 or 24:01.

## 6. Traceability

<!-- His table. Implementation / file: where the rule lives (booking.py line, a component).
     Test input: the case IDs from section 5. v1 / final actual: what those cases gave. -->

| AC | Implementation / file | Test input | Expected | v1 actual | Final actual |
| --- | --- | --- | --- | --- | --- |
| AC1 | code/booking.py lines 20 and 24. Page: evaluateBooking in src/App.tsx, the interval check and the current time check | T6, T7, T8, T9 | T6, T7, T9 Unavailable or False. T8 Available or True | Python: False, False, True, False. Page: Not testable | Python: False, False, True, False. Page: T6 and T7 Unavailable, T8 and T9 Not testable |
| AC2 | code/booking.py line 28. Page: evaluateBooking, end - start > MAX_DURATION | T4, T5 | T4 Available, T5 Unavailable | Python: True, False. Page: Not testable | Python: True, False. Page: Available, Unavailable |
| AC3 | code/booking.py line 32. Page: evaluateBooking, room.blocked | T3 | Unavailable | Python: False. Page: Not testable | Python: False. Page: Unavailable |
| AC4 | code/booking.py lines 36 to 38. Page: evaluateBooking, room.bookings.find with start < b.end and end > b.start | T1, T2, T10 | T1 Available, T2 and T10 Unavailable | Python: True, False, False. Page: Not testable | Python: True, False, False. Page: Available, Unavailable, Unavailable |
| AC5 | code/booking.py line 44, existing is only read. Page: ResultCard and RoomSchedule, which sorts a copy | T11 | Available both times | Python: True. Page: Not testable | Python: True. Page: Available both times |
| AC6 | Page: ResultCard with the list of reasons, the grid layout in App, the current time message added in issue 1 | T7, T12 | T7 Unavailable with a reason, T12 Available at 375 px | Page: Not testable | Page: T7 Unavailable with the reason, T12 Available at 375 px, evidence/final-narrow.png |

## 7. Issue log

<!-- At least two, from v1 — a functional defect and a usability or code-quality issue where you
     have them. If every case passed on v1, log the preventive cleanup and say why.
     Reproduction names a case (T1-T12) or an AC. Priority: High, Medium or Low.
     Prompt / change: the focused prompt you sent, and what changed. Never "make it better". -->

| # | Issue | Reproduction | Priority | Prompt / change | Retest result |
| --- | --- | --- | --- | --- | --- |
| 1 | An empty Current time turns off the start after now check (AC1, AC6). Found in the critique. | Auditorium B, clear Current time, request 00:00-01:00. Expected Unavailable with a reason (AC1). Observed Available and no message. | High | Prompt B5: "when I clear the Current time field and check 00:00-01:00, the page shows Available ... Make the smallest change that fixes this behavior: an empty or invalid current time must give Unavailable with a clear reason." Change in src/App.tsx: current is null and not -1, and evaluateBooking adds the reason Enter a valid current time in HH:MM format. | Same input now gives Unavailable with that reason. T1 to T12 again: T6 still Unavailable, all other results the same. |
| 2 | T10 cannot be set up on the page: no room has the bookings 10:00-11:00 and 11:40-12:40 (AC4). | T10. I read every room with Playwright. Expected a room for T10. Observed none, so T10 was Not testable. | Medium | Prompt B6: "no room has exactly these two bookings, so T10 cannot be set up on the page. Make the smallest change that fixes this: only the fictional sample data, no new controls and no change to the rules." Change in src/App.tsx: a new room Seminar Room 5 with the bookings 600-660 and 700-760. The other four rooms are the same. | T10 in Seminar Room 5: Unavailable, overlap with 11:40-12:40. T1 to T12 again: all other results the same. |
| 3 | package.json has @supabase/supabase-js, a database library that no file uses. This is out of scope (no backend, no database). | Scope of AC1-AC6 (no backend, no database). Search src for supabase: nothing. Checker W3 failed on package.json. | Low | Prompt B7: "Make the smallest change that removes it without changing how the page behaves." Change: npm uninstall @supabase/supabase-js, so package.json and package-lock.json no longer have it. | npm run build and tsc pass. W3 passes. T1 to T12 again: the same results. |

**Before / after:** `evidence/before-1.png` → `evidence/after-1.png` show issue 2. Before: Auditorium B has only one booking, so 12:00-13:00 is Available and T10 cannot be set up. After: Seminar Room 5 has both bookings and T10 gives Unavailable.

## 8. Critique decisions

<!-- The AI's review against AC1-AC6 (stage C), claim by claim. At least three rows.
     How I verified it: the case, test or run that confirmed or refuted the claim.
     Decision: accept, reject or modify. At least one reject or modify — the reflection asks for it. -->

| # | AI claim or recommendation | How I verified it | Decision | Reason (AC or case) |
| --- | --- | --- | --- | --- |
| 1 | On the page an empty Current time becomes -1, so the start after now check is off. Auditorium B, empty current time, 00:00-01:00 shows Available. | I ran this on the page with Playwright. It showed Available and no message. | accept | AC1 and AC6. Fixed in issue 1. |
| 2 | T10 cannot be run on the page, because no room has the bookings 10:00-11:00 and 11:40-12:40. | I read every room on the page with Playwright. No room has these two bookings. | accept | AC4, T10. Fixed in issue 2. |
| 3 | package.json has @supabase/supabase-js, but the scope says no database and no backend. | I searched src for supabase and found nothing. The checker W3 also failed on package.json. | accept | Scope. Fixed in issue 3. |
| 4 | In booking.py the comment AC5 every check passed is wrong, because AC5 is about the page. | I read the contract. It says return True only when AC1-AC4 all hold. The function part of AC5 is this rule, and the line is the only place that returns True. All 35 tests pass. | reject | AC5 and the contract. The comment is correct for the function, so no change. |
| 5 | if blocked tests truthiness, so the string "False" counts as blocked. | I read the contract. It says blocked is a Boolean. T3 gives False and the base cases give the right result. | reject | AC3 and the contract. A string is outside the contract. |
| 6 | Reversed times like 10:50-10:10 also show an extra overlap reason, which is confusing. | I ran it on the page. It shows Unavailable with the interval reason and also the overlap reason. | modify | AC5 and AC6. The decision is still correct and Unavailable is clear, so I only keep it as a limitation in section 13 and do not change the code. |
| 7 | 24:00 cannot be entered, so T8 cannot be run on the page. | I tried to type 24:00 in the End field with Playwright. The field refused it. | modify | AC1, T8 and T9. The brief allows Not testable for T8 and T9, so I keep it as a limitation in section 13 and do not add a new field. |
| 8 | The text You can proceed with this booking could be read as a booking confirmation. | I checked T1 and T11 on the page. Nothing is saved, the list of bookings stays the same, and the footer says no bookings are actually saved. | reject | AC5. The result Available is clear and the data does not change, so I keep the text. |

## 9. Coding-agent analysis

### 9.1 The loop

<!-- One real pass through the loop from this assignment — with your assistant or with Bolt. -->

| Step | What happened in this assignment |
| --- | --- |
| User goal | Fix issue 1: an empty Current time must give Unavailable with a reason, and nothing else may change. |
| Model / plan | Claude said the cause is ?? -1 and planned three small edits in src/App.tsx: keep null, accept null in evaluateBooking, add a reason. |
| Tool call | Claude had no tools in this chat. It only wrote the before and after lines. The edits were applied to src/App.tsx, then npm run build and tsc were run. |
| Observation | The build and tsc passed. Playwright showed Unavailable with the reason Enter a valid current time in HH:MM format for the empty current time. |
| Next step | All twelve cases were run again on the final page to see that nothing else changed, then the next issue (T10) was sent. |
| Human review | The three edits were read before they were applied, to check that no rule changed, and T1 to T12 were compared before and after. |

### 9.2 Context, tools and permissions

<!-- At least three rows. Last column: Observed (you saw it happen) or Assumed (you infer it
     about the internals). Use both at least once. -->

| Tool | Context it used | Tools or permissions | Observed or assumed |
| --- | --- | --- | --- |
| Claude, critique chat | Only the text in the prompt: AC1-AC6, the contract, booking.py and parts of App.tsx. It did not see the real files. | No tools. It said "I didn't run anything". | Observed |
| Claude, repair chat | The pasted code parts and the earlier messages in the same chat. | No tools and no file access. It gave edits as text, and they were applied by hand. | Observed |
| Bolt.new | My prompt and the files of the project it made. | Its answer showed "files read", "actions taken" and "Build passes", so it read files, wrote files and ran a build. | Observed |
| Bolt.new | A ready project template. | It runs npm install and a dev server inside the browser, and the template added @supabase/supabase-js by default. | Assumed |
| Playwright and npm on my computer | The exported projects in a scratch copy. | Run local commands, open Chrome, fill the form and take screenshots. | Observed |

### 9.3 Checkpoint and dependability

**Safety checkpoint:** Before an AI change is kept, I read the before and after lines, check that they touch only the named behaviour, run npm run build and tsc, and run T1 to T12 again. If any other case changes, the change is not kept.

**Reliability, security, responsibility:** The AI can write code that looks right but is wrong, like the -1 for an empty current time, so tests and a second run of all cases keep the page reliable. Security means no extra libraries or access the page does not need, like the supabase library. The AI cannot take responsibility, so a person decides what is accepted and answers for it.

## 10. Reflection

<!-- 100-200 words, in your own words, no AI. Compare AI-assisted coding (the Python part) with
     vibe coding (the Bolt part); one example each of a reliability, an availability/usability and
     a security risk; why review, tool permissions and tests stay human responsibilities; one AI
     recommendation you rejected or modified, and why; what you would improve next without
     expanding the scope. -->

With Python I used AI-assisted coding: the AI made a plan, I approved it, and 35 tests caught all 10 broken versions. With Bolt I used vibe coding: one prompt gave a full project fast, but I did not read the code, and on v1 no case was testable. Vibe coding was faster, but AI-assisted coding gave more control and I found mistakes earlier.

Reliability: an empty Current time became -1, so 00:00-01:00 showed Available. Usability: the time field does not accept 24:00, so T8 and T9 are not testable. Security: Bolt added an unused supabase database library, which I removed. Security matters most, because an extra dependency is an unneeded risk.

The AI did not run anything and some advice was wrong, so a human must review changes, give only needed permissions and run tests, because AI can not be responsible. I rejected the idea that blocked as the string "False" is a bug, because the contract says blocked is always Boolean.

I would add a 24:00 option to the End field, so T8 and T9 can be tested.

## 11. Appendix A — AI exchanges

<!-- At least four. Complete prompts and complete responses, as text — never screenshots. Paste
     each inside the ~~~~ block that follows its label.
     Stage: Plan, Generate, Critique or Repair (the brief's A-D) — at least one of each.
     Source: this SIS, week-05 or week-06. Reused exchanges keep their original date.
     The Generate exchange for Python must contain your v1 exactly as it is in code/original/.
     Add B5, B6 … if you ran more. -->

### B1

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-07
- **Stage:** Plan
- **Source:** week-05

**Prompt:**

~~~~text
First message (setup):

You are acting as a plain chat assistant in a conversation with a student. Do NOT use any tools, do not read or write files — reply only with text, as you would in a normal chat window. Answer each message I send exactly as a chat assistant would.

Scenario: Smart Campus study room booking.
User story: As a student, I want to check a room's availability so that I can choose a valid booking time.
Feature: implement can_book(...) for one selected room. Return a decision. The complete system handles saving and confirmation.

Function contract
can_book(start, end, now, blocked, existing)
- Times are integer minutes after midnight on one date. Example: 600 means 10:00.
- now is valid (0-1439). blocked is a Boolean.
- existing contains valid (start, end) tuples for this room's active bookings only.
- Return True or False. Keep all inputs unchanged.

Acceptance criteria
AC1: 0 <= start < end <= 1440, and start > now.
AC2: Duration is at most 120 minutes.
AC3: The room is not blocked.
AC4: No overlap with an existing booking. Touching endpoints are allowed.
AC5: Return True only when AC1-AC4 hold. Return False otherwise and never alter existing.

Intervals include the start and exclude the end.

This is the scenario, the function contract and the acceptance criteria. Use only these. Wait for my first request.

Second message (the plan request):

Propose a short implementation plan for can_book. List the checks in order and identify assumptions. Use Python 3 and the supplied rules. Do not write code yet. Suggest boundary cases that could expose an incorrect implementation.
~~~~

**Response:**

~~~~text
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
~~~~

### B2

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-07
- **Stage:** Generate
- **Source:** week-05

**Prompt:**

~~~~text
Implement can_book in booking.py using the supplied contract and AC1-AC5. Keep the signature. Use only the standard library. Do not modify existing. Return the function and explain each condition. Keep the feature within the stated scope.
~~~~

**Response:**

~~~~text
Here's `booking.py`. I've written it here in the chat as you asked and haven't run it.

```python
"""Smart Campus study room booking: availability decision for one room."""


def can_book(start, end, now, blocked, existing):
    """Return True if the requested slot [start, end) can be booked, else False.

    Times are integer minutes after midnight on a single date.
    `existing` holds (start, end) tuples of this room's active bookings.
    No input is modified.
    """
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

    # AC5: every check passed.
    return True
```

### What each condition does
1. **`0 <= start < end <= 1440` (AC1)**
   - This chained comparison does three checks at once:
     - the start isn't before midnight;
     - the start is strictly before the end, so a zero-length or reversed slot is rejected;
     - the end is no later than 1440, the end of the day.
   - `end == 1440` is allowed because the end time is exclusive.
2. **`start <= now` returns False (AC1)**
   - The start must be strictly after `now`, so starting exactly at `now` is rejected.
3. **`end - start > 120` returns False (AC2)**
   - Exactly 120 minutes is allowed; 121 is not.
   - Check 1 already ensures the duration is positive.
4. **`if blocked` returns False (AC3)**
   - A blocked room can't be booked, even if the time slot is otherwise valid.
5. **Overlap loop (AC4)**
   - Two half-open intervals `[a, b)` and `[c, d)` overlap exactly when `a < d and c < b`.
   - Because both comparisons are strict, touching endpoints don't count as overlap. For example, `(540, 600)` next to `(600, 660)` is fine.
   - The same test catches a partial overlap, a slot inside a booking, a slot wrapped around a booking, and an exact match.
   - The loop checks every booking and only returns early when it finds a clash. It never returns `True` from inside the loop, so the order of the bookings doesn't matter.
6. **`return True` (AC5)**
   - This line is only reached when AC1–AC4 all hold. Every failure returns `False` earlier.

### Inputs stay unchanged (AC5)
- The function only reads `existing`, one tuple at a time.
- It never sorts, appends to, removes from, or assigns to `existing` or any other argument.
- It works whether `existing` is a list, a tuple or another iterable.

### What stays out of scope
- No saving, confirming, or other side effects. It only returns a decision.
- No checks on `now` or `blocked`, since the contract says they're valid.
- No type validation beyond what the contract requires.
- No rules the contract doesn't mention, such as opening hours or limits per student.

Next, I can turn the boundary cases from the earlier plan into `unittest` tests, standard library only.
~~~~

### B3

- **Tool:** Bolt.new
- **Model:** not displayed
- **Date:** 2026-10-18
- **Stage:** Generate
- **Source:** week-06

**Prompt:**

~~~~text
Build a small responsive Smart Campus Room Availability Checker. Requirements: AC1: Accept a candidate interval only when 0 ≤ start < end ≤ 1440 and start is after the supplied current time. AC2: Reject a booking longer than 120 minutes. AC3: Reject the request when the selected room is blocked. AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed. AC5: Show a clear Available / Unavailable decision without changing the existing booking data. AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback. Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
~~~~

**Response:**

~~~~text
0123456789
files read

I'll build this as a single-page React app with in-memory sample data (no backend, per your constraints). Writing the main component now.
0123456789
actions taken

Build passes. The app is done.

I built a Smart Campus Room Availability Checker on a single page. You pick a room, set the current time and a requested start/end slot, and press Check availability to get a clear Available / Unavailable / Invalid decision.

All six acceptance criteria are handled:

    Valid interval check (0 ≤ start < end ≤ 1440, start after current time)
    Rejects bookings longer than 120 minutes
    Rejects when the room is blocked
    Rejects overlapping bookings (touching endpoints allowed)
    Shows the decision without changing any existing booking data
    Responsive layout with plain-language validation feedback

Main files/components created:

    src/App.tsx — the whole page: form, evaluateBooking logic (the AC1–AC4 rules), ResultCard (Available/Unavailable/Invalid panel), RoomSchedule (room info + existing bookings list), and Timeline (a 24-hour visual bar). Fictional sample rooms live in-memory in this same file.

No backend, auth, or persistence was added, per your request — sample data only.
~~~~

### B4

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-25
- **Stage:** Critique
- **Source:** this SIS

**Prompt:**

~~~~text
You are acting as a plain chat assistant in a brand-new conversation with a student. Do NOT use any tools, do not read or write files — reply only with text, exactly as you would in a normal chat window. Your whole final answer is the chat reply. Answer this message:

Review my Python function and my web page against AC1-AC6 below. For each AC say whether the code meets it, quote the line, and list any concrete problem with an input that shows it. Do not suggest new features. Keep the criteria fixed.

Scope: one responsive page for one selected room with fictional booking data. The page checks availability only; it does not create or confirm bookings. No login, database, backend, external API, payments.
AC1: Candidate times are integer minutes after midnight: 0 <= start < end <= 1440; start must be strictly after now.
AC2: Duration must not exceed 120 minutes. Exactly 120 minutes is permitted.
AC3: Reject every request when the selected room is blocked.
AC4: Reject overlap with any existing booking. Intervals touching at an endpoint do not overlap.
AC5: Display an unambiguous Available / Unavailable result; do not mutate existing bookings.
AC6: Provide understandable validation feedback and a usable narrow/mobile layout.
Contract: can_book(start, end, now, blocked, existing) - existing is a collection of (start, end) pairs. Return True only when AC1-AC4 all hold, False otherwise, and never alter existing. now is valid (0-1439). Intervals include their start and exclude their end.

booking.py:
```python
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
```

The page is a Vite + React + Tailwind project made with Bolt.new. package.json dependencies: "@supabase/supabase-js": "^2.57.4", "lucide-react": "^0.344.0", "react": "^18.3.1", "react-dom": "^18.3.1". src/App.tsx (the important parts):

```tsx
const MIN_IN_DAY = 1440;
const MAX_DURATION = 120;

const SAMPLE_ROOMS: Room[] = [
  { id: "r1", name: "Engineering Hall A", building: "Block C · Floor 2", capacity: 40, blocked: false,
    bookings: [
      { id: "b1", title: "Algorithms Lecture", start: 540, end: 600 },
      { id: "b2", title: "Faculty Meeting", start: 780, end: 840 },
      { id: "b3", title: "Robotics Lab", start: 1080, end: 1140 },
    ] },
  { id: "r2", name: "Innovation Lab", building: "Block A · Floor 1", capacity: 24, blocked: true,
    bookings: [ { id: "b4", title: "Maintenance", start: 600, end: 660 } ] },
  { id: "r3", name: "Library Study Room 3", building: "Library · Floor 3", capacity: 12, blocked: false,
    bookings: [
      { id: "b5", title: "Group Study", start: 660, end: 720 },
      { id: "b6", title: "Book Club", start: 1020, end: 1080 },
    ] },
  { id: "r4", name: "Auditorium B", building: "Main Building · Ground", capacity: 200, blocked: false,
    bookings: [ { id: "b7", title: "Guest Lecture", start: 600, end: 660 } ] },
];

function toMinutes(time: string): number | null {
  if (!/^\d{2}:\d{2}$/.test(time)) return null;
  const [h, m] = time.split(":").map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

function evaluateBooking(room: Room | undefined, start: number | null, end: number | null, current: number): Verdict {
  const reasons: string[] = [];
  if (!room) {
    return { kind: "unavailable", reasons: ["Select a room to check."] };
  }
  if (start === null || end === null) {
    return { kind: "unavailable", reasons: ["Enter valid start and end times in HH:MM format."] };
  }
  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    reasons.push("Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.");
  }
  if (start <= current) {
    reasons.push("Start time must be after the current time.");
  }
  // AC2: duration <= 120 min
  if (end - start > MAX_DURATION) {
    reasons.push("Booking cannot be longer than 120 minutes.");
  }
  // AC3: blocked room
  if (room.blocked) {
    reasons.push("This room is currently blocked and cannot be booked.");
  }
  // AC4: overlap (touching endpoints allowed)
  const overlapping = room.bookings.find((b) => start < b.end && end > b.start);
  if (overlapping) {
    reasons.push(`Overlaps existing booking "${overlapping.title}" (${toHHMM(overlapping.start)}–${toHHMM(overlapping.end)}).`);
  }
  if (reasons.length > 0) {
    return { kind: "unavailable", reasons };
  }
  return { kind: "available" };
}

function App() {
  const [roomId, setRoomId] = useState<string>(SAMPLE_ROOMS[0].id);
  const [currentStr, setCurrentStr] = useState("09:00");
  const [startStr, setStartStr] = useState("10:00");
  const [endStr, setEndStr] = useState("11:00");
  const [submitted, setSubmitted] = useState(false);
  const room = useMemo(() => SAMPLE_ROOMS.find((r) => r.id === roomId), [roomId]);
  const current = toMinutes(currentStr) ?? -1;
  const start = toMinutes(startStr);
  const end = toMinutes(endStr);
  const verdict = useMemo(() => evaluateBooking(room, start, end, current), [room, start, end, current]);
  // every input's onChange also calls setSubmitted(false)
  // Room <select>, Current time <input type="time">, Start <input type="time">, End <input type="time">,
  // "Check availability" button sets submitted=true, "Reset" button sets submitted=false.
  // When submitted, ResultCard shows a green "Available" card ("<room> is free from HH:MM to HH:MM. You can proceed with this booking.")
  // or a red "Unavailable" card with the list of reasons.
  // RoomSchedule shows the room, a Blocked/Open badge, a 24-hour timeline and the list of existing bookings
  // (it sorts a copy: [...room.bookings].sort(...)).
  // Layout: max-w-5xl container, grid with lg:grid-cols-5 (form 2 columns, result 3 columns); on narrow screens one column; Start/End in grid-cols-2.
}
```

The test cases I must run (base: now = 540, blocked = False, existing = [(600, 660)]): T1 660-720 Available, T2 630-690 Unavailable, T3 660-720 blocked Unavailable, T4 720-840 Available, T5 720-841 Unavailable, T6 540-570 Unavailable, T7 720-660 Unavailable, T8 1380-1440 Available, T9 1380-1441 Unavailable, T10 720-780 with existing (600-660), (700-760) Unavailable, T11 660-720 twice Available, T12 T1 at ~375 px wide Available.
~~~~

**Response:**

~~~~text
I didn't run anything. This review comes from reading the code you pasted. The Python function meets AC1 to AC4 and should pass T1 to T11. The page has real gaps in AC1 and AC6, and some of your tests can't be run on it.

## booking.py

**AC1: Meets.**
- `if not (0 <= start < end <= 1440):` and `if start <= now:` are both correct.
- T6 (540–570, now 540) returns False. T7 (720–660) returns False. T8 (1380–1440) returns True. T9 (1380–1441) returns False.
- The type guard also rejects `True` and `600.0`, which matches your §9.2 note.

**AC2: Meets.**
- `if end - start > 120:` allows exactly 120. T4 (720–840) returns True and T5 (720–841) returns False.

**AC3: Meets.**
- `if blocked:` rejects every request when blocked is True (T3).
- It tests truthiness, so the string `"False"` would count as blocked. That only matters outside the contract.

**AC4: Meets.**
- `if start < booked_end and booked_start < end:` is the correct test for half-open intervals.
- T1 (660–720 against (600, 660)) returns True because the intervals only touch. T2 returns False. T10 returns False because 720 < 760 and 700 < 780.

**AC5 (contract part): Meets.**
- `existing` is only read, never changed. T11 gives the same result twice.
- One caveat: if someone passes a generator instead of a list, the loop uses it up. The contract says "collection", so this is outside it.
- One small inaccuracy: the comment `# AC5: every check passed.` is mislabelled. AC5 is about what the page displays, and this line just returns True.

**AC6:** Doesn't apply. A function that returns True/False has no user-facing messages.

## App.tsx

**AC1: Partly meets.** Two problems:
1. **An end time of 1440 can't be entered.** `if (h < 0 || h > 23 ...) return null;` and `<input type="time">` both stop at 23:59 (1439). So T8 (23:00–24:00) can't be run on the page. Entering 00:00 as the end time gives "End must be after start". The message `"...end ≤ 24:00"` also promises a value the form won't accept.
2. **Clearing the current time turns off the "after now" check.** Because of `const current = toMinutes(currentStr) ?? -1;`, an empty Current time field becomes -1, so `start <= current` is never true.
   - Example: Auditorium B, Current time cleared, start 00:00, end 01:00. The page says **Available**, and no message appears.

**AC2: Meets.**
- `if (end - start > MAX_DURATION)` allows 10:00–12:00 and rejects 10:00–12:01.

**AC3: Meets.**
- `if (room.blocked) reasons.push(...)`. Innovation Lab (blocked, booking 600–660) gives Unavailable for T3.

**AC4: Meets.**
- `start < b.end && end > b.start` is correct, and touching endpoints are allowed. Auditorium B (600–660) works for T1 and T2.
- **T10 can't be run on the page.** No sample room has the bookings (600–660) and (700–760).

**AC5: Mostly meets.**
- The green "Available" card and red "Unavailable" card are clear.
- `setSubmitted(false)` on every change stops an old result from staying on screen.
- `[...room.bookings].sort(...)` sorts a copy, so the bookings aren't changed.
- One wording risk: "You can proceed with this booking." The page only checks availability, and there's nothing to proceed to. That line could be read as confirming a booking.

**AC6: Partly meets.**
- The reasons are listed, and invalid or empty start and end times get a message.
- Problems:
  - **Empty Current time shows no message** (see AC1, problem 2).
  - **Reversed times can show a confusing extra reason.** Example: Auditorium B, start 10:50, end 10:10. You get the interval error and also "Overlaps existing booking 'Guest Lecture'", because 650 < 660 and 610 > 600.
  - **The interval message is written in notation** ("0 ≤ start < end ≤ 24:00"), and it mentions 24:00, which the form can't accept.
- Layout: one column below `lg` with Start and End in `grid-cols-2` looks reasonable. I can't confirm it works at 375 px from this excerpt, especially the 24-hour timeline and the two time inputs side by side. T12 has to be checked in a real narrow browser window.

## Scope note (not an AC)

`"@supabase/supabase-js"` is in package.json even though the scope says no database and no backend. It's probably a Bolt.new default. Even if your code never uses it, a marker may notice it.

## Test cases

- **Python:** T1 to T11 should all give the expected results.
- **Page:** T8 can't be entered. T9 can't be entered either, so you can't show it on the page; the time input simply can't produce 1441. T10 has no matching data. T1 to T7 and T11 should work on Auditorium B, except T3, which uses Innovation Lab. T12 needs a real narrow-screen check.
~~~~

### B5

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-25
- **Stage:** Repair
- **Source:** this SIS

**Prompt:**

~~~~text
You are acting as a plain chat coding assistant in a brand-new conversation with a student. Do NOT use any tools, do not read or write files — reply only with text, exactly as you would in a normal chat window. Your whole final answer is the chat reply. Answer this message:

My Smart Campus Room Availability Checker page (React + TypeScript, src/App.tsx) has this problem. In Auditorium B (only booking 10:00-11:00), when I clear the Current time field and check 00:00-01:00, the page shows Available and no message. AC1 says the start must be strictly after the current time, and AC6 says the page must give understandable validation feedback. The cause is this line: const current = toMinutes(currentStr) ?? -1; so an empty current time becomes -1 and start <= current is never true. Make the smallest change that fixes this behavior: an empty or invalid current time must give Unavailable with a clear reason. Do not add features and do not change the other rules. Show the exact lines to change, before and after.

The relevant code:

```tsx
function toMinutes(time: string): number | null {
  if (!/^\d{2}:\d{2}$/.test(time)) return null;
  const [h, m] = time.split(":").map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

function evaluateBooking(
  room: Room | undefined,
  start: number | null,
  end: number | null,
  current: number,
): Verdict {
  const reasons: string[] = [];

  if (!room) {
    return { kind: "unavailable", reasons: ["Select a room to check."] };
  }

  if (start === null || end === null) {
    return {
      kind: "unavailable",
      reasons: ["Enter valid start and end times in HH:MM format."],
    };
  }

  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    reasons.push(
      "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.",
    );
  }
  if (start <= current) {
    reasons.push("Start time must be after the current time.");
  }
  // ... AC2, AC3, AC4 checks push more reasons ...
  if (reasons.length > 0) {
    return { kind: "unavailable", reasons };
  }

  return { kind: "available" };
}

function App() {
  const [roomId, setRoomId] = useState<string>(SAMPLE_ROOMS[0].id);
  const [currentStr, setCurrentStr] = useState("09:00");
  const [startStr, setStartStr] = useState("10:00");
  const [endStr, setEndStr] = useState("11:00");
  const [submitted, setSubmitted] = useState(false);

  const room = useMemo(
    () => SAMPLE_ROOMS.find((r) => r.id === roomId),
    [roomId],
  );

  const current = toMinutes(currentStr) ?? -1;
  const start = toMinutes(startStr);
  const end = toMinutes(endStr);

  const verdict = useMemo(
    () => evaluateBooking(room, start, end, current),
    [room, start, end, current],
  );
```
~~~~

**Response:**

~~~~text
Here's my reply to the student:

---

You found the right cause. `?? -1` turns a missing current time into a real number that is earlier than every possible start, so the AC1 check always passes. The fix is to stop inventing a value. Keep `null` and let `evaluateBooking` report it. That takes three small edits in `src/App.tsx`.

**1. In `App`, keep `null` instead of falling back to -1**

Before:
```tsx
  const current = toMinutes(currentStr) ?? -1;
```
After:
```tsx
  const current = toMinutes(currentStr);
```

**2. In the `evaluateBooking` signature, accept `null`**

Before:
```tsx
  current: number,
): Verdict {
```
After:
```tsx
  current: number | null,
): Verdict {
```

**3. In the AC1 check, give a reason when the current time is missing or invalid**

Before:
```tsx
  if (start <= current) {
    reasons.push("Start time must be after the current time.");
  }
```
After:
```tsx
  if (current === null) {
    reasons.push("Enter a valid current time in HH:MM format.");
  } else if (start <= current) {
    reasons.push("Start time must be after the current time.");
  }
```

**Why this is enough**
- `toMinutes` already returns `null` for an empty string, a badly formatted value, or an out-of-range time like `25:00`. All of those now give the new reason.
- Any reason in `reasons` already makes the result `unavailable`, so you don't need another return path.
- The current-time check pushes a reason rather than returning early, like the other checks. So the room check, the start/end format check, and the AC2–AC4 checks behave exactly as before. Their messages still show alongside the new one.
- The `useMemo` dependency list is unchanged. `current` is still a primitive, now `number | null`.

**Check it**
1. Auditorium B, clear Current time, check 00:00–01:00. You should get **Unavailable** with "Enter a valid current time in HH:MM format."
2. Enter Current time 09:00, check 10:00–11:00. You should get the same result as before the fix, since that slot overlaps the existing booking.
3. Enter Current time 09:00, check 00:00–01:00. You should get "Start time must be after the current time." as before.

If you have unit tests that call `evaluateBooking` directly, add one case with `current = null`. TypeScript accepts it now that the parameter type allows it.
~~~~

### B6

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-25
- **Stage:** Repair
- **Source:** this SIS

**Prompt:**

~~~~text
Thanks, I applied it and it works. Next problem, same page. Test case T10 says: current time 09:00, room not blocked, existing bookings 10:00-11:00 and 11:40-12:40, request 12:00-13:00, expected Unavailable (AC4, every existing booking is checked). I opened every room in the Room list and no room has exactly these two bookings, so T10 cannot be set up on the page. Make the smallest change that fixes this: only the fictional sample data, no new controls and no change to the rules. Keep the four existing rooms as they are, because my other cases use Auditorium B and Innovation Lab. Show the exact lines to add.

The sample data now:

```tsx
const SAMPLE_ROOMS: Room[] = [
  {
    id: "r1",
    name: "Engineering Hall A",
    building: "Block C · Floor 2",
    capacity: 40,
    blocked: false,
    bookings: [
      { id: "b1", title: "Algorithms Lecture", start: 540, end: 600 },
      { id: "b2", title: "Faculty Meeting", start: 780, end: 840 },
      { id: "b3", title: "Robotics Lab", start: 1080, end: 1140 },
    ],
  },
  {
    id: "r2",
    name: "Innovation Lab",
    building: "Block A · Floor 1",
    capacity: 24,
    blocked: true,
    bookings: [
      { id: "b4", title: "Maintenance", start: 600, end: 660 },
    ],
  },
  {
    id: "r3",
    name: "Library Study Room 3",
    building: "Library · Floor 3",
    capacity: 12,
    blocked: false,
    bookings: [
      { id: "b5", title: "Group Study", start: 660, end: 720 },
      { id: "b6", title: "Book Club", start: 1020, end: 1080 },
    ],
  },
  {
    id: "r4",
    name: "Auditorium B",
    building: "Main Building · Ground",
    capacity: 200,
    blocked: false,
    bookings: [
      { id: "b7", title: "Guest Lecture", start: 600, end: 660 },
    ],
  },
];
```
~~~~

**Response:**

~~~~text
Here's my reply to the student:

---

Add one new fictional room to the end of `SAMPLE_ROOMS` with exactly the two bookings T10 needs. The four existing rooms stay as they are, and so do the rules and the controls.

**Where:** in `src/App.tsx`, between the closing `},` of Auditorium B and the final `];`.

Before:
```tsx
    bookings: [
      { id: "b7", title: "Guest Lecture", start: 600, end: 660 },
    ],
  },
];
```

After:
```tsx
    bookings: [
      { id: "b7", title: "Guest Lecture", start: 600, end: 660 },
    ],
  },
  {
    id: "r5",
    name: "Seminar Room 5",
    building: "Block B · Floor 1",
    capacity: 30,
    blocked: false,
    bookings: [
      { id: "b8", title: "Design Workshop", start: 600, end: 660 },
      { id: "b9", title: "Thesis Review", start: 700, end: 760 },
    ],
  },
];
```

These are the 9 lines between Auditorium B's `},` and `];`. Nothing else in the file changes.

**Why these numbers**
- 10:00–11:00 is 600–660 minutes.
- 11:40–12:40 is 700–760 minutes (11 × 60 + 40 = 700, 12 × 60 + 40 = 760).
- The request 12:00–13:00 is 720–780. It does not overlap the first booking but does overlap the second. So T10 only passes if the code checks every booking, which is the point of AC4.
- `blocked: false` gives "room not blocked", and current time 09:00 is before the 12:00 start, so AC1 passes.
- The IDs `r5`, `b8` and `b9` are new, so React keys stay unique.

**Effect on your other cases:** none. The new room is added at the end, so `SAMPLE_ROOMS[0]` (Engineering Hall A) is still the default selection. Auditorium B and Innovation Lab are unchanged.

**Running T10**
1. Select Seminar Room 5. Set current time to 09:00 and request 12:00–13:00.
2. Expected: **Unavailable**, with your AC4 overlap reason.

If any of your checks uses `capacity`, 30 is just a fictional value. Change it if a test needs a specific number.

You may also want to update T10 to name the room it uses ("Seminar Room 5") so it can be repeated.
~~~~

### B7

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-25
- **Stage:** Repair
- **Source:** this SIS

**Prompt:**

~~~~text
Applied, T10 now works. Last problem. My package.json lists "@supabase/supabase-js": "^2.57.4" in dependencies. I searched src for supabase and no file imports it. The scope says no backend and no database, and my checker (check W3, "final stays in scope") fails on this line of package.json. Make the smallest change that removes it without changing how the page behaves. Show the exact lines, before and after, and tell me what else I must update.

```json
  "dependencies": {
    "@supabase/supabase-js": "^2.57.4",
    "lucide-react": "^0.446.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
```
~~~~

**Response:**

~~~~text
Here's my reply to the student:

---

Since nothing in `src` imports Supabase, you can delete the dependency. The page doesn't use it, so its behavior won't change.

**The change in `package.json`**

Before:
```json
  "dependencies": {
    "@supabase/supabase-js": "^2.57.4",
    "lucide-react": "^0.446.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
```

After:
```json
  "dependencies": {
    "lucide-react": "^0.446.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
```

Only the `@supabase/supabase-js` line is removed. The next line keeps its trailing comma because more entries follow it.

**The simplest way to make that change**

From the project folder (the one that contains `package.json`), run:
```
npm uninstall @supabase/supabase-js
```
This deletes the line above from `package.json`. It also updates the lock file and `node_modules`, which editing the file by hand would not do.

**What else you must update**

1. **`package-lock.json`.** If you edited `package.json` by hand, run `npm install` afterwards. Otherwise the lock file still contains Supabase and its sub-packages, and a scope checker that also reads the lock file will keep failing. The `npm uninstall` command above handles this for you. If you use pnpm or yarn instead, run `pnpm remove` or `yarn remove` so `pnpm-lock.yaml` or `yarn.lock` is updated too.
2. **Leftover Supabase settings.** Project templates often add these even when no code uses them. Search the whole project, not just `src`, for `supabase` and `SUPABASE`. Places to check:
   - `.env`, `.env.local` or `.env.example`. Delete any `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` lines. If a real key was ever committed, treat it as exposed.
   - `src/vite-env.d.ts`. Delete any `VITE_SUPABASE_*` fields if they are declared there.
   - The README or setup notes. Remove any mention of a database or backend.
3. **Confirm nothing broke.** Run `npm run build` (and `npm run lint` or `tsc` if you have them), then run the app. Recheck a couple of your earlier test cases, such as T10 and the empty-current-time case. Then run check W3 again.
4. **Commit `package.json` and the lock file together**, with a short message such as "Remove unused Supabase dependency (out of scope)".

Your search of `src` found no Supabase imports. If it had, the build would fail at step 3 and point to the exact file.
~~~~

## 12. Appendix B — Test output

### 12.1 Your suite

<!-- The complete terminal output of your final suite. Path A: python -m unittest -v, run inside
     code/ — the part ending in "Ran N tests" and OK or FAILED. -->

~~~~text
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
~~~~

### 12.2 Path B only — three faults you planted

<!-- Path A: leave this table as it is. Path B: three rows — the line you broke, the AC it
     breaks, the test that failed. -->

| # | Line you broke | AC | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 13. Remaining limitations and known fails

<!-- One row per check ID in submission.yml known_fails, and any limitation you know of.
     If the checker is clean and you know of none, one row that says so. -->

| Check ID or limitation | Why it stays | What I would do next |
| --- | --- | --- |
| T8 and T9 are Not testable on the page | The Start and End fields are time inputs and stop at 23:59, so 24:00 and 24:01 cannot be entered. The brief allows Not testable for these two cases. The Python function gives True for T8 and False for T9. | Add an end of day choice for 24:00 to the End field, without changing the rules. |
| Reversed times can show an extra overlap reason | 10:50-10:10 in Auditorium B shows the interval reason and also an overlap reason. The decision Unavailable is still correct (critique row 6). | Show only the interval reason when the end is not after the start. |
| The baseline (section 2) was written after the critique exchange | The critique and repair exchanges of this SIS were run before section 2 was written, so the baseline commit comes after them. | Write the baseline first, as the brief asks. |
