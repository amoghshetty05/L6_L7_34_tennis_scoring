import pytest
from tennis_scoring import game_score, set_winner, match_status


# ======================= game_score =======================
# Branch 1: a < 0 or b < 0  -> True / False

def test_game_negative_a():
    with pytest.raises(ValueError):
        game_score(-1, 0)

def test_game_negative_b():
    with pytest.raises(ValueError):
        game_score(0, -1)

# Branch 2: a >= 3 and b >= 3 -> False (normal scoring)

def test_game_start():
    assert game_score(0, 0) == "0-0"

def test_game_regular_score():
    assert game_score(2, 1) == "30-15"

def test_game_a_at_40_b_below_3():
    # a >= 3 but b < 3 -> condition False, falls to normal scoring
    assert game_score(3, 2) == "40-30"

# Branch 2 True -> deuce section, each inner if True / False

def test_game_deuce():
    assert game_score(3, 3) == "deuce"

def test_game_deuce_later():
    assert game_score(6, 6) == "deuce"

def test_game_a_wins_after_deuce():
    assert game_score(5, 3) == "game A"

def test_game_b_wins_after_deuce():
    assert game_score(3, 5) == "game B"

def test_game_advantage_a():
    assert game_score(4, 3) == "advantage A"

def test_game_advantage_a_later():
    assert game_score(5, 4) == "advantage A"

def test_game_advantage_b():
    assert game_score(3, 4) == "advantage B"

def test_game_advantage_b_later():
    assert game_score(4, 5) == "advantage B"

# a >= 4 / b >= 4 outside deuce section -> True / False

def test_game_a_wins_straight():
    assert game_score(4, 1) == "game A"

def test_game_b_wins_straight():
    assert game_score(1, 4) == "game B"


# ======================= set_winner =======================

def test_set_undecided():
    assert set_winner(3, 2) is None

def test_set_a_wins():
    assert set_winner(6, 3) == "A"

def test_set_a_wins_7_5():
    assert set_winner(7, 5) == "A"

def test_set_b_wins():
    assert set_winner(2, 6) == "B"

def test_set_b_wins_5_7():
    assert set_winner(5, 7) == "B"

def test_set_a_wins_tiebreak():
    assert set_winner(7, 6) == "A"

def test_set_b_wins_tiebreak():
    assert set_winner(6, 7) == "B"

def test_set_6_5_not_finished():
    # a >= 6 but lead is only 1 -> no winner yet
    assert set_winner(6, 5) is None

def test_set_5_6_not_finished():
    assert set_winner(5, 6) is None

def test_set_6_6_not_finished():
    assert set_winner(6, 6) is None


# ======================= match_status =======================
# Best of 3 (needed = 2)

def test_match_a_wins():
    assert match_status(2, 0, 3) == "A wins"

def test_match_b_wins():
    assert match_status(1, 2, 3) == "B wins"

def test_match_decider():
    assert match_status(1, 1, 3) == "decider"

def test_match_in_progress():
    assert match_status(1, 0, 3) == "in progress"

def test_match_in_progress_start():
    assert match_status(0, 0, 3) == "in progress"

# Best of 5 (needed = 3)

def test_match_a_wins_best_of_5():
    assert match_status(3, 1, 5) == "A wins"

def test_match_b_wins_best_of_5():
    assert match_status(1, 3, 5) == "B wins"

def test_match_decider_best_of_5():
    assert match_status(2, 2, 5) == "decider"

def test_match_in_progress_best_of_5():
    # sets_a == needed - 1 but sets_b is not -> not a decider
    assert match_status(2, 1, 5) == "in progress"
