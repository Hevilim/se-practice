# Week 07 — Lab report

**Name:** Karim Aliyev
**Group:** Monday 16:00 - 19:00
**Date:** 6.11.2026

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Project I continue (`week-06` = my Week 06 Bolt project, `starter` = the provided starter) | week-06 |
| Bolt project link (or `not shared`, and why) | https://bolt.new/p/72159062 |
| Assistant that generated the tests (tool) | Claude (claude.ai) |
| Exact model (with its version, or `not displayed`) | Claude Opus 5.5 |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | my computer |
| Vitest version (the `RUN  v…` line of a run) | 3.2.7 |
| Test command | npx vitest run |

---

## 2. Task 1 — baseline and the booking function

**Before editing:** where did the booking decision live in the project you started from?

| | |
| --- | --- |
| File and function (or "inside the page component") | src/App.tsx, function evaluateBooking (outside the App component, but in the same file) |
| Its inputs | the room object (with blocked and bookings), start and end in minutes or null, and the current time in minutes |
| What it returned | a verdict object: kind available, or kind unavailable with a list of reasons (messages) |
| How the page used it | App calls it in useMemo with the selected room and the times from the form. ResultCard shows Available, or Unavailable with the reasons. |

**What I changed to extract `canBook`.** Say which file it now lives in, what you moved, and why
the behaviour did not change. Also say which file of the page now calls it. 40 words or more.

<!-- Write below this line -->

canBook now lives in src/booking.ts. I moved the five checks from evaluateBooking into it: the AC1 interval check, start after now, the 120 minute limit, the blocked room and the overlap check. I copied each condition as it was, with the same signs, so the behaviour did not change. evaluateBooking in src/App.tsx imports canBook and calls it for the decision. If canBook returns true, the page shows Available. If it returns false, the page still builds the same reason messages, and the conversion from HH:MM to minutes stays in the page. I opened the page in the browser after the change. Auditorium B with now 09:00 gave the same results as before: 11:00-12:00 and 12:00-14:00 Available, 10:30-11:30, 12:00-14:01 and 09:00-09:30 Unavailable, and the blocked Innovation Lab Unavailable.

---

## 3. Task 2 — the test plan

Default fixture: `now = 540`, `blocked = false`, `bookings = [{ start: 600, end: 660 }]`, fresh
for every test. **The Expected column comes from AC1–AC4, never from the code.** Write the
**reason** for each expected result **before** you send the generation prompt.

