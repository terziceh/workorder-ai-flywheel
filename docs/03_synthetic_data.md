# 03 — Public Synthetic Companion Data

## Objective

Provide a small, reproducible dataset that lets readers run the public tutorial without distributing the private source dataset.

The synthetic data is a teaching and testing companion. It does not claim to reproduce the employer’s records, taxonomy, volumes, distributions, or operational results.

## Grain

One row represents one fictional work-order phase in one generated source batch.

## Current implementation

`src/workorder_ai/synthetic.py` generates fictional facilities, assets, descriptions, priorities, crafts, and labels. A fixed seed makes tests and tutorial examples reproducible.

## Public uses

- Demonstrate the Databricks file-landing workflow
- Exercise Bronze ingestion and rerun behavior
- Show Silver cleaning and quality flags
- Validate Gold dataset contracts
- Provide runnable model examples
- Populate screenshots without exposing real rows

## Required safeguards

- No employer records or copied descriptions
- No internal work-code mappings
- No real facilities, assets, employees, or locations
- No attempt to reproduce confidential distributions exactly
- Synthetic metrics labeled as demonstration results
- Private results published only when explicitly authorized and sufficiently aggregated

## Validation

- Identifiers are unique within a generated batch.
- Descriptions are non-empty.
- Labels belong to the fictional public taxonomy.
- The same seed produces the same output.
- Synthetic rows contain no known employer identifiers.

## Current scope

The public generator is sufficient for repository tests and small examples. It should be expanded only when a downstream engineering or model test requires a specific scenario; synthetic-data expansion is not a standalone milestone.

## Next step

Use a generated sample to reproduce the Bronze ingestion process documented in [the Bronze chapter](04_bronze_ingestion.md).
