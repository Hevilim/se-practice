# SIS #05 — Repository Customization, Agent Readiness and Risk Governance

**Course:** AI-Driven Software Engineering (Fall 2026, KBTU SITE)
**SIS #05** · 2 points · individual · AI-use level: **D (AI-integrated, disclosure required)**
**Deadline:** Sunday 6 December 2026, 23:59 (Almaty)

> **This time it is your repository.** Choose a small, non-sensitive project of your own: a task
> tracker, an expense calculator, a notes app, an inventory tool, or another small program you can
> run. You prepare it for a coding agent (an `AGENTS.md` with safe and forbidden actions), decide
> whether one design pattern is justified, have an AI propose risks without touching the files,
> verify them, score them, fix two, and make a release decision you can defend.
>
> **Any language, any project you are allowed to share.** The Smart Campus project is **not
> required**. You may use it, but then everything in this SIS is new work: nothing copied from your
> Week 10 or Week 11 worksheet, and the findings must be about the project as it is now.
>
> **Your choices, frozen once made:** the project, its language, and the assistant (record the
> **exact model**: "ChatGPT" is a tool, not a model; write `not displayed` if the tool hides it).
> **The same for everyone:** the tasks and their order (§4), the file layout (§2), the risk scale,
> the readiness rows (§7), and the rule that every claim needs evidence.

---

## 1. The idea

Weeks 09–11 gave you the pieces: a repository that tells an agent how to behave, a readiness audit,
a risk register, background agents, and an AI reviewer whose findings you verify. This SIS puts them
together on a codebase **you** chose, so nothing has been prepared for you to find.

Two rules carry the whole assignment, from the brief:

> **Use at least one AI assistant, but independently inspect, test and approve every finding.**
> **No real credentials, confidential data or fabricated test results.**

