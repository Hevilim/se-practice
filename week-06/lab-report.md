# Week 06 — Lab report

**Name:** Karim Aliyev
**Group:** Monday 16:00 - 19:00
**Date:** 18.10.2026

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Tool | Bolt.new |
| Exact model (as Bolt shows it, or `not displayed`) | not displayed |
| Bolt project link (or `not shared`, and why) | https://bolt.new/p/72159062 |
| Browser and version | Claude in-app browser (Chromium 152.0.7977.149) on macOS |
| If you could not use Bolt.new: the tool you used instead, and why | n/a - used Bolt.new |

---

## 2. Task 1 — define before generating

**Two predictions, written BEFORE you send the first prompt.** Where do you expect v1 to go wrong?
Fill the first three columns now; fill the last one after Task 3.

| # | What I expect to go wrong | AC it concerns | Was I right? (after Task 3) |
| --- | --- | --- | --- |
| 1 | Bolt will not add a field to supply the current time. It will use the real device clock as "now", so I cannot set now = 09:00 and case T6 (starts now) cannot be tested as written. | AC1 | No. v1 has a Current time field and it starts at 09:00, so I can supply now. |
| 2 | Bolt will not give a way to block the selected room (no blocked room in the sample data and no toggle), so case T3 (blocked room) cannot be set up. | AC3 | Partly. There is one blocked room (Innovation Lab), but it has its own booking 08:00-20:00 and I cannot block the room with the 10:00-11:00 booking, so T3 cannot be set up. |

**The initial prompt exactly as I sent it** — the deck's prompt with AC1–AC6 pasted in place of
`[paste AC1–AC6]`, nothing else changed:

```text
Build a small responsive Smart Campus Room Availability Checker. Requirements: AC1: Accept a candidate interval only when 0 ≤ start < end ≤ 1440 and start is after the supplied current time. AC2: Reject a booking longer than 120 minutes. AC3: Reject the request when the selected room is blocked. AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed. AC5: Show a clear Available / Unavailable decision without changing the existing booking data. AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback. Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
```

---

## 3. Task 2 — prototype v1

v1 export saved in `original/` and screenshot saved as `evidence/v1.png` **before** any cleanup
prompt: yes

**Bolt's list of the files/components it created, pasted unedited:**

```text
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
```

**What v1 does — one line per thing that works, or visibly does not:**

- The page has a Room list with four fictional rooms. One of them, Innovation Lab, is blocked.
- The page has a Current time field. It starts at 09:00, so I can supply the current time.
- Start and End are time fields in HH:MM. They stop at 23:59, so I cannot ask for 24:00.
- The Check availability button shows Available, Unavailable or Invalid input, with reasons.
- No room has only one booking 10:00-11:00, so I cannot build the base setup of the nine cases.
- The blocked room has its own booking 08:00-20:00, and there is no way to block another room.
- When the start is not after now or the end is before the start, the page says Invalid input, not Unavailable.
- A check does not change the list of existing bookings. Nothing is saved.
- package.json has the dependency @supabase/supabase-js, but the code never uses it.

**Repair prompt** (only if the first build did not run — the deck allows one, then the result is
v1). Leave empty if you did not need it:

```text
```

---

## 4. Task 3 — the nine cases

Base for every case unless the row says otherwise: **current time 09:00**, room **not blocked**,
the room's **only booking 10:00–11:00**. The Expected column comes from AC1–AC6 — do not change it.
Write each result exactly as **Available**, **Unavailable** or **Not testable** (the page gives you
no way to set up the case). Save each final run as `evidence/final-T<n>.png`.

| # | Case | What you set up and request | Expected | AC | Result on v1 | Result on final | Final screenshot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 11:00–12:00 | Available | AC4 | Not testable | Available | final-T1.png |
| T2 | Overlap | 10:30–11:30 | Unavailable | AC4 | Not testable | Unavailable | final-T2.png |
| T3 | Blocked | 11:00–12:00, room blocked | Unavailable | AC3 | Not testable | Unavailable | final-T3.png |
| T4 | Exactly 2 hours | 12:00–14:00 | Available | AC2 | Not testable | Available | final-T4.png |
| T5 | Over 2 hours | 12:00–14:01 | Unavailable | AC2 | Not testable | Unavailable | final-T5.png |
| T6 | Starts now | 09:00–09:30 (current time 09:00) | Unavailable | AC1 | Not testable | Unavailable | final-T6.png |
| T7 | Reversed times | 12:00–11:00, and the page says why | Unavailable | AC1, AC6 | Not testable | Unavailable | final-T7.png |
| T8 | Same check twice | T1, then T1 again without reloading | Available | AC5 | Not testable | Available | final-T8.png |
| T9 | Narrow screen | T1 at about 375 px wide | Available | AC6 | Not testable | Available | final-T9.png |

