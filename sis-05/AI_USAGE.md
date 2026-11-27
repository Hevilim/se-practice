# AI Usage Disclosure — SIS #05

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude Code (claude -p, plan mode, read tools only) | Claude Opus 5.5 | read-only risk review (Task 4) | none — "do not modify files" |
| Claude Code (claude -p, plan mode, read tools only) | Claude Opus 5.5 | AGENTS.md draft, Strategy evaluation, the R1 and R2 patches (exchanges 1, 2 and 4) | none; the main session wrote project/AGENTS.md and applied the patches |
| Claude Code (main session) | Claude Opus 5.5 | I asked it to do the whole SIS: copy the project, run every command, write project/README.md, review and apply the drafts, verify the findings, write the R1 and R2 tests and fixes, and write report.md (all sections, including the weaknesses, labels, scores, decisions and the reflection), this file and submission.yml | project/README.md, project/AGENTS.md, project/.gitignore, project/booking.py, project/test_booking.py, report.md, AI_USAGE.md, submission.yml |

**The risk review ran in a mode where the assistant could not modify files, and `git status` showed
no change afterwards:** yes
It ran in plan mode with only Read, Glob and Grep. git status showed no change afterwards.

**Every finding in report.md §5.2 was labelled after I opened the file or ran the command myself:** no
The main Claude Code session ran every check command and wrote the labels.

**Every change to `project/` was reviewed by me as a diff before I accepted it:** no
<!-- Name anything you accepted without reading. -->
The main Claude Code session reviewed the diffs and applied them. The diffs are in report.md §8.

**`AGENTS.md`: the assistant loaded it by itself / I pasted it / I did not use it with an assistant:**
<!-- Say which. The brief asks you to disclose a pasted file. -->
The assistant did not load it by itself. Every prompt after Task 2 told it to read AGENTS.md first, and it read the file with its Read tool.

**The weaknesses, the labels, the scores, the decisions and the reflection are my own judgement,
written by me:** no
I asked Claude Code to do the whole SIS, so the main session wrote these parts, including §10. README §18 says such parts score Not met; I accepted that.

**Every output in report.md was pasted from a real run, unedited:** yes

**No real credentials, confidential data or personal data are anywhere in `sis-05/`:** yes

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. An honest entry here costs far less than a blank one that turns out to be untrue. -->
All of report.md and the changes in project/ were written by Claude Code. I did not check them line by line myself.

Signed: Karim Aliyev
Date: 27.11.2026
