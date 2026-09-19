# Participant Setup Guide — V2.2

## Before class — complete these steps in order

### 1. Create a free Databricks account

Open:

`https://login.databricks.com/signup`

Create/sign in to your Databricks account.

### 2. Open the public training repository

`https://github.com/Decoding-Data-Science/enec2026`

### 3. Download the data pack from the GitHub Release

Open:

`https://github.com/Decoding-Data-Science/enec2026/releases/tag/enec-2026-final`

Under **Assets**, download:

`ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

Extract it on your computer. Confirm that you can see:

- `nuclear_enterprise_360_v2_2_clean.db`
- nine A-001 PDF files
- V2.2 README

The `.db` file is the real SQLite training database. It is compressed inside the ZIP because the raw database is approximately 120 MB.

### 4. GitHub account

If you want to clone/fork the repository, create/sign in to GitHub:

`https://github.com/signup?source=login`

## Previous quick links

Repository: `https://github.com/Decoding-Data-Science/enec2026`

Release: `https://github.com/Decoding-Data-Science/enec2026/releases/tag/enec-2026-final`

## Databricks setup

### Step 1 — Open the repository notebooks

Recommended: clone the GitHub repository into a Databricks Git folder.

Start with:

`Day_1_Databricks_Data_ML/notebooks/00_Setup_Nuclear_Enterprise_360.py`

Attach Serverless compute.

### Step 2 — Create the schema and Volume

Run the first setup cell.

Expected structure:

```text
workspace
└── nuclear_enterprise_360
    └── training_files
```

### Step 3 — Upload the V2.2 SQLite database

Extract:

`nuclear_enterprise_360_v2_2_clean.db`

from the companion ZIP.

Upload it to:

```text
/Volumes/workspace/nuclear_enterprise_360/training_files/
```

Expected complete path:

```text
/Volumes/workspace/nuclear_enterprise_360/training_files/nuclear_enterprise_360_v2_2_clean.db
```

Do not try to open the `.db` as a text/notebook file.

### Step 4 — Run the setup

Return to `00_Setup_Nuclear_Enterprise_360.py`.

Run the upload check and then the remaining cells.

The setup imports SQLite tables into managed Delta tables/views.

### Step 5 — Validate

Confirm that A-001 is available:

```sql
SELECT *
FROM workspace.nuclear_enterprise_360.asset_360
WHERE asset_id = 'A-001';
```

Confirm the main forecasting view:

```sql
SELECT COUNT(*)
FROM workspace.nuclear_enterprise_360.a001_sensor_hourly;
```

Expected: **8,760 rows**.

## Day 2 document setup

### Repo-native path

If you cloned the repo into Databricks, the Day 2/3 notebooks first look for:

`Day_2_GenAI_RAG/documents/a001/`

The repository contains readable mirrors of all nine documents.

### Original PDF path

For exercises specifically using PDFs, extract the nine PDFs from the companion ZIP and upload them to:

```text
/Workspace/Nuclear_Enterprise_360/A001 Documents/
```

The corpus deliberately contains APPROVED, DRAFT and SUPERSEDED material.

## Day 3 skill setup

If the repo is cloned into Databricks, the notebook first looks for:

`Day_3_Agentic_AI/skills/`

Fallback manual location:

```text
/Workspace/Nuclear_Enterprise_360/02_Agent_Skills/
```

Files:

- `skills_catalog.md`
- `asset_summary.md`
- `approved_procedure.md`
- `reliability_review.md`

## Troubleshooting

| Symptom | Check |
|---|---|
| Database not found | Exact V2.2 filename and Volume path |
| Tables not visible | Setup notebook completed; refresh Catalog |
| RAG finds no documents | Repo cloned correctly or PDFs uploaded to fallback path |
| Skills not found | Repo path or fallback skills folder |
| Model endpoint error | Databricks workspace entitlement / model availability |
| Draft returned as authority | Check approval-status filtering and prompt/tool logic |

## Minimum successful setup

You are ready when:

- Databricks opens
- repository notebooks are accessible
- V2.2 database is uploaded
- setup notebook runs
- `asset_360` returns A-001
- `a001_sensor_hourly` returns 8,760 rows
- Day 2 documents are discoverable
- Day 3 skill files are discoverable
