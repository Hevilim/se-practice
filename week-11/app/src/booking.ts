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

export const MIN_IN_DAY = 1440;
export const MAX_DURATION = 120;

// Each failed rule is returned as data so the page can explain it
// without re-implementing the rule.
export type Rejection<B extends BookingInterval = BookingInterval> =
  | { rule: "invalid-now" }
  | { rule: "invalid-interval" }
  | { rule: "not-after-now" }
  | { rule: "too-long" }
  | { rule: "blocked" }
  | { rule: "overlap"; booking: B };

// Touching endpoints (a.end === b.start) is not an overlap.
export function overlaps(a: BookingInterval, b: BookingInterval): boolean {
  return a.start < b.end && a.end > b.start;
}

export function findRejections<B extends BookingInterval>(
  input: Omit<CanBookInput, "bookings"> & { bookings: B[] },
): Rejection<B>[] {
  const { start, end, now, blocked, bookings } = input;
  const rejections: Rejection<B>[] = [];

  // AC1: without a real current time we cannot tell whether a request is in the past.
  if (!(0 <= now && now < MIN_IN_DAY)) rejections.push({ rule: "invalid-now" });
  if (!(0 <= start && start < end && end <= MIN_IN_DAY)) rejections.push({ rule: "invalid-interval" });
  if (!(start > now)) rejections.push({ rule: "not-after-now" });
  // AC2
  if (end - start > MAX_DURATION) rejections.push({ rule: "too-long" });
  // AC3
  if (blocked) rejections.push({ rule: "blocked" });
  // AC4
  const clash = bookings.find((b) => overlaps({ start, end }, b));
  if (clash) rejections.push({ rule: "overlap", booking: clash });

  return rejections;
}

// The six reason codes of the explanation contract, spelled exactly as in the lab README.
export const REASON_CODES = [
  "invalid_time",
  "past_time",
  "too_long",
  "room_blocked",
  "overlap",
  "available",
] as const;

export type ReasonCode = (typeof REASON_CODES)[number];

const CODE_FOR_RULE: Record<Rejection["rule"], ReasonCode> = {
  // An unknown current time is an invalid time input, not a past one.
  "invalid-now": "invalid_time",
  "invalid-interval": "invalid_time",
  "not-after-now": "past_time",
  "too-long": "too_long",
  blocked: "room_blocked",
  overlap: "overlap",
};

// The first failed rule, in the same order canBook checks them (AC1, AC2, AC3, AC4).
export function availabilityReason(input: CanBookInput): ReasonCode {
  const [first] = findRejections(input);
  return first ? CODE_FOR_RULE[first.rule] : "available";
}

export function canBook(input: CanBookInput): boolean {
  return availabilityReason(input) === "available";
}
