# Week 08 — Lab report

**Name:** Karim Aliyev
**Group:** Monday 16:00 - 19:00
**Date:** 8.11.2026

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I debugged with (tool) | Claude (claude.ai) |
| Exact model (with its version, or `not displayed`) | Claude Opus 5.5 |
| Where the skill was installed (ChatGPT / Claude web / Claude Code / prompt-only simulation) | Claude web |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | my computer |
| Vitest version (the `RUN  v…` line of a run) | 3.2.7 |
| Language of my booking module (`ts` or `js`) — the file I copied from `buggy/` | ts |

---

## 2. Task 1 — baseline, buggy code, failing tests

### 2.1 My Week 07 suite on my own code

The **real** output of your Week 07 suite, run in `week-08/app/` **before** you replace
anything. It should be green. If it is not, say why under the block.

```text

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-08/app

 ✓ src/booking.test.ts (24 tests) 3ms

 Test Files  1 passed (1)
      Tests  24 passed (24)
   Start at  21:51:04
   Duration  442ms (transform 30ms, setup 0ms, collect 23ms, tests 3ms, environment 0ms, prepare 145ms)
```

### 2.2 The same suite on the provided canBook

You copied the whole `canBook` function from `buggy/booking.ts` (or `.js`) over yours and changed
nothing else. This is the real output:

```text

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-08/app

 ❯ src/booking.test.ts (24 tests | 5 failed) 7ms
   ✓ canBook - AC1: valid interval, start after now > T02 AC1: request starting exactly at now (540-570) is rejected 1ms
   ✓ canBook - AC1: valid interval, start after now > T03 AC1: zero-duration request (720-720) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > T04 AC1: reversed request (750-720) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > T05 AC1: request ending past the end of the day (1380-1441) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > X1 AC1: request ending exactly at 24:00 (1380-1440) is accepted 0ms
   ✓ canBook - AC1: valid interval, start after now > R01 AC1: request starting one minute after now (541-570) is accepted 0ms
   ✓ canBook - AC1: valid interval, start after now > R07 AC1: negative start (-10 to 30) is rejected even when now is earlier (-20) 0ms
   ✓ canBook - AC2: at most 120 minutes > T06 AC2: exactly 120 minutes (720-840) is accepted 0ms
   ✓ canBook - AC2: at most 120 minutes > T07 AC2: 121 minutes (720-841) is rejected 0ms
   ✓ canBook - AC3: blocked room > T13 AC3: otherwise-available request (660-720) in a blocked room is rejected 0ms
   × canBook - AC4: no overlap, touching allowed > T01 AC4: request touching the end of the booking (660-720) is accepted 4ms
     → expected false to be true // Object.is equality
   × canBook - AC4: no overlap, touching allowed > T08 AC4: request touching the start of the booking (570-600) is accepted 0ms
     → expected false to be true // Object.is equality
   ✓ canBook - AC4: no overlap, touching allowed > T09 AC4: partial overlap (630-690) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T10 AC4: request containing the booking (570-690) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T11 AC4: request inside the booking (615-645) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T12 AC4: request identical to the booking (600-660) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R02 AC4: one-minute overlap at the booking end (659-720) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R03 AC4: one-minute overlap at the booking start (570-601) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R04 AC4: overlap with the second booking only (750-800) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T14 AC4: 630-690 with no existing bookings is accepted 0ms
   × canBook - AC4: no overlap, touching allowed > X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted 0ms
     → expected false to be true // Object.is equality
   × canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged 0ms
     → expected false to be true // Object.is equality
   × canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call 1ms
     → expected false to be true // Object.is equality
   ✓ canBook - AC5: decision without changing booking data > R06 AC5: a rejected overlap request (630-690) leaves the bookings unchanged 0ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 5 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook - AC4: no overlap, touching allowed > T01 AC4: request touching the end of the booking (660-720) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:67:40
     65| describe('canBook - AC4: no overlap, touching allowed', () => {
     66|   test('T01 AC4: request touching the end of the booking (660-720) is …
     67|     expect(canBook(request(660, 720))).toBe(true);
       |                                        ^
     68|   });
     69| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/5]⎯

 FAIL  src/booking.test.ts > canBook - AC4: no overlap, touching allowed > T08 AC4: request touching the start of the booking (570-600) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:71:40
     69| 
     70|   test('T08 AC4: request touching the start of the booking (570-600) i…
     71|     expect(canBook(request(570, 600))).toBe(true);
       |                                        ^
     72|   });
     73| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/5]⎯

 FAIL  src/booking.test.ts > canBook - AC4: no overlap, touching allowed > X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:128:28
    126|       ],
    127|     };
    128|     expect(canBook(input)).toBe(true);
       |                            ^
    129|   });
    130| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/5]⎯

 FAIL  src/booking.test.ts > canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:137:28
    135|     const before = structuredClone(input.bookings);
    136| 
    137|     expect(canBook(input)).toBe(true);
       |                            ^
    138| 
    139|     expect(input.bookings).toEqual(before);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/5]⎯

 FAIL  src/booking.test.ts > canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:152:28
    150|     const input = { start: 660, end: 720, now: 540, blocked: false, bo…
    151| 
    152|     expect(canBook(input)).toBe(true);
       |                            ^
    153| 
    154|     expect(input.bookings).toBe(bookings);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/5]⎯


 Test Files  1 failed (1)
      Tests  5 failed | 19 passed (24)
   Start at  21:51:25
   Duration  356ms (transform 26ms, setup 0ms, collect 22ms, tests 7ms, environment 0ms, prepare 37ms)
```