| ID | Candidate / changed input | Expected | AC | Reason (in your words) |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | The booking ends at 660 and the request starts at 660. 660 is not inside 600-660, so they only touch. 60 minutes, after now, room open. |
| T02 | 540–570 (starts now) | false | AC1 | The request starts at 540 and now is 540. AC1 needs start after now, and 540 is equal, not after. |
| T03 | 720–720 (zero duration) | false | AC1 | Start 720 and end 720 are equal. AC1 needs start < end, so a request of 0 minutes is not a real interval. |
| T04 | 750–720 (reversed) | false | AC1 | Start 750 is bigger than end 720. AC1 needs start < end, so a reversed interval is not valid. |
| T05 | 1380–1441 (past day end) | false | AC1 | End 1441 is one minute after midnight. AC1 needs end <= 1440, so the request goes past the end of the day. |
| T06 | 720–840 (120 minutes) | true | AC2 | 720 to 840 is exactly 120 minutes. AC2 rejects only longer than 120, so 120 is still allowed. No overlap, after now. |
| T07 | 720–841 (121 minutes) | false | AC2 | 720 to 841 is 121 minutes. This is longer than 120, so AC2 rejects it, even though everything else is fine. |
| T08 | 570–600 (touching before) | true | AC4 | The request ends at 600 and the booking starts at 600. 600 is not inside both, so they only touch. 570 is after now 540. |
| T09 | 630–690 (partial overlap) | false | AC4 | 630-690 and 600-660 share the minutes 630-660. This is an overlap, so AC4 rejects it. |
| T10 | 570–690 (contains booking) | false | AC4 | 570-690 covers the whole booking 600-660, so all 60 booked minutes are shared. AC4 rejects it. |
| T11 | 615–645 (inside booking) | false | AC4 | 615-645 is fully inside 600-660, so every minute of the request is already booked. AC4 rejects it. |
| T12 | 600–660 (identical interval) | false | AC4 | 600-660 is the same interval as the booking, so all minutes are shared. AC4 rejects it. |
| T13 | 660–720, blocked = true | false | AC3 | 660-720 alone would be Available (it only touches the booking), but the room is blocked. AC3 rejects any request in a blocked room. |
| T14 | 630–690, bookings = [] | true | AC4 | 630-690 would overlap 600-660, but here the room has no bookings. Nothing to overlap, 60 minutes, after now, so it is accepted. |
| AC5 | an Available request — the bookings after the call equal the bookings before | true, data unchanged | AC5 | 660-720 is Available. AC5 says the check must not change the booking data, so the array must still be [{600, 660}] after the call. |
| X1 | 1380-1440 (ends exactly at 24:00) | true | AC1 | AC1 allows end <= 1440, so 1440 itself is allowed. 60 minutes, after now, no overlap. This is the other end of the day, T05 only checks 1441. |
| X2 | 660-720, bookings = [{600, 660}, {720, 780}] (touches two bookings) | true | AC4 | The request touches the first booking at 660 and the second at 720. Touching is allowed by AC4, and there is no shared minute with either one. |

X1 and X2 are **your own two cases**: a boundary or a state that T01–T14 do not reach. Fill all
five columns.

---

## 4. Task 3 — the generation prompt and the first suite

**The prompt exactly as I sent it.** Use the deck's prompt with `[our test framework]` replaced by
`Vitest`, followed by the case table from section 3:

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.

Default fixture: now = 540, blocked = false, bookings = [{ start: 600, end: 660 }], fresh for every test.

| ID | Candidate / changed input | Expected | AC | Reason (in your words) |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | The booking ends at 660 and the request starts at 660. 660 is not inside 600-660, so they only touch. 60 minutes, after now, room open. |
| T02 | 540–570 (starts now) | false | AC1 | The request starts at 540 and now is 540. AC1 needs start after now, and 540 is equal, not after. |
| T03 | 720–720 (zero duration) | false | AC1 | Start 720 and end 720 are equal. AC1 needs start < end, so a request of 0 minutes is not a real interval. |
| T04 | 750–720 (reversed) | false | AC1 | Start 750 is bigger than end 720. AC1 needs start < end, so a reversed interval is not valid. |
| T05 | 1380–1441 (past day end) | false | AC1 | End 1441 is one minute after midnight. AC1 needs end <= 1440, so the request goes past the end of the day. |
| T06 | 720–840 (120 minutes) | true | AC2 | 720 to 840 is exactly 120 minutes. AC2 rejects only longer than 120, so 120 is still allowed. No overlap, after now. |
| T07 | 720–841 (121 minutes) | false | AC2 | 720 to 841 is 121 minutes. This is longer than 120, so AC2 rejects it, even though everything else is fine. |
| T08 | 570–600 (touching before) | true | AC4 | The request ends at 600 and the booking starts at 600. 600 is not inside both, so they only touch. 570 is after now 540. |
| T09 | 630–690 (partial overlap) | false | AC4 | 630-690 and 600-660 share the minutes 630-660. This is an overlap, so AC4 rejects it. |
| T10 | 570–690 (contains booking) | false | AC4 | 570-690 covers the whole booking 600-660, so all 60 booked minutes are shared. AC4 rejects it. |
| T11 | 615–645 (inside booking) | false | AC4 | 615-645 is fully inside 600-660, so every minute of the request is already booked. AC4 rejects it. |
| T12 | 600–660 (identical interval) | false | AC4 | 600-660 is the same interval as the booking, so all minutes are shared. AC4 rejects it. |
| T13 | 660–720, blocked = true | false | AC3 | 660-720 alone would be Available (it only touches the booking), but the room is blocked. AC3 rejects any request in a blocked room. |
| T14 | 630–690, bookings = [] | true | AC4 | 630-690 would overlap 600-660, but here the room has no bookings. Nothing to overlap, 60 minutes, after now, so it is accepted. |
| AC5 | an Available request — the bookings after the call equal the bookings before | true, data unchanged | AC5 | 660-720 is Available. AC5 says the check must not change the booking data, so the array must still be [{600, 660}] after the call. |
| X1 | 1380-1440 (ends exactly at 24:00) | true | AC1 | AC1 allows end <= 1440, so 1440 itself is allowed. 60 minutes, after now, no overlap. This is the other end of the day, T05 only checks 1441. |
| X2 | 660-720, bookings = [{600, 660}, {720, 780}] (touches two bookings) | true | AC4 | The request touches the first booking at 660 and the second at 720. Touching is allowed by AC4, and there is no shared minute with either one. |

