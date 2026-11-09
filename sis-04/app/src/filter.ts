import type { Room } from "./rooms";

// F1: capacity >= attendees. F2: room has every required item.
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
