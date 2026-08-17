import re

import numpy as np
import pandas as pd


def choice_letter(value: object) -> str:
    match = re.search(r"\b([A-D])\b", str(value).upper()); return match.group(1) if match else ""


def evaluate_responses(responses: pd.DataFrame, expected: pd.DataFrame | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = responses.copy(); frame["predicted_choice"] = frame.simulated_answer.map(choice_letter); frame["gold_choice"] = frame.gold_answer.map(choice_letter); frame["correct"] = frame.predicted_choice == frame.gold_choice
    if expected is not None:
        frame = frame.merge(expected[["question_id", "k", "expected_answer"]], on=["question_id", "k"], how="left"); frame["expected_choice"] = frame.expected_answer.map(choice_letter); frame["matches_expected"] = frame.predicted_choice == frame.expected_choice
    frame["knowledge_leakage"] = frame.correct & (~frame.get("matches_expected", pd.Series(False, index=frame.index)))
    frame["failure_mode"] = np.select([frame.knowledge_leakage, frame.get("matches_expected", False), ~frame.correct], ["knowledge_leakage", "expected_naive_reasoning", "incorrect_other"], default="correct_non_leakage")
    aggregations = {"samples": ("question_id", "size"), "accuracy": ("correct", "mean"), "mean_confidence": ("confidence", "mean"), "leakage_rate": ("knowledge_leakage", "mean")}
    if "matches_expected" in frame: aggregations["expected_match_rate"] = ("matches_expected", "mean")
    summary = frame.groupby(["strategy", "k"], as_index=False).agg(**aggregations)
    return frame, summary


def calibration_table(frame: pd.DataFrame, bins: int = 5) -> pd.DataFrame:
    result = frame.copy(); result["confidence_bin"] = pd.cut(result.confidence, np.linspace(0, 1, bins + 1), include_lowest=True); return result.groupby("confidence_bin", observed=False).agg(samples=("correct", "size"), accuracy=("correct", "mean"), mean_confidence=("confidence", "mean")).reset_index().assign(confidence_bin=lambda d: d.confidence_bin.astype(str))
