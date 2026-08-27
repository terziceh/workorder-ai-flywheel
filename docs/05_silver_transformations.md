# 05 — Silver Transformations

## Objective

Clean and organize the Bronze records using the rules supported by our profiling, without hiding data-quality problems.

## Current status

Initial Bronze profiling has been reviewed and documented in the [Bronze validation walkthrough](04_bronze_ingestion.md#bronze-validation-and-profiling). Silver is the next implementation step; the rules below are planned, not implemented.

Related issue: [#5 — Build the Silver pipeline](https://github.com/terziceh/workorder-flywheel/issues/5).

## What Bronze profiling taught us

- Missing values are concentrated in supplemental fields. Missing optional information should not automatically disqualify a record.
- Repeated work-order numbers can represent multiple phases.
- Exact source repeats need review before any deletion; their origin is unconfirmed.
- Work order plus phase is a candidate key, but duplicates remain and the business meaning still needs confirmation.
- Date examples were inspected, but full-column date conversion has not been validated.
- The saved ingestion-lineage completeness checks passed.
- Descriptive field renaming exists in the validation DataFrame; the persisted schema must be checked before deciding where the mapping belongs.

## First Silver version

| Area | Planned rule | Validation |
|---|---|---|
| Identifiers | Keep as strings; preserve leading zeros | Check required identifiers and review normalization effects |
| Missing values | Convert empty and whitespace-only values to null | Report missing counts; do not assume every field is mandatory |
| Descriptions | Trim surrounding whitespace and preserve wording | Retain original values where needed for comparison |
| Creation date | Parse the confirmed source format | Flag missing values and nonblank values that fail conversion |
| Optional fields | Keep nullable | Do not drop otherwise useful rows for missing optional values |
| Repeated records | Retain and flag pending review | Do not enforce work-order/phase uniqueness while repeats remain |
| Lineage | Preserve source filename and ingestion timestamp | Check completeness in Silver |
| Row counts | Preserve records in the initial version | Reconcile Bronze and Silver totals and investigate differences |

No blanket case conversion, placeholder replacement, source-label correction, or duplicate removal is approved yet. Date format and any timezone assumptions must be confirmed before conversion.

## Output and scope

Start with one cleaned work-order/phase table carrying quality flags. The initial implementation will process the current snapshot; file discovery, incremental ingestion, and batch tracking are deferred.

Earlier architecture ideas included separate text, work-code reference, and quality-issue tables:

```text
silver_workorder_phase
silver_workorder_text
silver_work_code_reference
silver_workorder_quality_issue
```

These remain possible later outputs, not a requirement to build four tables now.

## Before implementation

1. Confirm the persisted Bronze column names and own the descriptive mapping in one place.
2. Confirm the creation-date format and how failed conversions will be flagged.
3. Agree on the quality-flag names and required fields.
4. Implement the simple rules against the current snapshot.
5. Reconcile counts and inspect the flags before writing the final output.

## Deferred work

- Automatic duplicate removal, pending review.
- Approved code-reference and deeper relationship checks.
- Incremental loads and recurring-file orchestration.
- Separate reference and exception tables unless the first version needs them.
- Gold datasets and model-specific text preprocessing.

## Privacy

Operational records and review exports remain private. Public examples use synthetic or generalized data; a passing public CI run does not validate the private Databricks dataset.
