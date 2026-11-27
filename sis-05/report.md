# SIS #05 — Report

**Name:**
**Group:**
**Date:**

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup and the project

| | |
| --- | --- |
| Project (name, and what it does in one line) | |
| Language and stack | |
| Where it comes from (my own / Smart Campus / other: say what) | |
| Baseline commit — the project brought in unchanged (§3 of the README) | |
| Assistant (tool) | |
| Exact model (with its version, or `not displayed`) | |
| Where I ran the commands (my computer / Codespace / Bolt terminal / …) | |

---

## 2. Task 1 — baseline and context

### 2.1 Repository map

Real paths in `project/`.

| Part | Where (paths) and what it does |
| --- | --- |
| Entry points | |
| Modules | |
| Dependencies (and where they are declared) | |
| Tests | |
| Build / run scripts | |

### 2.2 Commands

At least three. **Kind:** `test`, `lint`, `type`, `build` or `run`. **Exists:** `yes` / `no`.
**Result:** `pass`, `fail`, `missing` or `not run` (say why in the note).

| Command | Kind | Exists | Result | Note |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |

### 2.3 Baseline output

The **real** output of the baseline test run (or of running the program, if there were no tests):

```text
(paste here)
```

### 2.4 Weaknesses and missing checks

At least three. **Evidence:** a file and line, or a command and its output. **Kind:** `fact` (you saw
it) or `assumption` (not yet shown).

| # | Weakness or missing check | Evidence | Kind |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

### 2.5 Acceptance criteria

Three to five things that must still be true after every change, and how you check each one.

| ID | Must remain true | How I check it (a test, a command, a step) |
| --- | --- | --- |
| AC1 | | |
| AC2 | | |
| AC3 | | |

---

## 3. Task 2 — agent instructions

### 3.1 The file and how the assistant reads it

| | |
| --- | --- |
| File (`project/AGENTS.md` or `project/CLAUDE.md`) | |
| Created or improved? | |
| Does the assistant load it by itself? (`yes` / `no, I pasted it` / `not sure, I pasted it`) | |

### 3.2 What it covers

Where each topic is in the file (the heading, or the line).

| Topic | Where in the file |
| --- | --- |
| Purpose | |
| Architecture | |
| Setup | |
| Safe commands | |
| Coding conventions | |
| Test expectations | |
| Forbidden actions | |

---

## 4. Task 3 — a focused pattern decision

### 4.1 The maintainability problem

<!-- One problem: the file and lines, and why it makes the code harder to change. Write below this line -->

### 4.2 The pattern I evaluated

<!-- Strategy, Adapter, or another you can name; what it would change for this problem. Write below this line -->

### 4.3 My decision, before and after

**Decision:** applied / not warranted

<!-- Why, and the structure before and after (functions, modules, or a diagram in a code block). Write below this line -->

### 4.4 The acceptance criteria still hold

The real output of the same checks, run after the decision:

```text
(paste here)
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