src/booking.ts (the page imports it with: import { canBook } from "./booking"):

export type BookingInterval = {
  start: number; // minutes from midnight
  end: number;
};

export type CanBookInput = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: BookingInterval[];
};

const MIN_IN_DAY = 1440;
const MAX_DURATION = 120;

export function canBook({ start, end, now, blocked, bookings }: CanBookInput): boolean {
  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    return false;
  }
  if (start <= now) {
    return false;
  }

  // AC2: duration <= 120 min
  if (end - start > MAX_DURATION) {
    return false;
  }

  // AC3: blocked room
  if (blocked) {
    return false;
  }

  // AC4: overlap (touching endpoints allowed)
  const overlapping = bookings.find((b) => start < b.end && end > b.start);
  if (overlapping) {
    return false;
  }

  return true;
}
```

**The assistant's answer: run command, AC mapping and any unclear requirements it flagged,
pasted unedited.** Its test file goes to `suites/first/` and is not pasted here:

```text
I wrote the test suite to `/Users/hevilim/Developer/se-practice/week-07/app/src/booking.test.ts`. As you asked, I did not run it. I also did not commit anything or touch `booking.ts`. The README wants the unedited first suite saved as `week-07/suites/first/booking.test.ts`, so copy the file there yourself, byte for byte.

**About the file**
- It imports the real function with `import { canBook } from './booking'`, the same import `App.tsx` uses. It has no mocks, no `.skip`/`.only` and no `test.each`.
- Time is fixed: `now` is always `540`, and there is no `Date` or `Math.random`.
- Fixtures are fresh. A helper, `request(start, end)`, builds a new input object and a new bookings array (`[{start:600,end:660}]`) for every test. T13, T14 and X2 write their full input inline, so `blocked: true`, `bookings: []` and the two-booking list are visible in the test itself.
- It has 17 tests, one per ID, with the ID and AC in each title (e.g. `'T05 AC1: request ending past the end of the day (1380-1441) is rejected'`). Each test asserts the exact result with `.toBe(true)` or `.toBe(false)`.
- The AC5 test calls 660–720, expects `true`, and then compares `bookings` both to a `structuredClone` taken before the call and to the literal `[{ start: 600, end: 660 }]`.

**Run command** (from `week-07/app`, Vitest is already installed):
```
npx vitest run
```
`npm test` does the same thing (`vitest run`).

**AC mapping**
| AC | Tests |
|---|---|
| AC1 | T02, T03, T04, T05, X1 |
| AC2 | T06, T07 |
| AC3 | T13 |
| AC4 | T01, T08, T09, T10, T11, T12, T14, X2 |
| AC5 | AC5 (bookings unchanged after an Available call). The "clear Available / Unavailable" wording is about the page, so a unit test can't check it. |
| AC6 | Not covered. It's about layout and feedback, which needs the manual UI checks (`evidence/ui-*.png`). |

