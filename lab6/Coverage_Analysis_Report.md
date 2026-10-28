# Lab 6: Code and Branch Coverage Analysis Report

**Name:** Amogh Shetty
**SRN:** PES1UG24AM034
**Repository:** L6_L7_34_tennis_scoring
**Application under test:** `tennis_scoring.py`
**Tools:** Python 3.14, pytest 9.1.1, coverage 7.17.0

---

## 1. Application Overview

`tennis_scoring.py` has three functions:

| Function | Purpose | Decision points |
|---|---|---|
| `game_score(a, b)` | Returns the score of a game (e.g. "30-15", "deuce", "advantage A", "game B"). Raises `ValueError` for negative points. | 8 `if` statements |
| `set_winner(a, b)` | Returns "A", "B" or `None` depending on games won in a set, including the 7-6 tiebreak case. | 4 `if` statements |
| `match_status(sets_a, sets_b, best_of)` | Returns "A wins", "B wins", "decider" or "in progress" for best-of-3 / best-of-5 matches. | 3 `if` statements |

In total the module has **38 statements** and **30 branches** (15 decisions × True/False).

---

## 2. Baseline (Original Test File)

The provided `test_tennis_scoring.py` contained only 2 tests:
- `game_score(0, 0) == "0-0"`
- `set_winner(3, 2) is None`

| Metric | Result |
|---|---|
| Line coverage | 14 / 38 statements (~37%) |
| Branch coverage | 8 / 30 branches (~32% combined) |

Both tests only take the "False" path of every `if` they reach, and `match_status` is never called. The deuce/advantage logic, the negative-input error, all set-win conditions and all match outcomes were untested.

---

## 3. Code (Line) Coverage

**Test file:** `CodeCoverageTest_PES1UG24AM034.py` (19 tests)

**Commands:**
```
python -m coverage run -m pytest CodeCoverageTest_PES1UG24AM034.py
python -m coverage report -m
```

**Result:** 19 passed, `tennis_scoring.py` → 38 statements, 0 missed, **100% line coverage**.
Screenshot: `code_coverage.png`

**Approach:** one test per `return`/`raise` statement so that every line executes at least once:
- `game_score`: normal score, negative input, deuce, game A/B after deuce, advantage A/B, straight game A/B
- `set_winner`: undecided, A wins, B wins, A/B win by 7-6 tiebreak
- `match_status`: A wins, B wins, decider, in progress

---

## 4. Branch Coverage

**Test file:** `BranchCoverageTest_PES1UG24AM034.py` (34 tests)

**Commands:**
```
python -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM034.py
python -m coverage report -m
```

**Result:** 34 passed, `tennis_scoring.py` → 38 statements, 30 branches, 0 partial branches, **100% branch coverage**.
Screenshot: `branch_coverage.png`

**Additional tests added beyond line coverage**, to make every decision evaluate both True and False and to cover edge cases:

| Test input | Why it was added |
|---|---|
| `game_score(0, -1)` | Negative check triggered by `b` instead of `a` |
| `game_score(3, 2)` → "40-30" | `a >= 3` but `b < 3`: deuce condition is False, normal scoring used |
| `game_score(6, 6)`, `(5, 4)`, `(4, 5)` | Deuce and advantage after extended play |
| `set_winner(7, 5)`, `(5, 7)` | Win by 2 games above 6 |
| `set_winner(6, 5)`, `(5, 6)`, `(6, 6)` | One player reaches 6 but without a 2-game lead → `None` |
| `match_status(0, 0, 3)` | Start of match |
| `match_status(3, 1, 5)`, `(1, 3, 5)`, `(2, 2, 5)`, `(2, 1, 5)` | Best-of-5 format; `(2, 1, 5)` checks that only one player at `needed - 1` is not a decider |

---

## 5. Line Coverage vs Branch Coverage: Observations

- **Line coverage can be misleading.** 100% line coverage only proves every statement ran once. For example, `set_winner(6, 3)` covers the `return "A"` line, but says nothing about what happens at 6-5, where `a >= 6` is True yet the set is not over. That case is only exercised when we aim for branch coverage.
- **Branch coverage is stricter.** It requires each `if` to be both True and False, which forced tests for boundary values (6-5, 6-6, 3-2 in a game) and for the best-of-5 format, which is where real scoring bugs tend to appear.
- **Compound conditions** like `a < 0 or b < 0` and `a >= 6 and a - b >= 2` count as a single branch point in coverage.py. To actually test each sub-condition, separate tests were written (`(-1, 0)` and `(0, -1)`; `(6, 3)` and `(6, 5)`), even though the tool would report 100% without them.
- **No dead code** was found: every statement and branch in `tennis_scoring.py` is reachable.

---

## 6. Summary

| Stage | Tests | Line coverage | Branch coverage |
|---|---|---|---|
| Baseline | 2 | ~37% | ~32% |
| Code coverage tests | 19 | **100%** | — |
| Branch coverage tests | 34 | 100% | **100%** |

**Commits:**
1. Add code coverage test cases and report (100% line coverage)
2. Add branch coverage test cases and report (100% branch coverage)
3. Add coverage analysis report
