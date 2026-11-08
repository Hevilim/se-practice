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

export function canBook({ start, end, now, blocked, bookings }: CanBookInput): boolean {
  // AC1: 0 <= start < end <= 1440, start after current time
  if (start < 0 || end > MIN_IN_DAY || start >= end) {
    return false;
  }
  if (start <= now) {
    return false;
  }

  // AC2: duration <= 120 min
  if (end - start > MAX_DURATION) {
    return false;
  }

  // AC3: blocked room
  if (blocked) {
    return false;
  }

  // AC4: overlap (touching endpoints allowed)
  const overlapping = bookings.find((b) => start < b.end && end > b.start);
  if (overlapping) {
    return false;
  }

  return true;
}
