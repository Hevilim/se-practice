# AI Usage Disclosure — Week 05

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude (claude.ai) | Claude Opus 5.5 | the plan (Task 1) | lab-report.md section 2 |
| Claude (claude.ai) | Claude Opus 5.5 | the first version, v1 (Task 2) | code/original/booking_v1.py, code/booking.py |
| Claude (claude.ai) | Claude Opus 5.5 | debug help and critique (Task 4 and Task 5) | lab-report.md sections 5 and 6, code/booking.py |
| Claude (claude.ai) | Claude Opus 5.5 | tests, running the checker, report text, commits | code/test_booking.py, lab-report.md, AI_USAGE.md, submission.yml |

**The assistant wrote, or helped write, my tests in `code/`:** yes
<!-- Either answer is allowed. If "yes": say which tests, and how you checked that their EXPECTED
     values come from AC1–AC5 and not from what the generated code happens to return. -->
All 35 tests were written with Claude. Every expected value comes from AC1 to AC5 (see the AC column in section 4), not from running the code. The checker shows that all contract tests pass on a correct version and catch all 10 faulty versions.

**`code/original/` holds the assistant's first answer exactly as returned:** yes

**Everything I submitted, I can explain and defend in class — including the overlap condition:** no

**Anything I accepted from the AI without fully understanding it:** the overlap check in code/booking.py, the line if start < booked_end and booked_start < end. The tests show that it works, but I cannot explain it well without help yet. The report text, also sections 9 and 10, was written with Claude.

Signed: Karim Aliyev
Date: 07.10.2026
