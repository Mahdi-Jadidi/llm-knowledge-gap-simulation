import pandas as pd
from tqdm import tqdm

from .prompts import ENRICHMENT_PROMPT
from .schemas import Annotation


def enrich_questions(frame: pd.DataFrame, provider) -> pd.DataFrame:
    records = []
    for row in tqdm(frame.itertuples(), total=len(frame), desc="enriching"):
        annotation = provider.structured(ENRICHMENT_PROMPT.format(question=row.question_stem, choices=row.choices), Annotation); records.append({**row._asdict(), **annotation.model_dump()})
    return pd.DataFrame(records).drop(columns=["Index"], errors="ignore")
