"""analyze_marks: summary statistics for a flat list of marks."""

import unittest


def _check_number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number, got {type(value).__name__}: {value!r}")
    if value != value:  # NaN
        raise ValueError(f"{label} must be a real number, got NaN")
    if value in (float("inf"), float("-inf")):
        raise ValueError(f"{label} must be a finite number, got {value!r}")
    if value < 0 or value > 100:
        raise ValueError(f"{label} must be between 0 and 100, got {value!r}")


def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass_rate for a list/tuple of marks.

    A mark passes when it is >= pass_mark. Raises ValueError on any bad input.
    """
    if not isinstance(marks, (list, tuple)):
        raise ValueError(
            f"marks must be a list or tuple of numbers, got {type(marks).__name__}"
        )

    _check_number(pass_mark, "pass_mark")

    values = list(marks)
    if not values:
        raise ValueError("marks must not be empty")

    for index, mark in enumerate(values):
        _check_number(mark, f"mark at index {index}")

    count = len(values)
    passed = sum(1 for mark in values if mark >= pass_mark)

    return {
        "average": round(sum(values) / count, 2),
        "highest": max(values),
        "lowest": min(values),
        "pass_rate": round(passed * 100 / count, 2),
    }


class TestAnalyzeMarks(unittest.TestCase):
    def test_example_from_spec(self):
        self.assertEqual(
            analyze_marks([40, 60, 80], 50),
            {"average": 60.0, "highest": 80, "lowest": 40, "pass_rate": 66.67},
        )

    def test_single_mark(self):
        self.assertEqual(
            analyze_marks([73]),
            {"average": 73.0, "highest": 73, "lowest": 73, "pass_rate": 100.0},
        )

    def test_decimal_marks(self):
        result = analyze_marks([55.5, 60.25, 40.125])
        self.assertEqual(result["average"], 51.96)
        self.assertEqual(result["highest"], 60.25)
        self.assertEqual(result["lowest"], 40.125)
        self.assertEqual(result["pass_rate"], 66.67)

    def test_custom_pass_mark(self):
        result = analyze_marks([30, 50, 70, 90], pass_mark=70)
        self.assertEqual(result["pass_rate"], 50.0)
        self.assertEqual(result["average"], 60.0)

    def test_mark_equal_to_pass_mark_counts_as_pass(self):
        self.assertEqual(analyze_marks([50, 49], 50)["pass_rate"], 50.0)

    def test_input_list_is_not_modified(self):
        marks = [10, 20, 30]
        analyze_marks(marks)
        self.assertEqual(marks, [10, 20, 30])

    def test_empty_list_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([])

    def test_text_value_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, "60", 70])

    def test_none_value_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, None])

    def test_bool_value_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, True])

    def test_mark_below_zero_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([-1, 50])

    def test_mark_above_hundred_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, 101])

    def test_bad_pass_mark_raises(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, 60], pass_mark="50")
        with self.assertRaises(ValueError):
            analyze_marks([50, 60], pass_mark=101)
        with self.assertRaises(ValueError):
            analyze_marks([50, 60], pass_mark=-0.5)


if __name__ == "__main__":
    unittest.main()
