# Data — Nuclear Enterprise 360 V2.2

## Primary training dataset

Use **Nuclear Enterprise 360 — V2.2 Clean Beginner Version** for the final ENEC 2026 delivery.

Created: **16 September 2026**

## Companion package

The final participant download is:

`ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

It is distributed as a GitHub Release asset rather than committed as a normal repository file.

The companion archive contains:
- `nuclear_enterprise_360_v2_2_clean.db`
- the nine A-001 PDF evidence documents
- the V2.2 README

The raw SQLite database is approximately **120 MB**, which is larger than GitHub's normal 100 MB single-file limit, so the repository stores the compressed training package instead.

After extraction, upload the `.db` file to:

```text
/Volumes/workspace/nuclear_enterprise_360/training_files/
```

## Beginner forecasting flow

V2.2 deliberately removes confusing duplicate forecasting views.

Use:

1. `sensor_readings_a001_1min` — 525,600 raw one-minute readings
2. `a001_sensor_hourly` — 8,760 hourly rows for teaching/ML
3. target — `avg_vibration_mm_s`
4. forecast — next 7 days / 168 hours

Removed from the beginner V2.2 flow:
- `a001_forecasting_1min`
- `a001_forecasting_series`
- `a001_sensor_daily`

## A-001 context views to keep

- `a001_sensor_hourly`
- `a001_event_timeline`
- `a001_project_risk_360`
- `a001_document_evidence`
- `asset_project_map`
- `asset_project_risk_map`
- `asset_360`

## Document corpus

Exactly nine synthetic evidence PDFs are registered in:
- `a001_source_documents`
- `a001_source_document_links`
- `a001_document_evidence`

## Important evidence rule

The uploaded work-order PDF `WO-2026-0817` does **not** provide an estimated-hours value. V2.2 does not invent one merely to satisfy a structured schema.

## Useful files

- `DATA_DICTIONARY.md` — generated schema + row counts
- `A001_QUICKSTART.sql` — starter queries
- `verify_v2_2.py` — integrity and expected-count checks
- `Nuclear_Enterprise_360_V2_2_README.txt` — original V2.2 release note
- `SHA256SUMS.txt` — checksums for companion ZIPs and original A-001 PDFs


See [`resources/BINARY_ASSETS.md`](../resources/BINARY_ASSETS.md) for binary distribution details.\n