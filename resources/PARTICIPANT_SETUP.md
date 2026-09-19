# Participant Setup

## What you need

- ENEC/suitable laptop
- reliable internet access
- modern web browser
- access to public GitHub
- access to Databricks
- permission to download the training files from this repository

No specialist local software is required for the core exercises.

## Create accounts before the programme

Databricks:
https://login.databricks.com/signup

GitHub:
https://github.com/signup?source=login

## Databricks target structure

The instructor will guide the exact setup, but the expected environment is:

```text
Catalog: workspace
Schema: nuclear_enterprise_360
Volume: training_files
```

Expected file path:

```text
/Volumes/workspace/nuclear_enterprise_360/training_files/nuclear_enterprise_360_v2_2_clean.db
```

## One-time setup journey

```text
Download package
   ↓
Extract SQLite DB
   ↓
Open Databricks
   ↓
Create/confirm schema + Volume
   ↓
Upload DB to Volume
   ↓
Import setup notebook
   ↓
Convert SQLite tables to Delta
   ↓
Validate key tables/views
   ↓
Start Day 1 exercises
```

## Before class

Confirm you can:
- sign in to GitHub
- open this repository
- sign in to Databricks
- create/open a notebook
- access the instructor-provided compute/serverless environment
- download the training package

## Important

All A-001 data and documents are synthetic training material.
