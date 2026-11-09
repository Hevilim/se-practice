# Week 09 — Lab Report: canBook as a Tool

Fill in every section. Do not delete or renumber the headings: the README and the checker point at
them. Replace every `<!-- comment -->` with your own text (comments are ignored by the checker).

**Name:** Karim Aliyev
**Student ID:** 24B031620
**GitHub:** Hevilim

---

## 1. Setup

| | |
| --- | --- |
| Assistant (frozen for the whole lab) | Claude (claude.ai) |
| Exact model (or "not displayed") | Claude Opus 5.5 |
| Three fresh chats for R1, R2, R3? (yes / no) | yes |
| Python version (`python --version`) | Python 3.12.4 |

## 2. Your tool definition — a reason for every constraint

Paste your final `tool/check_room.json`, then fill the table: one row per constraint you wrote.

```json
{
  "name": "check_room",
  "description": "Checks if a study room can be booked for the requested time. All times are whole minutes since midnight, from 0 to 1440 (for example 10:00 is 600 and 24:00 is 1440). The tool only checks and answers Available or Unavailable. It does not save, create or change any booking.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "start": {
        "type": "integer",
        "description": "Requested start time in minutes since midnight, 0 to 1440.",
        "minimum": 0,
        "maximum": 1440
      },
      "end": {
        "type": "integer",
        "description": "Requested end time in minutes since midnight, 0 to 1440.",
        "minimum": 0,
        "maximum": 1440
      },
      "now": {
        "type": "integer",
        "description": "The current time in minutes since midnight, 0 to 1440.",
        "minimum": 0,
        "maximum": 1440
      },
      "blocked": {
        "type": "boolean",
        "description": "true if the room is blocked, for example for maintenance."
      },
      "bookings": {
        "type": "array",
        "description": "Existing bookings of the room. Can be empty.",
        "items": {
          "type": "object",
          "properties": {
            "start": { "type": "integer", "minimum": 0, "maximum": 1440 },
            "end": { "type": "integer", "minimum": 0, "maximum": 1440 }
          },
          "required": ["start", "end"],
          "additionalProperties": false
        }
      }
    },
    "required": ["start", "end", "now", "blocked", "bookings"],
    "additionalProperties": false
  }
}
```

| Field | Constraint (e.g. `"type": "integer"`, `"maximum": 1440`) | What goes wrong without it |
| --- | --- | --- |
| start, end, now | "type": "integer" | The model can send "11:00" as a string or 600.5, and canBook gets a value it cannot compare (S03, S10). |
| start, end, now | "minimum": 0 | A negative time like -30 is not a time of the day, but it would reach the function (S06). |
| start, end, now | "maximum": 1440 | A time after 24:00 like 1500 would pass (S07). The maximum is 1440 and not 1439, because end = 1440 means 24:00 and must be accepted (S11). |
| blocked | "type": "boolean" | The model can send the string "false", and in JavaScript a non-empty string is true, so the room looks blocked (S09). |
| bookings | "type": "array" | Without it bookings can be one object or a string, and the loop in canBook breaks. |
| bookings items | "type": "object" with integer start and end, 0 to 1440 | A booking can come as a pair [660, 720] or with times as strings (S12), and b.start and b.end are undefined. |
| bookings items | "required": ["start", "end"] | A booking with no end, like {start: 660}, passes, and the overlap check compares with undefined, so the overlap is never found (S08). |
| bookings items | "additionalProperties": false | The model can add fields like "room" to a booking, and the caller thinks they are used, but canBook ignores them. |
| inputSchema | "required" with all five fields | A call without now passes, and canBook cannot check that start is after the current time (S04). |
| inputSchema | "additionalProperties": false | The model can invent a field like "room": "204", and the call passes although canBook does not know rooms (S05). |

## 3. The twelve calls — first run and final run

Your **first** run's S verdicts (before any fix), and your final ones. For every case that changed,
say what you changed.

| Case | First run | Final run | What you changed |
| --- | --- | --- | --- |
| S01 | PASS | PASS | nothing |
| S02 | PASS | PASS | nothing |
| S03 | PASS | PASS | nothing |
| S04 | PASS | PASS | nothing |
| S05 | PASS | PASS | nothing |
| S06 | PASS | PASS | nothing |
| S07 | PASS | PASS | nothing |
| S08 | FAIL | PASS | I added "required": ["start", "end"] and "additionalProperties": false to the items of bookings. |
| S09 | PASS | PASS | nothing |
| S10 | PASS | PASS | nothing |
| S11 | PASS | PASS | nothing |
| S12 | PASS | PASS | nothing |

## 4. Function calling — what the model wrote

For each request, paste the model's reply exactly, then judge it against the request.

### R1

```text
{"name": "check_room", "arguments": {"start": 600, "end": 660, "now": 540, "blocked": false, "bookings": [{"start": 660, "end": 720}]}}
```

Match. F3 passed. The model wrote now = 540 (9:00), start = 600 (10:00), end = 660 (11:00), blocked = false and one booking 660 to 720 (11:00 to 12:00). All five values are what the request says. The request ends at 11:00 and the booking starts at 11:00, so they only touch. canBook will say Available, because touching is allowed by AC4.

### R2

```text
{"name": "check_room", "arguments": {"start": 840, "end": 990, "now": 810, "blocked": true, "bookings": []}}
```

Match. F6 passed. The model did not refuse to call. It wrote now = 810 (13:30), start = 840 (14:00), end = 990 (16:30), blocked = true and bookings = []. It converted 16:30 correctly to 990, not 960. The schema accepted the call, but canBook will say Unavailable for two reasons: the room is blocked (AC3) and 840 to 990 is 150 minutes, more than 120 (AC2). The model did not say anything about this, and this is right, because deciding is the job of the function.

