# Architecture

## Current state: v0.1

The repository currently provides a deterministic synthetic-data source and validation tests. It deliberately starts small so later lakehouse and ML components are justified by working requirements.

## Target components

1. Synthetic batch generator
2. Bronze immutable ingestion
3. Silver schema and quality enforcement
4. Gold training, inference, feedback, and monitoring models
5. TF-IDF recommendation baseline
6. Human-review application
7. Evaluation and retraining workflow

## Architectural constraints

- Public data must be independently generated.
- Pipeline reruns must be idempotent.
- Model predictions must retain model-version metadata.
- Reviewer corrections must not overwrite original predictions.
- Exploratory notebooks cannot become production dependencies.
