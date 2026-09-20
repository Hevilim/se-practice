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
Looked long and nice, so I thought it was good.

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
2. Is `pass_rate` a percent (0..100) or a fraction (0..1)?
3. Does a mark equal to `pass_mark` pass? ">" or ">="?
4. Is `bool` a number or not?
5. Does it accept a tuple, or only a list?
6. Are `highest` and `lowest` rounded too?

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
but the harness needs `ValueError`. Case 5 is ERROR in section 6, even though all 21 of the AI's
own tests passed.

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
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | ERROR | PASS | PASS | PASS |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | ERROR | PASS | PASS | PASS |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | ERROR | PASS | PASS | PASS |
| 4 | `analyze_marks([], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | ERROR | PASS | ERROR | PASS |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| | **Totals** | | 0/6 | 6/6 | 5/6 | 6/6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| A | 1–6 | There is no `analyze_marks` in the file. The harness cannot import it, so all six cases are ERROR. |
| C | 5 | Raised `TypeError: marks[1] must be int or float, got str` instead of `ValueError`. |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

**Prompt A**

```
hevilim@MacBook-Pro-Karim week-02 % python3 tests/test_analyze_marks.py code/prompt_a.py

ERROR: code/prompt_a.py defines no callable named 'analyze_marks'.
All six cases count as ERROR. Record that in lab-report.md.
```

**Prompt B**

```
hevilim@MacBook-Pro-Karim week-02 % python3 tests/test_analyze_marks.py code/prompt_b.py

========================================================================
analyze_marks harness — code/prompt_b.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.67
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: marks must not be empty
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: non-numeric mark at index 1: '60'
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: mark out of range 0..100 at index 0: -1
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_b.py)
========================================================================
```

**Prompt C**

```
hevilim@MacBook-Pro-Karim week-02 % python3 tests/test_analyze_marks.py code/prompt_c.py

========================================================================
analyze_marks harness — code/prompt_c.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.67
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: marks must not be empty
------------------------------------------------------------------------
case 5  ERROR  analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised TypeError instead of ValueError: marks[1] must be int or float, got str
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: marks[0] must be between 0 and 100, got -1
------------------------------------------------------------------------
RESULT  5 PASS · 0 FAIL · 1 ERROR   (code/prompt_c.py)
========================================================================
```

**Prompt D**

```
hevilim@MacBook-Pro-Karim week-02 % python3 tests/test_analyze_marks.py code/prompt_d.py

========================================================================
analyze_marks harness — code/prompt_d.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.67
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: marks must not be empty
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: mark at index 1 must be a number, got str: '60'
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: mark at index 0 must be between 0 and 100, got -1
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_d.py)
========================================================================
```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | 0 | 2 | 2 | 2 |
| Requirement coverage | 0 | 2 | 1 | 2 |
| Verifiability (tests) | 0 | 0 | 2 | 2 |
| Assumptions stated | 0 | 1 | 2 | 1 |
| Noise (2 = none) | 0 | 2 | 1 | 1 |
| **Total / 10** | **0** | **7** | **8** | **8** |

**Prompt length, in words:** A 7 · B 44 · C 84 · D 250

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:
B added 37 words to A and gained 7 points. C added 40 words to B and gained 1 point. D added 166
words to C and gained 0 points, only one more passing case. The first few sentences buy almost
everything; after that I pay a lot of words for very little.

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
C and D each got 8 out of 10. But in tests B and D, 6 out of 6 cases passed, while C only passed 5. D's code was the best. It's also the one I'd use at work because I defined all the rules myself and didn't let the model guess them. The most useful thing I added was the error type. Case 5, analyze_marks([40, "60"], 50), changed its result because of this. C raised a TypeError with the message "marks[1] must be int or float, got str," so it got an ERROR because the test required a ValueError. In D, I wrote "always ValueError, never TypeError," and the same case passed. Some things were just noise. C added type hints, a test with a tuple, and a test that the list is immutable. D added checks for NaN and infinity. I didn't ask for any of this.The hidden problem was the boundary. In the example [40, 60, 80] with a pass_mark of 50, there is no mark equal to 50, so ">" and ">=" yield the same answer, 66.67. In D, I wrote that a mark equal to pass_mark is a passing score, and I gave a second example, analyze_marks([50, 49], 50), which yields 50.0. Case 3 verifies this.
```

**Word count:**
196

---

## 9. Two questions for the debrief

Written before class, answered in class.

1. Prompt B scored 6/6 with far fewer words than my Prompt D. When is a long prompt actually worth writing, and when is it just cost?
2. Prompt C wrote 21 tests and all of them passed, but it still failed case 5. How do we catch this in real work, where nobody gives us an outside harness?
