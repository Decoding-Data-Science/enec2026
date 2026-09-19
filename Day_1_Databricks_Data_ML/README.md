# Day 1 — Databricks Foundations, Enterprise Data & Machine Learning

## Goal

Set up the Databricks environment, understand the synthetic enterprise database and supporting document set, and take historical A-001 sensor data through to a simple predictive workflow.

## First half — Databricks setup & enterprise data foundations

Cover:
- Databricks workspace navigation
- notebooks and compute
- catalogs, schemas, tables and files/Volumes
- import of training notebooks
- loading the SQLite training database
- conversion to managed Delta tables
- key table relationships
- SQL and Python exploration
- filtering and aggregation
- supporting policies, procedures and reports
- environment validation and troubleshooting

### Core notebooks

Run in this order:

1. `notebooks/00_Setup_Nuclear_Enterprise_360.py`
2. `notebooks/01_SQL_and_Delta_Foundations.py`
3. `notebooks/A001_Forecasting_Databricks_Notebook.py`

The `.ipynb` version of the forecasting notebook is also provided.

## Second half — enterprise data to simple prediction

Use A-001 vibration as the teaching target.

Recommended dataset:
- `a001_sensor_hourly`
- 8,760 hourly observations
- target: `avg_vibration_mm_s`
- forecast horizon: 168 hours / 7 days

Teaching sequence:

```text
Raw sensor data
  ↓
Aggregate to hourly
  ↓
Data quality checks
  ↓
Visualise
  ↓
Create baseline / features
  ↓
Train
  ↓
Evaluate
  ↓
Forecast
  ↓
Interpret with business context
```

## Optional Day 1 extensions

These are intentionally optional. Use them only if the group is comfortable and time permits:
- `A001_Multivariate_Forecasting_Beginner.*`
- `A001_Beginner_Anomaly_Detection_Databricks.*`

Do not let the optional notebooks distract from the core outcome.

## Key teaching question

**Is a prediction enough to make a maintenance decision?**

No. A prediction is analytical evidence. It does not automatically include the current approved procedure, recent field observations, work-order context or enterprise escalation rules. That gap sets up Day 2.

## End-of-day outcome

Participants should leave with:
- a working Databricks environment
- familiarity with the enterprise database
- confidence using basic SQL/Python exploration
- a working A-001 prediction/forecasting notebook
- a clear understanding that data predictions need organisational context

## Instructor cue

Keep returning to:

> Data tells us what happened. ML helps estimate what may happen next. Neither one by itself tells us what the organisation currently authorises or expects.
