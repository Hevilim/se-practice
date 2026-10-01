# Week 04 — Lab report: Modeling the System with UML

> The single worksheet for this lab. Fill in every section. **Do not delete, rename or renumber
> the headings** — the checker and the grader find your work by them. Replace every `<...>`
> placeholder; a row that still contains `<...>` counts as empty.

---

## 1. Setup

| Field | Value |
| --- | --- |
| Name | Karim Aliyev |
| Group | Monday 16:00 - 19:00 |
| AI assistant | Claude (claude.ai) |
| Exact model | Claude Opus 5.5) |
| Renderer | PlantUML local jar 1.2025.4 |
| Behaviour diagram | activity |
| Stories used | my week-03 stories, revised (US-01 … US-06) |

---

## 2. Prompts as sent

Paste every prompt **exactly as you sent it**, in the order you sent it, one code block each. The
AI's first replies are saved as files in `models/original/` — do not paste them here.

### 2.1 Task 1 — use-case prompt

```text
Using the supplied scenario and approved stories, generate PlantUML for a use-case diagram. Include Student and Administrator outside a named system boundary. Model their goals, show justified associations, and list assumptions. Use include or extend only with a clear reason.
```

### 2.2 Task 2 — class prompt

```text
Create a UML domain class diagram in PlantUML for Smart Campus. Start with Student, Room, and Booking. Add attributes, appropriate operations, and association multiplicities. Add other classes only when requirements justify them. Explain each relationship and list assumptions. Avoid unjustified inheritance or composition.
```

### 2.3 Task 3 — behaviour prompt (3A sequence or 3B activity)

```text
Generate a UML activity diagram in PlantUML for Book room. Show the initial node, actions, guarded decisions, and final nodes. Check the time range, blocked-room status, and overlapping bookings. Show confirmation after success and rejection after failure. Use branches rather than parallel paths unless concurrency is required.
```

### 2.4 Focused correction prompts (if you sent any)

```text
none
```

### 2.5 Critique prompt

```text
Compare my diagrams with the requirements. Identify missing rules, inconsistent names, and unjustified elements. Cite each issue and propose a specific correction.
```

---

## 3. Task 1 — use-case review

**Assumptions the AI listed:** (1) both actors are logged in, login is out of scope; (2) a student can cancel only his own bookings; (3) US-04 asks for a confirmation after booking and after cancelling, so "Send confirmation" is included in both "Book room" and "Cancel own booking".

At least **two** findings. A finding names the element, the problem and the rule or story that
proves it is a problem.

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | Use case "Send confirmation" (UC4) | It is a system action, not a goal. No actor starts it. The student's goal is the booking; the confirmation is only its result. | R4 ("a successful booking produces a confirmation"), US-04 | Removed UC4. The confirmation is written in a note on "Book room" and is an action in the activity diagram. |
| 2 | include arrow "Cancel own booking" to "Send confirmation" | A confirmation after cancelling is a notification other than the booking confirmation, which this lab puts out of scope. Also, neither include had a `' why:` comment. | Out-of-scope list in approved-stories.md, R4, README §4 | Both include arrows removed with UC4. The cancellation part of US-04 is declared out of scope (A5). |
| 3 | "Book room", "Cancel own booking", "Block room", "Review room usage" | The diagram does not show which rules and stories each goal depends on, so they cannot be traced from it. | R1, R2, R3, US-02, US-03, US-05, US-06 | Added notes: rules on "Book room", "own ACTIVE booking" on "Cancel own booking", R3 + A2 on "Block room", "cancelled not counted" on "Review room usage". |

---

## 4. Task 2 — class diagram review

### 4.1 Relationships, read both ways

One row per association in your **revised** class diagram.

| Association | Read left → right | Read right → left | Multiplicities |
| --- | --- | --- | --- |
| Student — Booking | one student makes 0..* bookings | each booking is made by exactly 1 student | 1 / 0..* |
| Room — Booking | one room is reserved by 0..* bookings | each booking reserves exactly 1 room | 1 / 0..* |
| Booking — Confirmation | each booking produces exactly 1 confirmation | each confirmation belongs to exactly 1 booking | 1 / 1 |

### 4.2 Constraints the multiplicities cannot show

