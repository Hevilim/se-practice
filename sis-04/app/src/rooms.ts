// Fictional room catalog. Data only, no rules.

export type Room = {
  id: string;
  name: string;
  capacity: number;
  equipment: string[];
  blocked: boolean;
  bookings: { start: number; end: number; title?: string }[]; // minutes after midnight, 600 = 10:00
  building?: string;
};

export const EQUIPMENT = ["projector", "whiteboard", "video-call", "computers"];

// The fixed current time of the demo: 09:00.
export const NOW = 540;

export const ROOMS: Room[] = [
  {
    id: "r1",
    name: "Engineering Hall A",
    capacity: 40,
    equipment: ["projector", "whiteboard", "video-call"],
    blocked: false,
    bookings: [
      { title: "Algorithms Lecture", start: 540, end: 600 },
      { title: "Faculty Meeting", start: 780, end: 840 },
      { title: "Robotics Lab", start: 1080, end: 1140 },
    ],
    building: "Block C · Floor 2",
  },
  {
    id: "r2",
    name: "Innovation Lab",
    capacity: 24,
    equipment: ["projector", "whiteboard", "computers"],
    blocked: true,
    bookings: [{ title: "Maintenance", start: 600, end: 660 }],
    building: "Block A · Floor 1",
  },
  {
    id: "r3",
    name: "Library Study Room 3",
    capacity: 12,
    equipment: ["whiteboard"],
    blocked: false,
    bookings: [
      { title: "Group Study", start: 660, end: 720 },
      { title: "Book Club", start: 1020, end: 1080 },
    ],
    building: "Library · Floor 3",
  },
  {
    id: "r4",
    name: "Auditorium B",
    capacity: 200,
    equipment: ["projector", "video-call"],
    blocked: false,
    bookings: [{ title: "Guest Lecture", start: 600, end: 660 }],
    building: "Main Building · Ground",
  },
  {
    id: "r5",
    name: "Seminar Room 5",
    capacity: 8,
    equipment: ["whiteboard", "video-call"],
    blocked: false,
    bookings: [],
    building: "Block B · Floor 1",
  },
];
