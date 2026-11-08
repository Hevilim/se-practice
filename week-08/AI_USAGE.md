# AI Usage Disclosure — Week 08

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude (claude.ai) | Claude Opus 5.5 | diagnosis without the skill (Task 4) | none — "Do not edit code" |
| Claude (claude.ai) | Claude Opus 5.5 | diagnosis with bug-detector (Task 5) | none — "Do not edit code" |
| Claude (claude.ai) | Claude Opus 5.5 | moving the project, pasting the buggy canBook, the BUG-A and BUG-B tests, SKILL.md and the ZIP, running both chats, both fixes, all test runs, install.png, report text, commits | app/src/booking.ts, app/src/booking.test.ts, skills/bug-detector/SKILL.md, skills/bug-detector.zip, evidence/install.png, lab-report.md, AI_USAGE.md, submission.yml |

**`skills/bug-detector/SKILL.md` was typed by me from the deck's text, not generated:** no
Claude wrote the file with the deck's text word for word. It did not generate new text, but I did not type it myself.

**I applied the patches myself, one minimal change per bug, after reviewing what the assistant
proposed:** no
<!-- If an assistant edited app/ directly, say which change and how you reviewed it. -->
Claude made the two changes in app/src/booking.ts, one commit each: < and > instead of <= and >= in the overlap check (BUG-A), and deleting bookings.push and its comment (BUG-B). They are the same as the patches both answers proposed. After each change it ran the BUG test and the full suite, see sections 8.1 and 8.2.

**I used another assistant as well (to explain a failure, to draft text in lab-report.md, …):** yes
<!-- If "yes": which one, the exact model, and for which section. -->
The same tool, Claude (claude.ai), Claude Opus 5.5, in a separate chat. It wrote the text of lab-report.md sections 2 to 10. It ran the two diagnosis chats with claude -p in Claude Code in an empty folder, with no access to my files: the no-skill chat with all skills turned off, the skill chat with only the Skill tool. Both used English output. An earlier try with two Claude Code agents was thrown away, because the no-skill agent used the bug-detector skill by itself and both agents read my repository. In the test runs only the terminal color codes were removed.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**I can explain both bugs and both fixes — which line, why it was wrong, which test proves the
fix — without the assistant:** no

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. An honest entry here costs far less than a blank one that turns out to be untrue. -->
app/src/booking.test.ts, test R05 from Week 07: the part with Object.freeze. I do not fully understand how a frozen array makes a change in canBook throw.

Signed: Karim Aliyev
Date: 8.11.2026
