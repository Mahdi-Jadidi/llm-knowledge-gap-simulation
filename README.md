# Simulating Human Knowledge Gaps in LLMs

A structured LLM evaluation framework for testing whether models can simulate agents with incomplete conceptual knowledge. The full workflow covers OpenBookQA ingestion, domain/difficulty enrichment, concept extraction, two knowledge-restriction prompting strategies, naive-answer generation, theory-of-mind probes, leakage detection, failure-mode analysis, and confidence calibration.

## Commands

```bash
pip install -e .
export GOOGLE_API_KEY=...
knowledge-gap-sim generate --data-dir data --output-dir outputs
knowledge-gap-sim analyze --data-dir . --output-dir outputs/analysis
```

`generate` runs model-backed enrichment, concept extraction, simulation, and naive baselines. `analyze` is fully offline and reproduces the strategy, leakage, failure-mode, and calibration tables from existing CSV artifacts.

## Package design

`provider.py` isolates the LLM API, `schemas.py` owns structured outputs, `prompts.py` contains versioned prompt contracts, `enrichment.py` and `concepts.py` construct the experiment, `simulation.py` executes conditions, and `evaluation.py` performs behavioral analysis.

No keys or secrets are stored in the repository.

## Topics

`llm-evaluation` `theory-of-mind` `knowledge-simulation` `behavioral-science` `openbookqa` `structured-output`
