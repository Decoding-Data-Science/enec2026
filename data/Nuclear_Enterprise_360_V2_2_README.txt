Nuclear Enterprise 360 - V2.2 Clean Beginner Version
Created: 2026-09-16

MAIN A-001 FORECASTING FLOW
1. Raw data: sensor_readings_a001_1min (525,600 rows)
2. Teaching/ML view: a001_sensor_hourly (8,760 hourly rows)
3. Recommended target: avg_vibration_mm_s
4. Recommended forecast: next 7 days / 168 hours

REMOVED AS CONFUSING
- a001_forecasting_1min
- a001_forecasting_series
- a001_sensor_daily

KEEP FOR A-001 STORY
- a001_sensor_hourly
- a001_event_timeline
- a001_project_risk_360
- a001_document_evidence
- asset_project_map
- asset_project_risk_map

A-001 DOCUMENT CORPUS
Exactly 9 uploaded PDFs are registered in:
- a001_source_documents
- a001_source_document_links
- a001_document_evidence

IMPORTANT DATA-EVIDENCE RULE
The uploaded work-order PDF WO-2026-0817 does not provide an estimated-hours value.
The original structured work_orders table requires estimated_hours, so V2.2 does NOT invent
that number. The work order remains verified document evidence instead.

SQLite integrity check: ok