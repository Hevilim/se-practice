import type { Room } from "./rooms";

export type BookingInterval = {
  start: number; // minutes from midnight
  end: number;
  title?: string;
};

export type CanBookInput = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: BookingInterval[];
};

export const MIN_IN_DAY = 1440;
export const MAX_DURATION = 120;

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

// F3, F5: check the chosen room with its own blocked status and bookings.
export function checkRoom(
  rooms: Room[],
  roomId: string,
  request: { start: number; end: number; now: number },
): boolean {
  const room = rooms.find((r) => r.id === roomId);
  if (!room) return false;
  return canBook({ ...request, blocked: room.blocked, bookings: room.bookings });
}

// The first booking that overlaps start-end. Touching endpoints is not an overlap (AC4).
export function findOverlap<T extends BookingInterval>(
  start: number,
  end: number,
  bookings: T[],
): T | undefined {
  return bookings.find((b) => start < b.end && end > b.start);
}

export type Reason =
  | { code: "interval" }
  | { code: "past" }
  | { code: "too-long" }
  | { code: "blocked" }
  | { code: "overlap"; booking: BookingInterval };

// Why a request is Unavailable, for the messages on the page. Empty when canBook is true.
export function reasonsFor({ start, end, now, blocked, bookings }: CanBookInput): Reason[] {
  const reasons: Reason[] = [];
  if (!(0 <= start && start < end && end <= MIN_IN_DAY)) reasons.push({ code: "interval" });
  if (!(start > now)) reasons.push({ code: "past" });
  if (end - start > MAX_DURATION) reasons.push({ code: "too-long" });
  if (blocked) reasons.push({ code: "blocked" });
  const booking = findOverlap(start, end, bookings);
  if (booking) reasons.push({ code: "overlap", booking });
  return reasons;
}
