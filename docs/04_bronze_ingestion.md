# 04 — Bronze Tables and Ingestion Notebook

Related issues:

- [#3 — Build the Bronze tables and Databricks ingestion notebook](https://github.com/terziceh/workorder-flywheel/issues/3)
- [#4 — Profile and validate the Bronze work-order data](https://github.com/terziceh/workorder-flywheel/issues/4)

## Management summary

The Bronze layer converts the landed CSV into a reliable Delta table without changing the business meaning of the source records. It gives the project one queryable starting point for later data quality, analytics, and machine-learning work while retaining basic ingestion lineage.

| Step | Business value |
|---|---|
| Load | Makes the landed file available to the data platform |
| Standardize names | Prevents Delta errors and simplifies future queries |
| Add lineage | Records when and from which file the data arrived |
| Save as Delta | Creates a queryable copy of the source snapshot |
| Reconcile | Checks that readable source and persisted table row totals match |

## Evidence reviewed

The uploaded private ingestion notebook contains the five steps below and a saved `Bronze ingestion validated.` message after the count assertion. This review inspected the notebook and its saved evidence; it did not execute a new Databricks run or verify a separate rerun test. Public snippets substitute a synthetic filename and omit private counts and outputs.

## Grain and design boundary

One row represents one work-order record as received from the source file. Bronze makes only technical changes; business cleaning, type conversion, text preprocessing, label decisions, and feature engineering are deferred to Silver and Gold.

The notebook uses ordinary Python configuration variables rather than widgets or a reusable ingestion function. It does not establish that a work-order identifier is unique: the business grain and candidate keys remain to be profiled.

## 1. Load the source file

The CSV is read from the Unity Catalog volume while keeping fields as text. This avoids premature type decisions and supports descriptions or notes containing line breaks and quotation marks.

```
source_path = "/Volumes/work_order_ai/bronze/raw_files/synthetic_workorders.csv"
bronze_table = "work_order_ai.bronze.workorders_raw"

raw_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .option("multiLine", True)
    .option("escape", '"')
    .csv(source_path)
)
```

| Option | Why it is used |
|---|---|
| `header=True` | Uses the CSV header as column names |
| `inferSchema=False` | Keeps source columns as strings, avoiding inferred numeric or date conversions |
| `multiLine=True` | Supports line breaks inside quoted CSV fields |
| `escape='"'` | Supports doubled quotation marks inside quoted fields |

These settings support the expected CSV format; they do not prove that every field parsed correctly. No explicit malformed-record capture or quarantine is implemented.

The public example uses `synthetic_workorders.csv`. The private implementation uses the authorized source, which is not committed to GitHub.

## 2. Standardize column names

The source contains column names that are not compatible with the initial Delta write. The helper converts them to lowercase `snake_case` and stops the notebook if two source columns would produce the same cleaned name.

```
import re


def clean_column_name(column_name):
    cleaned_name = column_name.strip().lower()
    cleaned_name = re.sub(r"[^a-z0-9]+", "_", cleaned_name)
    return cleaned_name.strip("_")


cleaned_columns = [clean_column_name(column) for column in raw_df.columns]

if len(cleaned_columns) != len(set(cleaned_columns)):
    raise ValueError("Multiple source columns produced the same cleaned name.")

bronze_df = raw_df.toDF(*cleaned_columns)
```

Example:

```text
Work Order   -> work_order
Phase Desc   -> phase_desc
Date-Created -> date_created
```

### Problem and resolution

**Problem:** The first Delta write rejected source column names containing spaces or unsupported characters.

**Impact:** The source file could be read, but the Bronze table could not be created reliably.

**Root cause:** CSV headers were designed for human-readable exports rather than Delta table identifiers.

**Resolution:** Apply one deterministic naming rule and verify that it does not create duplicate cleaned names.

**Validation:** The standardized DataFrame was written successfully to Delta.

**Remaining limitation:** The first version does not persist a separate mapping table. The transformation is deterministic and documented, and a formal mapping can be added if downstream governance requires it.

## 3. Add ingestion metadata

Two technical fields provide enough lineage for this full-refresh version: when the load occurred and which source file produced the records.

```
from pyspark.sql import functions as F

bronze_df = (
    bronze_df
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.lit("synthetic_workorders.csv"))
)
```

The private notebook uses the actual landed filename. The public snippet uses a fictional filename. `_source_file` is a manually supplied literal, so it must be updated along with `source_path` when changing inputs; it is not automatically extracted from the file. `_ingested_at` records the write-time evaluation of the timestamp expression, not the original work-order creation time.

## 4. Write the Bronze Delta table

The current source is a controlled historical snapshot, so the first version uses overwrite mode. This makes a rerun replace the snapshot instead of silently appending a duplicate copy.

```
(
    bronze_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(bronze_table)
)
```

`overwriteSchema=true` also permits the incoming schema to replace the existing table schema; it is not a schema-validation check. Only run this against the intended full-snapshot target, because overwrite replaces its current contents. A rerun refreshes the ingestion timestamp, so it is not a byte-for-byte identical result.

This choice is intentionally simple. Incremental batch tracking, append behavior, and change-data handling should be added only when recurring source deliveries require them.

## 5. Reconcile source and Bronze counts

The final check compares the readable source count with the persisted Delta count. The assertion stops the notebook if the two totals differ.

```
source_count = raw_df.count()
bronze_count = spark.table(bronze_table).count()

assert source_count == bronze_count, "Source and Bronze record counts do not match."

print("Bronze ingestion validated.")
```

Matching counts do not prove correct CSV parsing, matching field values, unique business keys, or valid labels. The assertion runs after the write and does not roll back the table if it fails. The source should remain unchanged during the read, write, and reconciliation because these are separate Spark actions.

Private totals are not published. The public evidence records that reconciliation passed without exposing operational volume.

## What was delivered

- A readable source file in a governed Unity Catalog volume
- A Bronze Delta table containing the standardized source snapshot
- Basic file and timestamp lineage
- Collision-safe column standardization
- Source-to-Bronze row-count reconciliation
- A documented full-refresh rerun strategy
- Public code examples that contain no source records or credentials

## Current limitations

- The notebook performs a full refresh rather than incremental ingestion.
- Malformed-record quarantine is not implemented in this version.
- Batch identifiers, record hashes, and incremental controls are not implemented; evaluate them if recurring loads require them.
- Empty cleaned names and collisions with reserved metadata fields are not explicitly checked.
- A separate rerun verification is not evidenced by the uploaded notebook.
- Initial missing-value and duplicate profiling is now documented below; label correctness and full-column date conversion remain unvalidated.

These are deliberate scope decisions rather than hidden production claims.

## Definition of done

- [x] Bronze schema and Delta table exist
- [x] Source file is read without business transformations
- [x] Delta-incompatible column names are standardized
- [x] Cleaned-name collisions are checked
- [x] Ingestion timestamp and source filename are added
- [x] Full-refresh rerun behavior is documented
- [x] Source and Bronze counts reconcile
- [x] The resulting table is queryable
- [x] Public snippets contain no real rows, secrets, or private outputs
- [x] Known limitations and next steps are documented

## Next step

Initial Bronze profiling is documented below. Next, implement the first [Silver transformations](05_silver_transformations.md) using those findings, while retaining the unresolved review items.

## Bronze validation and profiling

Related work: [Issue #4](https://github.com/terziceh/workorder-flywheel/issues/4). The private validation notebook was reviewed with its saved outputs; this documentation update did not rerun Databricks.

### What we did

We checked the structure of Bronze, measured missing values, investigated repeated records, inspected creation-date examples, and checked ingestion metadata. The goal was to understand what needs cleaning before Silver without changing the persisted Bronze table.

| Check | What it tells us | What was done |
|---|---|---|
| Structure | Whether the table is readable and how its fields are represented | Nonempty assertion and schema inspection |
| Field names | Which descriptions and shops belong to a work order versus a phase | Explicit mapping with missing-column and collision checks |
| Missing values | Where information is absent | Null, empty-string, and whitespace-only counts and percentages |
| Grain | Whether repeated work-order numbers reflect phase detail | Compared total rows, distinct work orders, distinct work-order/phase pairs, and distinct complete source rows |
| Exact repeats | Which exported records match across every business field | Window-based occurrence counts and a private review output |
| Creation dates | What populated source dates look like | Inspected a limited distinct-value sample |
| Lineage | Whether records retain source and ingestion information | Saved output shows neither lineage field was missing |

### Clarifying field names

The reviewed validation notebook applies this mapping to its in-memory DataFrame:

| Export field | Descriptive name |
|---|---|
| `description1` | `work_order_description` |
| `shop12` | `work_order_shop` |
| `description14` | `phase_description` |
| `shop16` | `phase_shop` |

No Delta write appears in the validation notebook, so the mapping alone does not persist new names in Bronze. Before building Silver, confirm which names the persisted table exposes and choose one place to own the mapping. The existing validation mapping expects the old names and will fail its missing-column check if applied unchanged to an already-renamed table.

### Missing-value check

The notebook profiles business columns separately from ingestion metadata. The core condition is:

```python
missing_value = F.col(column).isNull() | (F.regexp_replace(F.col(column), r"\s+", "") == "")
```

Here, `column` is the source field being profiled and `F` is `pyspark.sql.functions`. The notebook sums this condition for each source column and calculates a percentage; it does not modify the values.

Missingness is concentrated in supplemental fields, so an absent asset or location should not automatically cause the whole record to be discarded. Populated fields still need business validation: a nonblank work code is not proof of a correct label. Counts should be reviewed alongside percentages because rounding can hide small nonzero counts. Text placeholders such as `N/A` are not included in this missing-value rule.

### Grain and duplicate review

A work order can have multiple phases, so a repeated work-order number is not enough to label a row a duplicate. The comparison of distinct complete source records with distinct work-order/phase pairs supports one row per work order and phase as a candidate business grain after exact repeats are removed; the business definition still needs confirmation.

The duplicate check excludes ingestion metadata and counts matching source records:

```python
from pyspark.sql.window import Window

duplicate_window = Window.partitionBy(*source_columns)
duplicate_rows = source_df.withColumn("occurrences", F.count("*").over(duplicate_window)).filter(
    F.col("occurrences") > 1
)
```

This snippet follows the notebook's setup of `source_columns` and `source_df`. It retains every occurrence, including the first, for comparison. Consequently, the number of rows in the review output is larger than the number of excess copies.

The affected records were prepared for private review, including their asset associations. Some may reflect source or export issues, but the cause has not been established. No records were deleted, and automatic deduplication is not approved. The duplicate preview itself contains source fields and occurrence counts, not ingestion metadata; it does not establish which ingestion or export produced the repetition.

The notebook prepares a downloadable review table. Its code does not establish that a CSV was downloaded or saved elsewhere.

### Creation dates and lineage

Creation-date inspection was exploratory: populated values were sampled, not converted across the entire column. Silver still needs a confirmed format and a conversion-failure check. Missing dates will be flagged rather than invented.

The saved lineage result shows no missing source filename or ingestion timestamp under the implemented checks. The filename check covers nulls, empty strings, and ordinary surrounding spaces; it does not separately normalize all whitespace characters. This confirms basic completeness, not the authenticity of the filenames or timestamps.

### What this means for Silver

We now have enough direction for a first Silver implementation:

- Keep identifiers as strings to preserve leading zeros.
- Convert empty and whitespace-only values to null.
- Trim surrounding whitespace without changing descriptive wording.
- Parse creation dates with a confirmed format and flag failures.
- Keep optional fields nullable instead of dropping otherwise useful records.
- Retain and flag repeated records until their review is complete.
- Preserve ingestion metadata.
- Reconcile row counts and report quality flags after transformation.

These are proposed transformation rules, not completed Silver behavior. The initial profiling is not certification that every field or label is correct. Full-column date conversion, code-reference checks, deeper relationship checks, and recurring-file processing remain outside the completed work.

### Public evidence boundary

The uploaded notebook contains real row previews, date values, counts, and operational outputs. It and the duplicate-review CSV are not published. This chapter shares generalized methods and findings without publishing private records, exact operational counts, or percentages.
