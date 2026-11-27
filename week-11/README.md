# Week 11 — Explain, Don't Decide: an LLM Feature and an Agentic Code Review

**Course:** AI-Driven Software Engineering (Fall 2026, KBTU SITE)
**Practice work #11** · 1 point · AI-use level: **D (AI-integrated, disclosure required)**
**Deadline:** Sunday 29 November 2026, 23:59 (Almaty)

> **This week continues your Smart Campus project** from Week 10: the one-room checker with AC1–AC6,
> your Vitest suite and the `AGENTS.md` you patched. You add **one small AI-enabled feature**: an
> *Explain availability* button that turns the checker's decision into a short sentence for a student.
> Then an AI reviewer inspects your change, you check what it claims, and you fix the two findings
> that matter most.
>
> **A mock model is enough for full marks.** You need no API key and no paid account. The feature
> talks to the model through an **adapter**, and the adapter you build and test is a mock that
> follows the same contract a real model would. A real model is optional, ungraded, and allowed only
> from a server (§3.5).
>
> **Your choice:** the assistant that builds the feature, **Bolt.new** (the deck's tool), Claude Code,
> Cursor or Copilot, and the assistant that reviews it. The lecture recommends a **different model
> for review than for generation**. Freeze both for the whole lab and record their exact models.
>
> **Identical for everyone:** the contract in §3 (its field names, the six reason codes, F1–F5),
> the deck's two prompts (Parts 3 and 6), the test cases E1–E9, and the file layout (§2).

---

## 1. The idea of this lab

The checker already knows the answer. `canBook` says *Available* or *Unavailable*, and it is right,
because your suite proves it. What a student cannot see is **why**. An LLM is good at turning a
reason into a friendly sentence. It is not good at deciding, because it can be wrong, slow,
unavailable or talked into saying something else.

So this week's architecture has one rule, the deck's main message:

> **The deterministic checker decides. The LLM only explains. When the model fails, the page still
> works.**

```text
student input -> validation -> canBook / availabilityReason -> { isAvailable, reasonCode }
                                                                     |
              UI <- validated explanation <- adapter (mock or server-side model)
```

The second idea is the lecture's: **an AI review finding is a hypothesis until code, a test or a
reproducible step supports it.** An agentic reviewer reads more than the diff: the README, the
`AGENTS.md`, the tests. It finds real problems, and it also writes confident paragraphs about
problems your code does not have. Part 6 sorts them.

**Time budget:** ~50 min in class (Parts 0–3, with the instructor's demo), + ~3 h at home.

---

## 2. Deliverables

By the deadline, your branch `week-11` must contain:

```
week-11/
├── README.md                  # this file (read-only)
├── lab-report.md              # THE worksheet: fill in all 10 sections
├── AI_USAGE.md                # AI disclosure (every week)
├── submission.yml             # machine-readable declaration: facts only
├── app/                       # your Week 10 project, brought over in Part 0
│   ├── AGENTS.md              #   your patched playbook from Week 10
│   ├── package.json
│   └── src/
│       ├── booking.ts         #   canBook, unchanged rules, + the reason code (Part 3)
│       ├── booking.test.ts    #   your existing suite, every test kept
│       ├── explain.ts         #   NEW: the contract, the mock adapter, explainAvailability
│       ├── explain.test.ts    #   NEW: tests E1–E9 (Part 5)
│       └── App.tsx …          #   the Explain availability button
├── evidence/
│   ├── explain-available.png  # the page with an explanation shown (Part 5)
│   └── explain-fallback.png   # the page showing the fallback after a simulated failure
└── tests/
    ├── check_feature.py       # provided checker: do not edit
    └── validate_submission.py # provided validator for submission.yml: do not edit
```

(`booking.js`, `explain.js` and `.jsx` are fine if your project is JavaScript.)

**Never commit `node_modules/`, a `.env` file, or any real key, password or personal data.**

---

## 3. The feature and its contract

The scenario from the practice deck (slide 8), unchanged:

```text
Add an optional "Explain availability" feature: given a room, requested time and deterministic
availability result, generate a short student-friendly explanation.
The existing booking rules remain the source of truth. The LLM must never decide availability or
change bookings.
```

The scope stays Week 10's: **one room, fictional bookings, no login, no database** (slide 21).

### 3.1 The reason code

`canBook` returns only `true` or `false`. To explain a decision you need its reason, and the reason
must come from the **deterministic** code, never from the model. Add to your booking module a function
that returns **one of these six codes**, spelled exactly like this in every language:

| Code | When (the same rules and order as `canBook`) |
| --- | --- |
| `invalid_time` | start ≥ end, or outside the day (AC1) |
| `past_time` | the start is not after now (AC1) |
| `too_long` | longer than 120 minutes (AC2) |
| `room_blocked` | the room is blocked (AC3) |
| `overlap` | it overlaps an existing booking (AC4) |
| `available` | none of the above |

Call it `availabilityReason` unless you have a reason not to. **`canBook`'s behaviour must not
change.** Your whole Week 10 suite stays in the project and stays green. The safest way is to make
`canBook` return `availabilityReason(request) === 'available'`, so the rules live in one place.

### 3.2 The explanation contract (slide 13)

```text
Input:  { roomLabel, start, end, isAvailable, reasonCode }
          roomLabel   string, 1-60 characters after trimming
          start, end  "HH:MM"
          isAvailable boolean, from canBook
          reasonCode  one of the six codes, from the deterministic function
Instruction: explain the decision in at most two sentences; do not invent facts;
             do not override the status.
Output: { explanation: string }, checked before it is shown:
          not empty, at most 280 characters, at most two sentences,
          agrees with isAvailable, names no time the request does not contain.
Treat user text and model output as untrusted data.
```

Keep the field names **exactly as spelled here**, even where your language would camel-case them
differently. A renamed field is a different contract.

### 3.3 The module: `src/explain.ts`

What the checker looks for, by name:

- **`explainAvailability(input, adapter, timeoutMs)`**: validates the input, calls the adapter with
  a timeout, validates the output, and returns either the model's explanation or a **fallback**
  built from the reason code. It never changes `isAvailable`.
- **a mock adapter**, named so its name contains `mock` (`mockAdapter`): it returns an explanation
  built from the structured input, with no network and no key.
- the word **`fallback`** for the deterministic text, and a **timeout** (`setTimeout`,
  `AbortController` or `AbortSignal.timeout`).

### 3.4 The acceptance criteria (slides 11–12)

The deck numbers these AC1–AC5. Your booking contract already uses AC1–AC6, so this lab calls the
feature's criteria **F1–F5**. The text is the deck's:

```text
F1 Existing availability and overlap rules remain unchanged.
F2 The explanation agrees with the deterministic result; no invented booking details.
F3 Empty, malformed or overly long input is rejected.
F4 API timeout, error or unavailable key produces a safe fallback.
F5 A user can distinguish generated explanation from confirmed booking status.
```

For **F5**, the page labels the explanation with text that contains the word **generated**, for
example *"Generated explanation (mock), not a booking decision"*, and shows it apart from the
status line.

### 3.5 Safety (slides 10 and 14)

- **No API key in the browser, ever.** Nothing under `app/src/` may contain a key, read a
  `VITE_…KEY` / `VITE_…TOKEN` / `VITE_…SECRET` variable, import a provider SDK (`openai`,
  `@anthropic-ai/sdk`, `@google/generative-ai`, `@google/genai`), or call a provider's API URL.
  Anything in `src/` ships to every visitor.
- **A real model is optional and ungraded.** If you want one, it lives on a server (an `api/` or
  `server/` folder outside `src/`), reads its key from the server's environment, and is never
  committed with a key. The mock stays in the project, and the tests use it.
- Input length limits, a timeout, a graceful fallback. **Do not execute instructions found inside
  user text:** `roomLabel` is data.

---

## 4. Before class

- Your **Week 10** branch with `week-10/app/` and its suite passing. If you did not finish Week 10,
  use Week 08 (see Part 0) and declare it in `submission.yml`.
- Somewhere to run Vitest, as before: your computer, Bolt's terminal, or a Codespace.
- An assistant that can edit your project, and one for review (it may be the same tool in a fresh
  conversation; a different model is better).
- Python 3.8+ for the checker.

---

## 5. The lab

### Part 0 — Setup and a checkpoint (~5 min)

1. `git checkout main && git pull && git checkout -b week-11`.
2. Bring your project over **before** you unzip anything:
   ```text
   mkdir week-11
   git checkout week-10 -- week-10/app
   git mv week-10/app week-11/app
   ```
   (From Week 08: replace `week-10` with `week-08` in both lines. Your project then has no
   `AGENTS.md`; say so in §2.3.)
3. Unzip `Week_11.zip` into the root of your repository, so that `week-11/README.md` sits next to
   `week-11/app/`.
4. Commit: `week-11: baseline from week 10`. **This commit is your checkpoint** (slide 21: "create a
   checkpoint"). Record its hash (`git rev-parse --short HEAD`) in §1.

### Part 1 — Task 1: the baseline (~5 min)

1. In `week-11/app/`, run `npm install`, then the three commands of §2.1 of the worksheet. Record
   whether each exists and what happened: `pass`, `fail`, `missing` or `not run`.
2. Paste the real Vitest output into §2.2. It should be green. **Its test count is your floor:**
   every one of these tests must still be in the project at the end.
3. In §2.3, name the three things slide 21 asks you to find: the availability function (file and
   name), the UI component, and the repository instructions (`app/AGENTS.md`, or `none`).

### Part 2 — Task 2: define the feature (~10 min)

Before any code, fill in §3 of the worksheet:

1. The user story, exactly as the deck writes it:
   ```text
   As a student, I want a short explanation of room availability so I understand the decision.
   ```
2. The contract as you will implement it: each input field, the output, and what is validated (§3.2
   of this README is the specification; write it down in your own table).
3. F1–F5, and the **failure behaviour**: what the student sees when the input is invalid, when the
   model times out, when it fails, and when its answer contradicts the decision.
4. The flow (slide 23), as a diagram or a written flow with arrows: request → rule engine → LLM
   adapter → response. It must name your checker function and the adapter, and say **which one
   decides availability**.

### Part 3 — Task 3: build it with an AI assistant (~25 min)

1. Give your assistant the contract (§3 of this README, or your §3 of the worksheet) and send the
   deck's implementation prompt, **exactly as written**:

```text
Act as a software engineer. Extend the existing Smart Campus checker with an optional explanation feature. Preserve all booking rules and tests. The deterministic checker must remain authoritative. First, implement a mock adapter, validate inputs and outputs, handle failures gracefully, and describe each changed file. Do not add login, a database, real personal data, or client-side API secrets.
```

2. Paste what you sent and the answer into §4.1. If you sent the contract with it, paste that too.
3. **Inspect every generated change before you accept it** (slide 24). One row per changed file in
   §4.2: what changed, and your decision, `accept`, `modify` or `reject`, with why. A change to
   `booking.ts` that alters a rule is a `reject`.
4. Make sure the names of §3.3 exist (ask the assistant to rename if they do not), and that the page
   has the **Explain availability** button and the *generated* label (F5). A checkbox that switches
   to a failing adapter (*Simulate API failure*) is the easy way to show the fallback on the page.
5. Run `npx vitest run`. Every old test must still pass. Commit:
   `week-11: explain availability with a mock adapter`.

### Part 4 — Task 4: prompt engineering (~20 min, at home)

The mock does not read a prompt, but a real model will, so you choose the instruction now.

1. Write **three** candidate system instructions, A, B and C (§5.1). Each limits the model to the
   supplied facts (slide 25). Make them really different: a short one, one with explicit rules, one
   with an example.
2. In a **fresh chat** for each prompt, with the same model, send the prompt followed by the same
   three JSON inputs: an `available`, an `overlap` and a `room_blocked` request. Paste the answers in
   §5.2.
3. Score each prompt in §5.3 for clarity, consistency and factual agreement (slide 26): did any
   answer invent a time, a booking or a person, or contradict the status?
4. Choose one in §5.4, with the reason. Put it in `explain.ts` as the instruction a real adapter
   would send (`SYSTEM_INSTRUCTION`).

### Part 5 — Task 5: test normal and failure cases (~30 min, at home)

The deck's nine cases (slide 27), with fixed IDs:

| ID | Case | Expected |
| --- | --- | --- |
| E1 | available (11:00–12:00, now 09:00, booking 10:00–11:00) | `available`; explanation says available |
| E2 | overlap (10:30–11:30) | `overlap`; explanation says unavailable, mentions the overlap |
| E3 | blocked room | `room_blocked` |
| E4 | invalid time (12:30–12:00) | `invalid_time` |
| E5 | past time (08:00–08:30 at 09:00) | `past_time` |
| E6 | empty input (blank room label) | rejected before the adapter is called |
| E7 | long input (a 500-character room label) | rejected |
| E8 | timeout (an adapter that never answers) | the fallback, within the timeout |
| E9 | simulated API failure (an adapter that throws) | the fallback |

1. Write them as Vitest tests in `app/src/explain.test.ts`. **Each test title starts with its ID**:
   `test('E8 F4: an adapter that never answers times out into the fallback', …)`. Test the failure
   cases with **fake adapters** written in the test file (one that never resolves, one that throws).
   At least five of E1–E9 must be automated, including E8 or E9.
2. Run the whole suite and paste the output into §6.2.
3. Fill in the table of §6.1: expected, observed, verdict (`pass`, `fail` or `not run`) and how you
   tested it (the test title, or `manual`). **At least eight** of the nine must be `pass` or `fail`.
   Then the last row: **the UI never changes the deterministic decision**. Check it on the page and
   say how.
4. Run the page and take two screenshots (slide 27: "preserve screenshots"):
   `evidence/explain-available.png` (a decision with its explanation and the *generated* label) and
   `evidence/explain-fallback.png` (the fallback, after a simulated failure).

Commit: `week-11: tests E1-E9`.

### Part 6 — Task 6: the agentic code review (~25 min, at home)

1. Make sure the reviewer **cannot edit** (Plan mode in Bolt.new or Claude Code; a chat with pasted
   files). Afterwards, `git status` must show no change.
2. Give it what slide 28 lists: **the diff** (`git diff <checkpoint> -- app` from Part 0),
   **README**, **`AGENTS.md`** and **the acceptance criteria** (F1–F5 and AC1–AC6). Say in §7.1 what
   you gave it and which model reviewed.
3. Send the deck's review prompt, **exactly as written**:

```text
Act as a read-only agentic code reviewer. Inspect the proposed diff in context, repository instructions, and tests. Review correctness, security, maintainability, and performance. For each issue, provide severity, affected file, evidence, reproduction or verification method, and a minimal recommendation. Do not edit files. Clearly distinguish confirmed findings from hypotheses.
```

4. Paste it and the whole answer, unedited, into §7.2.
5. **Verify each finding yourself** (slide 16): open the file, run the test, try it on the page.
   Record at least **three** in §7.3 with IDs `V1`, `V2`, …, a category, a severity, the file,
   **how you verified it**, and your label:

| Label | When |
| --- | --- |
| `confirmed` | you reproduced it: a failing test, a line of code that does it, a step on the page |
| `plausible` | it could be true, but you could not show it |
| `unsupported` | the cited file, line or behaviour is not there, or contradicts what you see |

   The reviewer's own word "confirmed" is not your label. At least **two** must be `confirmed`. You
   may add findings of your own: say so in the *Found by* column.
6. In §7.4, **compare with your own inspection** (slide 28): what you checked by hand that the
   reviewer did not, and what a linter (`npm run lint`, ESLint) would have caught of these and what
   it could not (lecture: rule-based vs. contextual review).

### Part 7 — Task 7: repair and regression-test (~20 min, at home)

1. Choose the **two most important confirmed findings**. For each one in §8.1 and §8.2: the
   finding's ID, **why the fix is necessary**, what you rejected from the assistant's proposal (or
   `nothing`, with why), and the diff. Keep each fix focused. No unrelated refactoring.
2. A finding a test can show gets a test whose title starts with its ID (`V1 F2: …`). Run it before
   the fix if you can: a test that fails first is the best evidence that the finding was real.
3. **Rerun the old booking tests and the new feature tests** together. Paste the full final run into
   §8.3. Every test must pass.
4. In §8.4: **is the change ready for demonstration** (`yes` or `no`), and what remains unresolved
   (slide 29).

Commit each fix separately: `week-11: fix V<n> - <what>`.

### Part 8 — Reflection, declaration, submit (~15 min, at home)

1. In §10, 80–150 words in your own words, without the assistant: **what the AI generated, what you
   verified, and what you changed** (slide 33). Name at least one finding ID and one test ID.
2. From inside `week-11/`, run `python tests/check_feature.py`. Every FAIL or ERROR you keep goes in
   §9 with the reason.
3. Fill in `AI_USAGE.md`.
4. Commit, note the hash with `git rev-parse --short HEAD`, fill in `submission.yml`, run the
   validator, commit, push, and open the PR (§9).

---

## 6. Verdicts

```
PASS   the check found what it was looking for
FAIL   the content is there but wrong, or not enough of it
ERROR  it could not check: a file, a folder or a section is missing
```

The review labels are yours (`confirmed` / `plausible` / `unsupported`). The checker's verdicts are
about your files, never about whether your explanations are good English.

---

## 7. Checking your work

From inside `week-11/`:

```text
python tests/check_feature.py
```

It runs 27 checks:

| Checks | What they look at |
| --- | --- |
| **B1–B2** | `app/`: a `package.json` and a booking module with `canBook` (B1); no `node_modules/`, no `.env`, under 5 MB (B2). |
| **X1–X6** | The feature in `app/src/`: `explain.ts` with `explainAvailability` and a mock adapter (X1); the six reason codes (X2); a timeout and a fallback (X3); no key and no `VITE_…KEY` variable in `src/` (X4); no provider SDK or provider URL in `src/` (X5); the word *generated* on the page (X6). |
| **S1–S2** | Your suites: the booking suite imports `vitest` and the real `./booking`, nothing mocked, skipped or focused (S1); `explain.test.ts` imports `./explain` and names five or more of E1–E9 in its titles, including E8 or E9, nothing skipped (S2). |
| **E1–E2** | `evidence/explain-available.png` and `evidence/explain-fallback.png`. |
| **R1–R3** | §2.2 a real Vitest run (R1); §6.2 a run after the feature, with more tests than the baseline (R2); §8.3 the final run, all passing, with **the same number of tests as your committed files** (R3). |
| **L1–L12** | The worksheet: setup (L1), baseline commands and the three locations (L2), the feature definition: user story, contract, F1–F5, failure behaviour (L3), the flow (L4), the implementation prompt, its answer and your decisions per file (L5), three prompts compared and one chosen (L6), the test table (L7), the review prompt as sent and its answer (L8), three or more findings verified and labelled, two confirmed, and your own inspection (L9), two fixes (L10), demo readiness (L11), the reflection (L12). |

**The checker never runs your tests and never talks to an assistant.** It reads files. The grader
re-runs your suite. Pasted output that the committed suite cannot produce costs the whole
*Evidence and honesty* criterion.

The first run on the untouched folder gives `0 PASS · 15 FAIL · 12 ERROR`. That is the intended
start.

---

## 8. The declaration — `submission.yml`

Facts only. From inside `week-11/`:

```text
python tests/validate_submission.py
```

- **`checker.commit` is the commit you ran the checker at**, on your `week-11` branch.
- **Your numbers are re-run at the last commit of your pull request.** Numbers that do not match cost
  the whole *Evidence and honesty* criterion, so run the checker again after any change.
- **`project.baseline_commit`** is the checkpoint from Part 0.
- **A FAIL you report costs you nothing extra.** List it in `known_fails` and say why in §9.

---

## 9. Submit

1. Push the branch with `git push -u origin week-11`.
2. Open a Pull Request `week-11 → main` in your own repository. Title: `Week 11 — Explain
   Availability and Agentic Review`. Write the description in the fixed shape from `SETUP.md` §4.
3. **Leave the PR open. Do not merge it.**
4. In the Teams assignment *Practice 11*: **+ Add work → Link → paste the pull request URL.**

The deck asks you to email screenshots to the main lecturer. **That does not apply to our
groups.** The PR already holds the working prototype, the contract, the tests, the review and the
screenshots.

**Deadline:** Sunday 29 November 2026, 23:59 (Almaty). Late submissions follow the course policy.

---

## 10. Grading — 1 point, 4 × 0.25

| Criterion | Complete (0.25) when … | Checks it needs |
| --- | --- | --- |
| **Feature and contract** | The contract and F1–F5 written down before the code, with the failure behaviour; a flow in which the deterministic checker decides; the deck's implementation prompt sent as written and every changed file decided; `explain.ts` with a mock adapter, a timeout, a fallback and validated output; the six reason codes from the deterministic code; no key and no provider call in the browser; the *generated* label on the page | B1 X1 X2 X3 X4 X5 X6 L3 L4 L5 |
| **Prompts and tests** | A real baseline run; three instructions compared on the same three inputs and one chosen for a reason; E1–E9 with expected and observed results, five or more automated including a failure case; the UI shown not to change the decision; two screenshots; the old suite kept and green | S1 S2 E1 E2 R1 R2 L2 L6 L7 |
| **Agentic review and repair** | The deck's review prompt sent as written to a reviewer that could not edit, with the diff, README, `AGENTS.md` and criteria; three or more findings verified by you and labelled honestly, two confirmed; your own inspection compared with it; two focused fixes with reasons and diffs; the final suite green; an honest demo-readiness line | R3 L8 L9 L10 L11 |
| **Evidence and honesty** | §1 complete; no secrets or `node_modules`; §9 and §10 your own; `AI_USAGE.md` complete; `submission.yml` passes the validator and its numbers match the re-run; the PR is open with 3 or more meaningful commits | B2 L1 L12 |

**A FAIL you report and explain costs you nothing extra; one you hide costs the whole criterion.**
A criterion is Complete when the checks it names pass. A failing check you report and explain in
§9 can lower its own criterion to Partial, and never anything else.

**Not accepted:** an LLM that decides availability · an API key, or a provider call, anywhere in
`src/` · a booking rule changed to make a test pass · deleted or skipped old tests · findings
labelled from the reviewer's confidence without looking · "the tests pass" without pasted output ·
real names, keys or personal data anywhere · a merged PR, a repo link, or an emailed submission.

---

## 11. FAQ

**Do I need an OpenAI (or any) API key?** No. The mock adapter is the graded feature. A real model is
optional and must run on a server you control, never in the page.

**Bolt.new put the API call in `App.tsx`.** That is the most common finding of this lab, and X4 or X5
will fail. Ask for the mock adapter instead, or move the real call behind a server and keep it out
of `src/`. If the reviewer in Part 6 does not flag it, that is worth a line in §7.4.

**My explanation is the same as the fallback text.** That is fine for a mock: it builds a sentence
from the reason code. What makes it a mock *adapter* is that `explainAvailability` calls it through
the same contract a model would use, with the timeout and the output check around it.

**The reviewer found nothing confirmed.** Look at what it was given (the diff, not just one file?),
then at its claims about tests and security: "the API key is exposed" in a project with no key is
`unsupported`. You may add your own findings; two must be confirmed in the end. If your code
really has nothing, write a test for a failure case that is not covered yet and see whether it
passes.

**Can I change `canBook`?** Only without changing what it returns. Every Week 10 test stays and passes
(F1). Making it call `availabilityReason` is a refactor; changing a comparison is not.

**I started from Week 08.** Then you have no `AGENTS.md`. Give the reviewer the README and the
criteria, and say in §7.1 that there were no repository instructions.

**Where does the grader run my files?** The checker reads them and runs nothing. The grader runs your
suite in `app/` in an isolated container, without network access.
