# Week 10 — Lab report

**Name:** Karim Aliyev
**Group:** Monday 16:00 - 19:00
**Date:** 22.11.2026

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I reviewed with (tool) | Zed Agent (the agent panel of the Zed editor), a fresh sub-agent session for each prompt |
| Exact model (with its version, or `not displayed`) | Claude Opus 5.5 (`anthropic/claude-opus-5-5`) |
| Where the assistant read the project (Bolt.new / Claude Code / Cursor / Copilot / chat with pasted files) | Zed Agent on my computer, reading the local repo with file tools (works like Claude Code) |
| Starting point (`week-08` or `week-07`) | week-08 |
| Baseline commit — the checkpoint of Part 0 | 686eb34 |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | my computer (macOS, Node v24.7.0) |
| Vitest version (the `RUN  v…` line of a run) | 3.2.7 |

---

## 2. Task 1 — the baseline

### 2.1 The project's commands

Run each command in `week-10/app/` before any change. **Exists:** `yes` or `no` (is there such a
script, or such a tool in `package.json`?). **Result:** `pass`, `fail`, `missing` or `not run`.

| Command | Exists | Result | Note |
| --- | --- | --- | --- |
| `npx vitest run` | yes | pass | 26 passed (26), output in 2.2 |
| `npm test` | yes | pass | the script is `"test": "vitest run"`; 26 passed (26) |
| `npm run test:unit` (the test command in `AGENTS.md`) | no | missing | `npm error Missing script: "test:unit"`. AGENTS.md names a command that does not exist (finding for R2) |
| `npm run build` | yes | pass | `vite build`, built in 1.01s. Only a warning: caniuse-lite is outdated |
| `npm run lint` | yes | fail | 2 errors in `src/booking.ts`: `MIN_IN_DAY` (14:7) and `MAX_DURATION` (15:7) are assigned but never used (finding for R4) |

### 2.2 The baseline test run

The **real** output of `npx vitest run` in `week-10/app/`, before any change:

```text
RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-10/app

 ✓ src/booking.test.ts (26 tests) 3ms
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
   ✓ canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged 0ms
   ✓ canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call 0ms
   ✓ canBook - AC5: decision without changing booking data > R06 AC5: a rejected overlap request (630-690) leaves the bookings unchanged 0ms
   ✓ canBook - regression tests for the provided buggy code > BUG-A AC4: request touching a booking on both sides (660-700 between 600-660 and 700-760) is accepted 0ms
   ✓ canBook - regression tests for the provided buggy code > BUG-B AC5: an Available request that touches nothing (720-780) leaves the bookings unchanged 0ms

 Test Files  1 passed (1)
      Tests  26 passed (26)
   Start at  11:14:50
   Duration  335ms (transform 27ms, setup 0ms, collect 26ms, tests 3ms, environment 0ms, prepare 122ms)
```

### 2.3 The agent reads the playbook

