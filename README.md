# Work Order Data Flywheel

[![CI](https://github.com/terziceh/workorder-flywheel/actions/workflows/ci.yml/badge.svg)](https://github.com/terziceh/workorder-flywheel/actions/workflows/ci.yml)

**Project board:** [Work Order Data Flywheel](https://github.com/users/terziceh/projects/7)

An end-to-end build log and tutorial for developing a Databricks lakehouse, work-code recommendation model, and human-review data flywheel.

> [!IMPORTANT]
> The system may be developed and validated privately with authorized operational data. No source dataset is published. Every record, identifier, taxonomy example, screenshot preview, and reproducible result committed to this public repository must be synthetic, fictionalized, sanitized, or safely generalized.

## What this repository demonstrates

This repository follows the actual engineering dependency chain:

1. Define the business problem and privacy boundary.
2. Manage the work through GitHub Projects and implementation issues.
3. Land the source file in a governed Databricks Unity Catalog volume.
4. Build a traceable Bronze Delta ingestion notebook.
5. Profile and validate Bronze before downstream use.
6. Clean, standardize, and quality-check records in Silver.
7. Build versioned Gold training, inference, and evaluation datasets.
8. Analyze historical labels and define a defensible modeling strategy.
9. Train and evaluate a TF-IDF recommendation baseline.
10. Build and validate a hybrid SLM recommendation model.
11. Connect the approved model to a reviewer application and feedback flywheel.
12. Add application deployment automation only after the model and app are stable.

## Business problem

Facilities organizations produce large volumes of text-heavy work orders. Historical work codes can be missing, inconsistent, or incorrect, weakening operational reporting, asset analysis, and future model training. Manual review is slow, while fully automated classification can be unsafe when labels overlap or descriptions are ambiguous.

The proposed solution provides ranked work-code recommendations while keeping a human reviewer in control. Reviewer actions are preserved as evaluation evidence and potential retraining data.

## Target architecture

```mermaid
flowchart TD
    A["Source file landing"] --> B["Bronze: raw and traceable"]
    B --> C["Silver: clean and validated"]
    C --> D["Gold: versioned ML datasets"]
    D --> E["Baseline and hybrid SLM"]
    E --> F["Reviewer application"]
    F --> G["Human feedback"]
    G --> D
```

## Current implementation plan

| Issue | Deliverable | Completion evidence |
|---:|---|---|
| [#2](https://github.com/terziceh/workorder-flywheel/issues/2) | Load source data into Databricks | Safe screenshots, landing-path explanation, and read verification |
| [#3](https://github.com/terziceh/workorder-flywheel/issues/3) | Build Bronze tables and ingestion notebook | Delta write, file/timestamp metadata, and saved count reconciliation; full-refresh rerun strategy documented |
| [#4](https://github.com/terziceh/workorder-flywheel/issues/4) | Profile and validate Bronze | Initial schema, missingness, grain, duplicate, date-sample, and lineage profiling; findings documented |
| [#5](https://github.com/terziceh/workorder-flywheel/issues/5) | Build the Silver pipeline | Clean records, quality exceptions, tests, and reconciliation |
| [#6](https://github.com/terziceh/workorder-flywheel/issues/6) | Build Gold ML datasets | Reproducible train, validation, test, inference, and evaluation outputs |
| [#7](https://github.com/terziceh/workorder-flywheel/issues/7) | Analyze labels and modeling strategy | Label-quality findings, taxonomy decisions, and evaluation plan |
| [#8](https://github.com/terziceh/workorder-flywheel/issues/8) | Train the TF-IDF baseline | MLflow run, Top-k metrics, error analysis, and saved pipeline |
| [#9](https://github.com/terziceh/workorder-flywheel/issues/9) | Build the hybrid SLM model | Baseline comparison, structured inference, fallbacks, and model card |

## Tutorial chapters

| Chapter | Purpose |
|---|---|
| [Business problem](docs/00_business_problem.md) | Users, risks, scope, and success metrics |
| [GitHub project setup](docs/01_github_project_setup.md) | Board, issues, branches, pull requests, and current CI |
| [Databricks and source setup](docs/02_environment_setup.md) | Governed file landing and safe screenshot walkthrough |
| [Public synthetic companion data](docs/03_synthetic_data.md) | Reproducible examples without distributing the source dataset |
| [Bronze ingestion](docs/04_bronze_ingestion.md) | Full-refresh notebook, Delta table, basic lineage, and count reconciliation |
| [Bronze validation](docs/04_bronze_ingestion.md#bronze-validation-and-profiling) | Checks performed, generalized findings, duplicate review, and Silver decisions |
| [Silver transformations](docs/05_silver_transformations.md) | Cleaning, standardization, quality flags, and exceptions |
| [Gold data products](docs/06_gold_data_products.md) | Versioned ML datasets and leakage-resistant splits |
| [Baseline model](docs/07_baseline_model.md) | Label analysis and TF-IDF benchmark |
| [SLM recommendation engine](docs/08_slm_recommendation_engine.md) | Constrained hybrid recommendations and evaluation |
| [Feedback flywheel](docs/09_feedback_flywheel.md) | Governed reviewer actions and future learning data |
| [Reviewer application](docs/10_reviewer_application.md) | Accept, correct, flag, and abstain workflow |
| [CI/CD and deployment](docs/11_ci_cd_and_deployment.md) | Release workflow after model and application stability |
| [Results and lessons](docs/12_results_and_lessons.md) | Metrics, problems, fixes, limitations, and next steps |

## Current status

**Current work:** Initial Bronze profiling is documented under [#4](https://github.com/terziceh/workorder-flywheel/issues/4); next is the first Silver implementation under [#5](https://github.com/terziceh/workorder-flywheel/issues/5). This documentation update does not change issue states.

- [x] Repository foundation and public Project board
- [x] Privacy boundary
- [x] Documentation and issue structure
- [x] Repository CI
- [x] Complete the sanitized Databricks source-landing walkthrough
- [x] Build and validate the Bronze ingestion notebook
- [x] Profile Bronze structure, missing values, candidate grain, and exact repeats
- [x] Inspect creation-date samples and check ingestion metadata
- [x] Document initial Silver rules and unresolved review items
- [ ] Validate full-column date conversion and implement the first Silver table
- [ ] Continue through Silver, Gold, and modeling

### Ingestion implemented

The reviewed private notebook reads a landed CSV with source columns kept as strings, standardizes column names with a collision check, adds `_ingested_at` and `_source_file`, and overwrites the Bronze Delta snapshot. Its saved output confirms that the readable source and persisted Bronze row counts matched.

This version uses configuration variables and a manually supplied source filename, not notebook widgets or incremental batch controls. Overwrite is the documented full-refresh strategy; the uploaded notebook does not establish a separate rerun test. Count reconciliation verifies row totals, not field-level parsing, uniqueness, or business correctness.

See the [Bronze walkthrough](docs/04_bronze_ingestion.md) for code, explanations, and limitations. The original notebook and operational outputs remain private.

### Validation completed and what we learned

We reviewed missing values, compared work-order and phase counts, isolated exact repeated source records for private review, inspected creation-date examples, and checked ingestion metadata. The saved lineage checks passed. No Bronze records were deleted or rewritten by the validation notebook.

The findings support a simple Silver version: preserve identifiers as text, normalize blanks, trim surrounding spaces, parse dates with a confirmed format, retain optional fields, flag repeats, and reconcile counts. Work order plus phase is a candidate grain; duplicate removal and the source of the repeats remain unresolved. Date sampling is not full-column parsing validation.

The notebook also clarified work-order and phase field names in memory. Before Silver, the persisted schema and ownership of that mapping must be confirmed.

Read the [validation walkthrough](docs/04_bronze_ingestion.md#bronze-validation-and-profiling) and the [first Silver plan](docs/05_silver_transformations.md). Private previews, the uploaded notebook, review exports, and exact operational metrics are excluded from the public repository. Recurring-file automation remains deferred.

## Repository organization

```text
.
├── .github/             Issue templates, PR template, and current CI
├── configs/             Non-sensitive configuration
├── docs/                Build tutorial and engineering decisions
├── notebooks/           Exploration and communication only
├── sample_data/         Small generated examples only
├── scripts/             Developer entry points
├── src/workorder_ai/    Reusable pipeline and model code
├── tests/               Unit, integration, data, and model tests
├── CONTRIBUTING.md
├── Makefile
├── pyproject.toml
└── README.md
```

## Evidence standard

Every technical stage should include:

- Objective, input, output, and table grain
- Implementation or notebook walkthrough
- Validation and reconciliation
- Problems, root causes, fixes, and tradeoffs
- Tests and reproducibility instructions
- Sanitized screenshots or synthetic output
- Related issue, commit, or pull request
- Known limitations and next dependency

## Privacy and screenshot rules

Public screenshots must not expose real records, employer or employee identifiers, email addresses, workspace URLs, credentials, internal storage paths, or unauthorized operational metrics. Screenshots are reviewed and cropped or redacted before publication. Example rows and public model demonstrations use synthetic data.

See [Security and Privacy](docs/security_and_privacy.md).

## GitHub Actions scope

Current CI checks the public Python package, tests, and synthetic-data generation. Data and model checks will be added when their implementation reaches the repository. Application build and deployment workflows remain intentionally deferred until the reviewer application exists.

## License

Released under the [MIT License](LICENSE).
