# AI Usage Disclosure — Week 10

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Zed Agent (sub-agent session, Zed editor) | Claude Opus 5.5 | read-only risk review (Task 2) | none — "WITHOUT editing files" (`git status` was empty afterwards) |
| Zed Agent (sub-agent session) | Claude Opus 5.5 | reading AGENTS.md and summarising it (Task 1, Practice #09 prompt) | none |
| Zed Agent (sub-agent session) | Claude Opus 5.5 | AGENTS.md review and patch draft (Task 6) | none. The draft was not applied as written; the approved, changed version was written into `app/AGENTS.md` (decisions in lab-report §6.2) |
| Zed Agent (sub-agent session) | Claude Opus 5.5 | the refactor for R3 (Task 8): plan first, then the approved, reduced change | `app/src/booking.ts`, `app/src/App.tsx`, new `app/src/availability.ts`, new `app/src/availability.test.ts` |
| Zed Agent (main session) | Claude Opus 5.5 | I asked it to do the whole Week 10 lab for me: run the commands, send the prompts above, check the claims against the files, write the regression test for R3, apply the approved AGENTS.md patch, take the two screenshots with a headless Chrome script, and draft `lab-report.md`, this file and `submission.yml` | `app/AGENTS.md`, `app/src/booking.test.ts` (test R3), one empty line in `app/src/App.tsx`, `evidence/*.png`, `lab-report.md`, `AI_USAGE.md`, `submission.yml` |

**The review in Task 2 ran in a mode where the assistant could not edit, and `git status` showed no
change afterwards:** no
<!-- If it edited anything, say what and how you undid it. -->
It did not edit anything, and `git status --short week-10` was empty afterwards. But the Zed sub-agent
was not in a technically locked mode: it only had the instruction "read tools only, no terminal, no edits".
Details are in lab-report §3.1.

**I labelled every claim in lab-report.md §3.2 after opening the cited file myself:** no
<!-- The Zed agent (main session) opened the cited files, ran lint, test:unit and typecheck, and wrote the labels. -->
The Zed agent (main session) opened the cited files and ran the commands, then wrote the labels.
I read the labels afterwards.

**Every change to `app/` was reviewed by me as a diff before I accepted it:** no
<!-- Name anything you rejected in §8; name here anything you accepted without reading. -->
The diffs were reviewed by the main Zed agent session before they were committed. It rejected the
`readonly` type change, the `Timeline` change and the dev-server run (lab-report §8.2), and five parts
of the AGENTS.md draft (§6.2). I read the final diffs in lab-report §6.3 and §8.2.

**I used another assistant as well (to explain a risk, to draft text in lab-report.md, …):** yes
<!-- If "yes": which one, the exact model, and for which section. -->
Yes: the main Zed Agent session (Claude Opus 5.5), the same model as the sub-agents. It drafted the
text of every section of lab-report.md, including §9.3 and §10.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes
The only formatting change is the two-space indent of the review answer in §3.1, explained there.

**I can explain every score in my register, and why my release decision follows from it, without
the assistant:** yes

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. An honest entry here costs far less than a blank one that turns out to be untrue. -->
The generic type `Rejection<B extends BookingInterval>` and `findRejections<B>` in `app/src/booking.ts`.
I understand what they do (the overlap rejection carries the room's own booking, with its title), but
I would not have written the generics myself.

Signed: Karim Aliyev
Date: 22.11.2026