- R2: a note on `Booking` — two ACTIVE bookings for the same room must not overlap; time is [start, end).
- R1: the same note on `Booking` — start is in the future and 0 < end − start <= 2 hours.
- R3: a note on `Room` — `blocked = true` means no new booking.
- R4 / US-04: a note on `Confirmation` — created only for a successful booking.
- US-03: the note on `Booking` — only the student who made the booking can cancel it.

### 4.3 Assumptions

- A1: Touching bookings are allowed. Time is a half-open interval [start, end), so 10:00–12:00 and 12:00–13:00 do not overlap under R2.
- A2: Blocking a room keeps its existing bookings ACTIVE. R3 only talks about new bookings, and the assumption of US-05 says the same.
- A3: The three checks and "Create booking" happen as one step, so no other booking can take the slot between the R2 check and the create (from the critique, §6 row 4).
- A4: Room usage (US-06) is calculated from `Booking.start` and `Booking.end` of bookings that are not CANCELLED; it is not a stored class.
- A5: Only the booking confirmation is modelled. The confirmation after cancelling in US-04 is a notification other than the booking confirmation, which this lab puts out of scope.

### 4.4 Findings

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | `Administrator "1..*" -- "0..*" Room` | Read right to left: "each room is blocked by 1..* administrators" — every room must already have an administrator. No story stores who blocks a room. | US-05 (any administrator blocks/unblocks; nothing is recorded) | Removed the `Administrator` class and the association. Blocking is the `blocked` attribute and `block()` / `unblock()` on `Room`. |
| 2 | Class `UsageReport` | It is the result of a query, not something the system stores. | US-06 (booked hours over a chosen period) | Removed. Usage is calculated from bookings (A4). |
| 3 | `Booking "1" -- "1..2" Confirmation` and enum `ConfirmationType` | Models a second confirmation for cancelling, which is out of scope this week. | R4, A5, out-of-scope list | Changed to 1 / 1 and removed `ConfirmationType`. |
| 4 | `Booking --> BookingStatus`, `Confirmation --> ConfirmationType` | Associations with no multiplicities that repeat the attribute types. | CL3 (multiplicity at both ends), R2 ("active bookings") | Arrows removed; `status : BookingStatus` stays as an attribute type. |
| 5 | No note on `Booking` | R2 (no overlap) is not visible anywhere. Multiplicity cannot say "no overlap". | R2, README §4 | Added a note on `Booking` with R2, R1, US-03 and assumption A1. |
| 6 | `Student` operations `viewAvailability()`, `bookRoom()`, `cancelBooking()` | These are use cases, not behaviour of the student object. | US-01, US-02, US-03 are already use cases | Removed from `Student`; `cancel()` stays on `Booking` because it changes the booking's own status. |

---

## 5. Task 3 — behaviour diagram review

**Option chosen and why:** 3B activity — Book room is one workflow with three checks in a row, and an activity diagram shows each check and each rejection reason clearly.

**Design components added beyond the domain model:** none

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | Decision "Overlaps an active booking?" | It does not say "the same room". R2 is only about bookings of the same room; as written, a booking in any room would block the slot. | R2, US-02 | Text changed to "Overlaps an ACTIVE booking of the same room? (R2)". |
| 2 | Guards `(yes)` / `(no)` on all three decisions | Guards had no square brackets, which the README convention requires for activity diagrams. | README §4 (activity guards `([yes])`) | Changed to `([yes])` / `([no])`. |
| 3 | All three decisions and rejections | No rule ID on any decision or rejection, so the reader cannot see which rule failed. | R1, R2, R3, US-04 ("I know the system accepted my request") | Added (R1), (R3), (R2) to the decisions and to the reject actions, (R4) to the confirmation. |
| 4 | Nested decisions (R3 and R2 inside the R1 "yes" branch) | Hard to read; the order of the checks is hidden in the nesting. | US-02 (one flow, three rules) | Made the checks a flat sequence: each "fail" branch rejects and stops, each "pass" branch goes on. |
| 5 | Actions without owners | "Student selects room" and "Create booking" are in the same column, so it is not clear what the student does and what the system does. | US-02 | Added two partitions: `Student` and `Smart Campus`. |
| 6 | Touching bookings | The R2 decision depends on assumption A1, but the diagram did not say it. | R2, A1 | Added a note at the R2 rejection: time is [start, end). |

