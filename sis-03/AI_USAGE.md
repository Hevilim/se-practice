# AI Usage Disclosure — SIS #03

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched | Reused from |
| --- | --- | --- | --- | --- |
| Claude (claude.ai) | Claude Opus 5.5 | the plan (stage A) | report.md section 11 B1 | week-05 |
| Claude (claude.ai) | Claude Opus 5.5 | Python v1 (stage B) | `code/original/booking_v1.py` | week-05 |
| Bolt.new | not displayed | web prototype v1 (stage B) | `web/original/` | week-06 |
| Claude (claude.ai) | Claude Opus 5.5 | critique (stage C) | report.md section 8 and 11 B4 | this SIS |
| Claude (claude.ai) | Claude Opus 5.5 | repair (stage D) | `web/final/project/src/App.tsx`, `web/final/project/package.json`, `web/final/project/package-lock.json` | this SIS |
| Claude (claude.ai) | Claude Opus 5.5 | copying the week-05 and week-06 files, running the cases with Playwright, screenshots, report text in sections 1, 3 to 9, 11 to 13, commits | report.md, evidence/, code/, web/, submission.yml | this SIS |

Sections 2 and 10 of report.md were written by me without AI.

**The assistant wrote, or helped write, my tests in `code/`:** yes
<!-- Either answer is allowed. If "yes": say which tests, and how you checked that their EXPECTED
     values come from AC1–AC5 and not from what the generated code happens to return. -->
All 35 tests come from week-05 and were written with Claude. Every expected value comes from AC1 to AC5 or the contract, not from running the code. The checker shows that the tests catch all 10 faulty versions (M1 to M10).

**`code/original/` and `web/original/` hold the AI's first versions exactly as returned:** yes

**Every result in report.md section 5 was actually run or seen, not assumed:** yes

**Everything I submitted, I can explain and defend in class — including the overlap condition
and what the agent did in section 9:** no

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the line. An honest entry here costs far less than a blank one that turns out to be untrue. -->
The overlap check in code/booking.py line 37, if start < booked_end and booked_start < end. The tests show that it works, but I cannot explain it well without help yet.

Signed: Karim Aliyev
Date: 25.10.2026
