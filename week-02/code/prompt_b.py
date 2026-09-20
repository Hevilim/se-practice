"""Simple mark statistics with strict input validation."""

from numbers import Real


def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass rate for a list of marks.

    Args:
        marks: non-empty iterable of numbers in the range 0..100.
        pass_mark: threshold a mark must reach (>=) to count as a pass.

    Returns:
        dict with keys 'average', 'highest', 'lowest', 'pass_rate'
        (pass_rate is a percentage, 0..100).

    Raises:
        ValueError: empty input, non-numeric values, or values outside 0..100.
    """
    marks = list(marks)

    if not marks:
        raise ValueError("marks must not be empty")

    if not isinstance(pass_mark, Real) or isinstance(pass_mark, bool):
        raise ValueError(f"pass_mark must be numeric, got {pass_mark!r}")
    if not 0 <= pass_mark <= 100:
        raise ValueError(f"pass_mark must be between 0 and 100, got {pass_mark!r}")

    for index, mark in enumerate(marks):
        if isinstance(mark, bool) or not isinstance(mark, Real):
            raise ValueError(f"non-numeric mark at index {index}: {mark!r}")
        if not 0 <= mark <= 100:
            raise ValueError(f"mark out of range 0..100 at index {index}: {mark!r}")

    passed = sum(1 for mark in marks if mark >= pass_mark)

    return {
        "average": round(sum(marks) / len(marks), 2),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": round(passed / len(marks) * 100, 2),
    }


if __name__ == "__main__":
    print(analyze_marks([90, 45, 72, 50, 12]))
    # {'average': 53.8, 'highest': 90, 'lowest': 12, 'pass_rate': 60.0}
