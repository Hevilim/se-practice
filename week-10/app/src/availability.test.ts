import { describe, test, expect } from 'vitest';
import { evaluateBooking } from './availability';

describe('evaluateBooking - page messages', () => {
  test('R3 AC1: an empty current time (current = null) gives Unavailable with a current-time message', () => {
    const room = { blocked: false, bookings: [] };
    expect(evaluateBooking(room, 600, 660, null)).toEqual({
      kind: 'unavailable',
      reasons: ['Enter a valid current time in HH:MM format.'],
    });
  });

  test('AC1: a past request (now 09:00, request 08:00-08:30, free room) gives Unavailable', () => {
    const room = { blocked: false, bookings: [] };
    expect(evaluateBooking(room, 480, 510, 540)).toEqual({
      kind: 'unavailable',
      reasons: ['Start time must be after the current time.'],
    });
  });
});
