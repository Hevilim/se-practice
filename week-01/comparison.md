# Week 01 — Manual vs AI: Comparison

**Name:**
**Group:**
**Date:**

---

## 1. Facts

| | Manual (Part 1) | Rocket (Part 2) |
| --- | --- | --- |
| Language / stack used | python | React.js |
| Time to first version that ran (min) | 5| 10 |
| Time to all 4 test cases passing | 22 | 10|
| Number of attempts / prompts needed | 50 | 3 |
| Lines of code you actually wrote | 25 | many |
| Did it handle invalid marks (case B)? | yes | yes |
| Did it handle an empty list (case D)? | yes | yes |
| Did it use the ≥ 50 pass threshold? | yes | yes |
| Output format matches the spec? | yes | yes (but there are inaccuracies.) |
| Can you explain every line of it? | yes | no |

## 2. Test results

| Case | Input | Manual output | Rocket output | Spec says | Match? |
| --- | --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | avg 67.00 · high 92 · low 23 · pass 60.0% | avg 67.00 · high 92 · low 23 · pass 60.0% | avg 67.00 · high 92 · low 23 · pass 60.0% | yes |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | avg 71.60 · high 100 · low 47 · pass 80.0% | avg 71.60 · high 100 · low 47 · pass 80.0% | avg 71.60 · high 100 · low 47 · pass 80.0% | yes |
| C | `10, 20, 30` | avg 20.00 · high 30 · low 10 · pass 0.0% | avg 20.00 · high 30 · low 10 · pass 0.0% | avg 20.00 · high 30 · low 10 · pass 0.0% | yes |
| D | `abc, , xyz` | avg - · high - · low - · pass - | avg - · high - · low - · pass - | clear message, no crash | yes |

## 3. What the AI added that I never asked for

<!-- Tech stack, UI, extra features, a pass threshold it invented, styling, etc. -->

- Average by Group
- Overall Summary
- Discarded Entries

## 4. What the AI got wrong or silently skipped

<!-- Be concrete: input, expected, actual. -->

Nothing

## 5. The defect I asked Rocket to fix

**Prompt I used:** Fix the display of valid marks

**Result:** partly fixed

**What this tells me:** It's easier to fix it yourself.

---

## 6. Reflection (200–300 words)

Answer all four, in your own words:

1. Which parts of the work did the AI genuinely speed up?
2. Where did the AI cost you time, or give you something that looked right but was not?
3. Which of these two artefacts would you be willing to put your name on, and why?
4. What must a human engineer still be responsible for after this experiment?

<!-- Write your reflection below this line -->

1. Writing numerous lines of code.
2. To fix something
3. The one I wrote myself, because I’ll be able to quickly make corrections if the need arises.
4. Knowledge of the codebase