**Unclear requirements**
1. **Invalid existing booking.** No AC says what happens if a stored booking is reversed, e.g. `{700, 650}`. The overlap test `start < b.end && end > b.start` would ignore it. Your `submission.yml` asks you to check this yourselves, so I left it out.
2. **Non-numbers get accepted.** `NaN` passes every check because each comparison with `NaN` is false, so `canBook` returns `true` for `start = end = NaN`. The page catches empty times as `null` before calling `canBook`, but the function on its own does not. No AC covers this.
3. **No test for `start < 0`.** AC1 says `0 ≤ start` and the code checks it, but no case in the table does. Because of `now = 540`, a negative start would be rejected by the start-after-now rule first, so a test would need a different `now`.
4. **Can the page send 1440?** X1 checks that `end = 1440` is accepted, but a normal HH:MM field can't produce 24:00. Whether a user can ever book up to midnight depends on the page, not on `canBook`.
5. **"Longer than 120"** is read as `duration > 120`, so exactly 120 is allowed (T06). The table and the code agree on this.
6. **Rules are copied in `App.tsx`.** After `canBook` returns `false`, the page re-checks AC1–AC4 itself to build the error messages. If someone changes `booking.ts` later, the messages could stop matching the decision. AC6 mentions feedback, so this is worth a manual check.
7. **Several bookings, or ones before `now`.** Overlapping stored bookings, or bookings that ended before `now`, aren't in the table beyond X2. Rule order doesn't matter for a true/false result, so I added no cases.
```

The first suite was saved to `suites/first/` **before** I changed anything in it: yes

---

## 5. Task 4 — review of the first suite

Review it **before** you run it. Look at the imports, the expected values, isolation, duplicates
and skipped tests. Make one row per decision. At least **two** rows, and each one names the kind of
weakness (the deck's table: *no exception occurred* · *expected = current output* · *only valid
requests* · *mocked booking function*, or your own) and the AC that decides it.

| # | Test or part of the suite | What is weak or wrong | Decision: accept / revise / reject | AC or reason |
| --- | --- | --- | --- | --- |
| 1 | | | accept / revise / reject | |
| 2 | | | accept / revise / reject | |

---

## 6. Task 5 — running, diagnosing, improving

### 6.1 The first run

The **real** terminal output of the first run of the first suite, pasted unedited. Include the
`RUN  v…` line and the `Tests` summary line. A build message or the assistant saying "tests pass"
is not a run.

```text
(paste here)
```

**Each failure, diagnosed** (the deck's table: import/runner error · assertion mismatch · result
changing per run · no tests discovered). Write `none` in the first row if nothing failed.

| Failing test | Observed failure | First check | Test repair or implementation fix? | Action taken |
| --- | --- | --- | --- | --- |
| | | | | |

### 6.2 The improvement prompt

The deck's improvement prompt exactly as sent, followed by the actual output from 6.1. Then
paste the assistant's answer, unedited:

```text
(paste here)
```

### 6.3 The final run

The **real** output of the final suite (`booking.test.*` beside your module), after every
change and after restoring the correct code from section 7. Every test must pass. If a real defect
is still open, leave its test failing and explain it in 9.1.

```text
(paste here)
```

---

## 7. Task 6 — deliberate defects

You need a reviewed, passing suite first. Then introduce **one** defect at a time in your booking
module, leave the tests unchanged, run, record, and **restore** the code. A syntax or import
error does not count as detection.

| Trial | Intentional change | Detected / Survived | Failing test ID(s) | If it survived: why, and what you added |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >= 120 instead of > 120 | Detected / Survived | | |
| M2 | Treat touching endpoints as an overlap | Detected / Survived | | |
| M3 | Remove the blocked-room rejection | Detected / Survived | | |

**The run of each mutant, pasted unedited.** Paste the `Tests` summary line and the failing test
names at least:

```text
(paste here)
```

All three changes reverted, and the full suite run again (section 6.3): yes / no

---

## 8. Task 7 — manual UI checks

Use `now = 09:00` and an existing `10:00–11:00` booking. Do them in the page in a browser. Save a
screenshot of each as `evidence/ui-1.png` … `evidence/ui-5.png`. Take **ui-4 at phone width**
(about 375 px, portrait).

| # | Action | Expected observation | AC | What I observed | Pass / Fail / Not testable |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available, with the fixed sample booking | AC5 | Room Auditorium B (only booking Guest Lecture 10:00-11:00), Current time 09:00, 11:00-12:00, Check. The page shows Available: Auditorium B is free from 11:00 to 12:00. The list still shows only Guest Lecture 10:00-11:00. | Pass |
| U2 | Enable blocked, then check again | Unavailable replaces the earlier result | AC3, AC5 | The page has no switch to block a room. Only Innovation Lab is blocked in the sample data, and it has the same booking 10:00-11:00. I selected it after U1 and pressed Check again. Unavailable with the reason that the room is blocked replaced Available. But this is another room, not the same room after blocking, so the step as written cannot be done. | Not testable |
| U3 | Clear a required input and submit | Understandable validation feedback | AC6 | Auditorium B, 09:00, I cleared Start and pressed Check. The page shows Unavailable with the message Enter valid start and end times in HH:MM format. It is understandable, but it says Unavailable and does not point to the empty field. | Pass |
| U4 | Use a narrow (phone) width | Controls and result remain usable | AC6 | Phone width 375 px, portrait. The form is in one column, then the result card, then the schedule. 11:00-12:00 gives Available. No sideways scroll (page width 375 px), all buttons and fields can be used. | Pass |
| U5 | Repeat the checks on the same data | Existing bookings remain unchanged | AC5 | On Auditorium B I checked 11:00-12:00, then 10:30-11:30, then 11:00-12:00 again. Results: Available, Unavailable (overlaps Guest Lecture), Available. After all checks the list still shows only Guest Lecture 10:00-11:00. | Pass |

---

## 9. Comparison and what still fails

### 9.1 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 Original and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | | |
| Requirements with meaningful tests (AC IDs and gaps) | | |
| Selected mutants detected | | |
| Accepted / revised / rejected tests | | |
| Remaining limitations | | |

### 9.3 What no AC decides

Call your function with `bookings = [{ start: 700, end: 650 }]` (a reversed existing booking)
and a request of 660–720. What does it return? Does any AC say what it should return? (This is
the value you declare in `submission.yml` under `assumptions.invalid_existing_booking`.)

- My canBook returns true. The overlap check is start < b.end and end > b.start. With the booking 700-650, 660 < 650 is false, so it finds no overlap and does not throw. No AC says what to do with an invalid existing booking. AC4 only talks about overlap with a booking, and AC1 only checks the candidate interval. But if the booking really means 650-700, then 660-720 shares 660-700, so true is not safe. With 600-720 the same function returns false, so the answer depends on the request. I think a broken booking should be rejected or reported, not ignored, but this needs a decision from the product owner. I do not test it in my suite, because no AC gives the expected value.

---

## 10. Conclusion (120–180 words)

<!-- Answer all three in your own words, without the assistant:
     (a) Which mistake in the FIRST suite would have let a wrong canBook pass, and how did you find it?
     (b) What does your final green run prove, and what does it NOT prove? Use a mutant or a UI check.
     (c) One testing limitation that remains.
     Worthless: "The AI wrote good tests and they all passed."
     Worth everything: "The first suite expected T06 (exactly 120 minutes) to be rejected. That
     contradicts AC2, and it failed on a correct canBook. If I had changed the code to make it
     pass, M1 would have become the real behaviour." -->

<!-- Write your conclusion below this line -->
