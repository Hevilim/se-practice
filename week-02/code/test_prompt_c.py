"""Tests for analyze_marks. Run: python -m unittest test_marks -v"""

import unittest

from prompt_c import analyze_marks


class TestAnalyzeMarks(unittest.TestCase):

    def test_example_from_spec(self):
        result = analyze_marks([40, 60, 80], 50)
        self.assertEqual(
            result,
            {"average": 60, "highest": 80, "lowest": 40, "pass_rate": 66.67},
        )

    def test_single_mark_passing(self):
        result = analyze_marks([73])
        self.assertEqual(
            result,
            {"average": 73, "highest": 73, "lowest": 73, "pass_rate": 100.0},
        )

    def test_single_mark_failing(self):
        result = analyze_marks([12])
        self.assertEqual(result["pass_rate"], 0.0)
        self.assertEqual(result["highest"], result["lowest"])

    def test_decimal_marks(self):
        result = analyze_marks([55.5, 70.25, 49.75])
        # (55.5 + 70.25 + 49.75) / 3 = 58.5
        self.assertEqual(result["average"], 58.5)
        self.assertEqual(result["highest"], 70.25)
        self.assertEqual(result["lowest"], 49.75)
        self.assertEqual(result["pass_rate"], 66.67)

    def test_average_is_rounded_to_two_decimals(self):
        # 100/3 = 33.333...
        self.assertEqual(analyze_marks([33, 33, 34])["average"], 33.33)

    def test_custom_pass_mark(self):
        marks = [40, 60, 80]
        self.assertEqual(analyze_marks(marks, pass_mark=70)["pass_rate"], 33.33)
        self.assertEqual(analyze_marks(marks, pass_mark=90)["pass_rate"], 0.0)
        self.assertEqual(analyze_marks(marks, pass_mark=0)["pass_rate"], 100.0)

    def test_pass_mark_is_inclusive(self):
        self.assertEqual(analyze_marks([50, 49], pass_mark=50)["pass_rate"], 50.0)

    def test_default_pass_mark_is_fifty(self):
        self.assertEqual(
            analyze_marks([40, 60, 80]),
            analyze_marks([40, 60, 80], 50),
        )

    def test_boundary_marks_allowed(self):
        result = analyze_marks([0, 100])
        self.assertEqual(result["lowest"], 0)
        self.assertEqual(result["highest"], 100)
        self.assertEqual(result["average"], 50)

    def test_duplicates_counted(self):
        self.assertEqual(analyze_marks([60, 60, 60, 20])["pass_rate"], 75.0)

    def test_empty_list_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([])

    def test_text_value_raises_type_error(self):
        with self.assertRaises(TypeError):
            analyze_marks([40, "60", 80])

    def test_none_value_raises_type_error(self):
        with self.assertRaises(TypeError):
            analyze_marks([40, None])

    def test_bool_value_raises_type_error(self):
        with self.assertRaises(TypeError):
            analyze_marks([True, 60])

    def test_string_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            analyze_marks("406080")

    def test_mark_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([-1, 50])

    def test_mark_above_hundred_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, 101])

    def test_non_numeric_pass_mark_raises_type_error(self):
        with self.assertRaises(TypeError):
            analyze_marks([40, 60], pass_mark="50")

    def test_out_of_range_pass_mark_raises_value_error(self):
        with self.assertRaises(ValueError):
            analyze_marks([40, 60], pass_mark=150)

    def test_input_list_not_mutated(self):
        marks = [40, 60, 80]
        analyze_marks(marks)
        self.assertEqual(marks, [40, 60, 80])

    def test_tuple_accepted(self):
        self.assertEqual(analyze_marks((40, 60, 80))["average"], 60)


if __name__ == "__main__":
    unittest.main(verbosity=2)