---

## 5. Issue log — cleanup targets

One row per issue you chose to act on (or deliberately not act on). At least **two**: one
functional and one usability or code-quality issue when you have them. If v1 passed every case,
log a justified cleanup that preserves behaviour. Save a screenshot of each as
`evidence/issue-<n>.png`.

| # | Issue | Evidence: steps → expected → observed | Priority | Decision |
| --- | --- | --- | --- | --- |
| 1 | No room has only the booking 10:00-11:00, so the base of the nine cases cannot be set up (T1, T2, T4-T9). | Open the Room list and look at each room. Expected: an open room whose only booking is 10:00-11:00, so I can check 11:00-12:00 next to it (AC4). Observed: Engineering Hall A has 09:00-10:00, 13:00-14:00 and 18:00-19:00, Library Study Room 3 has 11:00-12:00 and 17:00-18:00, Auditorium B has 10:00-12:00. | High | Fix |
| 2 | I cannot block the room with the 10:00-11:00 booking, so T3 cannot be set up. | Look for a way to block a room. Expected: I can check 11:00-12:00 in the blocked room and get Unavailable (AC3). Observed: only Innovation Lab is blocked, it has its own booking 08:00-20:00, and there is no control to block a room. | High | Fix |
| 3 | When AC1 fails, the decision says Invalid input, not Unavailable (T6, T7). | Engineering Hall A, current time 09:00, request 12:00-11:00. Expected: a clear Unavailable decision with the reason (AC5, AC6). Observed: the title is Invalid input and the reason says the end must be after the start. | Medium | Fix |
| 4 | package.json has @supabase/supabase-js, a database library that the page never uses. | Open original/project/package.json and search src for supabase. Expected: no backend or database code (scope). Observed: the dependency is in package.json, line 14, and no file in src imports it. | Low | Defer |

---

## 6. Task 4 — cleanup with focused prompts

One issue per prompt. Paste every prompt **as sent** (every `[bracketed field]` and `AC#` filled
in) and Bolt's answer, unedited.

**Functional fix prompt, as sent, and Bolt's answer:**

```text
In the current prototype, opening the Room list to find an open room whose only booking is 10:00–11:00 produces no such room (every sample room has other bookings or different times), but AC4 requires that I can check 11:00–12:00 against an existing 10:00–11:00 booking, with touching endpoints allowed. Make the smallest change that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you changed and why.

The AC4 logic is already correct (touching endpoints allowed). The issue is sample data: no room has only a 10:00–11:00 booking. Auditorium B has a single booking of 10:00–12:00 — I'll shorten it to 10:00–11:00 so you can check 11:00–12:00 and get Available.
0123456789
actions taken

Build passes.

I changed one line in src/App.tsx: Auditorium B's single booking from 10:00–12:00 (600–720) to 10:00–11:00 (600–660).

Why: the overlap logic (start < b.end && end > b.start) already correctly allows touching endpoints — the real problem was purely sample data. No room had a single booking ending at 11:00 that would let you request 11:00–12:00 and get Available. Now Auditorium B has exactly one booking, 10:00–11:00, so checking 11:00–12:00 (with current time before 11:00) returns Available, exercising AC4's touching-endpoints rule. All other acceptance criteria remain untouched.
```

Functional fix prompt 2, as sent, and Bolt's answer:

```text
In the current prototype, selecting the room with the 10:00–11:00 booking and requesting 11:00–12:00 while that room is blocked produces no way to set the case up (the only blocked room, Innovation Lab, has its own 08:00–20:00 booking, and there is no control to block a room), but AC3 requires an Unavailable decision when the selected room is blocked. Make the smallest change that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you changed and why.

The blocked room (Innovation Lab) currently has a single 08:00–20:00 booking, so any daytime request also overlaps it — you can't isolate the AC3 "blocked" reason. I'll shorten that booking to 10:00–11:00 so requesting 11:00–12:00 against it returns Unavailable only because the room is blocked.
0123456789
actions taken

Build passes.

I changed one line in src/App.tsx: Innovation Lab's booking from 08:00–20:00 (480–1200) to 10:00–11:00 (600–660).

Why: the AC3 logic (rejecting when room.blocked is true) was already correct, but the sample data made the case impossible to isolate. The blocked room's all-day booking meant any daytime request also triggered AC4 overlap, so you couldn't see a clean "blocked" Unavailable decision. Now selecting Innovation Lab and requesting 11:00–12:00 (touching its booking, with current time before 11:00) returns Unavailable with the single reason "This room is currently blocked and cannot be booked." — exercising AC3 cleanly. All other acceptance criteria are preserved.
```

