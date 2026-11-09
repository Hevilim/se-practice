# AI Usage Disclosure — SIS #04

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Date | Used for | Which files it touched |
| --- | --- | --- | --- | --- |
| Claude (claude.ai) | Claude Opus 5.5 | 9.11.2026 | codebase analysis (Task 1) | none, the answer only (report 8.1) |
| Claude (claude.ai) | Claude Opus 5.5 | 9.11.2026 | improvement plan | none, the answer only (report 8.2) |
| Claude (claude.ai) | Claude Opus 5.5 | 9.11.2026 | feature extension (Task 2) | app/src/filter.ts, checkRoom in app/src/booking.ts (report 8.3) |
| Claude (claude.ai) | Claude Opus 5.5 | 9.11.2026 | refactoring (Task 3) | app/src/rooms.ts, app/src/booking.ts, app/src/App.tsx, app/package.json, app/package-lock.json, app/README.md, diagrams/before.puml, diagrams/after.puml |
| Claude (claude.ai) | Claude Opus 5.5 | 9.11.2026 | tests (Task 4) | app/src/filter.test.ts, app/src/booking.test.ts |
| Claude (claude.ai) | Claude Opus 5.5 | 9.11.2026 | running the tests and the checker, the five screenshots, the text of report.md sections 1 to 9, commits | evidence/, report.md, AI_USAGE.md, submission.yml |

The three exchanges in report section 8 were one chat, run with claude -p in Claude Code in an empty folder, with no tools and no access to my files. All other work was done by the same model in Claude Code in my repository. The screenshots were taken with Playwright in Google Chrome from the local dev server.

<!-- Delete rows you did not use the assistant for; add rows for anything else. The optional
     extension (an existing skill or a read-only MCP server) goes here too, with its permissions. -->

**The assistant wrote, or helped write, tests in `app/`:** yes
All tests in app/src/filter.test.ts (8 from the answer in 8.3, one added: F5 AC5) and the two reasonsFor tests at the end of app/src/booking.test.ts. The expected values were checked by hand against F1, F2 and AC1-AC5 before the code existed: the new tests failed first (Cannot find module ./filter, then checkRoom is not a function).

**Every run pasted in report.md was produced by my code on my machine (or Codespace), unedited:** yes
Only the terminal color codes were removed.

**Every number in report.md section 7 was measured the way its row says:** yes

**I shared no credentials, keys or private data with any tool:** yes

**Everything I submitted, I can explain and defend in class — including filterRooms, checkRoom and
why each module exists:** no

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the line. An honest entry here costs far less than a blank one that turns out to be untrue. -->
app/src/App.tsx, the line const room = matches.find((r) => r.id === roomId) ?? matches[0]; I do not fully understand how the selected room changes when it is filtered out.

Signed: Karim Aliyev
Date: 9.11.2026
