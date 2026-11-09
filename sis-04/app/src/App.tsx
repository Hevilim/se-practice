import { useState } from "react";
import {
  Building2,
  CalendarClock,
  CheckCircle2,
  Clock,
  DoorClosed,
  Filter,
  MapPin,
  SearchX,
  XCircle,
} from "lucide-react";
import { checkRoom, findOverlap, reasonsFor, MAX_DURATION, type Reason } from "./booking";
import { filterRooms } from "./filter";
import { EQUIPMENT, NOW, ROOMS, type Room } from "./rooms";

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

// Turns the reason codes from booking.ts into text. The rules themselves live in booking.ts.
function reasonText(reason: Reason): string {
  switch (reason.code) {
    case "interval":
      return "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.";
    case "past":
      return `Start time must be after the current time (${toHHMM(NOW)}).`;
    case "too-long":
      return `Booking cannot be longer than ${MAX_DURATION} minutes.`;
    case "blocked":
      return "This room is currently blocked and cannot be booked.";
    case "overlap":
      return `Overlaps existing booking${reason.booking.title ? ` "${reason.booking.title}"` : ""} (${toHHMM(reason.booking.start)}–${toHHMM(reason.booking.end)}).`;
  }
}

type Verdict =
  | { kind: "available" }
  | { kind: "unavailable"; reasons: string[] };

function evaluate(room: Room, start: number | null, end: number | null): Verdict {
  if (start === null || end === null) {
    return {
      kind: "unavailable",
      reasons: ["Enter valid start and end times in HH:MM format."],
    };
  }
  // The decision comes from checkRoom, with the chosen room's own data (F3, F5).
  if (checkRoom(ROOMS, room.id, { start, end, now: NOW })) {
    return { kind: "available" };
  }
  const reasons = reasonsFor({
    start,
    end,
    now: NOW,
    blocked: room.blocked,
    bookings: room.bookings,
  });
  return { kind: "unavailable", reasons: reasons.map(reasonText) };
}

const DEFAULTS = { attendees: "1", start: "10:00", end: "11:00" };
const DAY_LABEL = "Monday, 16 Nov (demo day)";

const inputClass =
  "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500";

function App() {
  const [attendeesStr, setAttendeesStr] = useState(DEFAULTS.attendees);
  const [selected, setSelected] = useState<string[]>([]);
  const [roomId, setRoomId] = useState<string>(ROOMS[0].id);
  const [startStr, setStartStr] = useState(DEFAULTS.start);
  const [endStr, setEndStr] = useState(DEFAULTS.end);

  const attendees = Number(attendeesStr) || 0;
  const matches = filterRooms(ROOMS, { attendees, equipment: selected });

  // If the chosen room is filtered out, the first match is shown instead (F5).
  const room = matches.find((r) => r.id === roomId) ?? matches[0];

  const start = toMinutes(startStr);
  const end = toMinutes(endStr);
  const verdict = room ? evaluate(room, start, end) : null;

  const toggle = (item: string) =>
    setSelected((prev) =>
      prev.includes(item) ? prev.filter((x) => x !== item) : [...prev, item],
    );

  const reset = () => {
    setAttendeesStr(DEFAULTS.attendees);
    setSelected([]);
    setRoomId(ROOMS[0].id);
    setStartStr(DEFAULTS.start);
    setEndStr(DEFAULTS.end);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-sky-600 text-white flex items-center justify-center shadow-sm shrink-0">
            <Building2 className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-semibold tracking-tight text-slate-900">
              Smart Campus Room Availability
            </h1>
            <p className="text-sm text-slate-500">
              Filter the rooms, choose one and check your time slot.
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 grid gap-6 lg:grid-cols-5">
        {/* Form column */}
        <section className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
            <div className="flex items-center gap-2 mb-5">
              <Filter className="h-4 w-4 text-sky-600" />
              <h2 className="font-semibold text-slate-900">Room requirements</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="attendees" className="block text-sm font-medium text-slate-700 mb-1">
                  Attendees
                </label>
                <input
                  id="attendees"
                  type="number"
                  min={1}
                  value={attendeesStr}
                  onChange={(e) => setAttendeesStr(e.target.value)}
                  className={inputClass}
                />
              </div>

              <fieldset>
                <legend className="block text-sm font-medium text-slate-700 mb-2">
                  Required equipment
                </legend>
                <div className="grid grid-cols-2 gap-2">
                  {EQUIPMENT.map((item) => (
                    <label
                      key={item}
                      className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm cursor-pointer hover:bg-slate-50"
                    >
                      <input
                        type="checkbox"
                        checked={selected.includes(item)}
                        onChange={() => toggle(item)}
                        className="accent-sky-600"
                      />
                      {item}
                    </label>
                  ))}
                </div>
              </fieldset>
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
            <div className="flex items-center gap-2 mb-5">
              <CalendarClock className="h-4 w-4 text-sky-600" />
              <h2 className="font-semibold text-slate-900">Time slot</h2>
            </div>

            <div className="space-y-4">
              <p className="text-sm text-slate-600">
                Current time: <span className="font-semibold tabular-nums">{toHHMM(NOW)}</span>
              </p>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label htmlFor="start" className="block text-sm font-medium text-slate-700 mb-1">
                    Start
                  </label>
                  <input
                    id="start"
                    type="time"
                    value={startStr}
                    onChange={(e) => setStartStr(e.target.value)}
                    className={inputClass}
                  />
                </div>
                <div>
                  <label htmlFor="end" className="block text-sm font-medium text-slate-700 mb-1">
                    End
                  </label>
                  <input
                    id="end"
                    type="time"
                    value={endStr}
                    onChange={(e) => setEndStr(e.target.value)}
                    className={inputClass}
                  />
                </div>
              </div>

              <button
                onClick={reset}
                className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
              >
                Reset
              </button>
            </div>
          </div>
        </section>

        {/* Rooms, result and schedule column */}
        <section className="lg:col-span-3 space-y-6">
          {matches.length === 0 ? (
            <EmptyState />
          ) : (
            <>
              <RoomList rooms={matches} selectedId={room?.id} onSelect={setRoomId} />
              <div aria-live="polite">
                {room && verdict && (
                  <ResultCard verdict={verdict} room={room} start={start} end={end} />
                )}
              </div>
              {room && <RoomSchedule room={room} todayLabel={DAY_LABEL} />}
            </>
          )}
        </section>
      </main>

      <footer className="max-w-5xl mx-auto px-4 sm:px-6 pb-10 text-center text-xs text-slate-400">
        Fictional sample data · Times are in 24-hour format · No bookings are
        actually saved
      </footer>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-8 text-center">
      <SearchX className="h-8 w-8 text-slate-400 mx-auto mb-3" />
      <h3 className="font-semibold text-slate-900">No rooms match your requirements</h3>
      <p className="text-sm text-slate-500 mt-1">
        Try fewer attendees or less equipment.
      </p>
    </div>
  );
}

