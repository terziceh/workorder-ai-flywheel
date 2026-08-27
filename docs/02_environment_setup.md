# 02 — Databricks Setup and Source-File Landing

Related issue: [#2 — Load the source data into Databricks and document the setup](https://github.com/terziceh/workorder-flywheel/issues/2)

## Objective

Place the source file in a governed Databricks landing location, verify that it is readable, and document the process without publishing the dataset.

The private implementation can use authorized operational data. Public instructions, screenshots, paths, examples, and downloadable files must remain synthetic, sanitized, or safely generalized.

## Prerequisites

- Access to a Databricks workspace
- Unity Catalog enabled
- Permission to create or use a catalog, schema, and volume
- An approved source file for the private implementation
- A generated sample file for public reproduction
- No secrets stored in notebooks or GitHub

## Landing design

The tutorial uses this generalized structure:

```text
catalog: work_order_ai
schema:  bronze
volume:  raw_files
path:    /Volumes/work_order_ai/bronze/raw_files/
```

A Unity Catalog volume provides a governed location for source files before they are read by the Bronze ingestion notebook. Landing the file separately from table creation preserves the original input and makes ingestion easier to rerun and audit.

## Walkthrough

### 1. Open Catalog Explorer

Open the intended catalog and Bronze schema, then select the `raw_files` volume.

### 2. Upload the source file

Select **Upload to this volume**, choose the approved source file, verify the destination volume, and upload it.

![Databricks dialog for uploading a source file to a Unity Catalog volume](assets/databricks/01-volume-upload-dialog.jpg)

> **Figure 1 — Opening the Unity Catalog upload workflow.** The destination is the `raw_files` volume inside the Bronze schema. At this stage, Databricks stores the source file but has not yet transformed it into a Delta table.

### 3. Confirm the landed file

Open the volume’s **Files** view and verify that the expected file appears.

![Databricks Unity Catalog volume showing the landed work-order source file](assets/databricks/02-source-file-landed.jpg)

> **Figure 2 — Confirming the landed source file.** Databricks displays the uploaded CSV inside the governed `raw_files` volume. The screenshot is cropped to exclude ownership information and other private metadata. The public reproduction uses a synthetic file even when the private implementation uses an authorized operational source.

### 4. Verify readability

Use a small notebook cell to confirm that Databricks can access the landed file. Do not publish a preview of real rows.

```python
source_path = "/Volumes/work_order_ai/bronze/raw_files/synthetic_workorders.csv"

source_df = spark.read.option("header", True).option("inferSchema", False).csv(source_path)

print(source_df.columns)
print(f"Readable source is non-empty: {source_df.limit(1).count() > 0}")
```

The one-row count checks that at least one readable record exists without displaying record values; counting a zero-row limit would always return zero. For the actual ingestion, use the multiline and quote-escape settings in the [Bronze walkthrough](04_bronze_ingestion.md).

The public example deliberately references `synthetic_workorders.csv`. The private notebook successfully read the authorized source and verified that the dataset was non-empty; its record previews and outputs are intentionally excluded from GitHub.

## Evidence checklist

- [x] Catalog, schema, volume, and purpose are explained
- [x] Upload interface is documented
- [x] Landed-file confirmation is documented
- [x] A safe read-verification example is included
- [x] Screenshots contain no real rows or employer identifiers
- [x] The public/private evidence boundary is documented
- [x] The source file itself is not committed

## Problems and resolutions

No blocking file-upload problem occurred. The source landed successfully in the intended Unity Catalog volume and was readable from the private notebook.

The first downstream issue appeared during the attempted Delta write: source column names contained characters that Delta would not accept. That problem belongs to the Bronze ingestion stage and was resolved through column-name standardization in [Issue #3](https://github.com/terziceh/workorder-flywheel/issues/3).

## Output

- The authorized source is accessible in the private Databricks workspace.
- The repository contains a reproducible synthetic companion dataset.
- The public tutorial documents the landing workflow without distributing source records.
- Sanitized screenshots provide evidence of the upload and landed-file verification.

## Status

Issue #2 is complete.

## Next step

The full-refresh Bronze ingestion notebook is complete and documented in the [Bronze walkthrough](04_bronze_ingestion.md). The next active stage is [Issue #4: Profile and validate Bronze](https://github.com/terziceh/workorder-flywheel/issues/4), which will inform the Silver rules.
