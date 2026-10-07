# Acceptance criteria — three selected stories

Assumptions first, then the criteria. Each block names the story it belongs to. 3 to 5 criteria per
story, every one in Given / When / Then form, and every set covers a validation or error case — not
three happy paths.

---

## Assumptions

- **Overlap:** a booking that ends exactly when another begins is allowed under R3 (not an overlap), because a booking is the time from its start up to, but not including, its end. 14:00–15:00 and 15:00–16:00 share no minute.
- **Duration:** a booking of exactly two hours is allowed under R2, because R2 says "at most two hours", and "at most" includes the maximum value itself.
- "Now" is the current time of the system when the student sends the request; all times are local campus time.
- A student can cancel only a booking they made (UC-03: "a reservation the student made").
- Blocking a room stops new bookings only; it does not change bookings that already exist.

---

## US-02 — Book room

### AC-01
- **Given** Room 101 is not blocked and has no bookings tomorrow between 14:00 and 16:00
- **When** a student books Room 101 for tomorrow 14:00–16:00 (exactly two hours)
- **Then** the booking is created for that student

### AC-02
- **Given** the current time is 10:00 today
- **When** a student tries to book Room 101 for today 09:00–10:00
- **Then** the booking is rejected with the message "A booking must start in the future"

### AC-03
- **Given** Room 101 is free tomorrow from 14:00 to 17:00
- **When** a student tries to book Room 101 for tomorrow 14:00–16:30
- **Then** the booking is rejected with the message "A booking cannot be longer than two hours"

### AC-04
- **Given** Room 101 is already booked tomorrow from 14:00 to 15:00
- **When** another student tries to book Room 101 for tomorrow 14:30–15:30
- **Then** the booking is rejected with the message "This room is already booked for part of that time"

### AC-05
- **Given** Room 101 is already booked tomorrow from 14:00 to 15:00
- **When** another student books Room 101 for tomorrow 15:00–16:00
- **Then** the booking is created, because touching bookings do not overlap

---

## US-03 — Cancel booking

### AC-06
- **Given** a student has a booking for Room 101 tomorrow 14:00–15:00
- **When** the student cancels that booking
- **Then** Room 101 is shown as free tomorrow 14:00–15:00 when any student views availability

### AC-07
- **Given** a booking for Room 101 was made by Student A
- **When** Student B tries to cancel that booking
- **Then** the request is rejected with the message "You can only cancel your own bookings"

### AC-08
- **Given** a student already cancelled their booking for Room 101 tomorrow 14:00–15:00
- **When** the student tries to cancel the same booking again
- **Then** the request is rejected with the message "This booking is already cancelled"

### AC-09
- **Given** a student has a booking for Room 101 tomorrow 14:00–15:00
- **When** the student cancels that booking
- **Then** the student receives one cancellation confirmation for Room 101, tomorrow 14:00–15:00

---

## US-05 — Block or unblock room

### AC-10
- **Given** Room 101 is not blocked
- **When** an administrator blocks Room 101
- **Then** Room 101 is shown as not available when any student views availability

### AC-11
- **Given** Room 101 is blocked
- **When** a student tries to book Room 101 for tomorrow 14:00–15:00
- **Then** the booking is rejected with the message "This room is not available for booking"

### AC-12
- **Given** Room 101 was blocked and an administrator has unblocked it
- **When** a student books Room 101 for tomorrow 14:00–15:00
- **Then** the booking is created