---

## 6. AI critique

Run the critique prompt once, on all your revised diagrams together. At least **three** rows. A
critique is another claim to evaluate, not a verdict: reject what is wrong and say why.

| # | Issue the AI raised | Element it cited | Verdict | Why |
| --- | --- | --- | --- | --- |
| 1 | US-04 asks for a confirmation after cancelling too, but no diagram shows it; add it to "Cancel own booking" and to `Confirmation`. | US-04, use case "Cancel own booking", class `Confirmation` | reject | The out-of-scope list allows no notification other than the booking confirmation. The decision is declared as A5, so the gap is intended. |
| 2 | "Block room" and "Unblock room" both trace to US-05; merge them into one use case. | Use cases "Block room", "Unblock room" | reject | They are two different goals done at different times, with opposite effects on `Room.blocked`. One story may trace to two use cases. |
| 3 | `Booking "1" -- "1" Confirmation` is wrong because a CANCELLED booking still has a confirmation. | `Booking — Confirmation` | reject | The confirmation was really issued when the booking was created (R4). Cancelling later does not undo that fact, so 1 / 1 is correct. |
| 4 | Between the R2 check and "Create booking" another student could take the same slot, so R2 can still be broken. | Activity: R2 decision and "Create booking with status ACTIVE" | accept | This is true. I did not change the workflow; I added assumption A3: the checks and the create are one step. |
| 5 | The assumption of US-05 cites R4 for blocking, but in this lab the blocked-room rule is R3. | `approved-stories.md`, US-05 | accept | Correct — week 03 used other numbers. I kept the approved text and added a note and a rules table to `approved-stories.md`. |

---

## 7. Consistency table

One row for each of **R1–R4**, then one row for **every use case in your revised use-case
diagram**, spelled exactly as in the diagram, with the story ID it traces to.

| Requirement / story | Use case | Classes | Behaviour element |
| --- | --- | --- | --- |
| R1 | Book room | Booking.start, Booking.end, note on Booking | decision "Start in future and 0 < duration <= 2 h? (R1)" |
| R2 | Book room | Booking.status, Booking.start, Booking.end, R2 note on Booking | decision "Overlaps an ACTIVE booking of the same room? (R2)" |
| R3 | Book room | Room.blocked, note on Room | decision "Room blocked? (R3)" |
| R4 | Book room | Confirmation, Booking — Confirmation (1 / 1) | action "Issue confirmation to the student (R4)" |
| US-01 | View room availability | Room.blocked, Booking.start, Booking.end, Booking.status | not part of the Book room activity (read-only query) |
| US-02 | Book room | Student, Booking, Room | whole activity "Book room" |
| US-03 | Cancel own booking | Student, Booking.status, Booking.cancel() | not part of the Book room activity |
| US-04 | Book room | Confirmation (booking part only, A5) | action "Issue confirmation to the student (R4)" |
| US-05 | Block room | Room.blocked, Room.block() | decision "Room blocked? (R3)" reads its result |
| US-05 | Unblock room | Room.blocked, Room.unblock() | decision "Room blocked? (R3)" reads its result |
| US-06 | Review room usage | Booking.start, Booking.end, Booking.status (A4) | not part of the Book room activity |

---

## 8. Change log

At least **three** rows, and at least one for each required diagram (use case, class, your
behaviour diagram). "Before" is what the AI produced; "After" is what you submitted.

