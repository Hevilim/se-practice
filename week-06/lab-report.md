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
| Exact model (as Bolt shows it, or `not displayed`) | |
| Bolt project link (or `not shared`, and why) | |
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
| T1 | Touching | 11:00–12:00 | Available | AC4 | Not testable | Available / Unavailable / Not testable | final-T1.png |
| T2 | Overlap | 10:30–11:30 | Unavailable | AC4 | Not testable | Available / Unavailable / Not testable | final-T2.png |
| T3 | Blocked | 11:00–12:00, room blocked | Unavailable | AC3 | Not testable | Available / Unavailable / Not testable | final-T3.png |
| T4 | Exactly 2 hours | 12:00–14:00 | Available | AC2 | Not testable | Available / Unavailable / Not testable | final-T4.png |
| T5 | Over 2 hours | 12:00–14:01 | Unavailable | AC2 | Not testable | Available / Unavailable / Not testable | final-T5.png |
| T6 | Starts now | 09:00–09:30 (current time 09:00) | Unavailable | AC1 | Not testable | Available / Unavailable / Not testable | final-T6.png |
| T7 | Reversed times | 12:00–11:00, and the page says why | Unavailable | AC1, AC6 | Not testable | Available / Unavailable / Not testable | final-T7.png |
| T8 | Same check twice | T1, then T1 again without reloading | Available | AC5 | Not testable | Available / Unavailable / Not testable | final-T8.png |
| T9 | Narrow screen | T1 at about 375 px wide | Available | AC6 | Not testable | Available / Unavailable / Not testable | final-T9.png |

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
| 4 | package.json has @supabase/supabase-js, a database library that the page never uses. | Open original/project/package.json and search src for supabase. Expected: no backend or database code (scope). Observed: the dependency is in package.json, line 14, and no file in src imports it. | Low | Fix |

---

## 6. Task 4 — cleanup with focused prompts

One issue per prompt. Paste every prompt **as sent** (every `[bracketed field]` and `AC#` filled
in) and Bolt's answer, unedited.

**Functional fix prompt, as sent, and Bolt's answer:**

```text
(paste here)
```

**Cleanup prompt, as sent, and Bolt's answer:**

```text
(paste here)
```

Add further blocks for further prompts.

**Every change or suggestion Bolt made, judged.** Accepting is a decision; so is rejecting. Cite
the AC (or the scope) that justifies it.

| # | What Bolt changed or suggested | accept / reject | Reason — cite the AC or the scope | Retest: which cases, result |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

Two to four concrete changes, each one retested.

| # | Issue | Decision | Change (file or component) | Result after retest |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |

---

## 8. One generated component, in my own words

Pick one file or component Bolt generated that matters for AC1–AC5 — the one that decides
availability is the best choice. Name its path in backticks, then explain in your own words, without
the assistant, what it does and how it decides. 60 words or more.

**File:** `(write here, e.g. src/App.tsx)`

<!-- Write your explanation below this line -->

---

## 9. What still fails, and what the criteria do not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 The end of the day

AC1 allows `end ≤ 1440` — a booking may end at 24:00. Can a user of your final page ask for
23:00–24:00? How — and if not, why is that acceptable or not? (This is the value you declare in
`submission.yml` under `assumptions.end_of_day`.)

-

### 9.3 Which "now"?

AC1 says "after the supplied current time". What did **v1** use as the current time, and what did
that mean for testing case T6?

-

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
