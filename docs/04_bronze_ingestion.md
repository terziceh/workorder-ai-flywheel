# 04 — Bronze Tables and Ingestion Notebook

Related issues:

- [#3 — Build the Bronze tables and Databricks ingestion notebook](https://github.com/terziceh/workorder-ai-flywheel/issues/3)
- [#4 — Profile and validate the Bronze work-order data](https://github.com/terziceh/workorder-ai-flywheel/issues/4)

## Objective

Create a parameterized Databricks notebook that reads the landed source file, preserves the received values, adds traceability metadata, and writes a queryable Bronze Delta table.

## Grain

One row represents one source work-order phase as received in one ingestion batch.

## Separation of responsibilities

| Landing volume | Bronze Delta table |
|---|---|
| Preserves the original source file | Makes source records queryable |
| Stores files before ingestion | Adds ingestion metadata |
| Supports replay and audit | Supports reconciliation and downstream reads |
| Does not apply business rules | Performs only technical standardization |

Business cleaning, label decisions, and text preprocessing belong in Silver or later layers.

## Notebook requirements

The Bronze notebook should:

1. Accept the source path, catalog, schema, target table, and batch identifier as configuration.
2. Read the landed file with explicit parsing options.
3. Preserve source values without business-rule transformations.
4. Standardize column names only where Delta requires it.
5. Retain an original-to-standardized column mapping.
6. Add ingestion metadata.
7. Write to a Delta table.
8. detect an already-processed batch before appending.
9. Reconcile source, accepted, rejected, and persisted counts.
10. Return a concise validation summary.

## Ingestion metadata

```text
ingested_at
source_file
source_batch
pipeline_run_id
record_hash
source_row_number
```

## Minimum validation

- Source exists and is non-empty.
- Expected columns are present.
- Required identifiers are observable.
- Ingestion metadata is populated.
- Source counts reconcile to accepted and rejected records.
- A completed batch cannot be silently duplicated.
- Empty, malformed, and schema-changed input produces actionable output.
- The Bronze table is queryable after the write.

## Known implementation problem

Delta rejects certain characters in column names. The tutorial will reproduce the general failure with a synthetic schema, implement a deterministic naming function, retain the mapping between original and standardized names, and verify the convention with tests.

Document this and later problems using:

> **Problem → Impact → Root cause → Options → Resolution → Validation → Remaining limitation**

## Public evidence

The repository may include:

- Parameterized notebook source without secrets
- Synthetic source-to-target examples
- Sanitized screenshots of notebook execution and table validation
- Synthetic reconciliation totals
- Unit and integration tests
- Generalized errors and resolutions

The repository must not include the private source file, real records, employer identifiers, internal storage details, secrets, or unauthorized production metrics.

## Definition of done

- [ ] Bronze schema and Delta table exist
- [ ] Parameterized notebook runs successfully
- [ ] Ingestion metadata is populated
- [ ] Counts reconcile
- [ ] Rerun behavior is verified
- [ ] Column-name handling is tested
- [ ] Safe screenshots and explanations are added
- [ ] Bronze validation report is complete
- [ ] Output is approved for the Silver pipeline

## Next step

Build the Silver cleaning and data-quality pipeline in [Issue #5](https://github.com/terziceh/workorder-ai-flywheel/issues/5).