Functional fix prompt 3, as sent, and Bolt's answer:

```text
In the current prototype, setting current time 09:00 and requesting 09:00–09:30, or requesting 12:00–11:00, produces the decision title "Invalid input", but AC5 requires a clear Available / Unavailable decision, with the reason shown (AC6). Make the smallest change that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you changed and why.

The "Invalid input" branch violates AC5 — invalid intervals should still produce an Unavailable decision with reasons. I'll make all failed checks return unavailable and remove the now-dead "invalid" UI branch.
0123456789
actions taken

Build passes.

I changed src/App.tsx in the evaluateBooking function and the ResultCard component.

Why: the old code split failures into "invalid" (bad interval / start ≤ current) and "unavailable" (blocked/overlap/too long), and ResultCard rendered "Invalid input" for the invalid branch. That violated AC5, which requires a clear Available / Unavailable decision — there's no "Invalid" verdict in the spec. Now every failed check returns unavailable with its reason(s) shown (AC6), and ResultCard always shows the Unavailable panel. So 09:00–09:30 with current 09:00 now shows "Unavailable — Start time must be after the current time," and 12:00–11:00 shows "Unavailable — End must be after start." The Available path and all other acceptance criteria are unchanged.
```

**Cleanup prompt, as sent, and Bolt's answer:**

```text
Review only package.json dependencies (@supabase/supabase-js is listed but never imported) for unnecessary duplication, confusing naming, or UI feedback problems. Suggest one small cleanup. Do not add features or redesign the whole application. Implement it only if it preserves AC1–AC6.

Searched
supabase
Open

Confirmed: @supabase/Bolt Database-js is declared in package.json but never imported anywhere in src/. It's dead weight — the app uses in-memory sample data only (per your original "no backend services" constraint). Removing it is a safe cleanup that doesn't touch any acceptance criteria.
0123456789
actions taken
Edited
package.json
Open
Reinstall and build to verify removal is clean
Open

Response interrupted.
```

Add further blocks for further prompts.

**Every change or suggestion Bolt made, judged.** Accepting is a decision; so is rejecting. Cite
the AC (or the scope) that justifies it.

| # | What Bolt changed or suggested | accept / reject | Reason — cite the AC or the scope | Retest: which cases, result |
| --- | --- | --- | --- | --- |
| 1 | Changed the only booking of Auditorium B from 10:00-12:00 to 10:00-11:00 in src/App.tsx. | accept | It changes only the sample data. Now the base of the nine cases can be set up and AC4 can be tested. The check logic is the same. | T1 in Auditorium B: Available. Then all nine: T1, T2, T4, T5, T8 and T9 as expected. T3 Unavailable, but also with an overlap reason. T6 and T7 Invalid input. |
| 2 | Changed the booking of the blocked room Innovation Lab from 08:00-20:00 to 10:00-11:00 in src/App.tsx. | accept | It changes only the sample data. Now T3 can be set up and the only reason is the blocked room (AC3). | T3 in Innovation Lab: Unavailable, the only reason is the blocked room. Then all nine: T1-T5, T8 and T9 as expected. T6 and T7 still Invalid input. |
| 3 | Removed the Invalid input decision in evaluateBooking and ResultCard. Every failed check now shows Unavailable with its reasons. | accept | AC5 asks for a clear Available or Unavailable decision. The reasons are still shown, so AC6 is kept. | T6 and T7: Unavailable with the reason. Then all nine: 9 of 9 as expected. |
| 4 | Said it removed @supabase/supabase-js from package.json. | reject | The answer was interrupted and the download still has the dependency, so the change was not applied. It does not change AC1-AC6, so I defer it. | Opened the downloaded package.json: line 14 still has the dependency. All nine on the download: 9 of 9 as expected. |

---

## 7. Change log — v1 to final

Two to four concrete changes, each one retested.

