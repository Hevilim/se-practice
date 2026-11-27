import { findRejections, MAX_DURATION, type BookingInterval, type Rejection } from "./booking";

export type TitledBooking = BookingInterval & { title: string };

export type CheckableRoom = {
  blocked: boolean;
  bookings: TitledBooking[];
};

export type Verdict =
  | { kind: "available" }
  | { kind: "unavailable"; reasons: string[] };

const INVALID_NOW_REASON = "Enter a valid current time in HH:MM format.";

export function toMinutes(time: string): number | null {
  if (!/^\d{2}:\d{2}$/.test(time)) return null;
  const [h, m] = time.split(":").map(Number);
  if (h < 0 || h > 23 || m < 0 || m > 59) return null;
  return h * 60 + m;
}

export function toHHMM(min: number): string {
  const h = Math.floor(min / 60);
  const m = min % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

function reasonFor(r: Rejection<TitledBooking>): string {
  switch (r.rule) {
    case "invalid-now":
      return INVALID_NOW_REASON;
    case "invalid-interval":
      return "Interval must satisfy 0 ≤ start < end ≤ 24:00. End must be after start.";
    case "not-after-now":
      return "Start time must be after the current time.";
    case "too-long":
      return `Booking cannot be longer than ${MAX_DURATION} minutes.`;
    case "blocked":
      return "This room is currently blocked and cannot be booked.";
    case "overlap":
      return `Overlaps existing booking "${r.booking.title}" (${toHHMM(r.booking.start)}–${toHHMM(r.booking.end)}).`;
  }
}

export function evaluateBooking(
  room: CheckableRoom | undefined,
  start: number | null,
  end: number | null,
  current: number | null,
): Verdict {
  if (!room) {
    return { kind: "unavailable", reasons: ["Select a room to check."] };
  }
  if (start === null || end === null) {
    return {
      kind: "unavailable",
      reasons: ["Enter valid start and end times in HH:MM format."],
    };
  }
  if (current === null) {
    return { kind: "unavailable", reasons: [INVALID_NOW_REASON] };
  }

  const rejections = findRejections({
    start,
    end,
    now: current,
    blocked: room.blocked,
    bookings: room.bookings,
  });

  return rejections.length === 0
    ? { kind: "available" }
    : { kind: "unavailable", reasons: rejections.map(reasonFor) };
}