| # | Diagram | Before (AI's original) | After (your revision) | Reason |
| --- | --- | --- | --- | --- |
| 1 | use case | "Send confirmation" use case, included from "Book room" and "Cancel own booking" | removed; booking confirmation is in a note on "Book room" | R4 — confirmation is an outcome, not a goal; cancel confirmation out of scope (§3 #1, #2) |
| 2 | use case | no notes | notes with rules and stories on "Book room", "Cancel own booking", "Block room", "Review room usage" | traceability to R1–R4, US-02, US-03, US-05, US-06 (§3 #3) |
| 3 | class | `Administrator` class with `"1..*" -- "0..*" Room` | removed | no story stores who blocks a room (§4.4 #1) |
| 4 | class | `UsageReport`, `ConfirmationType`, `Booking "1" -- "1..2" Confirmation`, enum arrows, use-case operations on `Student` | removed; Booking — Confirmation is 1 / 1 | US-06 is a query; A5; arrows had no multiplicities; operations are use cases (§4.4 #2–#4, #6) |
| 5 | class | no constraint notes | notes for R1/R2/A1/US-03 on `Booking`, R3/A2 on `Room`, R4/A5 on `Confirmation` | R2 cannot be shown with multiplicities (§4.4 #5) |
| 6 | activity | "Overlaps an active booking?" | "Overlaps an ACTIVE booking of the same room? (R2)" | R2 is about the same room (§5 #1) |
| 7 | activity | nested decisions, guards `(yes)`/`(no)`, no rule IDs, one column | flat checks, guards `([yes])`/`([no])`, rule IDs, partitions Student / Smart Campus, A1 note | README §4, readability, traceability (§5 #2–#6) |

---

## 9. Checker output

Paste the complete output of `python tests/check_models.py`, then explain **every FAIL you are
keeping**. The same IDs go in `submission.yml` under `checker.kept_fails`. A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.

```text
Week 04 structural check - shape only, never quality

UC1  PASS  Student and Administrator declared
UC2  PASS  named system boundary: "Smart Campus Room Booking System"
UC3  PASS  all actors declared outside the boundary
UC4  PASS  all scenario goals present (6 use cases)
UC5  PASS  no actor is associated with a confirmation use case
UC6  PASS  actor responsibilities match the scenario
UC7  PASS  use cases are goals, not screens or components
UC8  PASS  every include / extend / generalization carries a ' why: comment (or there are none)
UC9  PASS  revised diagram differs from the AI's original
CL1  PASS  Student, Room and Booking present
CL2  PASS  Booking is associated with Student and with Room
CL3  PASS  every association has multiplicities at both ends
CL4  PASS  1 student / 1 room per booking, 0..* bookings per student and per room
CL5  PASS  every inheritance / composition / aggregation carries a ' why: comment (or there are none)
CL6  PASS  only domain concepts in the class diagram
CL7  PASS  attributes needed by R1-R3 are present
CL8  PASS  a note states R2 (no overlapping active bookings)
AC1  PASS  initial and final nodes present
AC2  PASS  separate decisions check R1, R3 and R2 (3 decisions)
AC3  PASS  every branch has a labelled guard
AC4  PASS  no parallel paths
AC5  PASS  confirmation on success, rejection on failure
AC6  PASS  creation comes after all rule checks
FI1  PASS  the AI's original output is kept for every diagram
FI2  PASS  a rendered image for every diagram
LR1  PASS  §1 setup filled (tool and model recorded)
LR2  PASS  5 prompts pasted in §2
LR3  PASS  3 use-case findings in §3
LR4  PASS  §4 relationships read both ways, 5 assumption(s) declared
LR5  PASS  6 behaviour-diagram findings in §5
LR6  PASS  5 critique issues with a verdict
LR7  PASS  7 change-log rows covering all three diagrams
CS1  PASS  6 approved stories
CS2  PASS  §7 traces R1-R4 into the diagrams
CS3  PASS  every use case traces to an approved story

SUMMARY pass=35 fail=0 error=0
A FAIL you report and explain in lab-report.md §9 costs you nothing. One you hide costs the criterion.
```

**FAILs I am keeping, and why:** none

---

## 10. Conclusion (120–180 words)

The class diagram was the most wrong. The AI added an `Administrator` class with `"1..*" -- "0..*"`
to `Room`. Read from the room side, this says every room must already have at least one
administrator, and no story asks the system to store who blocks a room. It also modelled a second
confirmation for cancelling (`1..2`), which this lab puts out of scope, and a stored
`UsageReport`, which is only a query result. The error that would reach the code is in the activity
diagram: the overlap check did not say "of the same room". Code written from it would refuse a
booking because a different room is busy at that time. The critique found two things I missed: a
race between the R2 check and "Create booking" (A3), and the old rule number R4 in the assumption of
US-05. It also claimed that `Booking 1 — 1 Confirmation` is wrong for cancelled bookings. That is
false: the confirmation was really issued when the booking was created.