### 2.3 One failing test per bug

Add the two regression tests from README Part 1, step 5: one named `BUG-A` and one named `BUG-B`.
Run them **on the buggy code**. Both must fail here. That is the evidence that each test can see
its bug.

```text

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-08/app

 ❯ src/booking.test.ts (26 tests | 7 failed) 12ms
   ✓ canBook - AC1: valid interval, start after now > T02 AC1: request starting exactly at now (540-570) is rejected 1ms
   ✓ canBook - AC1: valid interval, start after now > T03 AC1: zero-duration request (720-720) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > T04 AC1: reversed request (750-720) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > T05 AC1: request ending past the end of the day (1380-1441) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > X1 AC1: request ending exactly at 24:00 (1380-1440) is accepted 0ms
   ✓ canBook - AC1: valid interval, start after now > R01 AC1: request starting one minute after now (541-570) is accepted 0ms
   ✓ canBook - AC1: valid interval, start after now > R07 AC1: negative start (-10 to 30) is rejected even when now is earlier (-20) 0ms
   ✓ canBook - AC2: at most 120 minutes > T06 AC2: exactly 120 minutes (720-840) is accepted 0ms
   ✓ canBook - AC2: at most 120 minutes > T07 AC2: 121 minutes (720-841) is rejected 0ms
   ✓ canBook - AC3: blocked room > T13 AC3: otherwise-available request (660-720) in a blocked room is rejected 0ms
   × canBook - AC4: no overlap, touching allowed > T01 AC4: request touching the end of the booking (660-720) is accepted 7ms
     → expected false to be true // Object.is equality
   × canBook - AC4: no overlap, touching allowed > T08 AC4: request touching the start of the booking (570-600) is accepted 1ms
     → expected false to be true // Object.is equality
   ✓ canBook - AC4: no overlap, touching allowed > T09 AC4: partial overlap (630-690) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T10 AC4: request containing the booking (570-690) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T11 AC4: request inside the booking (615-645) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T12 AC4: request identical to the booking (600-660) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R02 AC4: one-minute overlap at the booking end (659-720) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R03 AC4: one-minute overlap at the booking start (570-601) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R04 AC4: overlap with the second booking only (750-800) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T14 AC4: 630-690 with no existing bookings is accepted 0ms
   × canBook - AC4: no overlap, touching allowed > X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted 0ms
     → expected false to be true // Object.is equality
   × canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged 0ms
     → expected false to be true // Object.is equality
   × canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call 1ms
     → expected false to be true // Object.is equality
   ✓ canBook - AC5: decision without changing booking data > R06 AC5: a rejected overlap request (630-690) leaves the bookings unchanged 0ms
   × canBook - regression tests for the provided buggy code > BUG-A AC4: request touching a booking on both sides (660-700 between 600-660 and 700-760) is accepted 0ms
     → expected false to be true // Object.is equality
   × canBook - regression tests for the provided buggy code > BUG-B AC5: an Available request that touches nothing (720-780) leaves the bookings unchanged 1ms
     → expected '[{"start":600,"end":660},{"start":720…' to be '[{"start":600,"end":660}]' // Object.is equality

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 7 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook - AC4: no overlap, touching allowed > T01 AC4: request touching the end of the booking (660-720) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:67:40
     65| describe('canBook - AC4: no overlap, touching allowed', () => {
     66|   test('T01 AC4: request touching the end of the booking (660-720) is …
     67|     expect(canBook(request(660, 720))).toBe(true);
       |                                        ^
     68|   });
     69| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/7]⎯

 FAIL  src/booking.test.ts > canBook - AC4: no overlap, touching allowed > T08 AC4: request touching the start of the booking (570-600) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:71:40
     69| 
     70|   test('T08 AC4: request touching the start of the booking (570-600) i…
     71|     expect(canBook(request(570, 600))).toBe(true);
       |                                        ^
     72|   });
     73| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/7]⎯

 FAIL  src/booking.test.ts > canBook - AC4: no overlap, touching allowed > X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:128:28
    126|       ],
    127|     };
    128|     expect(canBook(input)).toBe(true);
       |                            ^
    129|   });
    130| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/7]⎯

 FAIL  src/booking.test.ts > canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:137:28
    135|     const before = structuredClone(input.bookings);
    136| 
    137|     expect(canBook(input)).toBe(true);
       |                            ^
    138| 
    139|     expect(input.bookings).toEqual(before);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[4/7]⎯

 FAIL  src/booking.test.ts > canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:152:28
    150|     const input = { start: 660, end: 720, now: 540, blocked: false, bo…
    151| 
    152|     expect(canBook(input)).toBe(true);
       |                            ^
    153| 
    154|     expect(input.bookings).toBe(bookings);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[5/7]⎯

 FAIL  src/booking.test.ts > canBook - regression tests for the provided buggy code > BUG-A AC4: request touching a booking on both sides (660-700 between 600-660 and 700-760) is accepted
AssertionError: expected false to be true // Object.is equality

- Expected
+ Received

- true
+ false

 ❯ src/booking.test.ts:180:28
    178|       ],
    179|     };
    180|     expect(canBook(input)).toBe(true);
       |                            ^
    181|   });
    182| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[6/7]⎯

 FAIL  src/booking.test.ts > canBook - regression tests for the provided buggy code > BUG-B AC5: an Available request that touches nothing (720-780) leaves the bookings unchanged
AssertionError: expected '[{"start":600,"end":660},{"start":720…' to be '[{"start":600,"end":660}]' // Object.is equality

Expected: "[{"start":600,"end":660}]"
Received: "[{"start":600,"end":660},{"start":720,"end":780}]"

 ❯ src/booking.test.ts:189:44
    187|     expect(canBook(input)).toBe(true);
    188| 
    189|     expect(JSON.stringify(input.bookings)).toBe(before);
       |                                            ^
    190|   });
    191| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[7/7]⎯


 Test Files  1 failed (1)
      Tests  7 failed | 19 passed (26)
   Start at  21:51:44
   Duration  470ms (transform 35ms, setup 0ms, collect 26ms, tests 12ms, environment 0ms, prepare 45ms)
```