### R3

```text
What exact start and end times do you want tomorrow (e.g., 14:00–16:00), and what are the current time, the room's blocked status, and its existing bookings for that day?
```

The model asked and did not call, so I saved calls/r3.txt. The request misses all five values: "tomorrow afternoon" is not an exact start, "a couple of hours" is not an exact end, and there is no current time, no blocked status and no bookings. The model invented no values. It asked for all of them in one question. One problem is that canBook only knows one day and has no date, so "tomorrow" cannot be checked at all. The model did not notice this. It also used 14:00 to 16:00 as an example, but only as an example, not in a call.

## 5. What the schema cannot check

The allowed keywords only check one value at a time. They cannot compare two fields. So these rules stay in canBook:

AC1: the schema cannot check that start < end and that start is after now, because these compare two fields. The schema CAN check the other part of AC1: every time is a whole number from 0 to 1440.

AC2: the schema cannot check that end - start is at most 120 minutes, because it needs a calculation with two fields. R2 (840 to 990, 150 minutes) passed the schema.

AC3: the schema checks that blocked is true or false, but it must not refuse blocked = true. A call for a blocked room is a correct call (R2), and the answer Unavailable is the function's job.

AC4: the schema cannot check overlap, because it must compare start and end with every booking in the list.

AC5: the schema checks only the input. It cannot see what the function does with the data, for example if it adds the request to bookings, like BUG-B in Week 08.

AC6: the feedback on the page is not part of the call at all.

## 6. Permissions — allow, ask or block

| # | Action | Decision (allow / ask / block) | Reason (the risk, in one sentence or more) |
| --- | --- | --- | --- |
| A1 | call `check_room` with the times the user just typed | allow | It only checks and does not save or change anything (AC5). The worst case is a wrong answer from wrong times, and the user sees the times in the call. |
| A2 | read `week-08/app/src/booking.ts` | allow | Reading the file changes nothing, and booking.ts has no secrets. The agent needs it to understand the rules. |
| A3 | edit `booking.ts` to raise the 120-minute limit to 180 | block | The 120-minute limit is AC2 from the requirements, not a wish of one user. If the agent changes it, the rule changes for all users and the tests for AC2 break. |
| A4 | run `npm test` in `week-08/app` | ask | npm test runs the scripts from package.json and code from node_modules, and the agent could change them before. I want to see what it runs first. |
| A5 | run `git reset --hard` to undo its own last three edits | block | git reset --hard throws away all uncommitted changes, also my own work, not only its three edits. This cannot be undone, and it can use git restore on single files instead. |
| A6 | `git commit` its change on the `week-09` branch | ask | A commit on week-09 can be undone, but this branch is my graded work. I want to read the diff before it goes into the history. |
| A7 | `git push` to `main` | block | The course rule is never to commit to main, and a push is public at once. A pushed change on main is hard to take back and can break the separation between weeks. |
| A8 | send the contents of `.env` to an MCP server it found online | block | .env holds secrets like API keys. A server from the internet is not trusted, and once the keys are sent I cannot get them back, I can only change them. |

## 7. Checkpoint

Before the agent edits anything, I would commit all my work. My checkpoint is the commit d2fcad0 week-09: calls for R1, R2 and R3 as returned. At this commit the tool definition and the three calls are saved.

The command that takes me back to it:

git reset --hard d2fcad0

It throws away every change in tracked files that is not committed, and it moves the branch back, so all commits after d2fcad0 are no longer on the branch. Files that git does not track, for example new files the agent created, stay in the folder. To remove them I would need git clean, so I would check git status after the reset.

## 8. Checker output

Paste the **whole** output of your last `python tests/check_tool.py`, unedited.

```t```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
PASS  D3    name is exactly "check_room"
PASS  D4    description: 25+ words, says minutes, 1440, and that it does not save
PASS  D5    inputSchema: an object with exactly the five fields, all required
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
PASS  S03   end as a string: "11:00" -> refuse
PASS  S04   now missing -> refuse
PASS  S05   an extra field: "room": "204" -> refuse
PASS  S06   start below the day: -30 -> refuse
PASS  S07   end beyond the day: 1500 -> refuse
PASS  S08   a booking with no end: {start: 660} -> refuse
PASS  S09   blocked as a string: "false" -> refuse
PASS  S10   start not a whole minute: 600.5 -> refuse
PASS  S11   end at the end of the day: 1440 -> accept
PASS  S12   a booking as a pair: [660, 720] -> refuse
PASS  F1    calls/r1.json: a call to check_room
PASS  F2    calls/r1.json: arguments valid against your schema
PASS  F3    calls/r1.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F4    calls/r2.json: a call to check_room
PASS  F5    calls/r2.json: arguments valid against your schema
PASS  F6    calls/r2.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F7    calls/r3: exactly one of r3.json (it called) or r3.txt (it asked), not empty
PASS  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
PASS  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
PASS  L3    section 7 names the checkpoint commit (a SHA)
PASS  L4    section 10: a conclusion of 80-150 words
PASS  L5    AI_USAGE.md filled in (a tool row, and signed)

SUMMARY: 30 PASS · 0 FAIL · 0 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

## 9. What still fails

None. All 30 checks pass.

## 10. Conclusion (80–150 words)

I learned that each layer checks something different. The schema checks only shape. My first run failed S08, because a booking without end passed, and the overlap check would compare with undefined. Two lines in items fixed it. But no allowed keyword can say start < end or at most 120 minutes, so R2 passed the schema with 150 minutes in a blocked room, and only canBook can say Unavailable. The model was good at numbers: it converted 16:30 to 990 and did not invent times for R3, it asked. Still, its question did not notice that canBook has no date, so the description should say it works for one day. The agent is the third layer: A5, A7 and A8 cannot be undone, so I block them.
