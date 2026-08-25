# 01 — GitHub Project Setup

## Objective

Use GitHub as visible evidence of professional planning, delivery, code review, automated validation, and release management.

## Project board

Create a public board named **Work Order AI Data Flywheel** with these statuses:

`Backlog → Ready → In Progress → Review → Done`

Recommended fields:

| Field | Values |
|---|---|
| Workstream | Documentation, Data, Lakehouse, Modeling, Flywheel, Application, DevOps |
| Priority | P0, P1, P2 |
| Size | Small, Medium, Large |
| Target release | v0.1 through v1.0 |

## Milestones

1. `v0.1 Documentation and Project Setup`
2. `v0.2 Synthetic Data and Bronze`
3. `v0.3 Silver and Gold Lakehouse`
4. `v0.4 Recommendation Baseline`
5. `v0.5 SLM Recommendation Engine`
6. `v0.6 Feedback Flywheel`
7. `v0.7 Reviewer Application`
8. `v1.0 Public Release`

## Initial issue catalog

### v0.1

- Define business problem, users, scope, and success criteria
- Establish public privacy and synthetic-data policy
- Create numbered tutorial structure
- Configure Python packaging and repository CI
- Create GitHub Project board and contribution workflow

### v0.2

- Define fictional work-code taxonomy
- Expand deterministic synthetic-data generator
- Document Bronze data contract and grain
- Recreate Bronze ingestion with synthetic batches
- Add idempotency, reconciliation, and corrupt-record tests
- Document actual Bronze problems and resolutions

### v0.3

- Implement Silver schema and type enforcement
- Implement text standardization and quality flags
- Analyze duplicates without unsafe deletion
- Create Gold training and inference datasets
- Create Gold feedback, evaluation, and monitoring contracts

## Branch and pull-request workflow

```text
main
└── docs/business-problem
└── feature/synthetic-data-generator
└── feature/bronze-ingestion
└── feature/silver-transformations
```

Every issue should result in a focused branch and pull request. A feature is done only when implementation, tests, documentation, and sanitized evidence are complete.

## Current Actions policy

Enable repository CI now. Defer model gates until the baseline exists and application deployment until the reviewer app exists. This prevents workflows that claim to validate components that have not yet been built.
