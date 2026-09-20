"""Summary statistics for a list of student marks."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

MIN_MARK = 0
MAX_MARK = 100
DEFAULT_PASS_MARK = 50


def _check_number(value: Any, label: str) -> None:
    """Reject anything that is not a real int/float. bool is an int subclass, so
    it is rejected explicitly."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be int or float, got {type(value).__name__}")


def _check_range(value: float, label: str) -> None:
    if not MIN_MARK <= value <= MAX_MARK:
        raise ValueError(f"{label} must be between {MIN_MARK} and {MAX_MARK}, got {value}")


def analyze_marks(marks: Sequence[float], pass_mark: float = DEFAULT_PASS_MARK) -> dict:
    """Return average, highest, lowest and pass_rate for a list of marks.

    Args:
        marks: non-empty sequence of numbers in the range 0..100.
        pass_mark: threshold to pass, inclusive. Defaults to 50.

    Returns:
        dict with keys "average", "highest", "lowest", "pass_rate".
        average and pass_rate are rounded to 2 decimals; pass_rate is a
        percentage (0..100).

    Raises:
        TypeError: marks is not a sequence, or a mark/pass_mark is not numeric.
        ValueError: marks is empty, or a mark/pass_mark is outside 0..100.
    """
    if isinstance(marks, (str, bytes)) or not isinstance(marks, Sequence):
        raise TypeError(f"marks must be a sequence of numbers, got {type(marks).__name__}")
    if len(marks) == 0:
        raise ValueError("marks must not be empty")

    _check_number(pass_mark, "pass_mark")
    _check_range(pass_mark, "pass_mark")

    for index, mark in enumerate(marks):
        _check_number(mark, f"marks[{index}]")
        _check_range(mark, f"marks[{index}]")

    total = len(marks)
    passed = sum(1 for mark in marks if mark >= pass_mark)

    return {
        "average": round(sum(marks) / total, 2),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": round(passed / total * 100, 2),
    }


if __name__ == "__main__":
    print(analyze_marks([40, 60, 80], 50))