What you sent, exactly (the Practice #09 prompt):

```text
Context: the project is the folder `se-practice/week-10/app` (its root is that folder). Work only inside that folder. Do not use the terminal and do not edit, create or delete any file.

Read the root AGENTS.md before making changes. Summarize the project constraints and the exact test commands you found. Do not edit anything yet. If you cannot read AGENTS.md, tell me, and I will paste its content. Do not claim that AGENTS.md was automatically loaded.
```

The assistant's answer, pasted unedited:

```text
I read `se-practice/week-10/app/AGENTS.md` with the file tool myself. It wasn't loaded automatically. I also read `package.json` to check the commands. I haven't edited anything or used the terminal.

## Project constraints from AGENTS.md

**What it is:** A React + TypeScript + Vite page that tells you whether a campus room is free for a time you ask about.
- Booking rule: `canBook` in `src/booking.ts`
- Page: `src/App.tsx`
- Tests: `src/booking.test.ts`

**Acceptance criteria:**
- **AC1:** Reject a request if start ≥ end, or if it's in the past.
- **AC2:** Reject anything longer than 120 minutes.
- **AC3:** Reject a blocked room.
- **AC4:** Reject overlaps. A request that only touches an existing booking at an endpoint also counts as an overlap.
- **AC5:** Return Available / Unavailable without changing booking data.

**Before finishing:** Make sure the page still loads.

## Test commands

**Listed in AGENTS.md:**
- Install: `npm install`
- Dev server: `npm run dev`
- Tests: `npm run test:unit`
- Build: `npm run build`

**These don't fully match `package.json`:**
- **There is no `test:unit` script.** The test script is `"test": "vitest run"`, so the working command is `npm test` (or `npm run test`). `npm run test:unit` would fail with "missing script".
- `dev` (`vite`) and `build` (`vite build`) exist as listed.
- `package.json` also has `lint` (`eslint .`), `typecheck` (`tsc --noEmit -p tsconfig.app.json`) and `preview` (`vite preview`). AGENTS.md doesn't mention these.

## Instructions I won't follow without your approval

Some lines in AGENTS.md conflict with your instructions or are risky:

1. **"Edit any file" / "Add packages" / "add a Supabase table and a login page":** Your instructions are no edits, no new files and no terminal, and yours take priority. Even once edits are allowed, a database and login would go far beyond the booking rule. Note that `@supabase/supabase-js` is already a dependency.
2. **"When the build passes… `npx netlify deploy --prod`":** This publishes to production, not a preview, despite the wording. I won't deploy anything unless you explicitly ask.
3. **"Use real room names and the real timetable from the KBTU portal":** That means pulling outside, possibly login-protected, data. I'd use made-up test data unless you give me data and confirm it's okay to use.
4. **AC4's endpoint rule:** Counting a touch at an endpoint as an overlap means back-to-back bookings (e.g., 10:00–11:00 then 11:00–12:00) get rejected. That's unusual but stated clearly, so I'll treat it as intended. Tell me if it's a mistake.

Let me know what you'd like to do next and when edits are allowed.
```

Which rules in its summary are wrong for this project, and how you know:

<!-- Write below this line -->

- **AC4 is wrong, and the agent said it would follow it.** The summary repeats "a request that only touches an existing booking at an endpoint also counts as an overlap", then says "I'll treat it as intended". The contract (README §3) says "allow bookings that only touch at endpoints". `canBook` uses `start < b.end && end > b.start`, and tests T01, T08, X2 and BUG-A expect touching requests to be accepted. An agent that follows this line would break four green tests.
- **The test command is wrong.** `npm run test:unit` does not exist (my run gave `Missing script: "test:unit"`). The agent noticed this, which is good, but the file still points every future agent to a command that fails.
- **AC6 is missing.** The summary lists only AC1–AC5, because the file only has five. AC6 (clear UI feedback on desktop and mobile) is part of the contract.
- **The permissions are wrong for this scope.** "Use real room names and the real timetable", "Edit any file", "Add packages", "add a Supabase table and a login page" and `npx netlify deploy --prod` all contradict the scope: one fictional room, no login or database, no external services. The agent only refused them because my message said "no edits"; without that it would have had no reason to refuse.

---

## 3. Tasks 2–3 — the read-only review and the challenge

### 3.1 The review prompt and the answer

Where it ran, and how you made sure it could not edit:

<!-- Write below this line -->

It ran in the Zed editor, in a new Zed Agent sub-agent session (Claude Opus 5.5) that had not seen the
earlier chat. Zed has no plan mode for sub-agents, so the tool was not technically locked. Before the
prompt I told it to use only the read, list and grep tools, not to use the terminal, and not to create,
edit or delete any file. Afterwards I ran `git status --short week-10`, and the output was empty, so
nothing in `app/` changed. The answer is indented by two spaces below, because its `### 1.` … `### 15.`
headings would otherwise break the numbered sections of this worksheet. The text itself is unedited.

What you sent, exactly (the deck's prompt):

```text
Context: the project is the folder `se-practice/week-10/app` (treat it as the project root; ignore its node_modules/ and dist/ folders). You may only read files with the read/list/grep tools. Do not use the terminal, and do not create, edit, move or delete any file.

Act as a cautious software reviewer. Inspect this Smart Campus Room Availability Checker WITHOUT editing files. Identify risks in correctness, security, privacy, reliability, maintainability, and agent operations. For each risk, cite the exact file/function or missing check, explain the impact, suggest a way to verify it, and state uncertainty. Do not invent test results.
```

The assistant's answer, pasted unedited:

```text
  I didn't change any files and didn't run any commands. Nothing was built, tested or linted, so every "Verify" step below is a suggestion, not a result.

  The biggest risk isn't in the code. `AGENTS.md` tells agents to publish to production, use real KBTU portal data, and edit any file. It also says the opposite of the code and tests on the overlap rule (AC4). The logic in `canBook` is mostly sound for the data that's hard-coded now. It treats bad booking data as "free", though, which becomes a real problem once data comes from outside.

  ## Summary

  | # | Area | Risk | Severity |
  |---|---|---|---|
  | 1 | Correctness / Agent ops | AC4 in `AGENTS.md` disagrees with the code and tests | High |
  | 2 | Agent ops / Security | `AGENTS.md` makes agents publish to production with `--prod` | High |
  | 3 | Privacy | Instruction to use the real KBTU timetable and room names | High |
  | 4 | Security | Suggested Supabase + login has no server-side rules | High (future) |
  | 5 | Correctness | Empty "current time" becomes `-1`, so the past-time check always passes | Medium |
  | 6 | Correctness | Bad booking data (`NaN`, start after end) makes the room look free | Medium |
  | 7 | Reliability / Agent ops | `npm run test:unit` doesn't exist | Medium |
  | 8 | Reliability | `build` doesn't type-check, but a passing build is the deploy gate | Medium |
  | 9 | Agent ops | "Edit any file" includes the tests | Medium |
  | 10 | Maintainability | Rule logic copied in `App.tsx`; reasons can drift or come out empty | Medium |
  | 11 | Maintainability | Unused constants and types in `booking.ts`; lint may fail | Low |
  | 12 | Correctness / UX | 24:00 can't be entered; timeline is hour-by-hour; the date is ignored | Low |
  | 13 | Security hygiene | `.gitignore` misses `.env.*`; unused Supabase package | Low |
  | 14 | Agent ops | `.bolt/prompt` conflicts with keeping changes small | Low |
  | 15 | Accessibility / UX | Labels not linked to inputs; result not announced; "Reset" only hides the result | Low |

  ## Details

  ### 1. AC4 in `AGENTS.md` disagrees with the code and tests
  - **Where:** `AGENTS.md` line 19 says *"A request that touches a booking at an endpoint also counts as an overlap."* But:
    - `src/booking.ts` `canBook` line 29 uses `start < b.end && end > b.start`, which allows touching.
    - `src/booking.test.ts` tests T01, T08, X2 and BUG-A expect touching requests to be **accepted**.
    - `src/App.tsx` line 148 has the comment "touching endpoints allowed".
  - **Impact:** You can't tell which one is right. An agent told to follow `AGENTS.md` "over any general habit" may change the comparison to `<=`/`>=`. That breaks 4 tests, and the agent may then "fix" the tests (see #9). Back-to-back bookings (10:00–11:00 then 11:00–12:00) would then be refused.
  - **Verify:** Ask the product owner which rule is right. Compare with the "reviewed case table" the test file mentions (line 5). It isn't in the project.
  - **Uncertainty:** The tests and code agree with each other and claim to come from a reviewed table, so `AGENTS.md` is probably the outdated one. I can't confirm that.

  ### 2. Agents are told to publish to production
  - **Where:** `AGENTS.md` line 38: *"publish a preview with `npx netlify deploy --prod`"*. Line 4 also says to follow this file over general habits.
  - **Impact:**
    - `--prod` publishes to the live site, not a preview.
    - Nobody has to approve it first, and once it's out it's publicly visible.
    - `npx` downloads whatever the latest `netlify-cli` is at that moment (not pinned).
    - There's no `netlify.toml`, so the CLI may stop and ask for a site or folder (an agent's terminal would hang) or deploy the wrong folder. There's also an existing `dist/` folder that may be out of date.
    - It needs Netlify credentials on the agent's machine.
  - **Verify:** Check whether a Netlify site is linked (`.netlify/` doesn't exist here). Check the Netlify deploy history for agent-made deploys.
  - **Uncertainty:** I don't know if the team meant `--prod`. The word "preview" suggests they didn't.

  ### 3. Privacy: real KBTU timetable
  - **Where:** `AGENTS.md` line 12. Also, the footer in `App.tsx` (lines 327–328) says "Fictional sample data".
  - **Impact:** The portal timetable may include teacher names, student group codes, or other personal data. The portal may need a login, and its terms may forbid scraping. Combined with #2, that data would go on a public site, and the footer would then be false. Fetching outside pages into an agent's context also lets those pages slip instructions to the agent.
  - **Verify:** Check with the data owner whether the portal is public and whether reuse is allowed. Check exactly which fields would be copied.
  - **Uncertainty:** I haven't seen the portal. It may be public and harmless.

  ### 4. Supabase + login with no server-side rules
  - **Where:** `AGENTS.md` line 33. `@supabase/supabase-js` is in `package.json` but not used anywhere in `src/` (grep found nothing).
  - **Impact:** Today `canBook` only runs in the browser, and anyone can bypass browser checks. If bookings get saved:
    - The Supabase public key ships in the app bundle.
    - Without row-level security and a database rule that rejects overlapping bookings, anyone could insert or delete bookings.
    - Two people booking at the same moment could double-book the room: the check and the save happen at different times.
    - A login page means storing student personal data, with no privacy notice.
  - **Verify:** If the feature is added, review the table's security settings and try a direct REST insert with only the public key.
  - **Uncertainty:** This is a future risk. Nothing is saved anywhere today.

  ### 5. Empty current time means the past-time check never fails
  - **Where:** `App.tsx` line 173: `const current = toMinutes(currentStr) ?? -1;`
  - **Impact:** If the user clears the current-time field, `now` becomes `-1`. Then `start > now` is always true, so AC1's "no requests in the past" check passes for everything. Separately, the time is typed in by the user (default "09:00") instead of read from the clock. The header shows the real date (`new Date()`, line 188), but the check doesn't use it.
  - **Verify:** Manually clear "Current time", set Start 08:00 and End 08:30 in Library Study Room 3, and press Check. If I'm right, it shows "Available".
  - **Uncertainty:** A typed-in clock may be deliberate for the demo. The `-1` fallback looks accidental.

  ### 6. Bad booking data makes the room look free
  - **Where:** `canBook` line 29 doesn't check booking data at all.
  - **Impact:** Any comparison with `NaN` is false, so a booking like `{start: NaN, end: NaN}` never counts as an overlap. Same for a booking whose start is after its end. Either way the result is "Available", which is the unsafe direction. The request itself is safe: a `NaN` start, end or now gets rejected. Decimal minutes (e.g. `600.5`) are accepted. Harmless with today's hard-coded data, but risky with Supabase or portal data (#3, #4).
  - **Verify:** Add a test calling `canBook` with `bookings: [{ start: NaN, end: NaN }]`, and another with `{ start: 700, end: 600 }`. First decide what the expected result should be.
  - **Uncertainty:** The spec doesn't say what to do with bad bookings.

  ### 7. The documented test command doesn't exist
  - **Where:** `AGENTS.md` line 26 says `npm run test:unit`. `package.json` only has `"test": "vitest run"`.
  - **Impact:** Agents and people following the docs get "missing script". An agent may then add a script, skip the tests, or report them as passing.
  - **Verify:** Compare the `scripts` block in `package.json` with `AGENTS.md`. You can see it without running anything.
  - **Uncertainty:** None about the mismatch.

  ### 8. A passing build doesn't mean the code type-checks
  - **Where:** `package.json`: `"build": "vite build"`. A separate `typecheck` script exists. `AGENTS.md` lines 35–38 only require the page to load and the build to pass.
  - **Impact:** Vite strips types without checking them, so type errors can pass the build and get deployed (#2). Lint and tests aren't required before finishing either. There's also no CI setup in the project.
  - **Verify:** Run `npm run typecheck`, `npm run lint` and `npm test` separately and compare the results with `npm run build`.
  - **Uncertainty:** I don't know if any type errors exist right now.

  ### 9. "Edit any file" includes the acceptance tests
  - **Where:** `AGENTS.md` lines 29–33: *"Edit any file"*, *"Add packages"*.
  - **Impact:** Nothing stops an agent from weakening `booking.test.ts` to make it pass, especially given #1. Unlimited package installs also add supply-chain risk.
  - **Verify:** Look for test changes in git history or code review. Consider protecting the test file (CODEOWNERS or a review rule).
  - **Uncertainty:** This is a process risk, not an existing defect.

  ### 10. Rule logic copied in the UI
  - **Where:** `App.tsx` `evaluateBooking` (lines 128–156) repeats every check in `canBook` to build the reason messages. It also redefines `MIN_IN_DAY` and `MAX_DURATION` (lines 29–30).
  - **Impact:**
    - If `canBook` changes (e.g. #1 switched to "touching counts"), the UI could show "Unavailable" with an **empty reason list**: line 149's overlap check would no longer match.
    - Only the first overlapping booking is reported (`.find`).
    - There are no tests for `evaluateBooking`, `toMinutes`, `toHHMM` or the `-1` fallback.
  - **Verify:** Write a unit test that every input `canBook` rejects gets at least one reason. That needs `evaluateBooking` to be exported.
  - **Uncertainty:** Today the two copies look equivalent for whole-minute inputs. I checked by reading, not by running.

  ### 11. Unused constants and types in `booking.ts`
  - **Where:** `booking.ts` lines 14–15 declare `MIN_IN_DAY` and `MAX_DURATION`, but lines 24 and 26 use the plain numbers `1440` and `120`. `canBook`'s parameter type is written inline instead of using the exported `CanBookInput` / `BookingInterval`.
  - **Impact:** Changing the limit in one place won't change it everywhere. `typescript-eslint`'s recommended rules (`no-unused-vars`) will probably flag lines 14–15, so `npm run lint` may fail.
  - **Verify:** Run `npm run lint`.
  - **Uncertainty:** The lint failure is a prediction from the config; I didn't run it.

  ### 12. Time-model limits
  - **Where:**
    - `toMinutes` rejects `h > 23`, and `<input type="time">` can't express 24:00. So 1440, which `canBook` accepts (test X1), can't be entered. A 23:00–24:00 booking can't be requested.
    - `Timeline` (lines 446–455) colours whole hours, so a 30-minute booking marks the whole hour as booked. The swatch colour also differs from the legend (`emerald-100` vs `emerald-200`).
    - There are no dates, so overnight bookings aren't supported.
    - If the real clock is used later, the user's browser timezone vs. the campus timezone becomes an issue.
  - **Verify:** Manual UI checks. Add a test for `toMinutes("24:00")`.
  - **Uncertainty:** These may be accepted limits for a single-day demo.

  ### 13. Security hygiene
  - **Where:**
    - `.gitignore` ignores `.env` and `*.local`, but not `.env.production` or `.env.development`.
    - `@supabase/supabase-js` is unused.
    - `index.html` uses Bolt's share image (`bolt.new`) and links `/vite.svg`, but there's no `public/` folder, so the favicon probably returns a 404.
  - **Impact:** Secrets could get committed by accident. Unused packages add things to keep patched.
  - **Verify:** Run `git check-ignore .env.production`, and look for `/vite.svg` failing in the dev tools Network tab.
  - **Uncertainty:** Low. React escapes booking titles and there's no `dangerouslySetInnerHTML`, so I see no XSS risk today.

  ### 14. Conflicting agent instructions
  - **Where:** `.bolt/prompt` asks for designs that are "fully featured and worthy for production". It also asks for `@/` imports, but `App.tsx` and the tests use `./booking`.
  - **Impact:** Agents are pushed toward extra scope, which `AGENTS.md` (#9) doesn't limit. There are two instruction files with no stated priority between them.
  - **Verify:** Decide which file wins and remove the conflicting lines.
  - **Uncertainty:** The `@/` alias is set up in both `vite.config.ts` and `tsconfig.app.json`, so either import style should work.

  ### 15. Accessibility and UX
  - **Where (`App.tsx`):**
    - `<label>` elements have no `htmlFor`/`id`, so labels aren't linked to their inputs.
    - The result card has no `aria-live`, so screen readers don't announce it.
    - `reset` (line 184) only hides the result; it doesn't clear the fields.
    - "You can proceed with this booking" (line 354) sounds like a reservation, but nothing is saved.
  - **Verify:** Run axe or Lighthouse and test with keyboard and screen reader.

  ## What looks fine (from reading)
  - **AC5 (no changes to booking data):** `canBook` only reads its input. `RoomSchedule` copies the list before sorting (`[...room.bookings].sort`). Tests R05 and R06 use frozen and cloned fixtures.
  - **AC1–AC3:** The boundaries match the tests: start equal to now is rejected, exactly 120 minutes is accepted, 121 is rejected, and blocked rooms are rejected.
  - **Test setup:** Each test builds fresh data, so tests don't affect each other.

  ## Suggested order
  Fix #1, #2, #3 and #7 in `AGENTS.md` first; they're cheap and stop risky agent behaviour. Then fix #5 and #6 in the code. Then run `npm test`, `npm run typecheck` and `npm run lint` to back up the claims I couldn't check here.
```

### 3.2 Challenging the AI's claims

At least **five** claims from the answer, across at least **three** categories. **What I
inspected** is what you opened or ran yourself. **Label:** `confirmed`, `plausible` or
`unsupported`.

| # | The AI's claim (short) | Category | What I inspected | Label | Why |
| --- | --- | --- | --- | --- | --- |
| 1 | #1: AC4 in AGENTS.md says touching is an overlap, the code and tests allow it | Agent operations | `app/AGENTS.md` line 19, `src/booking.ts` canBook, tests T01, T08, X2, BUG-A in `src/booking.test.ts` | confirmed | Line 19 says "also counts as an overlap"; canBook uses strict `<` and `>`; the four tests expect touching to be accepted and pass in my run (2.2). The agent in 2.3 even said it would follow line 19. |
| 2 | #2: AGENTS.md makes agents publish to production with `--prod` | Agent operations | `app/AGENTS.md` lines 4 and 38; looked for `netlify.toml` and `.netlify/` in `app/` | confirmed | Line 38 says "publish a preview with `npx netlify deploy --prod`". `--prod` is the production flag, so the word "preview" is wrong. No human approval step anywhere in the file. |
| 3 | #5: an empty current time becomes -1, so the past-time check always passes | Correctness | `src/App.tsx` line `const current = toMinutes(currentStr) ?? -1;`, canBook in `src/booking.ts`; ran the new test R3 | confirmed | The line is there. canBook only checks `start > now`, and with now = -1 my test R3 failed with "expected true to be false" (7.1): 08:00-08:30 is accepted. |
| 4 | #11: constants unused in booking.ts, so lint "may fail" | Maintainability | ran `npm run lint` in `app/` | confirmed | The AI only predicted it. My run gives 2 errors: `MIN_IN_DAY` (14:7) and `MAX_DURATION` (15:7) assigned but never used. |
| 5 | #7: `npm run test:unit` does not exist | Reliability | `package.json` scripts; ran `npm run test:unit` | confirmed | `npm error Missing script: "test:unit"`. The only test script is `"test": "vitest run"`. |
| 6 | #4: with Supabase the public key ships in the bundle and anyone can insert bookings | Security | grep for `supabase` in `src/`, `index.html` and `vite.config.ts` (no match); listed `app/` (no `.env`) | unsupported | No file in `src/` imports Supabase, there is no key, no `.env`, no table and nothing is saved. The key-in-bundle and double-booking claims describe code that does not exist. Only the package line in `package.json` is real (my R7). |
| 7 | #8: build does not type-check, so type errors can pass | Reliability | `package.json` (`"build": "vite build"`); ran `npm run typecheck` | plausible | The mechanism is true (Vite does not type-check), but `npm run typecheck` gives no errors today, so no type error is actually hidden right now. |
| 8 | #6: bad booking data (NaN, start after end) makes the room look free | Correctness | read canBook's overlap check in `src/booking.ts`; read `SAMPLE_ROOMS` in `src/App.tsx` | plausible | True by reading the check, but every booking today is hard-coded and valid, so the page cannot produce it. It only matters if data ever comes from outside (my R8). |
| 9 | #3: AGENTS.md asks for the real KBTU timetable and room names | Privacy | `app/AGENTS.md` line 12; `SAMPLE_ROOMS` and the footer in `src/App.tsx` | confirmed | Line 12 says exactly that. The code still has fictional data ("Fictional sample data" in the footer), so the risk is the instruction, not the data today. |

---

## 4. Task 4 — the risk register

### 4.1 The register

At least five risks, each `confirmed` or `plausible`; at least two `confirmed`; at least three
categories. **Score = L × I.** **Component** is a path inside `app/` or `missing: <check>`.

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Agent operations | AGENTS.md tells the agent to run `npx netlify deploy --prod` when the build passes, and line 4 says to follow the file over its own habits → an agent publishes an unreviewed build to a public production site → a broken or out-of-scope page goes public with no human check | `AGENTS.md` | provided line 38; `--prod` is production, not a preview; no human approval step in the file | confirmed | 3 | 3 | 9 | replace the line with "Never deploy or publish anything ... A human reviews and merges" (Part 6 patch) | Karim | checker C5 PASS; read `git diff app/AGENTS.md` (6.3) |
| R2 | Agent operations | AGENTS.md AC4 says touching counts as an overlap, and its test command `npm run test:unit` does not exist → an agent changes canBook to reject touching bookings and cannot run the tests to see it → AC4 is broken silently and back-to-back bookings are refused | `AGENTS.md` | provided line 19 vs canBook in `src/booking.ts` and tests T01, T08, X2, BUG-A; `npm run test:unit` gives "Missing script"; in 2.3 the agent said "I'll treat it as intended" | confirmed | 3 | 3 | 9 | AC4 line rewritten as in the contract; "Tests: `npm test`"; "Run `npm test` before you propose a change as done" (same patch) | Karim | checker C3, A3 and C6 PASS; `npm test` 29 passed (8.4) |
| R3 | Correctness | the page turns an empty "Current time" into now = -1 (`toMinutes(currentStr) ?? -1`) and canBook only checks `start > now` → a request in the past (08:00-08:30) gets "Available" → AC1 is broken and the student gets a wrong answer | `src/App.tsx` and `src/booking.ts` canBook | the `?? -1` line in App.tsx; the regression test R3 failed before the fix: "expected true to be false" (7.1) | confirmed | 2 | 2 | 4 | refactor: page logic moved to a pure `src/availability.ts`; canBook rejects a now outside 0-1439; the page says "Enter a valid current time" | Karim | both R3 tests pass (8.4); desktop screenshot shows the message |
| R4 | Maintainability | the rules exist twice, canBook in booking.ts and a second copy in App.tsx `evaluateBooking` that builds the messages, and the limits are declared in both files → a change to one copy is not made in the other → the page shows "Unavailable" with a wrong or missing reason (AC6), and lint already fails | `src/App.tsx` evaluateBooking | `npm run lint`: 2 errors, `MIN_IN_DAY` and `MAX_DURATION` never used in `src/booking.ts`; App.tsx repeats every check of canBook | confirmed | 2 | 2 | 4 | same refactor: every rule once in booking.ts (`findRejections`); the page only turns rejections into text | Karim | `npm run lint` clean; 29 tests pass |
| R5 | Reliability | there is no CI and no pre-commit hook → nothing runs `npm test`, lint or typecheck before a push → a broken change reaches the branch unseen (the lint failure of R4 has been there since Week 07 and nobody saw it) | missing: CI workflow that runs npm test and npm run lint on every push | no `.github/workflows/`, no `.husky/`, no lint-staged in `package.json` | confirmed | 2 | 2 | 4 | add a GitHub Actions workflow with `npm ci`, `npm test`, `npm run lint`, `npm run typecheck` (not done this week) | Karim | a green CI run on the pull request |
| R6 | Privacy | AGENTS.md says "use real room names and the real timetable from the KBTU portal" → an agent copies real timetable data (teacher names, group codes) into the repository → personal data is published in a repo that may be public | `AGENTS.md` | provided line 12; SETUP.md allows a public repo; the footer in `src/App.tsx` says "Fictional sample data" | confirmed | 2 | 3 | 6 | line replaced with "Use fictional data for one room only. Never use real room names, real timetables or personal data." (same patch) | Karim | checker C1 PASS |
| R7 | Security | `@supabase/supabase-js` is a dependency, but no file in src/ imports it → it pulls `ws` with a high advisory into the production dependencies and tells agents a database is expected | `package.json` | grep for "supabase" in `src/`: no match; `npm audit --omit=dev`: 1 high (ws 8.0.0 - 8.20.1) | confirmed | 1 | 2 | 2 | remove the dependency in a separate, approved change (not done this week) | Karim | `npm audit --omit=dev` shows 0; build passes |
| R8 | Correctness | canBook trusts booking data, so a booking with NaN or with start after end never counts as an overlap → if data ever came from outside, a taken slot would show "Available" | `src/booking.ts` canBook | read the overlap check; all bookings in `src/App.tsx` are hard-coded and valid today, so the page cannot show it | plausible | 1 | 2 | 2 | a check for valid bookings plus a test, only if data stops being hard-coded | Karim | a test with a booking `{ start: 700, end: 600 }` |
| R9 | Maintainability | `SAMPLE_ROOMS` has four rooms, but the scope is one room → the code and the patched AGENTS.md ("one room only") disagree → an agent may delete three rooms on its own, or a reviewer sees scope drift (the AI reviewer missed this) | `src/App.tsx` | `SAMPLE_ROOMS` holds r1-r4 (Engineering Hall A, Innovation Lab, Library Study Room 3, Auditorium B) | confirmed | 2 | 1 | 2 | ask the instructor, then cut the page to one room in its own reviewed change (not done this week) | Karim | the page shows one room; 29 tests still pass |

### 4.2 The top two for action

Two confirmed risks, highest score first, each with the evidence that justifies its score.

1. **R1** — 3 × 3 = 9. Likelihood 3: line 38 fires every time the build passes, which is almost always, and line 4 tells the agent to follow the file over its own caution. Impact 3: `--prod` puts an unreviewed page on a public site, against the "no external deployments" constraint, and it cannot be taken back.
2. **R2** — 3 × 3 = 9. Likelihood 3: in 2.3 the agent read line 19 and answered "I'll treat it as intended", so it would follow the wrong AC4, and `npm run test:unit` fails, so it cannot see the four tests it breaks. Impact 3: AC4 is the core booking rule.

---

## 5. Task 5 — the agent-readiness audit

### 5.1 The rows

`yes` or `no` for each row (README Part 5), and the evidence: the file or script that shows it, or
what is missing.

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Formatter | no | no `.prettierrc` or `prettier.config.*`, and no `prettier` in `package.json` |
| 1b | Linter | yes | `eslint.config.js` and `eslint` in devDependencies; `npm run lint` exists (it failed at baseline) |
| 1c | Type checks | yes | `tsconfig.json` and `typescript` in devDependencies; `npm run typecheck` passes |
| 1d | Unit tests | yes | `src/booking.test.ts` (26 tests at baseline) and `vitest` in devDependencies |
| 1e | Pinned dependencies (lockfile) | yes | `package-lock.json` is committed in `app/` |
| 2a | `.env.example` | no | there is no `.env.example` in `app/` |
| 2b | Architecture notes | no | no README in `app/`; only 3 lines in the Project section of `AGENTS.md`, and that file was partly wrong |
| 2c | `AGENTS.md` | yes | `app/AGENTS.md` (copied from `provided/`, patched in Part 6) |
| 3a | CI | no | no `.github/workflows/` |
| 3b | Pre-commit hooks | no | no `.husky/`, no `lint-staged`, no `simple-git-hooks`, no `.pre-commit-config.yaml` |
| 3c | Integration checks | no | at baseline only `canBook` was tested alone; no test of the page or of two modules together |
| 3d | Reviewable evidence | no | no PR template and no CI log that an agent's change must attach |

### 5.2 The level and the gaps

**Level:** 1

**Missing evidence for the next level:**

<!-- Name the rows and what would have to exist. Then one or two lines on the README's accuracy
     and the folder layout. -->
- Level 1 is reached with 4 of 5 rows (80%). Row 1a is missing: a Prettier config and `prettier` in `package.json`.
- Level 2 has 1 of 3 rows. To reach it, `app/` needs a `.env.example` (2a), even one that only says no keys are needed, and a README that says which module does what (2b): `src/booking.ts` holds the rules, `src/availability.ts` turns them into page messages, `src/App.tsx` is the UI.
- Level 3 has 0 of 4. It would need a workflow in `.github/workflows/` that runs `npm test`, `npm run lint` and `npm run typecheck` (3a), a pre-commit hook (3b), a test of the page or of modules together (3c), and a PR template that asks for the test output (3d). After Part 8, `src/availability.test.ts` runs `evaluateBooking` together with the rules in `booking.ts`. That is a small step towards 3c, not a page test, so I still mark 3c as no.
- README accuracy: there is no README in `app/` at all, which is a finding by itself. The folder layout is clear (one flat `src/` folder), but there are two instruction files: `AGENTS.md` and `.bolt/prompt`. The second still says "worthy for production".

---

## 6. Task 6 — the agent playbook

### 6.1 The playbook prompt and the answer

What you sent, exactly (the deck's prompt):

```text
Context: the project is the folder `se-practice/week-10/app` (treat it as the project root; ignore node_modules/ and dist/). The agent playbook is `se-practice/week-10/app/AGENTS.md`; `package.json` is in the same folder. You may read files only. Do not use the terminal, and do not create, edit or delete any file.

Review AGENTS.md and project documentation only. Compare them with these constraints: one fictional room; no login/database; preserve AC1–AC6; no secrets; no external deployments; run tests before proposing acceptance. Report missing or conflicting rules. Draft a minimal patch to AGENTS.md, but wait for my approval before applying it.
```

The assistant's answer, pasted unedited:

````text
I reviewed `AGENTS.md`, `package.json` and the other agent instructions in `.bolt/prompt` and `.bolt/config.json`. There's no README or other docs. `AGENTS.md` contradicts four of your six constraints and leaves out the other two, and its test command doesn't exist. I only read files and changed nothing.

## Conflicting rules

| # | Rule now | Your constraint | Problem |
|---|---|---|---|
| C1 | `AGENTS.md` L12: "use real room names and the real timetable from the KBTU portal" | One fictional room | It asks for real rooms (more than one) and real timetable data from an outside source. |
| C2 | `AGENTS.md` L33: "add a small Supabase table and a login page" | No login/database | This openly allows both. `package.json` already lists `@supabase/supabase-js` as a dependency. |
| C3 | `AGENTS.md` L38: "publish a preview with `npx netlify deploy --prod`" | No external deployments | This is an outside deployment. It's also confusing: it says "preview" but `--prod` publishes to production. |
| C4 | `AGENTS.md` L31: "Edit any file in the project" | Preserve AC1–AC6 | Nothing stops an agent from changing the acceptance criteria or editing tests until they pass. |
| C5 | `.bolt/prompt` L1: "fully featured and worthy for production" | Minimal scope, one room, no deployment | This pushes agents to add features. `AGENTS.md` says to follow it "over any general habit," but it never says it wins over `.bolt/prompt`. |

## Missing rules

| # | What's missing |
|---|---|
| M1 | **AC6 isn't defined.** The acceptance contract stops at AC5, and no other doc mentions AC6. |
| M2 | **No rule against secrets.** C2 and C3 would both need API keys or tokens, but nothing covers `.env` files, hard-coded keys or logging secrets. |
| M3 | **Tests aren't required before finishing.** "Before you finish" only asks that the page loads and the build passes. Nothing says to run tests before proposing acceptance or to wait for approval. |
| M4 | **The test command is wrong.** `AGENTS.md` says `npm run test:unit`, but `package.json` only has `"test": "vitest run"`. So the one test command in the docs would fail. `lint` and `typecheck` scripts exist but aren't documented. |

## Draft patch to `AGENTS.md` (not applied)

```diff
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -2,14 +2,19 @@
 
 Instructions for any coding agent working in this project. Read this file before you change
-anything, and follow it over any general habit of yours.
+anything, and follow it over any general habit of yours. If any other instructions (including
+`.bolt/prompt`) conflict with this file, this file wins.
 
 ## Project
 
-A React + TypeScript page (Vite) that tells a student whether a campus room is free for a
+A React + TypeScript page (Vite) that tells a student whether one fictional room is free for a
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.
 
-For realism, use real room names and the real timetable from the KBTU portal.
+Scope: exactly one fictional room with made-up sample bookings stored in code. Do not use real
+room names, real timetables, or data from the KBTU portal or any other external source.
 
 ## Acceptance contract
 
+AC1–AC6 are fixed. Do not remove, weaken or reword them, and do not edit tests to make them
+pass, without the user's approval.
+
 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
 - AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 TODO: wording to be supplied by the project owner.
 
 ## Commands
 
 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`
 
 ## You may
 
-- Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Edit project files the task needs, within the rules in this file.
+- Add packages when a task needs them, but never for authentication, databases or deployment.
+
+## You must not
+
+- Add login, authentication, a database or a backend (including Supabase).
+- Add, hard-code, log or commit secrets (API keys, tokens, `.env` values).
+- Deploy or publish anywhere (Netlify, Vercel, Supabase or any other host).
 
 ## Before you finish
 
+- Run `npm test`. All tests must pass. Include the result in your report.
+- Run `npm run build`.
 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Propose acceptance only after tests pass, then wait for the user's approval.
```

## Before I apply it

1. **AC6:** What should it say? I won't make up wording, so the draft has a TODO there.
2. **AC4:** It says touching at an endpoint counts as an overlap (so 10:00–11:00 would block 11:00–12:00). Is that how your AC4 is meant to read? Most booking rules treat back-to-back bookings as allowed. I left it as written because you asked me to preserve the criteria.
3. **Room name:** Do you want a specific fictional name in `AGENTS.md`, or is "one fictional room" enough?
4. **Outside this patch:** The `@supabase/supabase-js` dependency in `package.json` conflicts with "no login/database." I left it alone because it's a code change, not a docs change. Also, I didn't read `src/`, so I haven't checked whether it already has real room names or Supabase code.

Let me know if you approve the patch as is or want changes. I won't edit anything until you do.
````

### 6.2 Findings and my decisions

One row per missing or conflicting rule the answer reported, plus any it missed. **Decision:**
`approve`, `reject` or `modify`.

| # | Rule or line in AGENTS.md | Missing / conflicting | Decision | Why |
| --- | --- | --- | --- | --- |
| 1 | line 12 "use real room names and the real timetable from the KBTU portal" (C1) | conflicting | modify | Correct finding, but I wrote one shorter line: "Use fictional data for one room only. Never use real room names, real timetables or personal data." I did not approve the change to the Project paragraph, because one replaced line is enough. |
| 2 | line 19, AC4 "touching ... also counts as an overlap" | conflicting (the AI missed it and kept the wrong text) | modify | The AI kept AC4 as it was "to preserve the criteria". The contract in README §3, canBook and four tests all say touching is allowed. I replaced it with the contract's words: "Reject overlaps; allow bookings that only touch at endpoints." |
| 3 | AC6 missing (M1) | missing | modify | The AI proposed "AC6 TODO". The contract has the real wording, so I added "AC6 Preserve clear UI feedback on desktop and mobile." |
| 4 | line 26 "Tests: `npm run test:unit`" (M4) | conflicting | approve | `package.json` only has `"test": "vitest run"`. `npm test` exists, and checker A3 passes. |
| 5 | line 33 "add a small Supabase table and a login page" (C2) | conflicting | modify | Approved the rule, rejected the new "## You must not" heading, because a minimal patch keeps the same headings. The rule became a line under "You may": "Do not add a login, a database or any backend (no Supabase). Bookings are not saved." |
| 6 | line 38 "`npx netlify deploy --prod`" (C3) | conflicting | modify | Approved removing it. I wrote "Never deploy or publish anything (no Netlify, no production). A human reviews and merges." under "Before you finish", where the old line was, instead of under a new heading. |
| 7 | no rule against secrets (M2) | missing | modify | Approved, but shorter and under an existing heading: "Never commit secrets: no API keys, tokens, passwords or `.env` files." |
| 8 | no test gate before acceptance (M3) | missing | modify | Merged the AI's two lines into one: "Run `npm test` before you propose a change as done. All tests must pass; paste the output." Rejected "Run `npm run build`" as a separate line, because it is not one of the six constraints and the build is not the gate. |
| 9 | line 31 "Edit any file", line 32 "Add packages" (C4) | conflicting | modify | Approved the idea, changed the text: "Edit the files in `src/` that the task needs. Do not weaken or delete existing tests." and "Do not add packages unless the user approves them." The AI's version still allowed adding packages. |
| 10 | "this file wins over `.bolt/prompt`" (C5) | conflicting | reject | `.bolt/prompt` is Bolt's own template file, and I do not use Bolt this week. The line would add scope to a minimal patch. I keep it as a known gap in 5.2. |

### 6.3 The approved patch

`git diff app/AGENTS.md`, after you applied only what you approved:

```text
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
index b786d88..9d267be 100644
--- a/week-10/app/AGENTS.md
+++ b/week-10/app/AGENTS.md
@@ -9,30 +9,33 @@ A React + TypeScript page (Vite) that tells a student whether a campus room is f
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.

-For realism, use real room names and the real timetable from the KBTU portal.
+Use fictional data for one room only. Never use real room names, real timetables or personal data.

 ## Acceptance contract

 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Preserve clear UI feedback on desktop and mobile.

 ## Commands

 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`

 ## You may

-- Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Edit the files in `src/` that the task needs. Do not weaken or delete existing tests.
+- Do not add packages unless the user approves them.
+- Do not add a login, a database or any backend (no Supabase). Bookings are not saved.

 ## Before you finish

+- Run `npm test` before you propose a change as done. All tests must pass; paste the output.
 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Never deploy or publish anything (no Netlify, no production). A human reviews and merges.
+- Never commit secrets: no API keys, tokens, passwords or `.env` files.
```

---

## 7. Task 7 — verify safely

### 7.1 The regression test fails before the mitigation

The risk it covers: **R3**. The real run, with the new test failing:

```text
RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-10/app

 ❯ src/booking.test.ts (27 tests | 1 failed) 6ms
   ✓ canBook - AC1: valid interval, start after now > T02 AC1: request starting exactly at now (540-570) is rejected 1ms
   ✓ canBook - AC1: valid interval, start after now > T03 AC1: zero-duration request (720-720) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > T04 AC1: reversed request (750-720) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > T05 AC1: request ending past the end of the day (1380-1441) is rejected 0ms
   ✓ canBook - AC1: valid interval, start after now > X1 AC1: request ending exactly at 24:00 (1380-1440) is accepted 0ms
   ✓ canBook - AC1: valid interval, start after now > R01 AC1: request starting one minute after now (541-570) is accepted 0ms
   ✓ canBook - AC1: valid interval, start after now > R07 AC1: negative start (-10 to 30) is rejected even when now is earlier (-20) 0ms
   × canBook - AC1: valid interval, start after now > R3 AC1: an unknown current time (now = -1, empty field on the page) gives Unavailable for 08:00-08:30 4ms
     → expected true to be false // Object.is equality
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
   ✓ canBook - AC5: decision without changing booking data > AC5: an Available request (660-720) leaves the bookings unchanged 0ms
   ✓ canBook - AC5: decision without changing booking data > R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call 0ms
   ✓ canBook - AC5: decision without changing booking data > R06 AC5: a rejected overlap request (630-690) leaves the bookings unchanged 0ms
   ✓ canBook - regression tests for the provided buggy code > BUG-A AC4: request touching a booking on both sides (660-700 between 600-660 and 700-760) is accepted 0ms
   ✓ canBook - regression tests for the provided buggy code > BUG-B AC5: an Available request that touches nothing (720-780) leaves the bookings unchanged 0ms

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook - AC1: valid interval, start after now > R3 AC1: an unknown current time (now = -1, empty field on the page) gives Unavailable for 08:00-08:30
AssertionError: expected true to be false // Object.is equality

- Expected
+ Received

- false
+ true

 ❯ src/booking.test.ts:51:28
     49|   test('R3 AC1: an unknown curren…
     50|     const input = { start: 480, e…
     51|     expect(canBook(input)).toBe(f…
       |                            ^
     52|   });
     53| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 26 passed (27)
   Start at  11:30:52
   Duration  353ms (transform 28ms, setup 0ms, collect 23ms, tests 6ms, environment 0ms, prepare 35ms)
```

### 7.2 The manual UI check

| View | Width | What I checked | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Desktop | 1280 px | the R3 case: "Current time" cleared, Start 08:00, End 08:30, Engineering Hall A, then "Check availability". Is the result clear (AC6), is the form, result card and schedule fully visible with nothing overlapping? | Unavailable, with one clear reason: "Enter a valid current time in HH:MM format." Before the fix canBook accepted this case (test R3 failed in 7.1). The two columns are side by side and nothing is cut off. | `evidence/ui-desktop.png` |
| Mobile | 390 px (phone size, touch emulation) | an overlap case: current 09:00, Start 09:30, End 10:30, Engineering Hall A. Does the result card fit, does the long reason wrap, is there no sideways scroll? | Unavailable: 'Overlaps existing booking "Algorithms Lecture" (09:00–10:00).' The text wraps inside the card, the layout is one column, and the page has no horizontal overflow (`scrollWidth` is not larger than the window). | `evidence/ui-mobile.png` |

How it was run: `npm run build`, then `vite preview` on localhost, opened in headless Google Chrome by a
small Playwright script that the Zed agent wrote and ran. It filled the fields, pressed the button and
saved the screenshots. I looked at both images. I did not test on a real phone.

### 7.3 Tests and checks I did not run

<!-- Name each one and why. "None" only if it is true. -->
- No automatic test of `src/App.tsx` (rendering, clicks). It would need React Testing Library and jsdom, which are new dependencies, and AGENTS.md now forbids new packages without approval.
- No real phone and no Safari or Firefox. The mobile check is Chrome's phone emulation at 390 px only.
- `npm run dev` was not run. The UI check used `vite preview` of the production build instead.
- No keyboard-only or screen-reader check, so the accessibility points in the AI's #15 are not verified.
- No CI run, because the project has no CI (R5).
- I did not send the optional Part 7 prompt for extra regression tests, and I did not do the optional with/without AGENTS.md comparison in Part 8.
- I did not try the deploy line or Supabase, on purpose. Those are the risks, and running them is not a safe check.

---

## 8. Task 8 — mitigate two risks

### 8.1 The first mitigation

**Risk:** R1

**If this is the refactor** — the prompt you sent (README Part 8), then the problem → pattern → benefit
line. Otherwise leave both empty.

```text
(not the refactor: this mitigation is the approved AGENTS.md patch of Part 6)
```

**Problem → pattern → benefit:**

Not the refactor.

**What I rejected from the agent's patch, and why:**

From the AI's draft (6.1) I rejected the new "## You must not" heading, because a minimal patch keeps the same headings. I also rejected the "this file wins over `.bolt/prompt`" line, the separate "Run `npm run build`" line and the "AC6 TODO". And I rejected keeping the wrong AC4 text. All decisions are in 6.2. The same commit (`week-10: AGENTS.md patch, approved`) also closes R2 and R6, see 8.3.

The diff I approved (`git diff`):

```text
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
index b786d88..9d267be 100644
--- a/week-10/app/AGENTS.md
+++ b/week-10/app/AGENTS.md
@@ -9,30 +9,33 @@ A React + TypeScript page (Vite) that tells a student whether a campus room is f
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.

-For realism, use real room names and the real timetable from the KBTU portal.
+Use fictional data for one room only. Never use real room names, real timetables or personal data.

 ## Acceptance contract

 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Preserve clear UI feedback on desktop and mobile.

 ## Commands

 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`

 ## You may

-- Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Edit the files in `src/` that the task needs. Do not weaken or delete existing tests.
+- Do not add packages unless the user approves them.
+- Do not add a login, a database or any backend (no Supabase). Bookings are not saved.

 ## Before you finish

+- Run `npm test` before you propose a change as done. All tests must pass; paste the output.
 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Never deploy or publish anything (no Netlify, no production). A human reviews and merges.
+- Never commit secrets: no API keys, tokens, passwords or `.env` files.
```

### 8.2 The second mitigation

**Risk:** R3

**If this is the refactor** — the prompt you sent (README Part 8), then the problem → pattern → benefit
line. Otherwise leave both empty.

```text
Context: the project is `se-practice/week-10/app` (ignore node_modules/ and dist/). Read `AGENTS.md` in that folder first and follow it. The risk to fix is R3: in `src/App.tsx`, `const current = toMinutes(currentStr) ?? -1;` turns an empty "Current time" field into now = -1, and `canBook` in `src/booking.ts` never checks `now`, so a request in the past (08:00-08:30) shows "Available" (breaks AC1). The regression test `R3 AC1: ...` in `src/booking.test.ts` fails now and must pass after your change. Also, the page's availability logic (toMinutes, toHHMM, evaluateBooking with a second copy of every rule, and the constants MIN_IN_DAY / MAX_DURATION, which booking.ts declares but never uses, so `npm run lint` fails) lives inside the React component file.

Refactor the availability logic into a small, pure module, keeping the existing function inputs, outputs, and UI behavior. Use a pattern only if the identified design problem justifies it. Do not add new features or dependencies. Show the files you plan to edit before making changes.

For this turn: only show the plan (files and the exact changes you propose, as a diff if you can). Do not edit anything and do not run the terminal yet. I will review and approve.
```

**Problem → pattern → benefit:**

Problem: the availability logic was split. `canBook` decided, but `App.tsx` parsed the times, put in the `-1` fallback and kept a second copy of every rule to build the messages, so the AC1 hole sat in React code that no test could reach. Pattern: no named design pattern, only an extracted pure module. `src/booking.ts` now holds every rule once (`findRejections`, and `canBook` is `findRejections(...).length === 0` with the same input and output). `src/availability.ts` holds the pure page logic (`toMinutes`, `toHHMM`, `evaluateBooking`). Benefit: one source for the rules, the page messages can now be tested without React, an unknown current time is rejected with a clear message, and `npm run lint` is clean.

**What I rejected from the agent's patch, and why:**

From the agent's plan I rejected three things before it applied anything. First, making `CanBookInput.bookings` `readonly`, because it changes the public type and was not needed for R3. Second, changing `Timeline` in `App.tsx` to use the new `overlaps`, because it is UI code outside the risk. Third, starting the dev server, because I check the UI myself. I modified its optional test file to exactly two tests. After it applied the change I removed one extra empty line it left in `App.tsx`. Everything else I read line by line: all message texts are the same, in the same order, and `booking.test.ts` was not touched.

The diff I approved (`git diff`):

```text
diff --git a/week-10/app/src/booking.ts b/week-10/app/src/booking.ts
index 46ca44c..f3baf02 100644
--- a/week-10/app/src/booking.ts
+++ b/week-10/app/src/booking.ts
@@ -11,22 +11,45 @@ export type CanBookInput = {
   bookings: BookingInterval[];
 };

-const MIN_IN_DAY = 1440;
-const MAX_DURATION = 120;
+export const MIN_IN_DAY = 1440;
+export const MAX_DURATION = 120;

-export function canBook({ start, end, now, blocked, bookings }: {
-  start: number;
-  end: number;
-  now: number;
-  blocked: boolean;
-  bookings: { start: number; end: number }[];
-}): boolean {
-  if (!(0 <= start && start < end && end <= 1440)) return false;
-  if (!(start > now)) return false;
-  if (end - start > 120) return false;
-  if (blocked) return false;
-  for (const b of bookings) {
-    if (start < b.end && end > b.start) return false;
-  }
-  return true;
+// Each failed rule is returned as data so the page can explain it
+// without re-implementing the rule.
+export type Rejection<B extends BookingInterval = BookingInterval> =
+  | { rule: "invalid-now" }
+  | { rule: "invalid-interval" }
+  | { rule: "not-after-now" }
+  | { rule: "too-long" }
+  | { rule: "blocked" }
+  | { rule: "overlap"; booking: B };
+
+// Touching endpoints (a.end === b.start) is not an overlap.
+export function overlaps(a: BookingInterval, b: BookingInterval): boolean {
+  return a.start < b.end && a.end > b.start;
+}
+
+export function findRejections<B extends BookingInterval>(
+  input: Omit<CanBookInput, "bookings"> & { bookings: B[] },
+): Rejection<B>[] {
+  const { start, end, now, blocked, bookings } = input;
+  const rejections: Rejection<B>[] = [];
+
+  // AC1: without a real current time we cannot tell whether a request is in the past.
+  if (!(0 <= now && now < MIN_IN_DAY)) rejections.push({ rule: "invalid-now" });
+  if (!(0 <= start && start < end && end <= MIN_IN_DAY)) rejections.push({ rule: "invalid-interval" });
+  if (!(start > now)) rejections.push({ rule: "not-after-now" });
+  // AC2
+  if (end - start > MAX_DURATION) rejections.push({ rule: "too-long" });
+  // AC3
+  if (blocked) rejections.push({ rule: "blocked" });
+  // AC4
+  const clash = bookings.find((b) => overlaps({ start, end }, b));
+  if (clash) rejections.push({ rule: "overlap", booking: clash });
+
+  return rejections;
+}
+
+export function canBook(input: CanBookInput): boolean {
+  return findRejections(input).length === 0;
 }
diff --git a/week-10/app/src/App.tsx b/week-10/app/src/App.tsx
index 56061cb..e68c24c 100644
--- a/week-10/app/src/App.tsx
+++ b/week-10/app/src/App.tsx
@@ -8,7 +8,7 @@ import {
   MapPin,
   XCircle,
 } from "lucide-react";
-import { canBook } from "./booking";
+import { evaluateBooking, toHHMM, toMinutes, type Verdict } from "./availability";

 type Booking = {
   id: string;
@@ -26,9 +26,6 @@ type Room = {
   bookings: Booking[];
 };

-const MIN_IN_DAY = 1440;
-const MAX_DURATION = 120;
-
 const SAMPLE_ROOMS: Room[] = [
   {
     id: "r1",
@@ -75,89 +72,6 @@ const SAMPLE_ROOMS: Room[] = [
   },
 ];

-function toMinutes(time: string): number | null {
-  if (!/^\d{2}:\d{2}$/.test(time)) return null;
-  const [h, m] = time.split(":").map(Number);
-  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
-  return h * 60 + m;
-}
-
-function toHHMM(min: number): string {
-  const h = Math.floor(min / 60);
-  const m = min % 60;
-  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
-}
-
-type Verdict =
-  | { kind: "available" }
-  | { kind: "unavailable"; reasons: string[] };
-
-function evaluateBooking(
-  room: Room | undefined,
-  start: number | null,
-  end: number | null,
-  current: number,
-): Verdict {
-  const reasons: string[] = [];
-
-  if (!room) {
-    return { kind: "unavailable", reasons: ["Select a room to check."] };
-  }
-
-  if (start === null || end === null) {
-    return {
-      kind: "unavailable",
-      reasons: ["Enter valid start and end times in HH:MM format."],
-    };
-  }
-
-  // The decision itself comes from canBook in src/booking.ts.
-  // The checks below only build the messages for the page.
-  if (
-    canBook({
-      start,
-      end,
-      now: current,
-      blocked: room.blocked,
-      bookings: room.bookings,
-    })
-  ) {
-    return { kind: "available" };
-  }
-
-  // AC1: 0 <= start < end <= 1440, start after current time
-  if (start < 0 || end > MIN_IN_DAY || start >= end) {
-    reasons.push(
-      "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.",
-    );
-  }
-  if (start <= current) {
-    reasons.push("Start time must be after the current time.");
-  }
-
-  // AC2: duration <= 120 min
-  if (end - start > MAX_DURATION) {
-    reasons.push("Booking cannot be longer than 120 minutes.");
-  }
-
-  // AC3: blocked room
-  if (room.blocked) {
-    reasons.push("This room is currently blocked and cannot be booked.");
-  }
-
-  // AC4: overlap (touching endpoints allowed)
-  const overlapping = room.bookings.find(
-    (b) => start < b.end && end > b.start,
-  );
-  if (overlapping) {
-    reasons.push(
-      `Overlaps existing booking "${overlapping.title}" (${toHHMM(overlapping.start)}–${toHHMM(overlapping.end)}).`,
-    );
-  }
-
-  return { kind: "unavailable", reasons };
-}
-
 function App() {
   const [roomId, setRoomId] = useState<string>(SAMPLE_ROOMS[0].id);
   const [currentStr, setCurrentStr] = useState("09:00");
@@ -170,7 +84,7 @@ function App() {
     [roomId],
   );

-  const current = toMinutes(currentStr) ?? -1;
+  const current = toMinutes(currentStr);
   const start = toMinutes(startStr);
   const end = toMinutes(endStr);

diff --git a/week-10/app/src/availability.ts b/week-10/app/src/availability.ts
new file mode 100644
index 0000000..4b74fce
--- /dev/null
+++ b/week-10/app/src/availability.ts
@@ -0,0 +1,76 @@
+import { findRejections, MAX_DURATION, type BookingInterval, type Rejection } from "./booking";
+
+export type TitledBooking = BookingInterval & { title: string };
+
+export type CheckableRoom = {
+  blocked: boolean;
+  bookings: TitledBooking[];
+};
+
+export type Verdict =
+  | { kind: "available" }
+  | { kind: "unavailable"; reasons: string[] };
+
+const INVALID_NOW_REASON = "Enter a valid current time in HH:MM format.";
+
+export function toMinutes(time: string): number | null {
+  if (!/^\d{2}:\d{2}$/.test(time)) return null;
+  const [h, m] = time.split(":").map(Number);
+  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
+  return h * 60 + m;
+}
+
+export function toHHMM(min: number): string {
+  const h = Math.floor(min / 60);
+  const m = min % 60;
+  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
+}
+
+function reasonFor(r: Rejection<TitledBooking>): string {
+  switch (r.rule) {
+    case "invalid-now":
+      return INVALID_NOW_REASON;
+    case "invalid-interval":
+      return "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.";
+    case "not-after-now":
+      return "Start time must be after the current time.";
+    case "too-long":
+      return `Booking cannot be longer than ${MAX_DURATION} minutes.`;
+    case "blocked":
+      return "This room is currently blocked and cannot be booked.";
+    case "overlap":
+      return `Overlaps existing booking "${r.booking.title}" (${toHHMM(r.booking.start)}–${toHHMM(r.booking.end)}).`;
+  }
+}
+
+export function evaluateBooking(
+  room: CheckableRoom | undefined,
+  start: number | null,
+  end: number | null,
+  current: number | null,
+): Verdict {
+  if (!room) {
+    return { kind: "unavailable", reasons: ["Select a room to check."] };
+  }
+  if (start === null || end === null) {
+    return {
+      kind: "unavailable",
+      reasons: ["Enter valid start and end times in HH:MM format."],
+    };
+  }
+  if (current === null) {
+    return { kind: "unavailable", reasons: [INVALID_NOW_REASON] };
+  }
+
+  const rejections = findRejections({
+    start,
+    end,
+    now: current,
+    blocked: room.blocked,
+    bookings: room.bookings,
+  });
+
+  return rejections.length === 0
+    ? { kind: "available" }
+    : { kind: "unavailable", reasons: rejections.map(reasonFor) };
+}
diff --git a/week-10/app/src/availability.test.ts b/week-10/app/src/availability.test.ts
new file mode 100644
index 0000000..f4ae3ab
--- /dev/null
+++ b/week-10/app/src/availability.test.ts
@@ -0,0 +1,20 @@
+import { describe, test, expect } from 'vitest';
+import { evaluateBooking } from './availability';
+
+describe('evaluateBooking - page messages', () => {
+  test('R3 AC1: an empty current time (current = null) gives Unavailable with a current-time message', () => {
+    const room = { blocked: false, bookings: [] };
+    expect(evaluateBooking(room, 600, 660, null)).toEqual({
+      kind: 'unavailable',
+      reasons: ['Enter a valid current time in HH:MM format.'],
+    });
+  });
+
+  test('AC1: a past request (now 09:00, request 08:00-08:30, free room) gives Unavailable', () => {
+    const room = { blocked: false, bookings: [] };
+    expect(evaluateBooking(room, 480, 510, 540)).toEqual({
+      kind: 'unavailable',
+      reasons: ['Start time must be after the current time.'],
+    });
+  });
+});
```

### 8.3 The residual risk

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 3 | 3 | 9 | 1 | 3 | 3 | AGENTS.md now says "Never deploy or publish anything ... A human reviews and merges"; checker C5 PASS. Impact stays 3: a human can still deploy by hand, and `.bolt/prompt` still says "worthy for production". |
| R3 | 2 | 2 | 4 | 1 | 2 | 2 | canBook rejects a now outside 0-1439; the page passes `null` and shows "Enter a valid current time"; both R3 tests pass (8.4); desktop screenshot. Remaining: the current time is still typed by hand, not read from the clock. |
| R2 | 3 | 3 | 9 | 1 | 3 | 3 | closed by the same AGENTS.md patch: AC4 as in the contract (C3 PASS), `npm test` exists (A3 PASS), tests before acceptance (C6 PASS). An agent can still ignore the file. |
| R6 | 2 | 3 | 6 | 1 | 3 | 3 | closed by the same patch: "Use fictional data for one room only. Never use real room names ..." (C1 PASS). |
| R4 | 2 | 2 | 4 | 1 | 2 | 2 | closed by the same refactor: every rule once in `src/booking.ts`, the page only maps rejections to text; `npm run lint` now gives no errors. |

### 8.4 The final run

The real output of the **full** suite after both mitigations. Every test must pass.

```text
RUN  v3.2.7 /Users/hevilim/Developer/se-practice/week-10/app

 ✓ src/availability.test.ts (2 tests) 2ms
   ✓ evaluateBooking - page messages (2)
     ✓ R3 AC1: an empty current time (current = null) gives Unavailable with a current-time message 1ms
     ✓ AC1: a past request (now 09:00, request 08:00-08:30, free room) gives Unavailable 0ms
 ✓ src/booking.test.ts (27 tests) 3ms
   ✓ canBook - AC1: valid interval, start after now (8)
     ✓ T02 AC1: request starting exactly at now (540-570) is rejected 1ms
     ✓ T03 AC1: zero-duration request (720-720) is rejected 0ms
     ✓ T04 AC1: reversed request (750-720) is rejected 0ms
     ✓ T05 AC1: request ending past the end of the day (1380-1441) is rejected 0ms
     ✓ X1 AC1: request ending exactly at 24:00 (1380-1440) is accepted 0ms
     ✓ R01 AC1: request starting one minute after now (541-570) is accepted 0ms
     ✓ R07 AC1: negative start (-10 to 30) is rejected even when now is earlier (-20) 0ms
     ✓ R3 AC1: an unknown current time (now = -1, empty field on the page) gives Unavailable for 08:00-08:30 0ms
   ✓ canBook - AC2: at most 120 minutes (2)
     ✓ T06 AC2: exactly 120 minutes (720-840) is accepted 0ms
     ✓ T07 AC2: 121 minutes (720-841) is rejected 0ms
   ✓ canBook - AC3: blocked room (1)
     ✓ T13 AC3: otherwise-available request (660-720) in a blocked room is rejected 0ms
   ✓ canBook - AC4: no overlap, touching allowed (11)
     ✓ T01 AC4: request touching the end of the booking (660-720) is accepted 0ms
     ✓ T08 AC4: request touching the start of the booking (570-600) is accepted 0ms
     ✓ T09 AC4: partial overlap (630-690) is rejected 0ms
     ✓ T10 AC4: request containing the booking (570-690) is rejected 0ms
     ✓ T11 AC4: request inside the booking (615-645) is rejected 0ms
     ✓ T12 AC4: request identical to the booking (600-660) is rejected 0ms
     ✓ R02 AC4: one-minute overlap at the booking end (659-720) is rejected 0ms
     ✓ R03 AC4: one-minute overlap at the booking start (570-601) is rejected 0ms
     ✓ R04 AC4: overlap with the second booking only (750-800) is rejected 0ms
     ✓ T14 AC4: 630-690 with no existing bookings is accepted 0ms
     ✓ X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted 0ms
   ✓ canBook - AC5: decision without changing booking data (3)
     ✓ AC5: an Available request (660-720) leaves the bookings unchanged 0ms
     ✓ R05 AC5: frozen bookings in reverse order are not sorted or changed by an Available call 0ms
     ✓ R06 AC5: a rejected overlap request (630-690) leaves the bookings unchanged 0ms
   ✓ canBook - regression tests for the provided buggy code (2)
     ✓ BUG-A AC4: request touching a booking on both sides (660-700 between 600-660 and 700-760) is accepted 0ms
     ✓ BUG-B AC5: an Available request that touches nothing (720-780) leaves the bookings unchanged 0ms

 Test Files  2 passed (2)
      Tests  29 passed (29)
   Start at  11:38:24
   Duration  279ms (transform 36ms, setup 0ms, collect 47ms, tests 4ms, environment 0ms, prepare 63ms)
```

After this run, `npm run lint` and `npm run typecheck` gave no errors, and `npm run build` passed.

---

## 9. Task 9, and what still fails

### 9.1 A background agent on this project

Rules for an agent working asynchronously on a separate branch. Be specific to this project: name
its files and its commands.

| Rule | What I require |
| --- | --- |
| Isolation | its own branch made from `week-10` (for example `agent/<task>`) in a separate git worktree; it never commits to `main` or `week-10`, never force-pushes and never merges |
| Permitted files | only `week-10/app/src/booking.ts`, `src/availability.ts`, `src/App.tsx` and new test files in `src/`; it may add tests to `src/booking.test.ts`, but never change or delete an existing assertion. `AGENTS.md`, `package.json`, `package-lock.json` and everything outside `week-10/app/` are read-only |
| Commands | only `npm ci`, `npm test`, `npx vitest run`, `npm run lint`, `npm run typecheck` and `npm run build`, inside `week-10/app/`; no `npm install <package>`, no `npx` of any other tool, no network calls from the code |
| Prohibited actions | no deploy or publish (no `netlify`, no `vercel`, no GitHub Pages), no Supabase, login or database, no secrets or `.env` files, no real room names or KBTU timetable data, no new dependencies, no changing AC1–AC6 |
| Required evidence | the `git diff` of its branch, the full pasted output of `npm test` (all pass, same count or more than 29), the output of `npm run lint`, `npm run typecheck` and `npm run build`, a list of changed files, which risk IDs from the register it touched, and a short note on what it did not check |
| Before merging or deploying | I read the whole diff and rerun `npm test` and `npm run lint` myself on my computer; I check the UI at desktop and phone width; I update the risk register; only then do I merge by hand. Deploying is never allowed for this project |

### 9.2 Optional — the deck's checklist prompt (not graded)

<!-- If you sent it: the answer, and one thing it has that your rules in 9.1 do not, or the reverse. -->
Not sent.

### 9.3 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | the last run of `python3 tests/check_audit.py` gave 31 PASS, 0 FAIL, 0 ERROR |

---

## 10. Release decision and conclusion

**Decision:** CONDITIONAL

<!-- Keep one word above. GO is not allowed while any confirmed risk still scores 6 or more.
     Then 80-150 words, in your own words, without the assistant: why this decision, from the
     register, the tests and what you are still unsure about. Name at least two risk IDs.
     Worthless: "The project is mostly fine, so GO."
     Worth everything: "CONDITIONAL. R2 (the deploy line in AGENTS.md, 3 x 3 = 9) is closed by the
     approved patch, now 1 x 3. R4 (the page accepts a past start when 'now' is typed by hand,
     2 x 2 = 4) is open, owned by me, controlled by the AC1 test. The UI was checked at two widths,
     but no test covers App.tsx, so a regression there would be invisible." -->

<!-- Write your conclusion below this line -->

CONDITIONAL. The two 9s are closed by the approved AGENTS.md patch: R1 (the deploy line) and R2
(the reversed AC4 and the missing test command) are now 1 x 3 = 3, and R6 (real KBTU data) dropped
from 6 to 3. The code risk R3 (an empty current time gave Available for a past slot) is fixed by the
refactor and is now 1 x 2 = 2. Its regression test failed first and passes now, and all 29 tests are
green. No confirmed risk is at 6 or more. It is not a GO because R5 (no CI or hooks, 2 x 2 = 4) is
open: nothing stops a broken push. R7 (the unused Supabase package) and R9 (four rooms instead of
one) are also open. All three are owned by me. No test covers App.tsx, so a page bug would stay
invisible.
