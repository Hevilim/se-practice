#!/usr/bin/env python3
"""
Student marks analyzer.

Usage:
    python analyze_marks.py marks.csv      # analyze a CSV file
    python analyze_marks.py                # run on built-in sample data

Expected CSV format (first column = student name, rest = subjects):
    student,Math,Physics,Programming
    Aisha,92,88,95
    Daniyar,74,61,80
"""

import csv
import statistics as st
import sys
from collections import Counter

PASS_MARK = 60
GRADE_SCALE = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]

SAMPLE = [
    {"student": "Aisha",   "Math": 92, "Physics": 88, "Programming": 95},
    {"student": "Daniyar", "Math": 74, "Physics": 61, "Programming": 80},
    {"student": "Madina",  "Math": 55, "Physics": 49, "Programming": 67},
    {"student": "Timur",   "Math": 83, "Physics": 79, "Programming": 71},
    {"student": "Zhanel",  "Math": 68, "Physics": 90, "Programming": 88},
    {"student": "Arman",   "Math": 45, "Physics": 52, "Programming": 58},
]


def grade(score):
    for threshold, letter in GRADE_SCALE:
        if score >= threshold:
            return letter
    return "F"


def load(path):
    """Read marks from CSV. Non-numeric or empty cells are skipped."""
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        name_col = reader.fieldnames[0]
        for raw in reader:
            row = {"student": raw[name_col].strip()}
            for subject in reader.fieldnames[1:]:
                value = (raw.get(subject) or "").strip()
                if value:
                    try:
                        row[subject] = float(value)
                    except ValueError:
                        print(f"warning: bad value {value!r} "
                              f"for {row['student']}/{subject}", file=sys.stderr)
            rows.append(row)
    return rows


def subjects_of(rows):
    names = []
    for row in rows:
        for key in row:
            if key != "student" and key not in names:
                names.append(key)
    return names


def student_stats(rows, subjects):
    result = []
    for row in rows:
        scores = [row[s] for s in subjects if s in row]
        if not scores:
            continue
        avg = st.mean(scores)
        result.append({
            "student": row["student"],
            "scores": scores,
            "total": sum(scores),
            "average": avg,
            "grade": grade(avg),
            "best": max(subjects, key=lambda s: row.get(s, -1)),
            "worst": min(subjects, key=lambda s: row.get(s, 1e9)),
            "failed": [s for s in subjects if row.get(s, 100) < PASS_MARK],
        })
    result.sort(key=lambda r: r["average"], reverse=True)
    for i, r in enumerate(result, 1):
        r["rank"] = i
    return result


def subject_stats(rows, subjects):
    result = {}
    for s in subjects:
        scores = [row[s] for row in rows if s in row]
        if not scores:
            continue
        top = max(rows, key=lambda row: row.get(s, -1))
        result[s] = {
            "count": len(scores),
            "mean": st.mean(scores),
            "median": st.median(scores),
            "stdev": st.pstdev(scores) if len(scores) > 1 else 0.0,
            "min": min(scores),
            "max": max(scores),
            "pass_rate": 100 * sum(x >= PASS_MARK for x in scores) / len(scores),
            "topper": top["student"],
        }
    return result


def report(rows):
    subjects = subjects_of(rows)
    students = student_stats(rows, subjects)
    subs = subject_stats(rows, subjects)

    print("=" * 62)
    print(f"STUDENT RANKING  ({len(students)} students, {len(subjects)} subjects)")
    print("=" * 62)
    print(f"{'#':<3} {'Student':<14} {'Total':>7} {'Avg':>7} {'Grade':>6}  Weak spot")
    for r in students:
        weak = ", ".join(r["failed"]) if r["failed"] else "-"
        print(f"{r['rank']:<3} {r['student']:<14} {r['total']:>7.1f} "
              f"{r['average']:>7.2f} {r['grade']:>6}  {weak}")

    print("\n" + "=" * 62)
    print("SUBJECT BREAKDOWN")
    print("=" * 62)
    print(f"{'Subject':<14} {'Mean':>7} {'Med':>7} {'SD':>6} "
          f"{'Min':>6} {'Max':>6} {'Pass%':>7}  Top")
    for name, s in subs.items():
        print(f"{name:<14} {s['mean']:>7.2f} {s['median']:>7.2f} {s['stdev']:>6.2f} "
              f"{s['min']:>6.0f} {s['max']:>6.0f} {s['pass_rate']:>6.1f}%  {s['topper']}")

    print("\n" + "=" * 62)
    print("GRADE DISTRIBUTION")
    print("=" * 62)
    dist = Counter(r["grade"] for r in students)
    for letter in "ABCDF":
        n = dist.get(letter, 0)
        bar = "#" * n
        pct = 100 * n / len(students) if students else 0
        print(f"{letter}  {n:>3} ({pct:>5.1f}%) {bar}")

    all_avgs = [r["average"] for r in students]
    failing = [r["student"] for r in students if r["failed"]]
    print("\n" + "=" * 62)
    print("SUMMARY")
    print("=" * 62)
    print(f"Class average   : {st.mean(all_avgs):.2f}")
    print(f"Class median    : {st.median(all_avgs):.2f}")
    print(f"Spread (stdev)  : {st.pstdev(all_avgs):.2f}")
    print(f"Top student     : {students[0]['student']} ({students[0]['average']:.2f})")
    print(f"Hardest subject : {min(subs, key=lambda s: subs[s]['mean'])}")
    print(f"Easiest subject : {max(subs, key=lambda s: subs[s]['mean'])}")
    print(f"Needs attention : {', '.join(failing) if failing else 'nobody'}")


def main():
    if len(sys.argv) > 1:
        rows = load(sys.argv[1])
    else:
        print("No file given — using built-in sample data.\n")
        rows = SAMPLE
    if not rows:
        sys.exit("No data to analyze.")
    report(rows)


if __name__ == "__main__":
    main()
