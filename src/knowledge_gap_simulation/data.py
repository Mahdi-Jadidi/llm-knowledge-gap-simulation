from pathlib import Path

import pandas as pd


def load_openbookqa() -> pd.DataFrame:
    from datasets import load_dataset
    dataset = load_dataset("allenai/openbookqa", "main", split="train")
    rows = []
    for item in dataset:
        choices = "\n".join(f"{label}. {text}" for label, text in zip(item["choices"]["label"], item["choices"]["text"], strict=True)); rows.append({"id": item["id"], "question_stem": item["question_stem"], "choices": choices, "answerKey": item["answerKey"]})
    return pd.DataFrame(rows)


def load_artifacts(data_dir: Path) -> dict[str, pd.DataFrame]:
    names = ("enriched_questions", "concepts_all", "concepts_pilot", "simulated_responses_pilot", "simulated_responses_scaled", "expected_naive_answers_pilot")
    return {name: pd.read_csv(data_dir / f"{name}.csv") for name in names if (data_dir / f"{name}.csv").exists()}
