# AI Usage Disclosure — Week 11

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude Code (claude -p, a separate session) | Claude Opus 5.5 | the feature: mock adapter, explain.ts, the button (Task 3) | app/src/booking.ts, app/src/booking.test.ts (new tests only), app/src/explain.ts, app/src/explain.test.ts, app/src/App.tsx |
| Claude Code (no tools, a new empty folder each time) | Claude Opus 5.5 | the three prompts compared (Task 4) | none — a fresh chat per prompt |
| Claude Code (plan mode, only Read, Glob and Grep) | Claude Sonnet 5.5 | read-only agentic review (Task 6) | none — "Do not edit files" |
| Claude Code (main session) | Claude Opus 5.5 | the two fixes (Task 7). I also asked it to do the whole lab: run the commands, send the prompts, write tests E1-E9, take the screenshots with a headless Chrome script, verify the findings and draft lab-report.md, this file and submission.yml | app/src/explain.ts, app/src/explain.test.ts, evidence/*.png, lab-report.md, AI_USAGE.md, submission.yml |

**Every file the assistant changed in Task 3 was reviewed by me before I accepted it (§4.2):** no
<!-- Name anything you accepted without reading. -->
The main Claude Code session read every changed file and wrote the decisions in lab-report 4.2. It asked the builder to change App.tsx and explain.ts (message 2).

**No API key, token or provider call is anywhere in `app/src/`:** yes
The checker passes X4 and X5, and App.tsx has no fetch.

**The review in Task 6 ran in a mode where the assistant could not edit, and `git status` showed no
change afterwards:** yes
<!-- If it edited anything, say what and how you undid it. -->
It ran in plan mode with only read tools. git status showed no change afterwards.

**I labelled every finding in §7.3 after verifying it myself:** no
The main Claude Code session verified the findings with tests and by reading the code, and wrote the labels.

**I used another assistant as well (to explain an error, to draft text in lab-report.md, …):** yes
<!-- If "yes": which one, the exact model, and for which section. -->
Yes: the main Claude Code session (Claude Opus 5.5). It drafted every section of lab-report.md except section 10, and this file.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes
In lab-report 4.1 and 5.2 the lines with three backticks inside the pasted answers were removed, so the code blocks do not break. This is said there.

**I can explain how explainAvailability handles a timeout and a contradicting answer, without the
assistant:** yes / no

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. An honest entry here costs far less than a blank one that turns out to be untrue. -->

Signed: Karim Aliyev
Date: 27.11.2026
