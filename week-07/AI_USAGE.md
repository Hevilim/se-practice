# AI Usage Disclosure — Week 07

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude (claude.ai) | Claude Opus 5.5 | the first test suite (Task 3) | suites/first/booking.test.ts, app/src/booking.test.ts |
| Claude (claude.ai) | Claude Opus 5.5 | the improvement prompt (Task 5) | app/src/booking.test.ts (tests R01-R05) |
| Claude (claude.ai) | Claude Opus 5.5 | extracting canBook, running the suites and the three mutants, the UI checks with Playwright, report text, commits | app/src/booking.ts, app/src/App.tsx, app/package.json, app/src/booking.test.ts (tests R06, R07), evidence/ui-1.png to ui-5.png, lab-report.md, AI_USAGE.md, submission.yml |

**I used an assistant to extract `canBook` (Task 1), or to fix a defect in it:** yes
<!-- If "yes": which change, in which file, and how you checked that the behaviour did not change. -->
Claude (claude.ai), Claude Opus 5.5, moved the five checks from evaluateBooking in src/App.tsx into canBook in src/booking.ts, with the same conditions. App.tsx now calls canBook for the decision. It checked the page in Chromium with Playwright after the change: Auditorium B with now 09:00 gave the same results as before (11:00-12:00 and 12:00-14:00 Available, 10:30-11:30, 12:00-14:01 and 09:00-09:30 Unavailable, the blocked Innovation Lab Unavailable). No defect was fixed in canBook.

**I used another assistant as well (to explain a failure, to draft text in lab-report.md, …):** yes
<!-- If "yes": which one, the exact model, and for which section. -->
The same tool, Claude (claude.ai), Claude Opus 5.5, in a separate chat from the one that wrote the tests. It wrote the text of lab-report.md sections 2 to 10, ran all Vitest runs on my computer, ran the three mutants and restored booking.ts after each one, and took the five screenshots with Playwright in Chromium on the local page. The two test chats wrote the test file straight into app/src/booking.test.ts. The first file was then copied to suites/first/ without changes. In the mutant runs in section 7 only the terminal color codes were removed, the text is unchanged.

**`suites/first/` holds the assistant's first test file exactly as it generated it:** yes

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**I can explain every test in my final suite — its input, its expected result and the AC behind
it — without the assistant:** yes / no

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. An honest entry here costs far less than a blank one that turns out to be untrue. -->

Signed: Karim Aliyev
Date: 6.11.2026
