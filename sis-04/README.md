# SIS #04 — AI-Assisted Software Evolution, Refactoring and Quality Improvement

**AI-Driven Software Engineering · KBTU SITE · Fall 2026**
**SIS #04 · 2 points · individual · deadline Sunday 22 November 2026, 23:59**
**AI use: required.** Level D. Use at least one AI assistant, and check everything it recommends
yourself.

> **This time you extend a working application.** You take your Smart Campus room availability
> checker from Practice #08 (or #07, or SIS #03, or the starter in this folder) and give it new
> requirements: a catalog of **at least four rooms**, filtered by **capacity** and **equipment**.
> Then you reorganise the code into clear modules **without breaking AC1–AC6**, prove it with
> **10 or more automated tests**, and measure the result with evidence instead of impressions.
>
> **This is not Practice #08 again.** You do not debug planted bugs, and you do **not** write a new
> `SKILL.md`.
>
> **Your choices, frozen once made:** the assistant (record the **exact model**: "ChatGPT" is a
> tool, not a model; write `not displayed` if the tool hides it), and TypeScript or JavaScript (your
> project's language). **The same for everyone:** the requirements (§5), the module and function
> names (§7), the test IDs (§9), the screenshot names (§7) and the file layout (§2).

This is **Assignment #04** of the course. Every group gets the same scenario, requirements and
tasks. The report is a Markdown file in your repository. You get a checker you can run yourself,
and the rubric is written below (§15).

**The submission is the link to your open pull request, pasted into the Teams assignment.** Do not
upload a file, and do not send an e-mail.

---

## 1. The idea

Most software work is not writing something new. It is changing something that already works, for
a new requirement, without breaking what users rely on. An AI assistant is very good at producing
a lot of new code fast, and that is exactly the risk here: a "full rewrite" that looks clean and
quietly drops the touching-bookings rule from Week 05.

So this assignment has a fixed order, and the deck's suggested workflow is the order:

```text
BASELINE → CONTEXT → ANALYSIS → PLAN → ONE CHANGE → TESTS + DIFF → … → EVIDENCE
```

You record the baseline before you touch anything. You give the assistant a map and the
requirements, and ask for **a small plan, not a rewrite**. You make one change at a time and run
the tests after each one. You finish with numbers you can explain: how many tests passed, before
and after; which duplicated logic is gone; which modules exist and why.

**Main message:** an AI's "this is cleaner now" is not evidence. A green suite that still holds
AC1–AC5, and a diff you can explain line by line, are.

**Time budget:** about 6–8 hours over two weeks. A first commit within the first two days makes
everything after it easier.

---

## 2. What you hand in

By the deadline, your branch `sis-04` must contain:

```
sis-04/
├── README.md                  this file (read-only)
├── report.md                  THE worksheet: fill in all 10 sections
├── AI_USAGE.md                AI disclosure
├── submission.yml             the declaration: facts only, validated
├── app/                       YOUR project: the starting point, then your changes (§3, §7)
│   ├── README.md              setup, run and test commands (you write it)
│   ├── package.json
│   └── src/
│       ├── rooms.ts           the catalog: Room type + ROOMS (4+ rooms)        (or .js)
│       ├── booking.ts         canBook (AC1–AC5) + checkRoom                     (or .js)
│       ├── filter.ts          filterRooms (F1, F2)                              (or .js)
│       ├── App.tsx …          the page and its components, no rules of their own
│       └── *.test.ts          your tests, 10 or more, with the IDs from §9
├── diagrams/
│   ├── before.puml            the modules of your starting point (PlantUML)
│   └── after.puml             the modules of your final code
├── evidence/
│   ├── filter-match.png       five screenshots (§7)
│   ├── filter-empty.png
│   ├── switch-a.png
│   ├── switch-b.png
│   └── narrow.png
├── starter/                   provided: a project for anyone with no earlier one (§3). Do not edit.
└── tests/
    ├── check_sis.py           provided checker. Do not edit.
    └── validate_submission.py provided validator for submission.yml. Do not edit.
```

**Never commit `node_modules/` or a `.env` file.**

The brief asks for "source code for the initial and final versions (or Git commit references)". In
our groups the **initial version is a commit**: the one that brings your starting point into `app/`
unchanged (§3). You write its hash in report.md §1 and `submission.yml`. The **final version** is
the head of your pull request.

---

## 3. Starting point (~20 min)

Continue your own prototype. Pick **one** starting point. All four are worth the same:

| Starting point | When | Bring it in with (from the repository root, on branch `sis-04`) |
| --- | --- | --- |
| `week-08` *(recommended)* | you did Practice #08 | `git checkout week-08 -- week-08/app` then `git mv week-08/app sis-04/app` |
| `week-07` | you did Practice #07 but not #08 | `git checkout week-07 -- week-07/app` then `git mv week-07/app sis-04/app` |
| `sis-03` | your SIS #03 page is your best version | `git checkout sis-03 -- sis-03/web/final` then `git mv sis-03/web/final sis-04/app` |
| `starter` | you have none of these | `cp -R sis-04/starter sis-04/app` |

The brief allows "an equivalent minimal version" too. The `starter` is that version, so everyone
starts from something that runs. If you start from `sis-03` or `starter`, `canBook` still lives
inside the page. Moving it into `src/booking.ts` is part of your refactoring (§8). Both of these
start with **no tests**, and that is fine: your "original" number is 0/0.

**Then, before you change a single line:**

```text
git checkout main && git pull && git checkout -b sis-04
# unzip SIS_04.zip into the root of your se-practice repository, so sis-04/README.md exists
# bring your starting point in (the table above)
cd sis-04/app
npm install
npx vitest run            # paste the REAL output into report.md 1.1, even "No test files found"
cd ../..
git add sis-04 && git commit -m "sis-04: baseline from week-08"
git rev-parse --short HEAD  # this is your baseline commit: report.md section 1
```

That commit holds your starting point **unchanged**. Do not fix anything on the way in. If
something is broken, it is a risk for §6, not something to hide.

---

## 4. The order of work

| Step | What | Where it goes | Commit |
| --- | --- | --- | --- |
| 1 | Starting point in, baseline run | `app/`, report §1 | `sis-04: baseline from …` |
| 2 | Map, context, analysis, plan, **before editing code** | report §2–§3 | `sis-04: analysis and plan` |
| 3 | Catalog and filter, tests first, one change at a time | `app/src`, report §4 | one commit per change |
| 4 | Refactoring, the suite green after each move | `app/src`, `diagrams/`, report §5 | one commit per change |
| 5 | Test plan, final run, quality table | report §6–§7 | |
| 6 | AI appendix, reflection, checker, declaration | report §8–§10, `submission.yml` | `sis-04: declaration` |

At least **3 meaningful commits**, authored by your own GitHub account. The commit for step 2 must
come **before** the first commit that changes `app/src`, because a plan written after the code is
not a plan.

---

## 5. The requirements

**The scenario.** Smart Campus Room Availability Checker. Fictional bookings, a fixed current time.
No login, payments, live APIs or database. Use fictional data only.

**Preserve AC1–AC6** (the same criteria as Weeks 05–08):

```text
AC1 Reject start ≥ end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Clear, responsive feedback on desktop and mobile.
```

**New feature: room selection.** Extend the prototype from one room to a small fictional catalog of
**at least four** rooms. Each room has an **ID, name, capacity, equipment list, blocked status and
its own bookings**. Display only the rooms that satisfy the user's selected requirements. **The
availability check must use the chosen room's bookings, not another room's data.**

```text
F1 Capacity filter: room capacity must be greater than or equal to the requested attendees.
F2 Equipment filter: the room must contain ALL selected required items.
F3 A blocked room cannot be reported as available.
F4 Show a clear empty state when no rooms match.
F5 Changing the selected room must refresh the availability result appropriately.
```

---

## 6. Task 1 — codebase analysis → `report.md` §2–§3

1. **§2.1:** write a concise **repository map**: the files that matter and one line on what each
   does. Give it to the assistant in the next step.
2. **§2.2:** start a fresh chat and send **one context message**: the map, AC1–AC6, F1–F5 and the
   constraints from §5. Ask for maintainability risks with file/function references and a plan of
   small steps. **Ask for a plan, not a full rewrite, and no code yet.** Paste the message exactly
   as sent.
3. **§3.1:** at least **three maintainability risks** in your starting code, each with **where**
   (a file or a `function()`), the **evidence** you saw yourself, and a priority. The assistant may
   suggest them. You confirm each one in the code. An example of a real one: *"`blocked` is a
   checkbox in `App.tsx`, so it applies to whichever room is selected, and F3 cannot be true per
   room."*
4. **§3.2:** your **prioritised improvement plan**, numbered, smallest safe step first.
5. **§3.3:** **one AI suggestion you rejected or modified**, and why, naming the AC, F-rule, test
   or file behind your decision.

Commit §2–§3 **before** you change `app/src`.

---

## 7. Task 2 — feature extension → `report.md` §4

**The layout and names are fixed for everyone**, so every submission can be read, tested and
compared the same way. Inside `app/src/` (TypeScript shown; JavaScript is the same without types):

```ts
// src/rooms.ts — data only
export type Room = {
  id: string; name: string; capacity: number;
  equipment: string[]; blocked: boolean;
  bookings: { start: number; end: number }[];   // minutes after midnight, 600 = 10:00
};
export const ROOMS: Room[] = [ /* 4 or more fictional rooms, every field filled */ ];

// src/filter.ts — F1, F2
export function filterRooms(rooms: Room[], criteria: { attendees: number; equipment: string[] }): Room[];

// src/booking.ts — AC1–AC5 and the chosen room
export function canBook({ start, end, now, blocked, bookings }): boolean;   // unchanged from Practice #07/#08
export function checkRoom(rooms: Room[], roomId: string,
                          request: { start: number; end: number; now: number }): boolean;
```

- `checkRoom` finds the room by `roomId` and **calls `canBook`** with that room's own `blocked` and
  `bookings` (F3, F5). An unknown id is not available. It must not change anything (AC5).
- Equipment names are yours (`"projector"`, `"whiteboard"` …). The rule is the brief's: **all**
  selected items, not any (F2).
- Blocked rooms may stay in the filtered list (with a label) or be hidden. **Your choice:** state it
  as a design decision in §5.2. Either way they are never "Available" (F3).
- Keep the page **responsive** and the feedback clear (AC6). Nothing outside §5's scope: the
  checker scans for network calls, browser storage, backends, login and payments (A7).

**Work one change at a time:** write the test for a rule, see it fail, add the code, run **all**
tests, read the diff, commit.

**Screenshots**, PNG or JPG, named exactly, in `evidence/`, each described in §4.2:

| File | Shows |
| --- | --- |
| `filter-match.png` | a filter that leaves some rooms, and only rooms that satisfy it |
| `filter-empty.png` | a filter no room satisfies, and your empty-state message (F4) |
| `switch-a.png` | one room selected, a time entered, its result |
| `switch-b.png` | **the same times**, another room selected, a **different** result (F5) |
| `narrow.png` | the page at phone width, **portrait** (AC6) |

Together these show what the brief asks for: successful and unsuccessful filtering, room switching,
and availability checks.

---

## 8. Task 3 — refactoring → `report.md` §5 + `diagrams/`

**Separate room data, booking/availability rules, filtering logic and UI presentation.** That means
the four places in §7, plus any components you split the page into. The page **imports** the rules.
It holds no room data and repeats no rule of its own (A5).

- **Reduce duplicated validation or rendering logic.** List every duplicated location you removed
  in §5.3, one row each, and only what you can point at in the diff.
- **Keep behaviour consistent.** Your AC1–AC5 tests must stay green after every move. That is what
  they are for.
- **Diagrams:** `diagrams/before.puml` (your starting point) and `diagrams/after.puml` (your final
  code), as **PlantUML component diagrams** (Weeks 03–04): one box per module or component, an
  arrow per import. `after.puml` must name `rooms`, `booking`, `filter` and the UI (`App` or a
  component). Render them at plantuml.com to check they draw.
- **§5.2:** justify **at least two design decisions**, each with the alternative you did not take
  and why.

---

## 9. Task 4 — automated tests → `report.md` §6

**At least ten executable Vitest tests** in `app/`, next to the code they test. Your Week 07/08
suite counts; keep it. Every required **ID** must appear **as a word in a test title**. One test may
carry several IDs:

```ts
test('T06 B1 AC2: exactly 120 minutes (720-840) is available', () => { … });
```

| ID | What it tests | Must call |
| --- | --- | --- |
| **AC1–AC5** | the original rules still hold (regression) | anything |
| **F1–F5** | the five new rules, one test at least each | F1, F2: `filterRooms` · F4: `filterRooms` · F3, F5: `checkRoom` (F3–F5 may instead `render` the page) |
| **B1** | exactly **120** minutes → available, `toBe(true)` | `canBook` or `checkRoom` |
| **B2** | **121** minutes → rejected, `toBe(false)` | `canBook` or `checkRoom` |
| **B3** | **touching** an existing booking → available, `toBe(true)` | `canBook` or `checkRoom` |
| **B4** | **overlapping** an existing booking → rejected, `toBe(false)` | `canBook` or `checkRoom` |
| **B5** | capacity **exactly equal** to attendees → the room is included | `filterRooms` |
| **B6** | capacity **one below** attendees → the room is excluded | `filterRooms` |
| **INT** | an **integration or UI behaviour check**: `filterRooms` then `checkRoom` on what it returned, or a rendered page test | both, or `render` |

**Rules for every test:** import from `vitest` and from your real `./booking` and `./filter`; never
mock them. No `.skip`, `.only`, `.todo` or `test.each` (one test per case, so each has its own
title). Use a **fixed catalog inside the test file**, not the page's `ROOMS`, so a change to the
demo data cannot change a result. **Expected values come from §5, never from what your code
returns.**

A rendered UI test (`@testing-library/react` + `jsdom`) is welcome for INT or F4 but not required.
If you add it, its packages go in `package.json` and its commands in `app/README.md`.

**§6.2** — the commands you ran. **§6.3** — the **real** output of the final full run. Every test
passes, and the number Vitest reports equals the tests in your files (R2).

**`app/README.md`** — setup, run and test commands (`npm install`, `npm run dev`,
`npx vitest run`), as the brief requires (A8).

---

## 10. Task 5 — quality evaluation → `report.md` §7

A short evidence table, **original** (your baseline commit) against **final**:

| Measure | How to get it honestly |
| --- | --- |
| Automated tests passed / total | the `Tests` line of the runs in §1.1 and §6.3, as `passed/total` (checked: R3) |
| Duplicated logic locations removed | the rows of §5.3 |
| Code structure: modules and their responsibilities | `git ls-files app/src` before and after, read against §5.1 |
| Remaining limitation | at least one, from what actually happened, not "more tests could be added" |

**Do not invent metrics.** No "maintainability +40 %", no "complexity reduced" without a number and
the command that produced it. The last column says how each value was obtained, so someone else
could repeat it.

---

## 11. Task 6 — AI reflection, the AI appendix, the optional extension

**§10 — reflection, 200–300 words, your own words, no assistant.** Answer all five: *What context
did you provide the AI assistant? Which generated suggestions were useful or incorrect? What did you
personally verify? How did tests influence your engineering decisions? What would you improve
next?*

Worthless: *"AI was very helpful and the code is cleaner now."*
Worth everything: *"Its first capacity test expected only the 12- and 20-seat rooms for 8
attendees. F1 says ≥, so the 8-seat room belongs too. I wrote B5 from the rule, not from the
output."*

**§8 — AI evidence appendix.** At least **three exchanges**: the analysis (Task 1), the plan, and at
least one implementation, refactoring or test exchange. Each records the tool and model, the date,
the purpose, **the prompt as sent**, the output you used (cut to the part you used, with `[…]`), the
problems you found, the changes you made, and **what verified it** (a test, a run, a file, a
screenshot). "It looked right" verifies nothing.

**Optional, not graded:** use an **existing** Agent Skill (your `bug-detector` from Practice #08,
for example) or an approved MCP-enabled environment for codebase navigation or review. **Do not
create another `SKILL.md`.** Keep tool permissions minimal, and never share credentials or private
data. Record it in `AI_USAGE.md` and in an exchange in §8. It replaces none of the six tasks.

---

## 12. Check your work

The checker runs **33 checks**:

| Checks | What they look at |
| --- | --- |
| **A1–A8** | `app/`: `canBook` in `src/booking` (A1); `ROOMS` with 4+ complete rooms (A2); `filterRooms` (A3); `checkRoom` calling `canBook` (A4); the UI imports the rules and holds no room data or rule (A5); AC1–AC5 still in `canBook`: strict overlap, 120, `blocked`, no mutation (A6); no `node_modules`, `.env`, network, storage, login, payment (A7); `app/README.md` with the commands (A8) |
| **S1–S7** | your tests: real modules (S1); nothing mocked or skipped (S2); 10 or more (S3); AC1–AC5 (S4); F1–F5 (S5); B1–B6 (S6); INT (S7) |
| **D1–D2** | both diagrams are PlantUML and not the stub (D1); `after.puml` names the four parts and differs (D2) |
| **E1–E3** | the five screenshots: real images, all different, `narrow` in portrait |
| **R1–R3** | the baseline run (R1); the final run, green, same number of tests as your files (R2); §7's tests row equals both runs (R3) |
| **L1–L10** | the report: setup (L1), map and context (L2), risks (L3), plan and rejected suggestion (L4), screenshots described (L5), responsibilities, decisions, duplication (L6), test plan and commands (L7), quality table (L8), three exchanges (L9), reflection length (L10) |

**It never runs your tests or your code.** It reads files. The grader can run your tests with
`npx vitest run`. **Pasted output that your committed tests cannot produce costs the whole
*Automated testing* criterion, and fabricated output is an integrity matter.**

```text
PASS   the check found what it was looking for
FAIL   the content is there but wrong, or not enough of it
ERROR  it could not check: a file, a folder or a section is missing
```

From inside `sis-04/` (Python 3.8 or newer; no Python? open a GitHub Codespace on your branch):

```text
cd sis-04
python tests/check_sis.py
```

The untouched folder gives `pass=0 fail=14 error=19`. That is the intended start. **33 PASS means
your submission can be graded, not that it is good.** Your analysis, decisions and reflection are
read by a person.

---

## 13. The declaration — `submission.yml` (≈ 5 min, last)

Facts only: who you are, the assistant and model, your starting point and baseline commit, your
counts, your checker numbers, and the IDs of any check still failing.

```text
python tests/check_sis.py             # the final run: copy its three numbers
git add . && git commit -m "sis-04: final report"
git rev-parse --short HEAD            # this hash goes in checker.commit
python tests/validate_submission.py   # then fix anything it flags
git add submission.yml && git commit -m "sis-04: declaration" && git push
```

- **Your numbers are re-run at the head of your pull request.** Numbers that match are settled
  automatically. Numbers that do not match cost the whole *AI evidence & workflow* criterion. So
  after your final run, **change nothing** in `report.md`, `app/`, `diagrams/` or `evidence/`. If you
  do, run the checker again and update the declaration.
- **A FAIL you report costs you nothing extra.** List it under `known_fails` and explain it in §9.

---

## 14. Submit

1. Branch **`sis-04`** off `main`, folder **`sis-04/`** at the top of your `se-practice` repository.
   Never commit to `main`.
2. At least **3 meaningful commits**, authored by your own GitHub account (§4).
3. Push with `git push -u origin sis-04`, then open **one pull request `sis-04 → main`** in your own
   repository. Title: `SIS 04 - Room catalog and refactoring - <Surname Name>`. Description: the
   five-section shape from `SETUP.md` §4 (What I built · AI tools used · What the AI got wrong ·
   Time spent · What I would do differently). **All five headings are checked.**
4. **Leave the PR open. Do not merge it.**
5. In the Teams assignment: **+ Add work → Link → paste the pull request URL**, which looks like
   `https://github.com/<you>/se-practice/pull/N`. Do not paste the repository URL.

**Deadline: Sunday 22 November 2026, 23:59 (Almaty).** Lateness is read from GitHub's server-side
push time, not from commit dates. Late work follows the course policy.

---

## 15. Grading — 2 points, 8 criteria × 0.25

| # | Criterion | Full 0.25 | Half 0.125 | Zero |
| --- | --- | --- | --- | --- |
| 1 | **Baseline & context** | Starting point declared and committed unchanged, with a real baseline run; repository map and the context message as sent, with AC1–AC6, F1–F5 and the constraints | Map or context thin, or the baseline not separable from later changes | No baseline, or the context never sent |
| 2 | **Codebase analysis** | Three or more risks located in real files or functions, with evidence you checked; a prioritised plan committed before editing; one AI suggestion rejected or modified, with the reason | Risks generic or unlocated, or the plan written after the code | Missing, or the assistant's list pasted unverified |
| 3 | **Feature extension** | 4+ fictional rooms with every field; F1–F5 work on the page; the check uses the chosen room's data; in scope and responsive; five screenshots that show it | One rule or one screenshot missing, or out-of-scope code | No catalog or no filter |
| 4 | **Refactoring** | Rooms, booking rules, filtering and UI separated, and the UI holds no rule; duplication removed and pointed at; before/after diagrams; two design decisions justified; AC1–AC5 unchanged | One part still mixed, or decisions without reasons | No refactoring, or AC behaviour broken |
| 5 | **Automated testing** | 10+ tests with AC1–AC5, F1–F5, B1–B6 and INT; expected values from the requirements; real commands and output, consistent with the committed tests | An ID or a boundary missing | Fewer than 10, mocked, or output the tests cannot produce |
| 6 | **Quality evaluation** | Four measures, original against final, each with how it was obtained; no invented metric; a real remaining limitation | A measure without its method, or a vague limitation | Missing, or numbers that contradict the runs |
| 7 | **AI reflection** | 200–300 words in your own words, answering all five questions with specifics from this work | Generic, or a question unanswered | Missing, or written by the assistant |
| 8 | **AI evidence & workflow** | 3+ complete exchanges (tool, model, date, prompt, output, problems, changes, verification); `AI_USAGE.md`; `sis-04` branch, 3+ own commits; open PR in the standard shape; `submission.yml` validating | One element missing | Committed to `main`, PR merged, no disclosure, **or declared checker numbers that don't match the re-run** |

**A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.** Your
starting point, your assistant and your language never affect the mark.

**Not accepted (0 for the SIS):** a file upload or an e-mail instead of a pull-request link · a
report that is not in `sis-04/report.md` · a merged PR, a repository link or a branch with no PR ·
fabricated prompts, outputs, test runs, metrics or screenshots · a new `SKILL.md` submitted as the
work.

---

## 16. FAQ

**Can I e-mail the work instead, as the original brief says?** No. In our groups everything is in
the pull request, and the only thing you paste into Teams is its link.

**My Week 08 is not finished (a test still fails).** Bring it in as it is, paste the real baseline
run in §1.1, and fix it as one of your first changes: it is a risk for §3.1. The original number in
§7 is what the baseline run says.

**I started from `sis-03` and Vitest says "No test files found".** Paste exactly that in §1.1, write
`0/0` as the original in §7, and install Vitest (`npm i -D vitest`). R1 accepts it.

**Can I keep my Week 07 test IDs (T01–T14, X1, BUG-A …)?** Yes. Add the new IDs to the titles of
the tests that already prove them, e.g. `T06 B1 AC2: …`, and write new tests for the rest.

**My project is JavaScript.** Same file names with `.js`, same function names. Everything else is
identical.

**The assistant rewrote the whole `App.tsx` in one answer.** Do not paste it in. Ask for one step,
or take the part you need, and record the rest as a problem in §8. "Ask for a small implementation
plan, not a full rewrite" is the brief's own rule.

**Do blocked rooms appear in the list?** Your choice (§7). Say which and why in §5.2.

**Does `checkRoom` have to take the whole catalog?** Yes, `checkRoom(rooms, roomId, request)`. It is
how the tests prove that the result comes from the chosen room (F5). The page may keep other
helpers of its own.

**How many duplicated locations must I remove?** As many as you can point at, honestly counted.
Zero is possible in a small project. Then write one §5.3 row: `none found` and what you searched
(e.g. "every file under app/src, for repeated time parsing, rule checks and list rendering"), and
`0` in §7. An honest zero costs nothing. An invented duplicate does.

**My tool does not show the model.** Write `not displayed` in §1, §8 and `submission.yml`.

**Can I delete the `<!-- -->` guidance comments?** Yes. Never delete the numbered headings, the
`### N.M` sub-headings or the **Label:** words.