Slide numbers in this README refer to the decks posted in our Teams (Lessons #09–#11).

---

## 2. What you hand in

By the deadline, your branch `sis-05` must contain:

```
sis-05/
├── README.md                  # this file (read-only)
├── report.md                  # THE worksheet: fill in all 11 sections
├── AI_USAGE.md                # AI disclosure
├── submission.yml             # machine-readable declaration: facts only
├── project/                   # your project, brought in unchanged in the baseline commit (§3)
│   ├── README.md              #   its README (yours, or one you write in Task 1)
│   ├── AGENTS.md              #   created or improved in Task 2 (or CLAUDE.md)
│   ├── <the source files>
│   └── <the tests>            #   at least one testable behaviour, at least one test at the end
├── evidence/                  # optional: screenshots of runs or of the app (Task 7)
└── tests/
    ├── check_sis.py           # provided checker: do not edit
    └── validate_submission.py # provided validator: do not edit
```

**Never commit** `node_modules/`, a virtual environment (`venv/`, `.venv/`), a `.git` folder inside
`project/`, a `.env` file, or any real key, password, token or personal data. `project/` stays under
10 MB: source files, tests, configuration and docs only.

---

## 3. Starting point (~30 min)

1. **Choose the project.** It must run, and it must have **at least one testable behaviour** (brief,
   slide 8). Small is better: a few hundred lines is plenty. Nothing confidential, nobody else's
   private code, no real personal data.
2. Branch and folder:
   ```text
   git checkout main && git pull && git checkout -b sis-05
   # unzip SIS_05.zip into the root of your se-practice repository, so sis-05/README.md exists
   ```
3. **Copy the project into `sis-05/project/`** as it is now: the files only, not its `.git` folder,
   not `node_modules/` or a virtual environment.
4. Commit: `sis-05: baseline project, unchanged`. **This is your baseline** (brief: "preserve a
   baseline commit"). Record its hash (`git rev-parse --short HEAD`) in §1. Everything after it is
   your change, and the grader reads the diff from this commit to your last.

From here on you work in `sis-05/project/`.

---

## 4. The order of work

The brief's suggested workflow (slide 28), one section of `report.md` each:

| # | Task | `report.md` | Time |
| --- | --- | --- | --- |
| 1 | Baseline and context | §2 | ~45 min |
| 2 | Agent instructions: `AGENTS.md` | §3 | ~30 min |
| 3 | A focused pattern decision | §4 | ~40 min |
| 4 | Read-only AI risk review | §5 | ~30 min |
| 5 | Risk register | §6 | ~30 min |
| 6 | Agent-readiness audit | §7 | ~20 min |
| 7 | Two mitigations and verification | §8 | ~60 min |
| 8–9 | Background-agent safeguards; release decision | §9 | ~20 min |
| 10 | AI reflection | §10 | ~20 min |
| — | AI evidence appendix | §11 | as you go |

---

## 5. Task 1 — baseline and context → `report.md` §2

1. **Repository map** (§2.1): the entry points, the modules and what each does, the dependencies
   (and where they are declared), the tests, the build or run scripts. Real paths in `project/`.
2. **Run what exists** (§2.2): the tests, a linter or type checker, a build, the program itself.
   For each command: does it exist (`yes` / `no`), and the result (`pass`, `fail`, `missing`,
   `not run` with why). At least three commands.
3. **Paste the real output** of the baseline test run in §2.3. If the project had no tests at all,
   paste the output of running the program and say so; you add a test in Task 7.
4. **Three or more weaknesses or missing checks** (§2.4), each with evidence: a file and line, or a
   command and its output. Label each `fact` (you saw it) or `assumption` (you think so, not yet
   shown). An AI suggestion you have not checked is an assumption.
5. **Three to five acceptance criteria** (§2.5), AC1–AC5, that must still be true after every change
   you make, and how you check each one (a test, a command, a step).

## 6. Task 2 — agent instructions → `report.md` §3

Create `project/AGENTS.md` (or improve the one you have; `CLAUDE.md` is fine for a tool that reads
it). It must cover, under headings an agent can find:

| Topic | What it says |
| --- | --- |
| Purpose | what the project is for |
| Architecture | which file or module does what |
| Setup | how to install and run it |
| Safe commands | the exact commands to test, lint, build and run, and **every one must exist** |
| Coding conventions | the rules you follow in this codebase |
| Test expectations | what must pass before a change is done |
| Forbidden actions | **never** commit secrets; **never** deploy to production; **never** run destructive commands; **never** change dependencies without review (brief, slide 13) |

If your assistant does not load the file automatically, **paste its relevant parts into the
conversation and say so** in §3.1 (brief: "disclose this"). Record in §3.2 where each topic is in the
file.

## 7. Task 3 — a focused pattern decision → `report.md` §4

1. Find **one** maintainability problem (slide 14): duplicated conditionals, UI mixed with business
   logic, or tightly coupled dependencies. Point at the file and lines.
2. Evaluate a small pattern, **Strategy** or **Adapter** (or another you can name), against that
   problem. Would it make the code simpler to change, or only longer?
3. **Implement at most ONE focused refactoring, or explain why no pattern is warranted** (slide 15).
   Both are valid. A pattern added with no problem it solves is not.
4. Compare the structure before and after (a short description, a list of functions, or a diagram),
   and **prove the acceptance criteria still hold**: the same tests, run again, in §4.4.

Commit: `sis-05: <pattern or no-pattern> decision`.

## 8. Task 4 — read-only AI risk review → `report.md` §5

1. Make sure the assistant **cannot modify files** (Plan mode in Bolt.new or Claude Code, or a chat
   with pasted files). Afterwards, `git status` must show no change.
2. Ask it to propose risks. Write the prompt yourself; it must say that nothing may be modified and
   that it must not invent test results. Paste what you sent and the answer in §5.1.
3. **Investigate at least FIVE candidate findings spanning at least THREE categories** (slide 16):
   `correctness`, `maintainability`, `security`, `dependency`, `agent operations`. For each, open the
   file or run the command, and classify it (slide 17):

| Label | When |
| --- | --- |
| `confirmed` | you saw it: the file, line, command output or behaviour you can reproduce |
| `plausible` | it could be true, but you could not verify it ("plausible / unverified") |
| `unsupported` | the cited file, line or behaviour is not there, or contradicts what you see |

## 9. Task 5 — risk register → `report.md` §6

One row per risk (slide 18): **ID** (`R1`, …), **category** (the five above), **cause → event →
consequence**, **component** (a path in `project/`, or `missing: <the check that does not exist>`),
**evidence**, **status** (`confirmed` / `plausible`), **L** and **I** (1–3), **score = L × I** (1–9),
**mitigation**, **owner**, **verification plan**. At least five risks, at least two confirmed.

```text
Likelihood: 1 unlikely, 2 possible, 3 likely.
Impact:     1 minor,    2 moderate, 3 serious.
Score = likelihood × impact (1-9).
```

Then rank the **top two confirmed risks** for corrective action (§6.2), highest score first. **Do not
invent execution evidence**: a risk you did not reproduce is `plausible`, whatever the assistant said.

## 10. Task 6 — agent-readiness audit → `report.md` §7

Fill in the rows (slides 19–20), `yes` or `no`, with the evidence: the file, script or command.

| Row | Level | `yes` when `project/` has … |
| --- | --- | --- |
| 1a | 1 Baseline | automated **tests** that run with one command |
| 1b | 1 Baseline | a **lint or type check** configured |
| 1c | 1 Baseline | a **build or run** command that works from a clean copy |
| 1d | 1 Baseline | **pinned dependencies** (a lockfile, pinned versions, or no third-party dependencies at all) |
| 2a | 2 Documented | a **README that is accurate**: its commands work as written |
| 2b | 2 Documented | **reproducible setup**: a stranger could set it up from the README alone |
| 2c | 2 Documented | an **`AGENTS.md`** with safe commands and forbidden actions |
| 3a | 3 Agent-ready | **CI** that runs the checks on every push |
| 3b | 3 Agent-ready | **logging** or error output an agent can read |
| 3c | 3 Agent-ready | **security safeguards**: secret scanning, input validation, dependency audit |
| 3d | 3 Agent-ready | a **review gate**: `AGENTS.md` or the repository requires human approval before merge |

**The level** (§7.2), as in Week 10: a level is reached when at least 80% of its rows are `yes`
**and** every level below it is reached: 4 of 4 at Level 1, 3 of 3 at Level 2, 4 of 4 at Level 3.
The brief's levels are 1 Baseline, 2 Documented and 3 Agent-ready; **a project that does not reach
Level 1 is level `0`**, and says so. Then list the **missing evidence** for the next level.

## 11. Task 7 — two mitigations and verification → `report.md` §8

1. Implement **two minimal mitigations for confirmed risks** (slide 21), normally your top two. Ask
   the assistant for a patch if you like, but **review each diff before accepting it**, and say what
   you rejected.
2. **Add or improve a targeted automated test** for each when it is feasible: a test whose name
   starts with the risk ID (`test_R1_…`, `test('R1 …')`) and that **fails before** the fix. Paste
   that failing run. If a test is not feasible, say why.
3. Run the baseline checks and the final checks (§8.3, the real output), and **list every test or
   check you did not run** (slide 22).
4. **Update the risk scores** after each mitigation (§8.4): the score after may not be higher than
   before, and each change needs its evidence. Explain the remaining limitations and trade-offs.

Commit each mitigation separately: `sis-05: mitigate R<n> - <what>`.

## 12. Tasks 8–9 — background-agent safeguards and the release decision → `report.md` §9

1. **Design a hypothetical asynchronous agent task** on this project (slide 23). You do **not** need
   a paid background agent. Fill in the eight rows of §9.1: the task, isolation (branch or worktree),
   allowed files, commands, time limit, prohibited operations, required artifacts (change summary,
   diff, test logs, build result, risk notes), and the human approval gate with failure and
   rollback handling (slide 24).
2. **Choose GO, CONDITIONAL or NO-GO** for the reviewed version (slide 25):
   - **GO**: critical checks pass and no unacceptable unresolved risks remain.
   - **CONDITIONAL**: known limitations have explicit controls and owners.
   - **NO-GO**: serious risks or critical verification gaps remain.

   **GO is not allowed while any confirmed risk still scores 6 or more** (its §8.4 score if you
   mitigated it, its §6.1 score if not), as in Week 10. Support the decision in 80–150 words with the
   test evidence, the register and the readiness level. Name at least two risk IDs.

## 13. Task 10 — AI reflection → `report.md` §10

**200–300 words, in your own words, without the assistant** (slides 26–27):

1. Which assistant and model did you use, and what context did it receive?
2. One useful AI suggestion, and one inaccurate, weak or unverified one.
3. What did you personally check, and how did the tests change your decisions?
4. Did the repository instructions (`AGENTS.md`) improve the process? What should improve next?

## 14. The AI evidence appendix → `report.md` §11

**At least three exchanges** (slide 32), one per table: the tool and date, the exact model, a
summary of the prompt, the output you used, the problems you found in it, the changes you made, and
how you verified it. Normally: the risk review, a mitigation, and the pattern decision or
`AGENTS.md`.

---

## 15. Check your work

From inside `sis-05/`:

```text
python tests/check_sis.py
python tests/validate_submission.py
```

The checker runs 23 checks. **It never runs your project and never judges its quality.** It reads
files:

| Checks | What they look at |
| --- | --- |
| **P1–P6** | `project/`: source files and a README (P1); clean: no `.env`, `node_modules`, virtual environment, nested `.git` or key-like string, under 10 MB (P2); an `AGENTS.md` or `CLAUDE.md` (P3) covering the seven topics (P4) and forbidding the four actions (P5); at least one test file (P6). |
| **R1–R2** | §2.3 a real baseline output (R1); §8.3 the final output (R2). |
| **L1–L15** | The report: setup (L1), map and commands (L2), weaknesses with evidence (L3), AC1–AC5 (L4), `AGENTS.md` coverage and loading (L5), the pattern decision (L6), the review: read-only, prompt, answer, five findings in three categories (L7), the register: L × I, components, top two (L8), the audit rows and the level by the 80% rule (L9), two mitigations with diffs and residual scores (L10), the final checks and what was not run (L11), the eight safeguard rows (L12), the release decision (L13), the reflection, 200–300 words (L14), three complete AI exchanges (L15). |

The first run on the untouched folder gives `0 PASS · 17 FAIL · 6 ERROR`. That is the intended start.

**A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.** List
every FAIL or ERROR you keep in `submission.yml` `known_fails` and explain it in §11's last table.

## 16. The declaration — `submission.yml`

Facts only. `checker.commit` is the commit you ran the checker at; the numbers are re-run at the
last commit of your pull request, and numbers that do not match cost the *AI evidence & workflow*
criterion. `project.baseline_commit` is the commit of §3.

## 17. Submit

1. Push the branch: `git push -u origin sis-05`.
2. Open a Pull Request `sis-05 → main` in your own repository. Title: `SIS 05 — Repository
   Customization and Risk Governance`. Write the description in the fixed shape from `SETUP.md` §4.
3. **Leave the PR open. Do not merge it.**
4. In the Teams assignment *SIS 05*: **+ Add work → Link → paste the pull request URL.**

The brief asks for an e-mail. **That does not apply to our groups.** The PR holds the project
(baseline and final), the README, `AGENTS.md`, the acceptance criteria, the outputs, the register,
the audit, both mitigations, the decisions and the appendix.

**Deadline:** Sunday 6 December 2026, 23:59 (Almaty). Late submissions follow the course policy.

---

## 18. Grading — 2 points, 8 criteria × 0.25

| # | Criterion | Full 0.25 | Half 0.125 | Zero |
| --- | --- | --- | --- | --- |
| 1 | **Baseline & context** | Project committed unchanged as the baseline; a real repository map; commands run with real output; three or more weaknesses with evidence, facts kept apart from assumptions; 3–5 acceptance criteria with how each is checked | Map or weaknesses thin, or a weakness with no evidence | No baseline, or output that was not run |
| 2 | **Agent instructions & readiness** | `AGENTS.md` covering all seven topics with commands that exist and the four forbidden actions; loading disclosed; every audit row with evidence; the level by the 80% rule; missing evidence named | One topic or row missing, or a level not justified | No `AGENTS.md`, or audit rows claimed with nothing behind them |
| 3 | **Pattern decision** | One concrete maintainability problem located; a pattern evaluated against it; at most one focused refactoring or a reasoned "not warranted"; before/after compared; the acceptance criteria shown to hold | The problem generic, or the comparison thin | A pattern with no problem it solves, or behaviour broken |
| 4 | **Risk review & register** | A read-only review; five or more findings in three categories, each verified and labelled; a register of five or more specific risks with real components, evidence and scores = L × I; the top two justified | A label without its check, or generic risks | The assistant's list pasted as confirmed, or invented evidence |
| 5 | **Mitigation & verification** | Two confirmed risks mitigated with reviewed diffs, rejected changes named; a test per risk that fails first, or why not feasible; baseline and final output; tests not run listed; residual scores revised | One mitigation unverified, or no test without a reason | Missing, or "tests pass" with no output |
| 6 | **Safeguards & release** | Eight specific safeguard rows for this project; a decision that follows from the register, the tests and the level, naming risk IDs; no GO while a confirmed risk scores 6 or more | Safeguards generic, or a decision with thin reasons | Missing, or a GO against the rule |
| 7 | **AI reflection** | 200–300 words in your own words, answering all four questions with specifics from this work | Generic, or a question unanswered | Missing, or written by the assistant |
| 8 | **AI evidence & workflow** | 3+ complete exchanges; `AI_USAGE.md`; `sis-05` branch, 3+ own commits; open PR in the standard shape; `submission.yml` validating; no secrets or personal data | One element missing | Committed to `main`, PR merged, no disclosure, **or declared checker numbers that don't match the re-run** |

**A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.** Your
project, its language and your assistant never affect the mark.

**Parts you write yourself.** The weaknesses, the labels, the scores, the decisions, the reflection
are your judgement. A part handed to the assistant scores Not met, disclosed or not; a fabricated
exchange, run or finding scores Not met.

**Not accepted (0 for the SIS):** a file upload or an e-mail instead of a pull-request link · a
report that is not in `sis-05/report.md` · a merged PR, a repository link or a branch with no PR ·
fabricated prompts, outputs, test runs or findings · real credentials or personal data anywhere.

---

## 19. FAQ

**My project has no tests.** Then 1a is `no`, it is a weakness in §2.4, and probably a risk. Task 7
adds at least one test (P6), and the baseline output in §2.3 is a run of the program instead.

**My project has no dependencies at all.** Then 1d is `yes`: nothing to pin. Say so as the evidence.

**Can I use the Smart Campus app?** Yes (the brief: "not required"). Then nothing is copied from your
Week 10 or Week 11 worksheet: the register, the audit and the decisions are new, about the code as
it is now.

**No pattern fits my problem.** Then write why, with the problem located. "Not warranted" with a
reason is a full answer; a Strategy added to look busy is not.

**The assistant edited files during the review.** Undo it (`git checkout -- project`), note it in
§5.1, and send the prompt again read-only. An assistant that ignores "do not modify" is itself an
`agent operations` risk.

**My language is not JavaScript or Python.** Any language works. The checker reads file names
(`test_*.py`, `*.test.ts`, `*_test.go`, `*Test.java`, `tests/`…), the report and your pasted output;
it runs nothing.

**Where does the grader run my project?** It does not run it. It reads the diff from your baseline
commit, your pasted output and your report, and re-runs only the checker.
