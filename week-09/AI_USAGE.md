# AI Usage Disclosure — Week 09

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude (claude.ai) | Claude Opus 5.5 | Part 2 — writing the calls for R1, R2, R3 | calls/ (saved by Claude, unedited) |
| Claude (claude.ai) | Claude Opus 5.5 | writing check_room.json, running the checker and the three chats, saving the calls, report text, commits | tool/check_room.json, calls/r1.json, calls/r2.json, calls/r3.txt, lab-report.md, AI_USAGE.md, submission.yml |

**I wrote `tool/check_room.json` myself:** no
Claude wrote the whole file. The first version failed S08, so Claude added "required" and "additionalProperties": false to the items of bookings. It was checked with tests/check_tool.py: the final run passes D1 to D6 and S01 to S12.

**I used an AI to explain a JSON Schema keyword or a check:** no

**Every reply in `calls/` and in lab-report.md section 4 is exactly what the model returned:** yes
The three chats were run with claude -p in Claude Code, each in its own empty folder, with no tools and no access to my files. A first try of the three chats was thrown away, because the R3 answer came in Russian from my Claude Code language setting. The second try used English output and gave the same calls for R1 and R2.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. An honest entry here costs far less than a blank one that turns out to be untrue. -->
tool/check_room.json: the part with "additionalProperties": false inside the items of bookings. I do not fully understand why it is needed when "required" already fixed S08.

Signed: Karim Aliyev
Date: 9.11.2026
