# Approved stories — Smart Campus study room booking

> **Replace this file's stories with your own Week 03 stories, as revised after review**
> (`week-03/requirements/user-stories.md`), keeping their IDs. If you did not complete Week 03, or
> your set was rejected in review, keep the reference set below and say so in `lab-report.md` §1.
> Either way, the IDs here are the ones your consistency table (§7) must use.

**Source of this set:** my week-03 stories, revised

## Scenario (from the Lesson 04 practice deck, slide 7)

Students view room availability, book a room, and cancel their own bookings. Administrators block
or unblock rooms and review usage.

- **R1** Future start, with duration greater than 0 and at most 2 hours.
- **R2** Active bookings for the same room cannot overlap.
- **R3** A blocked room cannot accept a new booking.
- **R4** A successful booking produces a confirmation.

## My week-03 stories

### US-01
**Story:** As a Student, I want to see which study rooms are free and at what times, so that I can choose a room and a time before I try to book.
**Priority:** High
**Assumption:** Availability is shown per room for a day the student chooses, and a blocked room is shown as not available.

### US-02
**Story:** As a Student, I want to book a free study room for a time slot, so that my group and I have a place to study that nobody else can take.
**Priority:** High
**Assumption:** A time slot is a start time and an end time chosen by the student; the scenario gives no minimum length, so none is added.

### US-03
**Story:** As a Student, I want to find one of my own bookings and cancel it, so that the room is free again for other students.
**Priority:** High
**Assumption:** A student can see and cancel only the bookings they made; no time limit for cancelling is added, because the scenario has none.

### US-04
**Story:** As a Student, I want to get a confirmation after I book or cancel a room, so that I know the system accepted my request.
**Priority:** Medium
**Assumption:** The system sends exactly one confirmation for each booking and each cancellation, and nothing else; the channel is not fixed by the scenario.

### US-05
**Story:** As an Administrator, I want to block a room that cannot be used and unblock it when it can be used again, so that students cannot book a room that is out of service.
**Priority:** High
**Assumption:** Blocking stops only new bookings (R4); the scenario does not say what happens to bookings that already exist, so this story does not change them.

### US-06
**Story:** As an Administrator, I want to see how many hours each room was booked over a period I choose, so that I can decide whether the library needs more or fewer study rooms.
**Priority:** Low
**Assumption:** Usage means booked hours stored in the system; cancelled bookings are not counted.

## Rules per story (this lab's numbering)

| ID | Rules |
| --- | --- |
| US-01 | R3 (a blocked room is shown as not available) |
| US-02 | R1, R2, R3, R4 |
| US-03 | R2 (a cancelled booking is no longer ACTIVE) |
| US-04 | R4 |
| US-05 | R3 |
| US-06 | — |

> Note: the assumption of US-05 says "(R4)" because week 03 numbered the rules differently. In this
> lab (slide 7) the blocked-room rule is **R3**. The story text is kept as approved.

**Out of scope** (do not model): payments, equipment in rooms, recurring bookings, waiting lists,
notifications other than the booking confirmation, user registration.
