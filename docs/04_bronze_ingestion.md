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
| Save as Delta | Creates a governed, queryable source-of-truth table |
| Reconcile | Confirms that the load did not unexpectedly lose or add records |

## Grain and design boundary

One row represents one work-order record as received from the source file. Bronze makes only technical changes; business cleaning, type conversion, text preprocessing, label decisions, and feature engineering are deferred to Silver and Gold.

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

The private notebook uses the actual landed filename. The public snippet uses a fictional filename.

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

This choice is intentionally simple. Incremental batch tracking, append behavior, and change-data handling should be added only when recurring source deliveries require them.

## 5. Reconcile source and Bronze counts

The final check compares the readable source count with the persisted Delta count. The assertion stops the notebook if the two totals differ.

```
source_count = raw_df.count()
bronze_count = spark.table(bronze_table).count()

assert source_count == bronze_count, "Source and Bronze record counts do not match."

print("Bronze ingestion validated.")
```

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
- Batch identifiers and record hashes will be introduced when recurring loads require them.
- Detailed null, uniqueness, and label-quality analysis belongs to Bronze profiling and Silver.

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

Profile and validate the Bronze data in [Issue #4](https://github.com/terziceh/workorder-flywheel/issues/4) before building Silver.
