# Lab report — Practice #02: The Prompt Is an Engineering Input

**Name:**
**Group:**
**Date:**

> Fill in every section. **Do not delete or renumber the headings** — the grading pass reads them
> by number. If something did not happen, write "did not happen" and why; an empty section and a
> fabricated one are graded the same way.

---

## 1. The frozen experiment

| | |
| --- | --- |
| AI assistant | Claude (claude.ai) |
| Exact model name | Claude Opus 5 |
| Implementation language | Python |
| Date of the runs | 20.09.2026 |

**Non-Python students only** — paste your substituted Prompt B text here, so the substitution can
be checked:

```
n/a — used Python
```

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes 
- No follow-up questions were asked before Part 7: yes 
- Every output was saved **before** any editing: yes 

---

## 2. Prompt A — minimal

**Prompt sent** (should be exactly one sentence):

```
Write Python code to analyze student marks.
```

**Assumptions the AI made that I never gave it** — list them, one per line. A data format, a pass
threshold, a rounding rule, an input method, an invented feature all count.

1. CSV file as input
2. Pass mark = 60
3. Grades A, B, C, D, F
4. 6 fake students
5. Prints tables, returns nothing
6. Extra stats I never asked for

**Questions it should have asked and did not:**

1. What is the input?
2. Return or print?
3. What mark is a pass?
4. What name for the function?

**Is the function named `analyze_marks` with the required signature?** no, it is 
called: "report

**First impression before testing** (one sentence — you will compare this with section 6 later):
Looked long and nice, so I thought it was not bad but there are some mistakes.

---


## 3. Prompt B — structured context

**Prompt sent** (paste it in full, including any substitutions):

```
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return
average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100;
raise ValueError for an empty list, non-numeric values, or out-of-range values. Use
no external libraries. Return code plus a short explanation.
```

**What B fixed compared to A:**

1. Correct name `analyze_marks` and a clear signature
2. Input is a list of numbers, not a CSV file
3. Returns a dict, does not print
4. Pass mark is a parameter, not a guess
5. Checks empty list, bad types and range 0..100

**What B still leaves open:**

1. Rounding — it chose 2 decimals by itself
2. `pass_mark=50` default was its own choice
3. Is 0..100 the only valid range?
4. Should `pass_rate` be a percent or 0..1?
5. Error type — `ValueError` was not asked for
6. No subjects, only one flat list

---

## 4. Prompt C — examples and tests

**What I appended to Prompt B:**

```
Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40,
pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list,
text value, and marks below 0 or above 100. State any remaining assumptions before
the code.
```

**Tests the AI wrote for itself** — how many, and which situations do they cover?
21 tests.

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | yes |
| decimals | yes |
| custom pass_mark | yes |
| empty list | yes |
| text value | yse |
| below 0 / above 100 | yes |

**Do the AI's own tests pass against the AI's own code?** yes 

**Do they agree with the harness in section 6?** no — the AI raises `TypeError` for a text value,
but Prompt B raised `ValueError` for the same case. The AI chose the error type itself, so the
harness may expect a different one. It also decided that `bool` and a string input are errors.

**Assumptions C stated explicitly before the code:**

1. Marks must be between 0 and 100
2. Default pass mark is 50
3. `pass_mark` is inclusive (mark >= pass_mark)
4. average and pass_rate are rounded to 2 decimals
5. pass_rate is a percent, 0..100
6. `TypeError` for wrong type, `ValueError` for wrong value

---

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```
Write a Python function called analyze_marks(marks, pass_mark=50). It takes a list or tuple of numbers from 0 to 100, and a pass_mark from 0 to 100. A mark passes if it is greater than or equal to pass_mark, so a mark exactly equal to pass_mark counts as a pass. The function returns a dict with four keys: average, highest, lowest and pass_rate. Average is the mean rounded to 2 decimals, pass_rate is the percent of marks that passed rounded to 2 decimals, and highest and lowest are the raw values. If the list is empty, or a value is not a number (text, None or bool), or a mark is below 0 or above 100, or pass_mark is not a number or is outside 0 to 100, raise ValueError with a clear message. Always ValueError, never TypeError. Do not print, do not read files, do not use input, use only the standard library, and do not change the input list. It is one flat list of marks, no student names and no CSV. For example analyze_marks([40, 60, 80], 50) returns average 60.0, highest 80, lowest 40, pass_rate 66.67, and analyze_marks([50, 49], 50) returns pass_rate 50.0 because 50 is a pass. Also write unittest tests for one mark, decimal marks, a custom pass_mark, a mark equal to pass_mark, an empty list, a text value, a mark below 0 and a mark above 100. Put the function and the tests in one file and write no explanation before or after the code.
```

**What I deliberately added that A, B and C did not have:**

1. One error type for everything — always ValueError, never TypeError
2. A second example that shows the boundary case (50 with pass_mark 50)
3. Clear bans: no print, no files, no input(), standard library only
4. The input list must not be changed
5. bool is not a number and must raise an error

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**
The example `analyze_marks([40, 60, 80], 50) -> pass_rate 66.67` does not say what happens when a
mark is exactly equal to pass_mark. There is no 50 in that list, so the answer is 66.67 with `>=`
and also with `>`. The example looks complete but it hides this case. I resolved it in Prompt D: a
mark passes when `mark >= pass_mark`, and I added a second example `analyze_marks([50, 49], 50)`
with pass_rate 50.0 to prove it.
A second gap: Prompt B raised ValueError for a text value, Prompt C raised TypeError for the same
input. Nobody said which one is right. I fixed it to ValueError everywhere.

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | | | | |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | | | | |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | | | | |
| 4 | `analyze_marks([], 50)` | raises ValueError | | | | |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | | | | |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | | | | |
| | **Totals** | | /6 | /6 | /6 | /6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| | | |
| | | |
| | | |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

**Prompt A**

```

```

**Prompt B**

```

```

**Prompt C**

```

```

**Prompt D**

```

```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | | | | |
| Requirement coverage | | | | |
| Verifiability (tests) | | | | |
| Assumptions stated | | | | |
| Noise (2 = none) | | | | |
| **Total / 10** | | | | |

**Prompt length, in words:** A ____ · B ____ · C ____ · D ____

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
(150–200 words)



```

**Word count:**

---

## 9. Two questions for the debrief

Written before class, answered in class.

1.
2.