| # | Issue | Decision | Change (file or component) | Result after retest |
| --- | --- | --- | --- | --- |
| 1 | No room has only the booking 10:00-11:00 | Fix | src/App.tsx, sample data of Auditorium B | T1 Available. T1, T2, T4, T5, T8 and T9 now testable and as expected. |
| 2 | I cannot block the room with the 10:00-11:00 booking | Fix | src/App.tsx, sample data of Innovation Lab | T3 Unavailable, only because the room is blocked. No other case changed. |
| 3 | Invalid input instead of Unavailable | Fix | src/App.tsx, evaluateBooking and ResultCard | T6 and T7 Unavailable with the reason. All nine as expected. |

---

## 8. One generated component, in my own words

Pick one file or component Bolt generated that matters for AC1–AC5 — the one that decides
availability is the best choice. Name its path in backticks, then explain in your own words, without
the assistant, what it does and how it decides. 60 words or more.

**File:** `src/App.tsx`

<!-- Write your explanation below this line -->

The part that decides is the function evaluateBooking in this file. It gets the selected room, the start, the end and the current time. All times are in minutes after midnight. Before this, the function toMinutes changes the HH:MM text from the fields into minutes. If there is no room or a time is empty, evaluateBooking returns Unavailable at once. Then it checks the rules one by one and adds every broken rule to a list of reasons. For AC1, the start must be 0 or more, the end must be 1440 or less, the start must be before the end, and the start must be after the current time. For AC2, the end minus the start must be 120 or less. For AC3, the room must not be blocked. For AC4, no booking may overlap. A booking overlaps when the start is before its end and the end is after its start, so 11:00-12:00 next to 10:00-11:00 is fine. If the list is empty, the answer is Available. If not, the answer is Unavailable with all the reasons. The function only reads the room data and never changes it, so AC5 is kept.

---

## 9. What still fails, and what the criteria do not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| P3 | package.json in prototype/ still has @supabase/supabase-js. Bolt said it removed it, but the answer was interrupted and the download still has it (issue 4). No file in src imports it, the page makes no network calls and saves nothing, so AC1-AC6 are not affected. I decided to defer it. |

### 9.2 The end of the day

AC1 allows `end ≤ 1440` — a booking may end at 24:00. Can a user of your final page ask for
23:00–24:00? How — and if not, why is that acceptable or not? (This is the value you declare in
`submission.yml` under `assumptions.end_of_day`.)

- No. The Start and End fields are time inputs and stop at 23:59. The function toMinutes in src/App.tsx also does not accept 24:00. So the latest request is 23:00-23:59. I think this is acceptable for this prototype, because only the last minute of the day is lost and all nine cases still work. But the page does not fully cover AC1, so I declare not-expressible.

### 9.3 Which "now"?

AC1 says "after the supplied current time". What did **v1** use as the current time, and what did
that mean for testing case T6?

- v1 used the Current time field on the page, and it starts at 09:00. So the current time was supplied, not taken from the clock. The page only uses the clock to show the date. T6 was still Not testable on v1, because no room had only the booking 10:00-11:00. When I tried 09:00-09:30 in another room, v1 said Invalid input, not Unavailable. On the final page T6 gives Unavailable with the reason that the start must be after the current time.

---

## 10. Conclusion (120–180 words)

<!-- Answer all three, in your own words, without the assistant:
     (a) Which of your two predictions in section 2 was right, and what did v1 actually get wrong?
     (b) Which AI suggestion did you reject, or would have been wrong to accept, and why?
     (c) What is the difference between "the prototype looks finished" and "the prototype meets
         AC1-AC6" - shown with one case from section 4?
     Worthless: "Bolt made some mistakes and I fixed them."
     Worth everything: "T8 failed on v1: the Check button also added the booking to the list, so
     checking 11:00-12:00 a second time said Unavailable. AC5 says the check must not change the
     booking data." -->

<!-- Write your conclusion below this line -->

My first prediction was wrong. v1 had a Current time field that started at 09:00, so I could supply the current time. My second prediction was partly right. There was a blocked room, but its booking 08:00-20:00 hid the blocked reason. The real problem of v1 was the sample data. No room had only the booking 10:00-11:00, so all nine cases were Not testable. v1 also said Invalid input instead of Unavailable when the times were wrong. I rejected the supabase cleanup. Bolt said that it edited package.json, but the answer was interrupted and the download still had the dependency. I cannot accept a change that did not happen. v1 looked finished. It had a timeline, colors and clear cards. But it did not meet AC1-AC6. For example, 12:00-11:00 (T7) on v1 showed Invalid input, and AC5 asks for Available or Unavailable. On the final page T7 shows Unavailable and the reason that the end must be after the start.
