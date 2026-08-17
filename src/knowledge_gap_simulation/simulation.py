import pandas as pd
from tqdm import tqdm

from .concepts import concept_text
from .prompts import NAIVE_PROMPT, STRATEGY_A_PROMPT, STRATEGY_B_PROMPT
from .schemas import NaiveAnswer, SimulationResponse


def simulate_conditions(questions: pd.DataFrame, concepts: pd.DataFrame, provider, knowledge_levels=(1, 2, 3), strategies=("A", "B")) -> pd.DataFrame:
    merged = questions.merge(concepts, left_on="id", right_on="question_id"); records = []
    for row in tqdm(merged.to_dict("records"), desc="simulating"):
        for k in knowledge_levels:
            known = concept_text(row, k)
            for strategy in strategies:
                template = STRATEGY_A_PROMPT if strategy == "A" else STRATEGY_B_PROMPT; output = provider.structured(template.format(k=k, concepts=known, question=row["question_stem"], choices=row["choices"]), SimulationResponse); records.append({"question_id": row["id"], "k": k, "strategy": strategy, "simulated_answer": output.answer, "reasoning": output.reasoning, "confidence": output.confidence, "gold_answer": row["answerKey"]})
    return pd.DataFrame(records)


def generate_naive_answers(questions: pd.DataFrame, concepts: pd.DataFrame, provider, knowledge_levels=(1, 2, 3)) -> pd.DataFrame:
    merged = questions.merge(concepts, left_on="id", right_on="question_id"); records = []
    for row in tqdm(merged.to_dict("records"), desc="naive baselines"):
        for k in knowledge_levels:
            output = provider.structured(NAIVE_PROMPT.format(concepts=concept_text(row, k), question=row["question_stem"], choices=row["choices"]), NaiveAnswer); records.append({"question_id": row["id"], "k": k, "expected_answer": output.expected_answer, "justification": output.justification, "source": "model"})
    return pd.DataFrame(records)