---

## 3. Defect log

One row per defect. At least **BUG-A and BUG-B**. "Suspected cause" is your hypothesis
**before** you ask any assistant: the line and why.

| Defect | Test ID | Input | Expected | Actual | Suspected cause (line and why) |
| --- | --- | --- | --- | --- | --- |
| BUG-A | T01 (also T08, X2, AC5, R05, BUG-A) | 660-720, now 540, not blocked, bookings [600-660] | true | false | Line for (const b of bookings) { if (start <= b.end && end >= b.start) return false; }. It uses <= and >=, so 660 <= 660 counts as an overlap and a request that only touches the booking is rejected. It should be < and >. |
| BUG-B | BUG-B (my new test) | 720-780, now 540, not blocked, bookings [600-660] | true, bookings still [600-660] | true, but bookings became [600-660, 720-780] | Line bookings.push({ start, end }); before return true. It adds the request to the caller's bookings array, so an Available check changes the booking data (AC5). My AC5 test and R05 also failed, but for the wrong reason: their requests touch the booking, so BUG-A returned false before the push. The line should be deleted. |

---

## 4. Tasks 2–3 — the skill

**The checks from the deck, before you zip it.** Answer each one yes / no:

| Check | yes / no |
| --- | --- |
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | yes / no |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | yes / no |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | yes / no |
| I read the whole file once: no passwords, API keys or private student data | yes / no |

