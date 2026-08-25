# 04 — Bronze Ingestion

## Objective

Recreate the existing Bronze-layer design with synthetic source batches and document it as a reproducible Databricks tutorial.

## Grain

One row represents one source work-order phase as received in one ingestion batch.

## Planned ingestion metadata

```text
ingested_at
source_file
source_batch
pipeline_run_id
record_hash
source_row_number
```

## Bronze responsibilities

- Preserve source values with minimal transformation.
- Add traceable ingestion metadata.
- Make reruns idempotent.
- Reconcile source and persisted row counts.
- Retain or quarantine unreadable records visibly.

## Required validations

- Source exists and is non-empty.
- Required identifiers are present.
- Batch identity is recorded.
- Reprocessing does not create unintended duplicates.
- Source and target totals reconcile.
- Column-standardization mappings remain traceable.

## Known problem to document

The original development encountered invalid characters in Delta column names. The public implementation should reproduce the general problem using a synthetic schema, implement a deterministic standardization rule, retain an original-to-standardized mapping, and test the convention.

## Status

The conceptual Bronze layer exists from prior development. Public synthetic implementation and sanitized code are the first v0.2 deliverables.
