import unittest
from booking import can_book


class Minutes(int):
    """An integer type that is not exactly int."""


class BookingTests(unittest.TestCase):
    def test_touching_end_is_allowed(self):
        result = can_book(660, 720, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_overlap_is_rejected(self):
        result = can_book(630, 690, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_blocked_room_is_rejected(self):
        result = can_book(660, 720, 540, True, [(600, 660)])
        self.assertIs(result, False)

    def test_exactly_two_hours_is_allowed(self):
        result = can_book(720, 840, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_over_two_hours_is_rejected(self):
        result = can_book(720, 841, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_starts_now_is_rejected(self):
        result = can_book(540, 570, 540, False, [(600, 660)])
        self.assertIs(result, False)

    # AC1: start < end
    def test_zero_length_is_rejected(self):
        result = can_book(700, 700, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_reversed_times_are_rejected(self):
        result = can_book(720, 700, 540, False, [(600, 660)])
        self.assertIs(result, False)

    # AC1: day bounds
    def test_ends_exactly_at_end_of_day_is_allowed(self):
        result = can_book(1380, 1440, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_ends_after_end_of_day_is_rejected(self):
        result = can_book(1380, 1441, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_negative_start_is_rejected(self):
        result = can_book(-30, 30, 540, False, [(600, 660)])
        self.assertIs(result, False)

    # AC1: start > now
    def test_start_one_minute_after_now_is_allowed(self):
        result = can_book(541, 571, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_start_in_the_past_is_rejected(self):
        result = can_book(500, 530, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_start_one_minute_after_midnight_now_is_allowed(self):
        result = can_book(1, 61, 0, False, [(600, 660)])
        self.assertIs(result, True)

    # AC2
    def test_one_minute_booking_is_allowed(self):
        result = can_book(720, 721, 540, False, [(600, 660)])
        self.assertIs(result, True)

    # AC3
    def test_blocked_room_with_no_bookings_is_rejected(self):
        result = can_book(660, 720, 540, True, [])
        self.assertIs(result, False)

    # AC4: the other overlap relationships
    def test_touching_start_is_allowed(self):
        result = can_book(570, 600, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_partial_overlap_over_start_is_rejected(self):
        result = can_book(570, 630, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_inside_existing_is_rejected(self):
        result = can_book(615, 645, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_contains_existing_is_rejected(self):
        result = can_book(570, 690, 540, False, [(600, 660)])
        self.assertIs(result, False)

    def test_identical_interval_is_rejected(self):
        result = can_book(600, 660, 540, False, [(600, 660)])
        self.assertIs(result, False)

    # AC4: empty and several bookings
    def test_empty_existing_is_allowed(self):
        result = can_book(600, 660, 540, False, [])
        self.assertIs(result, True)

    def test_overlap_with_second_booking_is_rejected(self):
        result = can_book(720, 780, 540, False, [(600, 660), (700, 760)])
        self.assertIs(result, False)

    def test_overlap_with_later_booking_in_unsorted_list_is_rejected(self):
        result = can_book(610, 650, 540, False, [(900, 960), (600, 660)])
        self.assertIs(result, False)

    def test_fits_exactly_between_two_bookings_is_allowed(self):
        result = can_book(660, 720, 540, False, [(600, 660), (720, 780)])
        self.assertIs(result, True)

    def test_free_slot_among_three_bookings_is_allowed(self):
        result = can_book(760, 800, 540, False, [(600, 660), (700, 760), (800, 860)])
        self.assertIs(result, True)

    # AC5: existing is never altered
    def test_existing_unchanged_after_accept(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        snapshot = list(existing)
        result = can_book(780, 840, 540, False, existing)
        self.assertIs(result, True)
        self.assertEqual(existing, snapshot)

    def test_existing_unchanged_after_reject(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        snapshot = list(existing)
        result = can_book(610, 650, 540, False, existing)
        self.assertIs(result, False)
        self.assertEqual(existing, snapshot)

    # Outside the contract (lab-report §9.2): a non-integer time returns False, never crashes
    def test_string_start_returns_false(self):
        result = can_book("600", 660, 540, False, [(700, 760)])
        self.assertIs(result, False)

    def test_fractional_start_returns_false(self):
        result = can_book(600.5, 660, 540, False, [(700, 760)])
        self.assertIs(result, False)

    def test_none_end_returns_false(self):
        result = can_book(600, None, 540, False, [(700, 760)])
        self.assertIs(result, False)

    def test_integer_subclass_times_are_allowed(self):
        result = can_book(Minutes(660), Minutes(720), 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_boolean_start_returns_false(self):
        result = can_book(True, 61, 0, False, [])
        self.assertIs(result, False)

    def test_bad_now_returns_false(self):
        result = can_book(660, 720, None, False, [(600, 660)])
        self.assertIs(result, False)

    def test_bad_existing_returns_false(self):
        result = can_book(660, 720, 540, False, [(600,)])
        self.assertIs(result, False)
