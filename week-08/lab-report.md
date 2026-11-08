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
| The file is plain UTF-8 text, named exactly `SKILL.md` (not `SKILL.md.txt`) | yes |
| The first and the closing YAML delimiter are exactly three hyphens: `---` | yes |
| `name` is lowercase with hyphens, and `description` says WHEN to use it | yes |
| I read the whole file once: no passwords, API keys or private student data | yes |

**The contents of `skills/bug-detector.zip`.** Paste the listing (Windows: open the ZIP and copy
the paths; macOS/Linux: `unzip -l skills/bug-detector.zip`):

```text
Archive:  bug-detector.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  11-08-2026 21:51   bug-detector/
        0  10-31-2026 17:36   bug-detector/.gitkeep
      570  11-08-2026 21:51   bug-detector/SKILL.md
---------                     -------
      570                     3 files
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
Find the root cause of the failed room-booking test. Propose minimal patch and regression test. Do not edit code.

AC1 Reject start ≥ end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.

Failing test output:

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

The code of canBook:

export function canBook({ start, end, now, blocked, bookings }: {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
}): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted unedited:**

```text
# Root cause: the overlap check treats touching endpoints as a conflict

The overlap check uses **inclusive** comparisons, so a request that only touches an existing booking counts as overlapping:

```ts
if (start <= b.end && end >= b.start) return false;
```

The test name says the request touches the *end* of a booking, so the existing booking presumably ends at 660 (for example, 600–660). I haven't seen the fixture, so that is an inference. For the request 660–720:

- `start <= b.end` → `660 <= 660` → **true**
- `end >= b.start` → `720 >= 600` → **true**

`canBook` therefore returns `false`, which violates AC4 ("allow bookings that only touch at endpoints"). Treating time slots as half-open intervals `[start, end)` means they overlap only when `start < b.end && end > b.start`.

## Second defect: `canBook` modifies the bookings list (AC5)

```ts
bookings.push({ start, end });
```

A function that only checks availability must not change booking data (AC5). This also explains why there are **5 failures**, not just one. If the test file shares a `bookings` array across tests, every accepted request adds a phantom booking. Later tests then see overlaps that the fixture never contained. This is likely given the `[1/5]` count, but I can't confirm it without the test file.

## Proposed minimal patch

```diff
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
-  // keep the room's list current with the slot that was just found free
-  bookings.push({ start, end });
   return true;
 }
```

AC1, AC2, AC3 and AC6 are unaffected. The validation guards stay the same, and the return value is still a boolean that the UI can map to Available or Unavailable.

## Regression tests

These assume the existing `request()` helper builds a request against a booking of 600–660. Adjust the numbers if the fixture differs.

```ts
describe('canBook - AC4 regression: endpoint touching', () => {
  test('R01 AC4: request ending exactly at booking start (540-600) is accepted', () => {
    expect(canBook(request(540, 600))).toBe(true);
  });

  test('R02 AC4: request starting exactly at booking end (660-720) is accepted', () => {
    expect(canBook(request(660, 720))).toBe(true);
  });

  test('R03 AC4: one-minute overlap at the end (659-720) is rejected', () => {
    expect(canBook(request(659, 720))).toBe(false);
  });

  test('R04 AC4: one-minute overlap at the start (540-601) is rejected', () => {
    expect(canBook(request(540, 601))).toBe(false);
  });
});

describe('canBook - AC5 regression: no side effects', () => {
  test('R05 AC5: an accepted request leaves bookings unchanged', () => {
    const req = request(660, 720);
    const before = structuredClone(req.bookings);
    expect(canBook(req)).toBe(true);
    expect(req.bookings).toEqual(before);
  });

  test('R06 AC5: repeated identical checks give the same answer', () => {
    const req = request(660, 720);
    expect(canBook(req)).toBe(true);
    expect(canBook(req)).toBe(true); // would fail if the first call stored the slot
  });
});
```

- **R01–R04** fix the boundary semantics on both sides: touching is accepted, and a one-minute overlap is rejected.
- **R05–R06** guard against the mutation coming back.

If you share `src/booking.test.ts`, I can check whether the other four failures are caused by the mutation.
```

---

## 6. Task 5 — with the skill

**Another fresh chat, with `bug-detector` enabled.** Send exactly the same input as in section 5.
Only the question changes, to the deck's skill question:

```text
Use the bug-detector skill to diagnose the failed room-booking test.

AC1 Reject start ≥ end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Preserve clear UI feedback on desktop and mobile.

Failing test output:

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

The code of canBook:

