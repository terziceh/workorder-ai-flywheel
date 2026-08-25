# Roadmap

The roadmap follows working software and verifiable evidence rather than standalone planning artifacts.

## Completed — Repository foundation

- Public repository and Project board
- Privacy and publication boundaries
- Issue and pull-request templates
- Python package, tests, and repository CI
- Tutorial documentation structure

## Phase 1 — Databricks source landing

- Land the approved source file in a Unity Catalog volume
- Verify that Databricks can read it
- Publish a sanitized screenshot walkthrough
- Provide synthetic companion data for public reproduction

Tracking: [Issue #2](https://github.com/terziceh/workorder-ai-flywheel/issues/2)

## Phase 2 — Bronze ingestion and validation

- Create Bronze schema and Delta table
- Build the parameterized ingestion notebook
- Add ingestion metadata and batch controls
- Reconcile counts and test reruns
- Profile Bronze quality and document fixes

Tracking: [Issues #3–#4](https://github.com/terziceh/workorder-ai-flywheel/issues)

## Phase 3 — Silver pipeline

- Standardize types, categories, timestamps, and text
- Preserve raw and cleaned values
- Flag duplicates, missing identifiers, and conflicting labels
- Create visible quality-exception outputs
- Validate incremental and idempotent behavior

Tracking: [Issue #5](https://github.com/terziceh/workorder-ai-flywheel/issues/5)

## Phase 4 — Gold ML datasets

- Build versioned training, inference, and evaluation tables
- Define eligibility rules and grains
- Create leakage-resistant train, validation, and test splits
- Preserve dataset and feature lineage

Tracking: [Issue #6](https://github.com/terziceh/workorder-ai-flywheel/issues/6)

## Phase 5 — Label analysis and baseline

- Profile frequency, imbalance, overlap, and inconsistent labels
- Define modeling eligibility and human-review cases
- Train the TF-IDF baseline
- Track runs and artifacts with MLflow
- Report Top-k, class-level, and error-analysis results

Tracking: [Issues #7–#8](https://github.com/terziceh/workorder-ai-flywheel/issues)

## Phase 6 — Hybrid SLM recommendation model

- Generate a constrained candidate set
- Rank candidates with an SLM layer
- Enforce structured output and approved taxonomy
- Add confidence, abstention, and deterministic fallbacks
- Compare against the baseline on identical held-out data
- Publish a model card and intended-use limitations

Tracking: [Issue #9](https://github.com/terziceh/workorder-ai-flywheel/issues/9)

## Later — Reviewer application and feedback flywheel

- Ranked recommendation interface
- Accept, correct, flag, and abstain actions
- Governed feedback persistence
- Evaluation and retraining datasets
- Monitoring and model comparison
- Application CI/CD and public demo after stability

Deployment automation remains out of scope until the model and reviewer application are complete.
