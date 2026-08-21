# Simulating Human Knowledge Gaps in LLMs

An LLM-evaluation framework for a subtle theory-of-mind question: can a language model answer as an agent who lacks a particular concept, without accidentally using the knowledge it was instructed to withhold?

## Problem

Many models can state that a hypothetical person is uninformed, yet still give an expert answer on that person's behalf. This project turns that failure mode into a measurable experiment using OpenBookQA questions, structured knowledge restrictions, leakage checks, and confidence analysis.

## What was built

- OpenBookQA ingestion with domain and difficulty enrichment.
- Structured concept extraction and two knowledge-restriction prompting strategies.
- Naive-answer generation and theory-of-mind probes.
- Automatic leakage detection, failure-mode taxonomy, and confidence calibration analysis.
- Provider abstraction and versioned prompt contracts so the experiment can be rerun across models.

## Main takeaways

The important outcome is not only whether the model answers correctly. The framework separates correctness, faithfulness to the restricted knowledge state, leakage, and confidence, making it possible to detect fluent answers that violate the simulated agent's perspective.

## Reproduce

```bash
pip install -e .
export GOOGLE_API_KEY=...
knowledge-gap-sim generate --data-dir data --output-dir outputs
knowledge-gap-sim analyze --data-dir . --output-dir outputs/analysis
```

`analyze` works offline on existing artifacts. API keys and credentials are never stored in the repository; CI validates the offline package path.