export function canBook({ start, end, now, blocked, bookings }: {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
}): boolean {
  if (!(0 <= start && start < end && end <= 1440)) return false;
  if (!(start > now)) return false;
  if (end - start > 120) return false;
  if (blocked) return false;
  for (const b of bookings) {
    if (start <= b.end && end >= b.start) return false;
  }
  // keep the room's list current with the slot that was just found free
  bookings.push({ start, end });
  return true;
}
```

**The assistant's answer, pasted unedited:**

```text
I couldn't run a reproduction because the permission to start a shell process was declined. Everything below comes from tracing the code by hand. I also don't have the test fixture, so I assumed the existing booking is **600–660**, which is what the test name implies.

## Defect 1: bookings that only touch are rejected (confirmed, causes T01)

- **Defect:** A request that starts exactly when an existing booking ends is treated as an overlap. That violates AC4.
- **Evidence:** For the request 660–720 against the booking 600–660:
  - `start <= b.end` → `660 <= 660` → **true**
  - `end >= b.start` → `720 >= 600` → **true**
  - So the overlap check returns `false`. That matches the test output exactly: `expected false to be true`.
- **Root cause:** The overlap check in the `for` loop uses `<=` and `>=`, so it treats intervals as closed. Two bookings that share one endpoint count as overlapping. The mirror case is broken too: a request ending at the booking's start (540–600) is also rejected.
- **Fix:** Use strict comparisons so the intervals are half-open:
  ```ts
  if (start < b.end && end > b.start) return false;
  ```
- **Test:**

  | Request | Expected | Why |
  |---|---|---|
  | 660–720 | `true` | touches the end |
  | 540–600 | `true` | touches the start |
  | 659–720 | `false` | overlaps by 1 minute at the end |
  | 540–601 | `false` | overlaps by 1 minute at the start |
  | 610–650 | `false` | inside the booking |
  | 590–670 | `false` | covers the whole booking |

## Defect 2: `canBook` changes the booking list (confirmed by reading the code)

- **Defect:** On success, `canBook` adds the requested slot to the caller's `bookings` array. AC5 says it must return Available/Unavailable "without changing booking data".
- **Evidence:** The line `bookings.push({ start, end });` runs before `return true`. Calling `canBook` twice with the same input gives `true` and then `false`, because the first call booked the slot.
- **Root cause:** A check function also writes data. The comment ("keep the room's list current…") shows the push was added on purpose, but it puts a write in a function that AC5 says must only check.
- **Fix:** Delete the `push`. If a slot should actually be booked, do that in a separate function (for example `book()`) that calls `canBook` first.
- **Test:**
  - Copy `bookings` before the call (for example with `structuredClone`), call `canBook` with a free slot, and check that `bookings` still equals the copy.
  - Call `canBook` twice with the same free slot and check that both calls return `true`.

## Hypothesis (not confirmed)

The output shows `[1/5]`, so four other tests are failing. If the tests share one `bookings` array, Defect 2 could cause some of them: every accepted request leaves an extra booking behind, and later tests that should pass get rejected. To check, look at whether the fixture is created fresh in each test or `beforeEach`. Then rerun the tests after fixing both defects.

## Not a defect, but worth checking

`start > now` rejects a request that starts at exactly the current minute. AC1 says "in the past", which arguably allows `start === now`. Ask the product owner which behaviour they want, then add a test for `start === now`.

