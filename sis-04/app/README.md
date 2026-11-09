# Smart Campus Room Availability Checker

A React + TypeScript page (Vite, Tailwind). Fictional rooms, a fixed current time (09:00), nothing is saved.

## Setup

```bash
npm install
```

## Run

```bash
npm run dev
```

Then open the address Vite prints (usually http://localhost:5173).

## Test

```bash
npx vitest run
```

## Files

- src/rooms.ts: the Room type, the fixed current time NOW and the catalog ROOMS
- src/booking.ts: canBook (AC1-AC5), checkRoom, findOverlap and reasonsFor
- src/filter.ts: filterRooms (F1, F2)
- src/App.tsx: the page, it only imports the rules
