# 03 — Synthetic Data

## Objective

Generate reproducible facilities work orders that support engineering and model tests without deriving any content from employer data.

## Grain

One row represents one synthetic work-order phase in one source batch.

## Current implementation

`src/workorder_ai/synthetic.py` generates fictional facilities, assets, work descriptions, priorities, crafts, and historical labels. A seed makes test batches reproducible.

## Planned quality challenges

- Missing asset identifiers
- Duplicate and near-duplicate descriptions
- Conflicting labels
- Rare work codes and class imbalance
- Abbreviations, misspellings, and inconsistent capitalization
- Multiple source batches and controlled schema changes

## Validation

- Phase identifiers are unique within a generated batch.
- Descriptions are non-empty.
- Labels belong to the fictional taxonomy.
- The same seed produces the same dataset.

## Next step

Expand the taxonomy and generator during milestone v0.2 before using it to recreate Bronze ingestion.
