# ENEC 2026 Training Materials — Final

This release contains the companion resources for the **AI for Coders & Software Engineers** corporate training programme.

## Participant Data Pack

Download:

`ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

It contains:

- Nuclear Enterprise 360 V2.2 synthetic SQLite training database
- A-001 one-minute and hourly sensor datasets
- Enterprise asset, work-order, inspection, maintenance, project and risk data
- Nine original A-001 enterprise PDF documents used for RAG exercises
- Approved, draft and superseded procedure examples
- V2.2 dataset release notes

## How to Get the Data into Databricks

### Step 1 — Create a free Databricks account

Go to:

https://login.databricks.com/signup

Create/sign in to your Databricks account.

### Step 2 — Download the training data

On this Release page, under **Assets**, download:

`ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

### Step 3 — Extract the ZIP

After extraction, confirm you can see:

`nuclear_enterprise_360_v2_2_clean.db`

This is the actual SQLite training database.

You will also see the nine original A-001 PDF documents used in the RAG exercises.

### Step 4 — Open the training repository

https://github.com/Decoding-Data-Science/enec2026

Start with:

`START_HERE.md`

### Step 5 — Open Databricks and run the setup notebook

Open/import:

`Day_1_Databricks_Data_ML/notebooks/00_Setup_Nuclear_Enterprise_360.py`

Attach Serverless compute and run the first setup cell.

The notebook creates:

- schema: `nuclear_enterprise_360`
- Volume: `training_files`

### Step 6 — Upload the SQLite database

In Databricks choose:

**New → Add or upload data → Upload files to a volume**

Upload:

`nuclear_enterprise_360_v2_2_clean.db`

to:

`/Volumes/workspace/nuclear_enterprise_360/training_files/`

Expected full path:

`/Volumes/workspace/nuclear_enterprise_360/training_files/nuclear_enterprise_360_v2_2_clean.db`

### Step 7 — Complete the setup

Return to `00_Setup_Nuclear_Enterprise_360.py`.

Run the upload-check cell and then the remaining cells.

The setup notebook converts the SQLite database into managed Databricks Delta tables/views.

### Step 8 — Verify

Run:

```sql
SELECT *
FROM workspace.nuclear_enterprise_360.asset_360
WHERE asset_id = 'A-001';
```

Then:

```sql
SELECT COUNT(*)
FROM workspace.nuclear_enterprise_360.a001_sensor_hourly;
```

Expected result: **8,760 rows**.

## Trainer / Reference Pack

`ENEC_2026_Slides_and_Trainer_Materials.zip`

Contains slide decks, setup guides and trainer reference materials.

## Important

All datasets, assets, documents, procedures and observations are synthetic and provided for training purposes only.
