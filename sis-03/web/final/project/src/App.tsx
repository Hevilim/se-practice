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
  {
    id: "r5",
    name: "Seminar Room 5",
    building: "Block B · Floor 1",
    capacity: 30,
    blocked: false,
    bookings: [
      { id: "b8", title: "Design Workshop", start: 600, end: 660 },
      { id: "b9", title: "Thesis Review", start: 700, end: 760 },
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
  current: number | null,
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

  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    reasons.push(
      "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.",
    );
  }
  if (current === null) {
    reasons.push("Enter a valid current time in HH:MM format.");
  } else if (start <= current) {
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

  if (reasons.length > 0) {
    return { kind: "unavailable", reasons };
  }

  return { kind: "available" };
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

  const current = toMinutes(currentStr);
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