function RoomList({
  rooms,
  selectedId,
  onSelect,
}: {
  rooms: Room[];
  selectedId: string | undefined;
  onSelect: (id: string) => void;
}) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
      <h2 className="font-semibold text-slate-900 mb-3">
        Matching rooms <span className="text-slate-400 font-normal">({rooms.length})</span>
      </h2>
      <ul className="grid gap-2 sm:grid-cols-2">
        {rooms.map((r) => (
          <li key={r.id}>
            <button
              onClick={() => onSelect(r.id)}
              aria-pressed={r.id === selectedId}
              className={`w-full text-left rounded-xl border px-3 py-2.5 transition-colors ${
                r.id === selectedId
                  ? "border-sky-500 bg-sky-50 ring-1 ring-sky-500"
                  : "border-slate-200 hover:bg-slate-50"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <span className="text-sm font-medium text-slate-900">{r.name}</span>
                {r.blocked && (
                  <span className="rounded-full bg-rose-100 text-rose-700 px-2 py-0.5 text-xs font-medium">
                    Blocked
                  </span>
                )}
              </div>
              <div className="mt-1 text-xs text-slate-500">
                {r.capacity} seats · {r.equipment.join(", ")}
              </div>
            </button>
          </li>
        ))}
      </ul>
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
  room: Room;
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
              {room.name} is free from {toHHMM(start ?? 0)} to{" "}
              {toHHMM(end ?? 0)}. You can proceed with this booking.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 sm:p-6 shadow-sm">
      <div className="flex items-start gap-3">
        <XCircle className="h-6 w-6 text-rose-600 mt-0.5 shrink-0" />
        <div className="w-full">
          <h3 className="font-semibold text-rose-900">Unavailable</h3>
          <p className="text-sm text-rose-800 mt-1">{room.name}:</p>
          <ul className="mt-2 text-sm text-rose-800 space-y-1.5 list-disc list-inside">
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
        {room.building && <span>{room.building}</span>}
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
            <li key={`${b.start}-${b.end}`} className="flex items-center justify-between py-2 text-sm">
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
          const booking = findOverlap(start, end, room.bookings);
          let cls = "bg-emerald-100 hover:bg-emerald-200";
          if (room.blocked) cls = "bg-rose-200 hover:bg-rose-300";
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
