import { describe, test, expect } from 'vitest';
import { canBook } from './booking';
import type { BookingInterval, CanBookInput } from './booking';

// Default fixture from the reviewed case table:
//   now = 540 (09:00), blocked = false, bookings = [{ start: 600, end: 660 }]
// Time is a fixed number. A new object and a new bookings array are built for every test,
// so no test can change the data another test sees.
function freshBookings(): BookingInterval[] {
  return [{ start: 600, end: 660 }];
}

function request(start: number, end: number): CanBookInput {
  return { start, end, now: 540, blocked: false, bookings: freshBookings() };
}

describe('canBook - AC1: valid interval, start after now', () => {
  test('T02 AC1: request starting exactly at now (540-570) is rejected', () => {
    expect(canBook(request(540, 570))).toBe(false);
  });

  test('T03 AC1: zero-duration request (720-720) is rejected', () => {
    expect(canBook(request(720, 720))).toBe(false);
  });

  test('T04 AC1: reversed request (750-720) is rejected', () => {
    expect(canBook(request(750, 720))).toBe(false);
  });

  test('T05 AC1: request ending past the end of the day (1380-1441) is rejected', () => {
    expect(canBook(request(1380, 1441))).toBe(false);
  });

  test('X1 AC1: request ending exactly at 24:00 (1380-1440) is accepted', () => {
    expect(canBook(request(1380, 1440))).toBe(true);
  });
});

describe('canBook - AC2: at most 120 minutes', () => {
  test('T06 AC2: exactly 120 minutes (720-840) is accepted', () => {
    expect(canBook(request(720, 840))).toBe(true);
  });

  test('T07 AC2: 121 minutes (720-841) is rejected', () => {
    expect(canBook(request(720, 841))).toBe(false);
  });
});

describe('canBook - AC3: blocked room', () => {
  test('T13 AC3: otherwise-available request (660-720) in a blocked room is rejected', () => {
    const input = { start: 660, end: 720, now: 540, blocked: true, bookings: freshBookings() };
    expect(canBook(input)).toBe(false);
  });
});

describe('canBook - AC4: no overlap, touching allowed', () => {
  test('T01 AC4: request touching the end of the booking (660-720) is accepted', () => {
    expect(canBook(request(660, 720))).toBe(true);
  });

  test('T08 AC4: request touching the start of the booking (570-600) is accepted', () => {
    expect(canBook(request(570, 600))).toBe(true);
  });

  test('T09 AC4: partial overlap (630-690) is rejected', () => {
    expect(canBook(request(630, 690))).toBe(false);
  });

  test('T10 AC4: request containing the booking (570-690) is rejected', () => {
    expect(canBook(request(570, 690))).toBe(false);
  });

  test('T11 AC4: request inside the booking (615-645) is rejected', () => {
    expect(canBook(request(615, 645))).toBe(false);
  });

  test('T12 AC4: request identical to the booking (600-660) is rejected', () => {
    expect(canBook(request(600, 660))).toBe(false);
  });

  test('T14 AC4: 630-690 with no existing bookings is accepted', () => {
    const input = { start: 630, end: 690, now: 540, blocked: false, bookings: [] };
    expect(canBook(input)).toBe(true);
  });

  test('X2 AC4: request touching two bookings (660-720 between 600-660 and 720-780) is accepted', () => {
    const input = {
      start: 660,
      end: 720,
      now: 540,
      blocked: false,
      bookings: [
        { start: 600, end: 660 },
        { start: 720, end: 780 },
      ],
    };
    expect(canBook(input)).toBe(true);
  });
});

describe('canBook - AC5: decision without changing booking data', () => {
  test('AC5: an Available request (660-720) leaves the bookings unchanged', () => {
    const input = request(660, 720);
    const before = structuredClone(input.bookings);

    expect(canBook(input)).toBe(true);

    expect(input.bookings).toEqual(before);
    expect(input.bookings).toEqual([{ start: 600, end: 660 }]);
  });
});
