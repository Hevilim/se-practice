import { describe, expect, test } from "vitest";
import { filterRooms } from "./filter";
import { checkRoom } from "./booking";
import type { Room } from "./rooms";

// Small fixed catalog, independent of ROOMS. Times in minutes after midnight.
const CATALOG: Room[] = [
  {
    id: "a",
    name: "Room A",
    capacity: 10,
    equipment: ["projector", "whiteboard"],
    blocked: false,
    bookings: [{ start: 600, end: 660 }], // 10:00–11:00
  },
  {
    id: "b",
    name: "Room B",
    capacity: 30,
    equipment: ["projector"],
    blocked: false,
    bookings: [],
  },
  {
    id: "c",
    name: "Room C",
    capacity: 20,
    equipment: ["projector", "whiteboard", "video-call"],
    blocked: true,
    bookings: [],
  },
];

const NOW = 540; // 09:00

const ids = (rooms: { id: string }[]) => rooms.map((r) => r.id);

describe("filterRooms and checkRoom", () => {
  test("F1: excludes rooms with capacity below the attendees", () => {
    expect(ids(filterRooms(CATALOG, { attendees: 11, equipment: [] }))).toEqual(["b", "c"]);
  });

  test("F2: keeps only rooms that have ALL required equipment", () => {
    expect(
      ids(filterRooms(CATALOG, { attendees: 1, equipment: ["projector", "whiteboard"] })),
    ).toEqual(["a", "c"]);
  });

  test("F4: returns [] when no room matches", () => {
    expect(filterRooms(CATALOG, { attendees: 25, equipment: ["whiteboard"] })).toEqual([]);
  });

  test("B5: capacity exactly equal to attendees is included", () => {
    expect(ids(filterRooms(CATALOG, { attendees: 20, equipment: [] }))).toEqual(["b", "c"]);
  });

  test("B6: capacity one below attendees is excluded", () => {
    expect(ids(filterRooms(CATALOG, { attendees: 21, equipment: [] }))).toEqual(["b"]);
  });

  test("F3: a blocked room with a free slot is not available", () => {
    const request = { start: 600, end: 660, now: NOW };
    expect(checkRoom(CATALOG, "b", request)).toBe(true); // the slot itself is bookable
    expect(checkRoom(CATALOG, "c", request)).toBe(false);
  });

  test("F5: the same times give different results for two rooms", () => {
    const request = { start: 600, end: 660, now: NOW };
    expect(checkRoom(CATALOG, "a", request)).toBe(false); // overlaps A's booking
    expect(checkRoom(CATALOG, "b", request)).toBe(true);
  });

  test("F5 AC5: an unknown room id is not available and checkRoom changes nothing", () => {
    const before = JSON.stringify(CATALOG);
    expect(checkRoom(CATALOG, "zzz", { start: 600, end: 660, now: NOW })).toBe(false);
    expect(checkRoom(CATALOG, "b", { start: 600, end: 660, now: NOW })).toBe(true);
    expect(JSON.stringify(CATALOG)).toBe(before);
  });

  test("INT: checkRoom on a room returned by filterRooms", () => {
    const matches = filterRooms(CATALOG, { attendees: 10, equipment: ["projector", "whiteboard"] });
    expect(ids(matches)).toEqual(["a", "c"]);
    // 11:00–12:00 only touches A's 10:00–11:00 booking (AC4)
    expect(checkRoom(matches, "a", { start: 660, end: 720, now: NOW })).toBe(true);
  });
});
