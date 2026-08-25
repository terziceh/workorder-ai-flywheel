# Synthetic Work-Order Data Contract

## Grain

One row represents one synthetic work-order phase. Version 0.1 generates one phase for each work order; later versions may add multiple phases without changing the phase-level grain.

## Required fields

| Field | Type | Nullable | Meaning |
|---|---|---:|---|
| `workorder_id` | string | No | Synthetic parent work-order identifier |
| `phase_id` | string | No | Unique phase identifier |
| `created_at` | timestamp string | No | UTC creation timestamp |
| `facility_name` | string | No | Fictional facility name |
| `location_code` | string | No | Fictional room/location identifier |
| `asset_id` | string | Yes | Fictional asset identifier |
| `asset_type` | string | No | General asset category |
| `craft` | string | No | Responsible maintenance craft |
| `priority` | string | No | Service priority |
| `description` | string | No | Independently generated request text |
| `historical_work_code` | string | No | Synthetic historical label, occasionally corrupted |
| `source_batch` | string | No | Synthetic source-batch identifier |

## Initial quality rules

- `phase_id` is unique and non-null.
- Descriptions are non-empty.
- Work codes belong to the public synthetic taxonomy.
- Missing `asset_id` values are permitted and intentionally generated.
- Conflicting labels are retained for later label-quality analysis.
