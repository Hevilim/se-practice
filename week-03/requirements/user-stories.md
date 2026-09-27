# User stories — Smart Campus study room booking

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