As the skill requires, I haven't edited any code.
```

Did the environment show that the skill was invoked? yes

---

## 7. Comparison — judged against the actual code

Do not assume the skill did better. Judge both answers against the code and against what your
tests showed. Write a short verdict in each cell, and give a reason where they differ.

| Criterion | No skill | With skill |
| --- | --- | --- |
| Correct root cause | Correct. It names the line with <= and >= for T01 (660 <= 660) and the bookings.push line for AC5. Both match my defect log. | Correct. The same two lines and the same reasons. It also says that 540-600 touching the start is broken too, which is true for the code. |
| Reproducible test | Partly. R02 660-720, R03 659-720 and R05 (bookings compared with structuredClone) work with my request() helper. But R01 540-600 expects true, and in my suite now = 540, so canBook rejects it by AC1 even after the fix. R04 540-601 is false for the same AC1 reason, not because of the overlap. | Partly. It gives a table of inputs and two AC5 checks, not test code. The table has the same mistake: 540-600 expects true, but it starts at now = 540, so it is false by AC1 in my fixture. The rest of the table (659-720, 610-650, 590-670 false) is right. |
| Minimal proposed patch | Minimal: one line changed (< and >) and the push line with its comment deleted. Same as my fix. | Minimal: the same two changes. It also suggests a separate book() function, but only as advice, it did not write it. |
| Unsupported claims | Yes. It says the 5 failures are probably caused by a shared bookings array between tests. That is wrong: my suite makes fresh bookings for every test, and the other failures (T08, X2, AC5, R05) are all caused by BUG-A. It says this only as likely, not as a fact. | Fewer. It put the shared-array idea under Hypothesis (not confirmed). But it calls defect 2 confirmed only by reading the code, and it suggests that start = now might be allowed, which my Week 07 AC1 (start after the current time) does not support. It also tried to run node, the permission was declined, and it said so. |
| Clarity of explanation | Clear, with the numbers 660 <= 660 and 720 >= 600, then the patch and tests. | Clearer structure: defect, evidence, root cause, fix, test for each bug, then hypotheses separately, as the skill asks. |

**Which bugs did each answer find?** (BUG-A, BUG-B, both, neither)

- Both answers found both bugs, BUG-A and BUG-B, from the same T01 failure and the code. The input only had the T01 failure, so they found BUG-B by reading the push line, not from a failing test.

---

## 8. Task 6 — repair and regression

Review the proposed patch yourself, then make **one minimal change per bug**, one commit each.
Rerun the test that was failing, then the full suite.

### 8.1 The BUG-A patch

The change as a diff (`git diff`, or the old and the new line), then the real run:

```text
diff --git a/week-08/app/src/booking.ts b/week-08/app/src/booking.ts
index cea94c0..823ea3b 100644
--- a/week-08/app/src/booking.ts
+++ b/week-08/app/src/booking.ts
@@ -26,7 +26,7 @@ export function canBook({ start, end, now, blocked, bookings }: {
   if (end - start > 120) return false;
   if (blocked) return false;
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
   // keep the room's list current with the slot that was just found free
   bookings.push({ start, end });

$ npx vitest run -t "BUG-A"

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-08/app

 ✓ src/booking.test.ts (26 tests | 25 skipped) 2ms

 Test Files  1 passed (1)
      Tests  1 passed | 25 skipped (26)
   Start at  21:54:57
   Duration  640ms (transform 43ms, setup 0ms, collect 34ms, tests 2ms, environment 0ms, prepare 52ms)

$ npx vitest run

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-08/app

 ❯ src/booking.test.ts (26 tests | 3 failed) 12ms
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
   ✓ canBook - AC4: no overlap, touching allowed > T01 AC4: request touching the end of the booking (660-720) is accepted 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T08 AC4: request touching the start of the booking (570-600) is accepted 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T09 AC4: partial overlap (630-690) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T10 AC4: request containing the booking (570-690) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T11 AC4: request inside the booking (615-645) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T12 AC4: request identical to the booking (600-660) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R02 AC4: one-minute overlap at the booking end (659-720) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R03 AC4: one-minute overlap at the booking start (570-601) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > R04 AC4: overlap with the second booking only (750-800) is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed > T14 AC4: 630-690 with no existing bookings is accepted 0ms
   ✓ canBook - AC4: no overlap, touching allowed > X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted 0ms
   × canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged 5ms
     → expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]
   × canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call 0ms
     → Cannot add property 2, object is not extensible
   ✓ canBook - AC5: decision without changing booking data > R06 AC5: a rejected overlap request (630-690) leaves the bookings unchanged 0ms
   ✓ canBook - regression tests for the provided buggy code > BUG-A AC4: request touching a booking on both sides (660-700 between 600-660 and 700-760) is accepted 0ms
   × canBook - regression tests for the provided buggy code > BUG-B AC5: an Available request that touches nothing (720-780) leaves the bookings unchanged 4ms
     → expected '[{"start":600,"end":660},{"start":720…' to be '[{"start":600,"end":660}]' // Object.is equality

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 3 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged
AssertionError: expected [ { start: 600, end: 660 }, …(1) ] to deeply equal [ { start: 600, end: 660 } ]

- Expected
+ Received

  [
    {
      "end": 660,
      "start": 600,
    },
+   {
+     "end": 720,
+     "start": 660,
+   },
  ]

 ❯ src/booking.test.ts:139:28
    137|     expect(canBook(input)).toBe(true);
    138| 
    139|     expect(input.bookings).toEqual(before);
       |                            ^
    140|     expect(input.bookings).toEqual([{ start: 600, end: 660 }]);
    141|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/3]⎯

 FAIL  src/booking.test.ts > canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call
TypeError: Cannot add property 2, object is not extensible
 ❯ Module.canBook src/booking.ts:32:12
     30|   }
     31|   // keep the room's list current with the slot that was just found fr…
     32|   bookings.push({ start, end });
       |            ^
     33|   return true;
     34| }
 ❯ src/booking.test.ts:152:12

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/3]⎯

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

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[3/3]⎯


 Test Files  1 failed (1)
      Tests  3 failed | 23 passed (26)
   Start at  21:54:59
   Duration  470ms (transform 55ms, setup 0ms, collect 32ms, tests 12ms, environment 0ms, prepare 92ms)
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
