# SIS #04 — Report: Evolving the Smart Campus Room Availability Checker

<!-- The ONLY file you write prose in. Keep every numbered heading (## 1. … ## 10.), every
     ### sub-heading and every **Label:** word — the checker finds your answers by them.
     Replace every "(write here)" and "(paste here)". Delete these <!-- --> comments if you like. -->

## 1. Setup and starting point

<!-- Model: the exact model with its version, as the tool shows it ("ChatGPT" is a tool, not a
     model). If the tool does not show it, write: not displayed
     Starting point: week-08 | week-07 | sis-03 | starter   (README section 3)
     Baseline commit: the commit that brings your starting point into sis-04/app/ UNCHANGED —
     git rev-parse --short HEAD right after that commit. It is your "initial version". -->

| Item | Value |
| --- | --- |
| Assistant (tool) | Claude (claude.ai) |
| Assistant model | Claude Opus 5.5 |
| Starting point | week-08 |
| Baseline commit | f04e465 |
| Language (ts or js) | ts |
| Vitest version | 3.2.7 |
| Where I ran the tests | my computer |

### 1.1 Baseline run

<!-- Before you change anything: run the tests of your starting point inside app/ and paste the
     REAL output. No tests yet (starter, sis-03)? Paste the run anyway: Vitest prints
     "No test files found". That is your honest "original" number, 0/0. -->

```text

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/sis-04/app

 ✓ src/booking.test.ts (26 tests) 3ms

 Test Files  1 passed (1)
      Tests  26 passed (26)
   Start at  22:53:23
   Duration  349ms (transform 25ms, setup 0ms, collect 22ms, tests 3ms, environment 0ms, prepare 123ms)
```

## 2. Context for the assistant

### 2.1 Repository map

<!-- The concise map you gave the assistant: the files that matter and one line each on what
     they do. A tree is fine:  src/App.tsx — the page, holds the rooms and the form … -->

```text
sis-04/app/  (React 18 + TypeScript + Vite + Tailwind, tests with Vitest 3.2.7)
  package.json        scripts dev, build, test (vitest run); dependencies react, lucide-react, @supabase/supabase-js
  index.html          the page shell, loads src/main.tsx
  src/main.tsx        mounts <App /> into #root
  src/App.tsx         the whole page (487 lines): Room type, SAMPLE_ROOMS (4 rooms), toMinutes(), toHHMM(),
                      evaluateBooking() (calls canBook, then builds the reasons), App() (form and state),
                      ResultCard, RoomSchedule, Timeline
  src/booking.ts      canBook({ start, end, now, blocked, bookings }) for AC1-AC5, types BookingInterval and CanBookInput
  src/booking.test.ts 26 Vitest tests for canBook (T01-T14, X1, X2, R01-R07, AC5, BUG-A, BUG-B)
  src/index.css       Tailwind directives only
```

### 2.2 The context message as sent

<!-- The whole first message of your analysis chat: the map, AC1–AC6, F1–F5 and the constraints
     (no login, payments, live APIs or database; fictional data only). Unedited. -->

```text
Hello. I am working on a small university project: the Smart Campus Room Availability Checker. It is a React + TypeScript page made with Vite, tested with Vitest. I want to extend it and refactor it. Please do not write code yet and do not propose a full rewrite. I need an analysis and a plan of small steps.

Repository map:
sis-04/app/  (React 18 + TypeScript + Vite + Tailwind, tests with Vitest 3.2.7)
  package.json        scripts dev, build, test (vitest run); dependencies react, lucide-react, @supabase/supabase-js
  index.html          the page shell, loads src/main.tsx
  src/main.tsx        mounts <App /> into #root
  src/App.tsx         the whole page (487 lines): Room type, SAMPLE_ROOMS (4 rooms), toMinutes(), toHHMM(),
                      evaluateBooking() (calls canBook, then builds the reasons), App() (form and state),
                      ResultCard, RoomSchedule, Timeline
  src/booking.ts      canBook({ start, end, now, blocked, bookings }) for AC1-AC5, types BookingInterval and CanBookInput
  src/booking.test.ts 26 Vitest tests for canBook (T01-T14, X1, X2, R01-R07, AC5, BUG-A, BUG-B)
  src/index.css       Tailwind directives only

Requirements I must keep (AC1-AC6):
AC1 Reject start >= end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Clear, responsive feedback on desktop and mobile.

New feature: a catalog of at least four fictional rooms. Each room has id, name, capacity, equipment list, blocked status and its own bookings. Show only the rooms that satisfy the user's requirements. The availability check must use the chosen room's bookings, not another room's data.
F1 Capacity filter: room capacity must be greater than or equal to the requested attendees.
F2 Equipment filter: the room must contain ALL selected required items.
F3 A blocked room cannot be reported as available.
F4 Show a clear empty state when no rooms match.
F5 Changing the selected room must refresh the availability result appropriately.

Fixed structure: src/rooms.ts (Room type and ROOMS, data only), src/filter.ts (filterRooms(rooms, { attendees, equipment })), src/booking.ts (canBook unchanged, and checkRoom(rooms, roomId, { start, end, now }) which calls canBook with the chosen room's blocked and bookings). The UI imports the rules and holds no room data and no rule of its own.

Constraints: fictional data only, a fixed current time, no login, no payments, no live APIs, no database, no network calls, no browser storage.

Here are the two files with the logic.

src/booking.ts:
export type BookingInterval = {
  start: number; // minutes from midnight
  end: number;
};

export type CanBookInput = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: BookingInterval[];
};

const MIN_IN_DAY = 1440;
const MAX_DURATION = 120;

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
    if (start < b.end && end > b.start) return false;
  }
  return true;
}

src/App.tsx:
import { useMemo, useState } from "react";
import {
  Building2,
  CalendarClock,
  CheckCircle2,
  Clock,
  DoorClosed,
  MapPin,
  XCircle,
} from "lucide-react";
import { canBook } from "./booking";

type Booking = {
  id: string;
  title: string;
  start: number; // minutes from midnight
  end: number;
};

type Room = {
  id: string;
  name: string;
  building: string;
  capacity: number;
  blocked: boolean;
  bookings: Booking[];
};

const MIN_IN_DAY = 1440;
const MAX_DURATION = 120;

const SAMPLE_ROOMS: Room[] = [
  {
    id: "r1",
    name: "Engineering Hall A",
    building: "Block C · Floor 2",
    capacity: 40,
    blocked: false,
    bookings: [
      { id: "b1", title: "Algorithms Lecture", start: 540, end: 600 },
      { id: "b2", title: "Faculty Meeting", start: 780, end: 840 },
      { id: "b3", title: "Robotics Lab", start: 1080, end: 1140 },
    ],
  },
  {
    id: "r2",
    name: "Innovation Lab",
    building: "Block A · Floor 1",
    capacity: 24,
    blocked: true,
    bookings: [
      { id: "b4", title: "Maintenance", start: 600, end: 660 },
    ],
  },
  {
    id: "r3",
    name: "Library Study Room 3",
    building: "Library · Floor 3",
    capacity: 12,
    blocked: false,
    bookings: [
      { id: "b5", title: "Group Study", start: 660, end: 720 },
      { id: "b6", title: "Book Club", start: 1020, end: 1080 },
    ],
  },
  {
    id: "r4",
    name: "Auditorium B",
    building: "Main Building · Ground",
    capacity: 200,
    blocked: false,
    bookings: [
      { id: "b7", title: "Guest Lecture", start: 600, end: 660 },
    ],
  },
];

function toMinutes(time: string): number | null {
  if (!/^\d{2}:\d{2}$/.test(time)) return null;
  const [h, m] = time.split(":").map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

function toHHMM(min: number): string {
  const h = Math.floor(min / 60);
  const m = min % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

type Verdict =
  | { kind: "available" }
  | { kind: "unavailable"; reasons: string[] };

function evaluateBooking(
  room: Room | undefined,
  start: number | null,
  end: number | null,
  current: number,
): Verdict {
  const reasons: string[] = [];

  if (!room) {
    return { kind: "unavailable", reasons: ["Select a room to check."] };
  }

  if (start === null || end === null) {
    return {
      kind: "unavailable",
      reasons: ["Enter valid start and end times in HH:MM format."],
    };
  }

  // The decision itself comes from canBook in src/booking.ts.
  // The checks below only build the messages for the page.
  if (
    canBook({
      start,
      end,
      now: current,
      blocked: room.blocked,
      bookings: room.bookings,
    })
  ) {
    return { kind: "available" };
  }

  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    reasons.push(
      "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.",
    );
  }
  if (start <= current) {
    reasons.push("Start time must be after the current time.");
  }

  // AC2: duration <= 120 min
  if (end - start > MAX_DURATION) {
    reasons.push("Booking cannot be longer than 120 minutes.");
  }

  // AC3: blocked room
  if (room.blocked) {
    reasons.push("This room is currently blocked and cannot be booked.");
  }

  // AC4: overlap (touching endpoints allowed)
  const overlapping = room.bookings.find(
    (b) => start < b.end && end > b.start,
  );
  if (overlapping) {
    reasons.push(
      `Overlaps existing booking "${overlapping.title}" (${toHHMM(overlapping.start)}–${toHHMM(overlapping.end)}).`,
    );
  }

  return { kind: "unavailable", reasons };
}

function App() {
  const [roomId, setRoomId] = useState<string>(SAMPLE_ROOMS[0].id);
  const [currentStr, setCurrentStr] = useState("09:00");
  const [startStr, setStartStr] = useState("10:00");
  const [endStr, setEndStr] = useState("11:00");
  const [submitted, setSubmitted] = useState(false);

  const room = useMemo(
    () => SAMPLE_ROOMS.find((r) => r.id === roomId),
    [roomId],
  );

  const current = toMinutes(currentStr) ?? -1;
  const start = toMinutes(startStr);
  const end = toMinutes(endStr);

  const verdict = useMemo(
    () => evaluateBooking(room, start, end, current),
    [room, start, end, current],
  );

  const check = () => setSubmitted(true);

  const reset = () => {
    setSubmitted(false);
  };

  const dayNow = new Date();
  const todayLabel = dayNow.toLocaleDateString(undefined, {
    weekday: "long",
    month: "short",
    day: "numeric",
  });

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-sky-600 text-white flex items-center justify-center shadow-sm">
            <Building2 className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-semibold tracking-tight text-slate-900">
              Smart Campus Room Availability
            </h1>
            <p className="text-sm text-slate-500">
              Check whether a campus room is free for your requested time slot.
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 grid gap-6 lg:grid-cols-5">
        {/* Form column */}
        <section className="lg:col-span-2">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
            <div className="flex items-center gap-2 mb-5">
              <CalendarClock className="h-4 w-4 text-sky-600" />
              <h2 className="font-semibold text-slate-900">Check a slot</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Room
                </label>
                <select
                  value={roomId}
                  onChange={(e) => {
                    setRoomId(e.target.value);
                    setSubmitted(false);
                  }}
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                >
                  {SAMPLE_ROOMS.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.name} {r.blocked ? "(blocked)" : ""}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Current time (HH:MM)
                </label>
                <input
                  type="time"
                  value={currentStr}
                  onChange={(e) => {
                    setCurrentStr(e.target.value);
                    setSubmitted(false);
                  }}
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Start
                  </label>
                  <input
                    type="time"
                    value={startStr}
                    onChange={(e) => {
                      setStartStr(e.target.value);
                      setSubmitted(false);
                    }}
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    End
                  </label>
                  <input
                    type="time"
                    value={endStr}
                    onChange={(e) => {
                      setEndStr(e.target.value);
                      setSubmitted(false);
                    }}
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <div className="flex gap-2 pt-1">
                <button
                  onClick={check}
                  className="flex-1 rounded-lg bg-sky-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-sky-700 active:bg-sky-800 transition-colors"
                >
                  Check availability
                </button>
                <button
                  onClick={reset}
                  className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Result + schedule column */}
        <section className="lg:col-span-3 space-y-6">
          {submitted ? (
            <ResultCard verdict={verdict} room={room} start={start} end={end} />
          ) : (
            <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-8 text-center text-slate-500 text-sm">
              Fill in the form and press{" "}
              <span className="font-semibold text-slate-700">
                Check availability
              </span>{" "}
              to see the result.
            </div>
          )}

          {room && <RoomSchedule room={room} todayLabel={todayLabel} />}
        </section>
      </main>

      <footer className="max-w-5xl mx-auto px-4 sm:px-6 pb-10 text-center text-xs text-slate-400">
        Fictional sample data · Times are in 24-hour format · No bookings are
        actually saved
      </footer>
    </div>
  );
}

function ResultCard({
  verdict,
  room,
  start,
  end,
}: {
  verdict: Verdict;
  room: Room | undefined;
  start: number | null;
  end: number | null;
}) {
  if (verdict.kind === "available") {
    return (
      <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5 sm:p-6 shadow-sm">
        <div className="flex items-start gap-3">
          <CheckCircle2 className="h-6 w-6 text-emerald-600 mt-0.5 shrink-0" />
          <div>
            <h3 className="font-semibold text-emerald-900">Available</h3>
            <p className="text-sm text-emerald-800 mt-1">
              {room?.name} is free from {toHHMM(start ?? 0)} to{" "}
              {toHHMM(end ?? 0)}. You can proceed with this booking.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const palette = {
    border: "border-rose-200",
    bg: "bg-rose-50",
    icon: "text-rose-600",
    title: "text-rose-900",
    body: "text-rose-800",
    Icon: XCircle,
    label: "Unavailable",
  };

  return (
    <div className={`rounded-2xl border ${palette.border} ${palette.bg} p-5 sm:p-6 shadow-sm`}>
      <div className="flex items-start gap-3">
        <palette.Icon className={`h-6 w-6 ${palette.icon} mt-0.5 shrink-0`} />
        <div className="w-full">
          <h3 className={`font-semibold ${palette.title}`}>{palette.label}</h3>
          <ul className={`mt-2 text-sm ${palette.body} space-y-1.5 list-disc list-inside`}>
            {verdict.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function RoomSchedule({ room, todayLabel }: { room: Room; todayLabel: string }) {
  const sorted = [...room.bookings].sort((a, b) => a.start - b.start);
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
      <div className="flex items-center justify-between gap-2 mb-4">
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-sky-600" />
          <h2 className="font-semibold text-slate-900">{room.name}</h2>
        </div>
        <span className="text-xs text-slate-400">{todayLabel}</span>
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500 mb-4">
        <span>{room.building}</span>
        <span className="flex items-center gap-1">
          <DoorClosed className="h-3.5 w-3.5" /> Seats {room.capacity}
        </span>
        {room.blocked ? (
          <span className="inline-flex items-center rounded-full bg-rose-100 text-rose-700 px-2 py-0.5 font-medium">
            Blocked
          </span>
        ) : (
          <span className="inline-flex items-center rounded-full bg-emerald-100 text-emerald-700 px-2 py-0.5 font-medium">
            Open
          </span>
        )}
      </div>

      <Timeline room={room} />

      <h3 className="text-sm font-medium text-slate-700 mt-5 mb-2">
        Existing bookings
      </h3>
      {sorted.length === 0 ? (
        <p className="text-sm text-slate-400">No bookings today.</p>
      ) : (
        <ul className="divide-y divide-slate-100">
          {sorted.map((b) => (
            <li key={b.id} className="flex items-center justify-between py-2 text-sm">
              <span className="text-slate-700">{b.title}</span>
              <span className="flex items-center gap-1 text-slate-500 tabular-nums">
                <Clock className="h-3.5 w-3.5" />
                {toHHMM(b.start)}–{toHHMM(b.end)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Timeline({ room }: { room: Room }) {
  const blocks = Array.from({ length: 24 }, (_, h) => h);
  return (
    <div>
      <div className="flex h-8 w-full overflow-hidden rounded-md border border-slate-200">
        {blocks.map((h) => {
          const start = h * 60;
          const end = start + 60;
          const booking = room.bookings.find(
            (b) => start < b.end && end > b.start,
          );
          const blockedSeg = room.blocked;
          let cls = "bg-emerald-100 hover:bg-emerald-200";
          if (blockedSeg) cls = "bg-rose-200 hover:bg-rose-300";
          else if (booking) cls = "bg-sky-200 hover:bg-sky-300";
          return (
            <div
              key={h}
              title={`${toHHMM(start)}–${toHHMM(end)}`}
              className={`flex-1 transition-colors ${cls}`}
            />
          );
        })}
      </div>
      <div className="flex justify-between mt-1 text-[10px] text-slate-400 tabular-nums">
        <span>00:00</span>
        <span>06:00</span>
        <span>12:00</span>
        <span>18:00</span>
        <span>24:00</span>
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2 text-xs text-slate-500">
        <span className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-sm bg-emerald-200" /> Free
        </span>
        <span className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-sm bg-sky-300" /> Booked
        </span>
        <span className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-sm bg-rose-300" /> Blocked
        </span>
      </div>
    </div>
  );
}

export default App;

Please give me:
1. The maintainability risks you see, each with the file and function, and why it is a risk.
2. A numbered plan of small, safe steps for the feature and the refactoring, smallest first, so I can run the tests after each step.
No code yet.
```

## 3. Codebase analysis (Task 1)

### 3.1 Maintainability risks

<!-- At least three, found in YOUR starting code. "Where" names a file or a function(),
     e.g. src/App.tsx, check(). Evidence is what you saw, not what the assistant said.
     Priority: High / Medium / Low. -->

| # | Risk | Where (file / function) | Evidence | Priority |
| --- | --- | --- | --- | --- |
| 1 | Room data lives in the page | src/App.tsx, SAMPLE_ROOMS | Lines 32 to 87 of App.tsx hold the four rooms and the Room type. A filter module or checkRoom would have to import data from a React component. The rooms also have no equipment field. | High |
| 2 | The rules are written twice | src/App.tsx, evaluateBooking() | After canBook returns false, evaluateBooking() checks AC1 to AC4 again by itself to build the messages (lines 128 to 156), for example start < b.end && end > b.start on line 150. If one copy changes, the page can say Unavailable with no reason or a wrong reason. | High |
| 3 | Duplicated constants | src/booking.ts and src/App.tsx | MIN_IN_DAY = 1440 and MAX_DURATION = 120 are declared in both files (booking.ts lines 14 and 15, App.tsx lines 29 and 30). In booking.ts they are not used at all, canBook uses the literals 1440 and 120. | Medium |
| 4 | The overlap rule is copied a third time for the timeline | src/App.tsx, Timeline() | Line 450 uses the same formula start < b.end && end > b.start to colour the hours. | Low |
| 5 | An invalid current time becomes -1 | src/App.tsx, App() | Line 173: const current = toMinutes(currentStr) ?? -1. If the current time field is empty, every start is after now and the past check of AC1 is switched off without a message. | Medium |
| 6 | An unused backend package | package.json, @supabase/supabase-js | It is in dependencies, but grep finds no import of supabase in src. The brief says no database and no network. | Low |

### 3.2 Improvement plan — before editing

<!-- Numbered, in the order you will do it, smallest safe step first. Written BEFORE you change
     code: the commit that adds this section comes before the commit that changes app/src. -->

1. Remove @supabase/supabase-js from package.json. Export MIN_IN_DAY and MAX_DURATION from booking.ts without changing canBook, and import them in App.tsx. The 26 tests must stay green.
2. Move the Room type and the rooms into src/rooms.ts as ROOMS, add equipment to every room, and import ROOMS in App.tsx. The page looks the same.
3. Write the F1, F2, B5 and B6 tests with a fixed catalog in the test file, see them fail, then add filterRooms in src/filter.ts.
4. Write the F3 and F5 tests for checkRoom, see them fail, then add checkRoom in src/booking.ts. It calls canBook with the chosen room's blocked and bookings.
5. Move the reason messages into booking.ts, so App.tsx has no rule of its own. Add a test that the reasons are empty when the request is available.
6. Use a fixed current time NOW in rooms.ts and show it on the page instead of the editable field and new Date().
7. Add the attendees field and the equipment checkboxes to the page, show only the filtered rooms, and show an empty state when no room matches (F4).
8. Show the result live for the selected room (F5), move the selection when the room is filtered out, add the B1 to B4 and INT titles, and take the five screenshots.

### 3.3 One AI suggestion I rejected or modified

| Suggestion (as the assistant made it) | Decision | Why — with the AC, F-rule, test or file behind it |
| --- | --- | --- |
| Step 2: "src/rooms.test.ts checks that there are at least 4 rooms with unique ids. It also checks that every booking has start < end, that no two bookings in one room overlap" (tests on the page's ROOMS) | Modified | README section 9 says the tests must use a fixed catalog inside the test file, not the page's ROOMS, so a change to the demo data cannot change a result. I wrote no tests on ROOMS. The tests for F1 to F5 and B5, B6 use their own small catalog in filter.test.ts. |

## 4. Feature extension (Task 2)

### 4.1 What I added

The catalog in src/rooms.ts has five fictional rooms with capacities 8, 12, 24, 40 and 200. The equipment is projector, whiteboard, video-call and computers. Innovation Lab is blocked. The current time is fixed at 09:00 (NOW = 540) and is shown on the page, it cannot be edited.

On the page the user types the number of attendees and ticks the required equipment. The list "Matching rooms" shows only filterRooms(ROOMS, ...). A blocked room stays in the list with a red Blocked label. If no room matches, the page shows "No rooms match your requirements. Try fewer attendees or less equipment." and hides the result and the schedule.

The result is computed live with checkRoom for the selected room and the times, so there is no old result: when the user clicks another room, the result changes at once. If the selected room is filtered out, the first matching room is selected.

### 4.2 Demonstration

<!-- One row per screenshot in evidence/. Say what is on it: the filter values, the rooms shown,
     the room selected, the times entered and the result. -->

| Screenshot | What it shows |
| --- | --- |
| `evidence/filter-match.png` | Attendees 20 and projector ticked. Three rooms are shown: Engineering Hall A (40 seats), Innovation Lab (24 seats, Blocked) and Auditorium B (200 seats). Library Study Room 3 (12 seats, no projector) and Seminar Room 5 (8 seats, no projector) are not shown. |
| `evidence/filter-empty.png` | Attendees 50, whiteboard and computers ticked. No room has 50 seats and both items, so the page shows the empty state: No rooms match your requirements. Try fewer attendees or less equipment. |
| `evidence/switch-a.png` | No filter, times 10:00 to 11:00, current time 09:00, Engineering Hall A selected. The result is Available, because its booking 09:00 to 10:00 only touches the request. |
| `evidence/switch-b.png` | The same times 10:00 to 11:00, Auditorium B selected. The result is Unavailable: Overlaps existing booking Guest Lecture (10:00 to 11:00). |
| `evidence/narrow.png` | The page at 390 pixels wide, portrait, with Auditorium B selected and 10:00 to 11:00. The columns are stacked, nothing is cut, and the page has no horizontal scroll (scrollWidth 390). |

## 5. Refactoring (Task 3)

<!-- The diagrams are diagrams/before.puml and diagrams/after.puml (README section 8). -->

### 5.1 Module responsibilities after

| Module or component | Responsibility |
| --- | --- |
| `src/rooms.ts` | Data only: the Room type, the EQUIPMENT list, the fixed current time NOW and the five ROOMS. |
| `src/booking.ts` | The booking rules: canBook (AC1-AC5, not changed), checkRoom (the chosen room, F3, F5), findOverlap (the overlap rule for the timeline and the messages) and reasonsFor (why a request is Unavailable). |
| `src/filter.ts` | filterRooms: capacity >= attendees (F1) and all selected equipment (F2). Nothing else. |
| `src/App.tsx` (App, EmptyState, RoomList, ResultCard, RoomSchedule, Timeline) | The page: form state, the list of matching rooms, the empty state (F4), the result card and the schedule. It turns reason codes into text, but holds no room data and no rule. |

### 5.2 Design decisions

<!-- At least two. The alternative is what you could have done instead (often what the assistant
     proposed). The why names an AC, an F-rule, a test or a risk from 3.1. -->

| Decision | Alternative I did not take | Why |
| --- | --- | --- |
| Blocked rooms stay in the filtered list, with a Blocked label. | Hide blocked rooms inside filterRooms. | filterRooms then does only F1 and F2, so its tests do not depend on blocked. F3 is the job of checkRoom, and the F3 test proves it says false for a blocked room. The user also sees why the room cannot be used (AC6). |
| canBook stays exactly as in week-08, and the messages come from a new reasonsFor() next to it. | The assistant's step 2: change canBook to use CanBookInput and the constants, or make canBook return the reasons. | The brief says canBook is unchanged from Practice 07 and 08, and the 26 old tests are written for it. The cost is that the rules are written twice in booking.ts, so I added two tests that reasonsFor agrees with canBook. |
| The result is live: it is computed on every render from checkRoom and the selected room. | Keep the Check button and clear the result when the room changes, like the week-08 page. | F5 says a room change must refresh the result. With a live result the old room's verdict can never stay on the screen, switch-a and switch-b show it. |
| The components stay in App.tsx. | Split ResultCard, RoomSchedule, Timeline and RoomList into a components folder. | They are display only and hold no rule, so A5 passes already. Keeping them avoids pure moves in the diff, and the plan in 3.2 did not include it. |

### 5.3 Duplication removed

<!-- One row per duplicated location that is gone. Count what you can point at, nothing else. -->

| Before (file / function, what was repeated) | After (where it lives now) |
| --- | --- |
| src/App.tsx, top of the file: MIN_IN_DAY = 1440 and MAX_DURATION = 120, a copy of the constants in booking.ts | booking.ts exports them, App.tsx imports MAX_DURATION for the message (commit e3fc1b2) |
| src/App.tsx, evaluateBooking(): the overlap formula start < b.end && end > b.start | findOverlap() in booking.ts, used by reasonsFor() |
| src/App.tsx, Timeline(): the same overlap formula to colour each hour | findOverlap() in booking.ts, imported by Timeline() |

## 6. Automated tests (Task 4)

### 6.1 Test plan

<!-- One row per required ID. A test may carry several IDs in its title,
     e.g. test('T06 B1 AC2: exactly 120 minutes is available', …) covers B1 and AC2. -->

| ID | Test title (as in the file) | Input → expected |
| --- | --- | --- |
| AC1 | T02 AC1: request starting exactly at now (540-570) is rejected | now 540, 540-570 → false |
| AC2 | T07 B2 AC2: 121 minutes (720-841) is rejected | 720-841 → false |
| AC3 | T13 AC3: otherwise-available request (660-720) in a blocked room is rejected | 660-720, blocked true → false |
| AC4 | T12 AC4: request identical to the booking (600-660) is rejected | 600-660 with booking 600-660 → false |
| AC5 | AC5: an Available request (660-720) leaves the bookings unchanged | 660-720 → true, bookings still [600-660] |
| F1 | F1: excludes rooms with capacity below the attendees | attendees 11 → rooms b (30) and c (20), not a (10) |
| F2 | F2: keeps only rooms that have ALL required equipment | projector + whiteboard → a and c, not b (projector only) |
| F3 | F3: a blocked room with a free slot is not available | 600-660: room b → true, blocked room c → false |
| F4 | F4: returns [] when no room matches | attendees 25 + whiteboard → [] |
| F5 | F5: the same times give different results for two rooms | 600-660: room a (booking 600-660) → false, room b → true |
| B1 | T06 B1 AC2: exactly 120 minutes (720-840) is accepted | 720-840 → true |
| B2 | T07 B2 AC2: 121 minutes (720-841) is rejected | 720-841 → false |
| B3 | T01 B3 AC4: request touching the end of the booking (660-720) is accepted | 660-720 with booking 600-660 → true |
| B4 | T09 B4 AC4: partial overlap (630-690) is rejected | 630-690 with booking 600-660 → false |
| B5 | B5: capacity exactly equal to attendees is included | attendees 20 → b (30) and c (20) |
| B6 | B6: capacity one below attendees is excluded | attendees 21 → only b (30) |
| INT | INT: checkRoom on a room returned by filterRooms | filter attendees 10 + projector + whiteboard → a, c; then checkRoom a 660-720 → true |

### 6.2 Commands

<!-- The commands exactly as you typed them, from app/. -->

```text
cd sis-04/app
npm install
npx vitest run
npx tsc --noEmit -p tsconfig.app.json
```

### 6.3 Final run

<!-- The REAL output of the full run on your final code. Every test passes, and the number of
     tests equals what your test files hold (R2). -->

```text

 RUN  v3.2.7 /Users/hevilim/Developer/se-practice/sis-04/app

 ✓ src/filter.test.ts (9 tests) 2ms
 ✓ src/booking.test.ts (28 tests) 4ms

 Test Files  2 passed (2)
      Tests  37 passed (37)
   Start at  23:01:22
   Duration  284ms (transform 52ms, setup 0ms, collect 60ms, tests 6ms, environment 0ms, prepare 91ms)
```

## 7. Quality evaluation (Task 5)

<!-- Original = your baseline commit. Final = what you submit. "How I obtained it" says how you
     measured, so someone else could repeat it: "1.1 and 6.3 runs", "counted in 5.3",
     "git ls-files app/src". Do not invent a metric. Tests: write passed/total, e.g. 19/19. -->

| Measure | Original | Final | How I obtained it |
| --- | --- | --- | --- |
| Automated tests passed / total | 26/26 | 37/37 | The Tests line of the run in 1.1 (baseline commit f04e465) and of the run in 6.3, both with npx vitest run in app/. |
| Duplicated logic locations removed | 0 | 3 | Counted the rows of 5.3, each one can be seen in the diff from f04e465 to the final commit. |
| Code structure: modules and their responsibilities | 3 modules in src: App.tsx (room data, messages that repeat AC1-AC4, the whole UI), booking.ts (canBook), main.tsx | 5 modules in src: rooms.ts (data), booking.ts (rules), filter.ts (F1, F2), App.tsx (UI only), main.tsx | git ls-files app/src at f04e465 and at the final commit, read against 5.1. |
| Remaining limitation | The time input cannot give 24:00 as an end, so 23:00 to 24:00 cannot be checked on the page, although canBook allows end = 1440. | Not fixed. Also the rules are now written twice inside booking.ts, in canBook and in reasonsFor, because canBook must stay unchanged. | Read toMinutes() in App.tsx: an hour above 23 returns null, and an input of type time stops at 23:59. The second one is seen in booking.ts. |

## 8. AI evidence appendix

<!-- At least three exchanges, one ### 8.N block each: the analysis (Task 1), the plan, and at
     least one implementation, refactoring or test exchange. Copy the block for more.
     The prompt as you sent it; the output may be cut to the part you used, with "[…]" where
     you cut. Verified by: the test, run, file or check that confirmed it — not "it looked right". -->

### 8.1 Exchange 1

**Tool and model:** Claude (claude.ai), Claude Opus 5.5
**Date:** 9.11.2026
**Purpose:** Find maintainability risks and get a plan of small steps (Task 1)

**Prompt:**

```text
Hello. I am working on a small university project: the Smart Campus Room Availability Checker. It is a React + TypeScript page made with Vite, tested with Vitest. I want to extend it and refactor it. Please do not write code yet and do not propose a full rewrite. I need an analysis and a plan of small steps.

Repository map:
sis-04/app/  (React 18 + TypeScript + Vite + Tailwind, tests with Vitest 3.2.7)
  package.json        scripts dev, build, test (vitest run); dependencies react, lucide-react, @supabase/supabase-js
  index.html          the page shell, loads src/main.tsx
  src/main.tsx        mounts <App /> into #root
  src/App.tsx         the whole page (487 lines): Room type, SAMPLE_ROOMS (4 rooms), toMinutes(), toHHMM(),
                      evaluateBooking() (calls canBook, then builds the reasons), App() (form and state),
                      ResultCard, RoomSchedule, Timeline
  src/booking.ts      canBook({ start, end, now, blocked, bookings }) for AC1-AC5, types BookingInterval and CanBookInput
  src/booking.test.ts 26 Vitest tests for canBook (T01-T14, X1, X2, R01-R07, AC5, BUG-A, BUG-B)
  src/index.css       Tailwind directives only

Requirements I must keep (AC1-AC6):
AC1 Reject start >= end and requests in the past.
AC2 Enforce the maximum allowed duration (120 minutes).
AC3 Reject a blocked room.
AC4 Reject overlaps; allow bookings that only touch at endpoints.
AC5 Return Available / Unavailable without changing booking data.
AC6 Clear, responsive feedback on desktop and mobile.

New feature: a catalog of at least four fictional rooms. Each room has id, name, capacity, equipment list, blocked status and its own bookings. Show only the rooms that satisfy the user's requirements. The availability check must use the chosen room's bookings, not another room's data.
F1 Capacity filter: room capacity must be greater than or equal to the requested attendees.
F2 Equipment filter: the room must contain ALL selected required items.
F3 A blocked room cannot be reported as available.
F4 Show a clear empty state when no rooms match.
F5 Changing the selected room must refresh the availability result appropriately.

Fixed structure: src/rooms.ts (Room type and ROOMS, data only), src/filter.ts (filterRooms(rooms, { attendees, equipment })), src/booking.ts (canBook unchanged, and checkRoom(rooms, roomId, { start, end, now }) which calls canBook with the chosen room's blocked and bookings). The UI imports the rules and holds no room data and no rule of its own.

Constraints: fictional data only, a fixed current time, no login, no payments, no live APIs, no database, no network calls, no browser storage.

Here are the two files with the logic.

src/booking.ts:
export type BookingInterval = {
  start: number; // minutes from midnight
  end: number;
};

export type CanBookInput = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: BookingInterval[];
};

const MIN_IN_DAY = 1440;
const MAX_DURATION = 120;

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
    if (start < b.end && end > b.start) return false;
  }
  return true;
}

src/App.tsx:
import { useMemo, useState } from "react";
import {
  Building2,
  CalendarClock,
  CheckCircle2,
  Clock,
  DoorClosed,
  MapPin,
  XCircle,
} from "lucide-react";
import { canBook } from "./booking";

type Booking = {
  id: string;
  title: string;
  start: number; // minutes from midnight
  end: number;
};

type Room = {
  id: string;
  name: string;
  building: string;
  capacity: number;
  blocked: boolean;
  bookings: Booking[];
};

const MIN_IN_DAY = 1440;
const MAX_DURATION = 120;

const SAMPLE_ROOMS: Room[] = [
  {
    id: "r1",
    name: "Engineering Hall A",
    building: "Block C · Floor 2",
    capacity: 40,
    blocked: false,
    bookings: [
      { id: "b1", title: "Algorithms Lecture", start: 540, end: 600 },
      { id: "b2", title: "Faculty Meeting", start: 780, end: 840 },
      { id: "b3", title: "Robotics Lab", start: 1080, end: 1140 },
    ],
  },
  {
    id: "r2",
    name: "Innovation Lab",
    building: "Block A · Floor 1",
    capacity: 24,
    blocked: true,
    bookings: [
      { id: "b4", title: "Maintenance", start: 600, end: 660 },
    ],
  },
  {
    id: "r3",
    name: "Library Study Room 3",
    building: "Library · Floor 3",
    capacity: 12,
    blocked: false,
    bookings: [
      { id: "b5", title: "Group Study", start: 660, end: 720 },
      { id: "b6", title: "Book Club", start: 1020, end: 1080 },
    ],
  },
  {
    id: "r4",
    name: "Auditorium B",
    building: "Main Building · Ground",
    capacity: 200,
    blocked: false,
    bookings: [
      { id: "b7", title: "Guest Lecture", start: 600, end: 660 },
    ],
  },
];

function toMinutes(time: string): number | null {
  if (!/^\d{2}:\d{2}$/.test(time)) return null;
  const [h, m] = time.split(":").map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

function toHHMM(min: number): string {
  const h = Math.floor(min / 60);
  const m = min % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

type Verdict =
  | { kind: "available" }
  | { kind: "unavailable"; reasons: string[] };

function evaluateBooking(
  room: Room | undefined,
  start: number | null,
  end: number | null,
  current: number,
): Verdict {
  const reasons: string[] = [];

  if (!room) {
    return { kind: "unavailable", reasons: ["Select a room to check."] };
  }

  if (start === null || end === null) {
    return {
      kind: "unavailable",
      reasons: ["Enter valid start and end times in HH:MM format."],
    };
  }

  // The decision itself comes from canBook in src/booking.ts.
  // The checks below only build the messages for the page.
  if (
    canBook({
      start,
      end,
      now: current,
      blocked: room.blocked,
      bookings: room.bookings,
    })
  ) {
    return { kind: "available" };
  }

  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    reasons.push(
      "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.",
    );
  }
  if (start <= current) {
    reasons.push("Start time must be after the current time.");
  }

  // AC2: duration <= 120 min
  if (end - start > MAX_DURATION) {
    reasons.push("Booking cannot be longer than 120 minutes.");
  }

  // AC3: blocked room
  if (room.blocked) {
    reasons.push("This room is currently blocked and cannot be booked.");
  }

  // AC4: overlap (touching endpoints allowed)
  const overlapping = room.bookings.find(
    (b) => start < b.end && end > b.start,
  );
  if (overlapping) {
    reasons.push(
      `Overlaps existing booking "${overlapping.title}" (${toHHMM(overlapping.start)}–${toHHMM(overlapping.end)}).`,
    );
  }

  return { kind: "unavailable", reasons };
}

function App() {
  const [roomId, setRoomId] = useState<string>(SAMPLE_ROOMS[0].id);
  const [currentStr, setCurrentStr] = useState("09:00");
  const [startStr, setStartStr] = useState("10:00");
  const [endStr, setEndStr] = useState("11:00");
  const [submitted, setSubmitted] = useState(false);

  const room = useMemo(
    () => SAMPLE_ROOMS.find((r) => r.id === roomId),
    [roomId],
  );

  const current = toMinutes(currentStr) ?? -1;
  const start = toMinutes(startStr);
  const end = toMinutes(endStr);

  const verdict = useMemo(
    () => evaluateBooking(room, start, end, current),
    [room, start, end, current],
  );

  const check = () => setSubmitted(true);

  const reset = () => {
    setSubmitted(false);
  };

  const dayNow = new Date();
  const todayLabel = dayNow.toLocaleDateString(undefined, {
    weekday: "long",
    month: "short",
    day: "numeric",
  });

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-sky-600 text-white flex items-center justify-center shadow-sm">
            <Building2 className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-semibold tracking-tight text-slate-900">
              Smart Campus Room Availability
            </h1>
            <p className="text-sm text-slate-500">
              Check whether a campus room is free for your requested time slot.
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 grid gap-6 lg:grid-cols-5">
        {/* Form column */}
        <section className="lg:col-span-2">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
            <div className="flex items-center gap-2 mb-5">
              <CalendarClock className="h-4 w-4 text-sky-600" />
              <h2 className="font-semibold text-slate-900">Check a slot</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Room
                </label>
                <select
                  value={roomId}
                  onChange={(e) => {
                    setRoomId(e.target.value);
                    setSubmitted(false);
                  }}
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                >
                  {SAMPLE_ROOMS.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.name} {r.blocked ? "(blocked)" : ""}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Current time (HH:MM)
                </label>
                <input
                  type="time"
                  value={currentStr}
                  onChange={(e) => {
                    setCurrentStr(e.target.value);
                    setSubmitted(false);
                  }}
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    Start
                  </label>
                  <input
                    type="time"
                    value={startStr}
                    onChange={(e) => {
                      setStartStr(e.target.value);
                      setSubmitted(false);
                    }}
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    End
                  </label>
                  <input
                    type="time"
                    value={endStr}
                    onChange={(e) => {
                      setEndStr(e.target.value);
                      setSubmitted(false);
                    }}
                    className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                  />
                </div>
              </div>

              <div className="flex gap-2 pt-1">
                <button
                  onClick={check}
                  className="flex-1 rounded-lg bg-sky-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-sky-700 active:bg-sky-800 transition-colors"
                >
                  Check availability
                </button>
                <button
                  onClick={reset}
                  className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Result + schedule column */}
        <section className="lg:col-span-3 space-y-6">
          {submitted ? (
            <ResultCard verdict={verdict} room={room} start={start} end={end} />
          ) : (
            <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-8 text-center text-slate-500 text-sm">
              Fill in the form and press{" "}
              <span className="font-semibold text-slate-700">
                Check availability
              </span>{" "}
              to see the result.
            </div>
          )}

          {room && <RoomSchedule room={room} todayLabel={todayLabel} />}
        </section>
      </main>

      <footer className="max-w-5xl mx-auto px-4 sm:px-6 pb-10 text-center text-xs text-slate-400">
        Fictional sample data · Times are in 24-hour format · No bookings are
        actually saved
      </footer>
    </div>
  );
}

function ResultCard({
  verdict,
  room,
  start,
  end,
}: {
  verdict: Verdict;
  room: Room | undefined;
  start: number | null;
  end: number | null;
}) {
  if (verdict.kind === "available") {
    return (
      <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5 sm:p-6 shadow-sm">
        <div className="flex items-start gap-3">
          <CheckCircle2 className="h-6 w-6 text-emerald-600 mt-0.5 shrink-0" />
          <div>
            <h3 className="font-semibold text-emerald-900">Available</h3>
            <p className="text-sm text-emerald-800 mt-1">
              {room?.name} is free from {toHHMM(start ?? 0)} to{" "}
              {toHHMM(end ?? 0)}. You can proceed with this booking.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const palette = {
    border: "border-rose-200",
    bg: "bg-rose-50",
    icon: "text-rose-600",
    title: "text-rose-900",
    body: "text-rose-800",
    Icon: XCircle,
    label: "Unavailable",
  };

  return (
    <div className={`rounded-2xl border ${palette.border} ${palette.bg} p-5 sm:p-6 shadow-sm`}>
      <div className="flex items-start gap-3">
        <palette.Icon className={`h-6 w-6 ${palette.icon} mt-0.5 shrink-0`} />
        <div className="w-full">
          <h3 className={`font-semibold ${palette.title}`}>{palette.label}</h3>
          <ul className={`mt-2 text-sm ${palette.body} space-y-1.5 list-disc list-inside`}>
            {verdict.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function RoomSchedule({ room, todayLabel }: { room: Room; todayLabel: string }) {
  const sorted = [...room.bookings].sort((a, b) => a.start - b.start);
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
      <div className="flex items-center justify-between gap-2 mb-4">
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-sky-600" />
          <h2 className="font-semibold text-slate-900">{room.name}</h2>
        </div>
        <span className="text-xs text-slate-400">{todayLabel}</span>
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500 mb-4">
        <span>{room.building}</span>
        <span className="flex items-center gap-1">
          <DoorClosed className="h-3.5 w-3.5" /> Seats {room.capacity}
        </span>
        {room.blocked ? (
          <span className="inline-flex items-center rounded-full bg-rose-100 text-rose-700 px-2 py-0.5 font-medium">
            Blocked
          </span>
        ) : (
          <span className="inline-flex items-center rounded-full bg-emerald-100 text-emerald-700 px-2 py-0.5 font-medium">
            Open
          </span>
        )}
      </div>

      <Timeline room={room} />

      <h3 className="text-sm font-medium text-slate-700 mt-5 mb-2">
        Existing bookings
      </h3>
      {sorted.length === 0 ? (
        <p className="text-sm text-slate-400">No bookings today.</p>
      ) : (
        <ul className="divide-y divide-slate-100">
          {sorted.map((b) => (
            <li key={b.id} className="flex items-center justify-between py-2 text-sm">
              <span className="text-slate-700">{b.title}</span>
              <span className="flex items-center gap-1 text-slate-500 tabular-nums">
                <Clock className="h-3.5 w-3.5" />
                {toHHMM(b.start)}–{toHHMM(b.end)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function Timeline({ room }: { room: Room }) {
  const blocks = Array.from({ length: 24 }, (_, h) => h);
  return (
    <div>
      <div className="flex h-8 w-full overflow-hidden rounded-md border border-slate-200">
        {blocks.map((h) => {
          const start = h * 60;
          const end = start + 60;
          const booking = room.bookings.find(
            (b) => start < b.end && end > b.start,
          );
          const blockedSeg = room.blocked;
          let cls = "bg-emerald-100 hover:bg-emerald-200";
          if (blockedSeg) cls = "bg-rose-200 hover:bg-rose-300";
          else if (booking) cls = "bg-sky-200 hover:bg-sky-300";
          return (
            <div
              key={h}
              title={`${toHHMM(start)}–${toHHMM(end)}`}
              className={`flex-1 transition-colors ${cls}`}
            />
          );
        })}
      </div>
      <div className="flex justify-between mt-1 text-[10px] text-slate-400 tabular-nums">
        <span>00:00</span>
        <span>06:00</span>
        <span>12:00</span>
        <span>18:00</span>
        <span>24:00</span>
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1 mt-2 text-xs text-slate-500">
        <span className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-sm bg-emerald-200" /> Free
        </span>
        <span className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-sm bg-sky-300" /> Booked
        </span>
        <span className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-sm bg-rose-300" /> Blocked
        </span>
      </div>
    </div>
  );
}

export default App;

Please give me:
1. The maintainability risks you see, each with the file and function, and why it is a risk.
2. A numbered plan of small, safe steps for the feature and the refactoring, smallest first, so I can run the tests after each step.
No code yet.
```

**Output used:**

```text
### `src/booking.ts`
| B2 | `canBook`, body | `MIN_IN_DAY` and `MAX_DURATION` are declared but unused. The body uses the literals `1440` and `120` instead. | If the AC2 limit changes, the constant gets edited and nothing happens. The constants look authoritative but are not. |
[…]
### `src/App.tsx`
| A1 | Top of the file: `Room`, `Booking`, `SAMPLE_ROOMS` | Room data and types live in the UI. | This breaks your fixed structure. The new `filter.ts` and `checkRoom` would have to import from a React component, or the data would be duplicated. |
| A2 | `evaluateBooking` | It re-checks AC1–AC4 (range, past, duration, blocked, overlap) to build reasons. | There are two sources of truth for the rules. If they drift, you can get an "Unavailable" card with an empty reason list, or reasons that contradict the verdict. It also breaks "the UI holds no rule of its own". |
| A3 | Top of the file: `MIN_IN_DAY`, `MAX_DURATION` | These constants are duplicated from `booking.ts`. | If one copy changes, the message "cannot be longer than 120 minutes" becomes wrong. |
| A4 | `App`, `current = toMinutes(currentStr) ?? -1` | An empty or invalid current time silently becomes `-1`. | Every start then counts as "in the future", so AC1's past check is switched off without any message. This is a real bug path. |
[…]
| A10 | `evaluateBooking` and `Timeline` | `evaluateBooking` is not exported, and `Timeline` repeats the overlap formula. | […] `Timeline`'s copy only affects display, but it is a third copy of the overlap rule. |
[…]
- **`package.json`, `@supabase/supabase-js`.** This is an unused database/network client. It contradicts the "no database, no network calls" constraint and invites someone to use it by accident. Remove it.
```

**Problems found:** It gave 12 risks for App.tsx and 3 for booking.ts. Some are opinions, not risks, for example A8 (Reset only hides the result) and A11 (only the first overlap is reported). Its step 2 wanted to change the body of canBook, which the brief does not allow.
**Changes made:** I kept six risks for 3.1 and checked each one in the code myself. I did not take step 2 for canBook, I only exported the constants.
**Verified by:** grep in app/src: MIN_IN_DAY and MAX_DURATION on lines 14-15 of booking.ts and 29-30 of App.tsx, the overlap formula on lines 150 and 450 of App.tsx, ?? -1 on line 173, and no import of supabase.

### 8.2 Exchange 2

**Tool and model:** Claude (claude.ai), Claude Opus 5.5
**Date:** 9.11.2026
**Purpose:** Turn the analysis into a short plan after my decisions

**Prompt:**

```text
Thank you. I checked your risks in the code myself. My answers to your five questions:
1. canBook must stay unchanged, so I will not do Step 2 inside canBook. I will only export the constants.
2. Blocked rooms stay in the list with a "Blocked" label. filterRooms only does F1 and F2, and checkRoom does F3.
3. Yes, a function for the reasons in booking.ts is fine.
4. F5: the result is computed live from the selected room and the times, so a room change shows the new room's result at once.
5. 24:00 in the UI: I will only document it as a limitation.
I will not split the components into files now and I will not add UI tests (no new packages).

Please give me the final plan as a short numbered list, 6 to 9 steps, smallest safe step first. For each step say which tests I write first and which file changes. Still no code.
```

**Output used:**

```text
2. **Move the data into `src/rooms.ts`.**
   - *Tests first:* `src/rooms.test.ts` checks that there are at least 4 rooms with unique ids. It also checks that every booking has `start < end`, that no two bookings in one room overlap, and that every equipment item belongs to the equipment type.
[…]
3. **Add `filterRooms` (F1, F2).**
   - *Tests first:* `src/filter.test.ts` covers:
     - capacity below, equal and above the attendee count;
     - all, some or none of the required equipment present;
[…]
4. **Add `checkRoom` (F3, chosen-room data).**
   - *Tests first:* add to `src/booking.test.ts`:
     - the same slot gives different results in two rooms;
     - a blocked room with a free slot gives Unavailable;
[…]
5. **Move the reasons into `booking.ts`.**
   - *Tests first:* add to `src/booking.test.ts`:
     - one test per reason code (invalid range, past, too long, blocked, overlap with all overlapping bookings);
     - a consistency test over the existing test inputs: `canBook` is false exactly when the reason list is non-empty.
[…]
8. **Live result, selection sync and feedback polish (F5, AC6).**
[…]
     - resync `roomId` when it is not in the filtered list;
```

**Problems found:** Step 2 and step 6 test the page's ROOMS and NOW, but README section 9 asks for a fixed catalog inside the test file. Step 5 wanted a test per reason code and a big consistency test over all old inputs, which is more than I need.
**Changes made:** I wrote my own plan in 3.2 from it. No tests on ROOMS (3.3). For the reasons I wrote two tests: one available request with no reasons, one request that breaks four rules and gets four reasons.
**Verified by:** The steps were done in commits e3fc1b2, 1a42173 and ed91e9f, and the suite was green after each one: 26, then 35, then 37 tests.

### 8.3 Exchange 3

**Tool and model:** Claude (claude.ai), Claude Opus 5.5
**Date:** 9.11.2026
**Purpose:** Tests and code for filterRooms and checkRoom (Task 2 and Task 4)

**Prompt:**

```text
Steps 1 and 2 are done and the 26 tests are green. This is my src/rooms.ts now:

// Fictional room catalog. Data only, no rules.

export type Room = {
  id: string;
  name: string;
  capacity: number;
  equipment: string[];
  blocked: boolean;
  bookings: { start: number; end: number; title?: string }[]; // minutes after midnight, 600 = 10:00
  building?: string;
};

export const EQUIPMENT = ["projector", "whiteboard", "video-call", "computers"];

// The fixed current time of the demo: 09:00.
export const NOW = 540;

export const ROOMS: Room[] = [
  {
    id: "r1",
    name: "Engineering Hall A",
    capacity: 40,
    equipment: ["projector", "whiteboard", "video-call"],
    blocked: false,
    bookings: [
      { title: "Algorithms Lecture", start: 540, end: 600 },
      { title: "Faculty Meeting", start: 780, end: 840 },
      { title: "Robotics Lab", start: 1080, end: 1140 },
    ],
    building: "Block C · Floor 2",
  },
  {
    id: "r2",
    name: "Innovation Lab",
    capacity: 24,
    equipment: ["projector", "whiteboard", "computers"],
    blocked: true,
    bookings: [{ title: "Maintenance", start: 600, end: 660 }],
    building: "Block A · Floor 1",
  },
  {
    id: "r3",
    name: "Library Study Room 3",
    capacity: 12,
    equipment: ["whiteboard"],
    blocked: false,
    bookings: [
      { title: "Group Study", start: 660, end: 720 },
      { title: "Book Club", start: 1020, end: 1080 },
    ],
    building: "Library · Floor 3",
  },
  {
    id: "r4",
    name: "Auditorium B",
    capacity: 200,
    equipment: ["projector", "video-call"],
    blocked: false,
    bookings: [{ title: "Guest Lecture", start: 600, end: 660 }],
    building: "Main Building · Ground",
  },
  {
    id: "r5",
    name: "Seminar Room 5",
    capacity: 8,
    equipment: ["whiteboard", "video-call"],
    blocked: false,
    bookings: [],
    building: "Block B · Floor 1",
  },
];

Now steps 3 and 4. Please write:
1. src/filter.test.ts with Vitest. Use a small fixed catalog inside the test file, not ROOMS. Import from "./filter" and "./booking", no mocks, no test.each. One test per case, and put these IDs in the titles: F1, F2, F4 (filterRooms returns []), B5 (capacity exactly equal to attendees is included), B6 (capacity one below is excluded), F3 (checkRoom on a blocked room with a free slot is false), F5 (the same times give different results for two rooms), and INT (filterRooms, then checkRoom on a room it returned). Take the expected values from the rules F1-F5 and AC1-AC5, not from code.
2. src/filter.ts with filterRooms(rooms: Room[], criteria: { attendees: number; equipment: string[] }): Room[].
3. checkRoom(rooms: Room[], roomId: string, request: { start: number; end: number; now: number }): boolean for src/booking.ts. It must call canBook with the chosen room's blocked and bookings, an unknown id is false, and it changes nothing.
Keep it short.
```

**Output used:**

```text
const CATALOG = [
  { id: "a", name: "Room A", capacity: 10, equipment: ["projector", "whiteboard"], blocked: false, bookings: [{ start: 600, end: 660 }] },
[…]
  it("F1: excludes rooms with capacity below the attendees", () => {
    expect(ids(filterRooms(CATALOG, { attendees: 11, equipment: [] }))).toEqual(["b", "c"]);
  });
[…]
  it("INT: checkRoom on a room returned by filterRooms", () => {
    const matches = filterRooms(CATALOG, { attendees: 10, equipment: ["projector", "whiteboard"] });
    expect(ids(matches)).toEqual(["a", "c"]);
    // 11:00–12:00 only touches A's 10:00–11:00 booking (AC4)
    expect(checkRoom(matches, "a", { start: 660, end: 720, now: NOW })).toBe(true);
  });
[…]
export function filterRooms(
  rooms: Room[],
  criteria: { attendees: number; equipment: string[] },
): Room[] {
  return rooms.filter(
    (r) =>
      r.capacity >= criteria.attendees &&
      criteria.equipment.every((item) => r.equipment.includes(item)),
  );
}
[…]
  const room = rooms.find((r) => r.id === roomId);
  if (!room) return false;
  return canBook({ ...request, blocked: room.blocked, bookings: room.bookings });
```

**Problems found:** It used it() while my suite uses test(), and the catalog had no Room type. There was no test for an unknown room id or for AC5 in checkRoom, the answer said so itself.
**Changes made:** I changed it() to test(), typed the catalog as Room[], and added the test F5 AC5: an unknown room id is not available and checkRoom changes nothing. I checked every expected value against F1 and F2 by hand, for example attendees 11 excludes Room A with 10 seats.
**Verified by:** Before filter.ts existed the run failed with Cannot find module ./filter, and before checkRoom existed 4 tests failed with checkRoom is not a function. After the code: 35 passed (35), and 37 passed (37) in 6.3.

## 9. Checker results and known fails

<!-- Every check still FAIL or ERROR in your last run of python tests/check_sis.py, and why.
     The same IDs go in submission.yml known_fails. None left? Write: none. -->

| Check | Why it still fails |
| --- | --- |
| (write here) | (write here) |

## 10. AI reflection (Task 6)

<!-- 200–300 words, your own words, no assistant. Answer all five:
     What context did you provide the AI assistant? Which generated suggestions were useful or
     incorrect? What did you personally verify? How did tests influence your engineering
     decisions? What would you improve next? -->

(write here)
