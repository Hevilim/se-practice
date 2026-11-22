# AGENTS.md — Smart Campus Room Availability Checker

Instructions for any coding agent working in this project. Read this file before you change
anything, and follow it over any general habit of yours.

## Project

A React + TypeScript page (Vite) that tells a student whether a campus room is free for a
requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
the tests are in `src/booking.test.ts`.

Use fictional data for one room only. Never use real room names, real timetables or personal data.

## Acceptance contract

- AC1 Reject start ≥ end and requests in the past.
- AC2 Enforce the maximum allowed duration (120 minutes).
- AC3 Reject a blocked room.
- AC4 Reject overlaps; allow bookings that only touch at endpoints.
- AC5 Return Available / Unavailable without changing booking data.
- AC6 Preserve clear UI feedback on desktop and mobile.

## Commands

- Install: `npm install`
- Dev server: `npm run dev`
- Tests: `npm test`
- Build: `npm run build`

## You may

- Edit the files in `src/` that the task needs. Do not weaken or delete existing tests.
- Do not add packages unless the user approves them.
- Do not add a login, a database or any backend (no Supabase). Bookings are not saved.

## Before you finish

- Run `npm test` before you propose a change as done. All tests must pass; paste the output.
- Make sure the page still loads.
- Never deploy or publish anything (no Netlify, no production). A human reviews and merges.
- Never commit secrets: no API keys, tokens, passwords or `.env` files.
