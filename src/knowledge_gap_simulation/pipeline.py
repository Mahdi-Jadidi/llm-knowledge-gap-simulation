from pathlib import Path

import pandas as pd

from .concepts import extract_concepts
from .config import SimulationConfig
from .data import load_artifacts, load_openbookqa
from .enrichment import enrich_questions
from .evaluation import calibration_table, evaluate_responses
from .provider import GoogleProvider
from .simulation import generate_naive_answers, simulate_conditions


def select_pilot(frame: pd.DataFrame, per_subject: int, seed: int) -> pd.DataFrame:
    return frame.groupby("subject_area", group_keys=False).apply(lambda group: group.sample(min(per_subject, len(group)), random_state=seed), include_groups=False).reset_index(drop=True)


def generate_pipeline(config: SimulationConfig) -> dict[str, pd.DataFrame]:
    config.output_dir.mkdir(parents=True, exist_ok=True); provider = GoogleProvider(config.model_name); questions = load_openbookqa().sample(config.sample_size, random_state=config.seed); enriched = enrich_questions(questions, provider); concepts = extract_concepts(enriched, provider); pilot = select_pilot(enriched, config.pilot_per_subject, config.seed); pilot_concepts = concepts[concepts.question_id.isin(pilot.id)]; responses = simulate_conditions(pilot, pilot_concepts, provider, config.knowledge_levels, config.strategies); expected = generate_naive_answers(pilot, pilot_concepts, provider, config.knowledge_levels)
    artifacts = {"enriched_questions": enriched, "concepts_all": concepts, "simulated_responses_pilot": responses, "expected_naive_answers_pilot": expected}
    for name, frame in artifacts.items(): frame.to_csv(config.output_dir / f"{name}.csv", index=False)
    analyze_pipeline(config.output_dir, config.output_dir / "analysis"); return artifacts


def analyze_pipeline(data_dir: Path, output_dir: Path) -> pd.DataFrame:
    artifacts = load_artifacts(data_dir); response_frames = [frame for name, frame in artifacts.items() if name.startswith("simulated_responses")]
    if not response_frames: raise FileNotFoundError("No simulated_responses_*.csv artifacts found.")
    expected = artifacts.get("expected_naive_answers_pilot"); detailed, summary = evaluate_responses(pd.concat(response_frames, ignore_index=True), expected); output_dir.mkdir(parents=True, exist_ok=True); detailed.to_csv(output_dir / "evaluated_responses.csv", index=False); summary.to_csv(output_dir / "strategy_summary.csv", index=False); calibration_table(detailed).to_csv(output_dir / "calibration.csv", index=False); detailed.failure_mode.value_counts().rename_axis("failure_mode").reset_index(name="count").to_csv(output_dir / "failure_modes.csv", index=False); return summary