**The contents of `skills/bug-detector.zip`.** Paste the listing (Windows: open the ZIP and copy
the paths; macOS/Linux: `unzip -l skills/bug-detector.zip`):

```text
(paste here)
```

**Installation.** Where you uploaded it, what the upload said, and whether a new chat showed the
skill as enabled. If upload was not available, write `prompt-only simulation` and say why.
Screenshot of the result: `evidence/install.png`.

<!-- Write below this line -->

---

## 5. Task 4 — without the skill

A **fresh chat, with no skill enabled**. Paste exactly what you sent: the deck's question, then
the same input you will use in section 6 (AC1–AC6, the failing test output, the code of
`canBook`):

```text
(paste here)
```

**The assistant's answer, pasted unedited:**

```text
(paste here)
```

---

## 6. Task 5 — with the skill

**Another fresh chat, with `bug-detector` enabled.** Send exactly the same input as in section 5.
Only the question changes, to the deck's skill question:

```text
(paste here)
```

**The assistant's answer, pasted unedited:**

```text
(paste here)
```

Did the environment show that the skill was invoked? yes / no / not shown

---

## 7. Comparison — judged against the actual code

Do not assume the skill did better. Judge both answers against the code and against what your
tests showed. Write a short verdict in each cell, and give a reason where they differ.

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | | |
| Reproducible test | | |
| Minimal proposed patch | | |
| Unsupported claims | | |
| Clarity of explanation | | |

**Which bugs did each answer find?** (BUG-A, BUG-B, both, neither)

-

---

## 8. Task 6 — repair and regression

Review the proposed patch yourself, then make **one minimal change per bug**, one commit each.
Rerun the test that was failing, then the full suite.

### 8.1 The BUG-A patch

The change as a diff (`git diff`, or the old and the new line), then the real run:

```text
(paste here)
```

### 8.2 The BUG-B patch and the final run

The change as a diff, then the real output of the **full** suite. Every test must pass.

```text
(paste here)
```

---

## 9. What still fails, and what AI-assisted debugging cannot do

### 9.1 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 One limitation of AI-assisted debugging

<!-- Use something that actually happened in sections 5-8. 20 words or more. -->
-

---

## 10. Conclusion (80–150 words)

<!-- Answer both, in your own words, without the assistant (3-5 sentences, as the deck asks):
     (a) Did the skill help? Show it with one row of section 7.
     (b) What did your tests actually prove - and what did they not?
     Worthless: "The skill made the AI much better at debugging."
     Worth everything: "Both answers found BUG-A from the T01 failure. Only the skill answer
     separated BUG-B as a hypothesis instead of a fact, because step 4 told it to. BUG-B was only
     visible after the BUG-A patch: the AC5 test had been failing for the wrong reason." -->

<!-- Write your conclusion below this line -->
