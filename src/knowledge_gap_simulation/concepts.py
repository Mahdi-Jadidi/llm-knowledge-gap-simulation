import pandas as pd
from tqdm import tqdm

from .prompts import CONCEPT_PROMPT
from .schemas import ConceptExtraction


def extract_concepts(frame: pd.DataFrame, provider) -> pd.DataFrame:
    records = []
    for row in tqdm(frame.itertuples(), total=len(frame), desc="extracting concepts"):
        output = provider.structured(CONCEPT_PROMPT.format(question=row.question_stem, choices=row.choices, answer=row.answerKey), ConceptExtraction); record = {"question_id": row.id}
        for index, concept in enumerate(output.concepts, 1): record[f"concept_{index}"] = concept.name; record[f"concept_{index}_desc"] = concept.description
        records.append(record)
    return pd.DataFrame(records)


def concept_text(row, k: int) -> str:
    values = []
    for index in range(1, k + 1):
        name, description = row.get(f"concept_{index}"), row.get(f"concept_{index}_desc")
        if pd.notna(name): values.append(f"{index}. {name}: {description}")
    return "\n".join(values)
