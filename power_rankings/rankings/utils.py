from typing import Tuple, Optional

K = 20


def calculate_new_rankings(
    ranking1: float, ranking2: float, winner_is_1: Optional[bool]
) -> Tuple[float, float]:
    win_prob1, win_prob2 = calculate_elo_win_probabilities(ranking1, ranking2)
    actual1, actual2 = _get_actual_outcome(winner_is_1)
    new_ranking1 = _calculate_new_ranking(actual1, ranking1, win_prob1)
    new_ranking2 = _calculate_new_ranking(actual2, ranking2, win_prob2)
    return new_ranking1, new_ranking2


def _calculate_new_ranking(
    outcome: float, old_ranking: float, win_probability: float
) -> float:
    return old_ranking + K * (outcome - win_probability)


def _get_actual_outcome(winner_is_1: Optional[bool]) -> Tuple[float, float]:
    if winner_is_1 is None:
        return 0.5, 0.5
    if winner_is_1:
        return 1.0, 0.0
    else:
        return 0.0, 1.0


def calculate_elo_win_probabilities(
    ranking1: float, ranking2: float
) -> Tuple[float, float]:
    q1 = _exponentiate(ranking1)
    q2 = _exponentiate(ranking2)
    denominator = q1 + q2
    return q1 / denominator, q2 / denominator


def _exponentiate(ranking: float) -> float:
    return 10 ** (ranking / 400)
