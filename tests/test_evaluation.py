import pandas as pd

from knowledge_gap_simulation.evaluation import choice_letter, evaluate_responses


def test_choice_letter_extracts_multiple_choice_answer() -> None:
    assert choice_letter("The answer is B. mountains") == "B"


def test_response_evaluation() -> None:
    responses = pd.DataFrame([{"question_id": "q1", "k": 1, "strategy": "A", "simulated_answer": "A", "gold_answer": "B", "confidence": .7}]); detailed, summary = evaluate_responses(responses); assert not detailed.iloc[0].correct; assert len(summary) == 1
