# Databricks notebook source
# MAGIC %md
# MAGIC # A-001 Golden Story: Sensor Forecasting + Enterprise Context
# MAGIC 
# MAGIC **Training goal:** use one asset, **A-001 / Pump 001**, to teach a simple end-to-end journey:
# MAGIC 
# MAGIC **Raw sensor data → aggregation → data quality → visualization → time-series baseline → simple forecasting → business events → project/risk context**
# MAGIC 
# MAGIC ### Recommended forecasting dataset
# MAGIC Use **`a001_sensor_hourly`** for the main class.
# MAGIC 
# MAGIC - 8,760 hourly observations
# MAGIC - approximately one full year
# MAGIC - derived from the one-minute sensor table
# MAGIC - small enough for a live class
# MAGIC - detailed enough to retain hourly patterns
# MAGIC - good for a **7-day / 168-hour forecast**
# MAGIC 
# MAGIC Use **`a001_sensor_daily`** only for a very simple introductory example or a longer-horizon trend exercise.
# MAGIC 
# MAGIC Do **not** start the class with the 525,600-row one-minute view. Keep it for explaining raw IoT data and aggregation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## What the A-001 views mean
# MAGIC 
# MAGIC | View | Purpose | Recommended use |
# MAGIC |---|---|---|
# MAGIC | `a001_forecasting_1min` | One-minute raw A-001 sensor series | Explain raw IoT/high-frequency data |
# MAGIC | `a001_sensor_hourly` | Hourly aggregation of the one-minute series | **Main forecasting dataset** |
# MAGIC | `a001_sensor_daily` | Daily aggregation | Beginner trend / simple 30-day exercise |
# MAGIC | `a001_forecasting_series` | Earlier 6-hour compatibility series | Keep for history; not the main V2.1 model |
# MAGIC | `a001_event_timeline` | Work orders, inspections, maintenance, documents, project starts | Explain *why* the sensor pattern matters |
# MAGIC | `a001_project_risk_360` | Linked projects and risks for A-001 | Connect ML to enterprise risk/project decisions |
# MAGIC | `a001_document_evidence` | Structured links to unstructured evidence files | Connect SQL data to RAG/document evidence |
# MAGIC 
# MAGIC The notebook deliberately separates **forecasting data** from **business context**. The machine-learning model predicts a sensor metric; the timeline, project, risk and document views explain how that prediction can support a decision.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Connect to the SQLite database
# MAGIC 
# MAGIC Change only `DB_PATH` if your file is stored somewhere else in Databricks.

# COMMAND ----------

import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DB_PATH = "/Volumes/workspace/nuclear_enterprise_360/training_files/nuclear_enterprise_360_v2_2_clean.db"

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(
        f"Database not found at {DB_PATH}. "
        "Upload nuclear_enterprise_360_v2_2_clean.db and update DB_PATH in this cell."
    )

conn = sqlite3.connect(DB_PATH)
print("Connected to:", DB_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Confirm the A-001 training views

# COMMAND ----------

views = pd.read_sql_query(
    '''
    SELECT name
    FROM sqlite_master
    WHERE type = 'view'
      AND name LIKE 'a001_%'
    ORDER BY name
    ''',
    conn
)
views

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Compare the available forecasting granularities
# MAGIC 
# MAGIC This cell makes the choice visible to students:
# MAGIC 
# MAGIC - **1-minute:** 525,600 rows — realistic raw sensor stream, but unnecessarily large for a first forecast.
# MAGIC - **Hourly:** 8,760 rows — recommended.
# MAGIC - **Daily:** about 366 rows — easiest, but removes intraday behavior.

# COMMAND ----------

summary = pd.read_sql_query(
    '''
    SELECT '1-minute' AS granularity,
           COUNT(*) AS rows,
           MIN(reading_timestamp) AS start_time,
           MAX(reading_timestamp) AS end_time
    FROM a001_forecasting_1min

    UNION ALL

    SELECT 'hourly',
           COUNT(*),
           MIN(hour_timestamp),
           MAX(hour_timestamp)
    FROM a001_sensor_hourly

    UNION ALL

    SELECT 'daily',
           COUNT(*),
           MIN(reading_date),
           MAX(reading_date)
    FROM a001_sensor_daily
    ''',
    conn
)
summary

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Load the hourly series
# MAGIC 
# MAGIC For the class, forecast **average vibration (`avg_vibration_mm_s`)**.
# MAGIC 
# MAGIC Why vibration?
# MAGIC 
# MAGIC - It already plays a role in A-001's operational story.
# MAGIC - It is easy to visualize.
# MAGIC - Rising vibration is intuitive to explain as a possible degradation signal.
# MAGIC - It lets us connect the model back to inspections, work orders and risk.
# MAGIC 
# MAGIC The other sensor variables remain available for exploratory or multivariate analysis.

# COMMAND ----------

hourly = pd.read_sql_query(
    "SELECT * FROM a001_sensor_hourly ORDER BY hour_timestamp",
    conn
)

hourly["hour_timestamp"] = pd.to_datetime(hourly["hour_timestamp"])
hourly = hourly.sort_values("hour_timestamp").reset_index(drop=True)

print("Rows:", len(hourly))
print("Start:", hourly["hour_timestamp"].min())
print("End:", hourly["hour_timestamp"].max())
hourly.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Basic data-quality checks
# MAGIC 
# MAGIC A time-series model needs a regular timeline. For this view we expect exactly **60 one-minute readings per hour** and no missing target values.

# COMMAND ----------

quality_check = {
    "rows": len(hourly),
    "duplicate_timestamps": int(hourly["hour_timestamp"].duplicated().sum()),
    "missing_vibration": int(hourly["avg_vibration_mm_s"].isna().sum()),
    "hours_not_having_60_minutes": int((hourly["minute_readings"] != 60).sum()),
}

quality_check

# COMMAND ----------

expected = pd.date_range(
    hourly["hour_timestamp"].min(),
    hourly["hour_timestamp"].max(),
    freq="h"
)

missing_hours = expected.difference(hourly["hour_timestamp"])
print("Missing hourly timestamps:", len(missing_hours))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Visualize the full-year vibration trend

# COMMAND ----------

plt.figure(figsize=(14, 5))
plt.plot(hourly["hour_timestamp"], hourly["avg_vibration_mm_s"])
plt.title("A-001 — Hourly Average Vibration")
plt.xlabel("Time")
plt.ylabel("Vibration (mm/s)")
plt.grid(alpha=0.25)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Optional: show several sensor variables
# MAGIC 
# MAGIC This is useful when introducing **multivariate** thinking. We are not yet claiming that one variable causes another; we are simply exploring how they move together.

# COMMAND ----------

sensor_cols = [
    "avg_vibration_mm_s",
    "avg_temperature_c",
    "avg_pressure_bar",
    "avg_flow_rate_m3_h",
    "avg_electrical_current_a",
    "avg_ambient_temperature_c",
]

hourly[sensor_cols].corr().round(2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Bring in the business timeline
# MAGIC 
# MAGIC A forecast is more useful when students can connect it to actual operational events.
# MAGIC 
# MAGIC This view combines project starts, work orders, inspections, maintenance and documents related to A-001.

# COMMAND ----------

timeline = pd.read_sql_query(
    "SELECT * FROM a001_event_timeline ORDER BY event_date",
    conn
)
timeline["event_date"] = pd.to_datetime(timeline["event_date"])
timeline.tail(15)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Avoid data leakage
# MAGIC 
# MAGIC The sensor series ends at a defined cutoff. Any business event dated **after** that cutoff must not be used as a training feature for a model that is pretending to forecast from the cutoff date.
# MAGIC 
# MAGIC We therefore split the timeline into historical context and post-cutoff events. The post-cutoff records can be discussed later as operational follow-up, but they are not inputs to the forecasting model.

# COMMAND ----------

sensor_cutoff = hourly["hour_timestamp"].max()

historical_timeline = timeline[
    timeline["event_date"] <= sensor_cutoff
].copy()

post_cutoff_events = timeline[
    timeline["event_date"] > sensor_cutoff
].copy()

print("Sensor cutoff:", sensor_cutoff)
print("Historical events available at forecast time:", len(historical_timeline))
print("Post-cutoff events excluded from model inputs:", len(post_cutoff_events))

post_cutoff_events

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Train/test split
# MAGIC 
# MAGIC We hold out the **last 7 days = 168 hours**.
# MAGIC 
# MAGIC This is important: we evaluate the method on data the model did not see during training.

# COMMAND ----------

target = (
    hourly[["hour_timestamp", "avg_vibration_mm_s"]]
    .set_index("hour_timestamp")["avg_vibration_mm_s"]
    .asfreq("h")
)

FORECAST_HOURS = 24 * 7

train = target.iloc[:-FORECAST_HOURS]
test = target.iloc[-FORECAST_HOURS:]

print("Training observations:", len(train))
print("Test observations:", len(test))
print("Test period:", test.index.min(), "to", test.index.max())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Baseline: seasonal-naive forecast
# MAGIC 
# MAGIC Always start with a baseline.
# MAGIC 
# MAGIC For each future hour, this baseline simply uses the vibration measured at the **same hour one day earlier**. A more sophisticated model should beat this simple rule.

# COMMAND ----------

from sklearn.metrics import mean_absolute_error, mean_squared_error

last_24 = train.iloc[-24:].to_numpy()
seasonal_naive = np.tile(last_24, int(np.ceil(FORECAST_HOURS / 24)))[:FORECAST_HOURS]

naive_mae = mean_absolute_error(test, seasonal_naive)
naive_rmse = np.sqrt(mean_squared_error(test, seasonal_naive))

print(f"Seasonal-naive MAE : {naive_mae:.4f}")
print(f"Seasonal-naive RMSE: {naive_rmse:.4f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Simple time-series model: Holt-Winters
# MAGIC 
# MAGIC Holt-Winters is a good teaching model because it explicitly models:
# MAGIC 
# MAGIC 1. **Level** — the current typical value
# MAGIC 2. **Trend** — whether the series is generally increasing/decreasing
# MAGIC 3. **Seasonality** — recurring patterns
# MAGIC 
# MAGIC For hourly data we use a **24-hour seasonal period**.

# COMMAND ----------

# If statsmodels is not available on your cluster, run:
# %pip install statsmodels

from statsmodels.tsa.holtwinters import ExponentialSmoothing

hw_model = ExponentialSmoothing(
    train,
    trend="add",
    damped_trend=True,
    seasonal="add",
    seasonal_periods=24,
    initialization_method="estimated",
)

hw_fit = hw_model.fit(optimized=True, use_brute=False)
hw_test_forecast = hw_fit.forecast(FORECAST_HOURS)

hw_mae = mean_absolute_error(test, hw_test_forecast)
hw_rmse = np.sqrt(mean_squared_error(test, hw_test_forecast))

comparison = pd.DataFrame({
    "model": ["Seasonal Naive", "Holt-Winters"],
    "MAE": [naive_mae, hw_mae],
    "RMSE": [naive_rmse, hw_rmse],
})

comparison

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Visualize the backtest

# COMMAND ----------

plt.figure(figsize=(14, 5))

history_window = train.iloc[-24 * 7:]

plt.plot(history_window.index, history_window.values, label="Training history")
plt.plot(test.index, test.values, label="Actual")
plt.plot(test.index, hw_test_forecast.values, label="Holt-Winters forecast")

plt.title("A-001 Vibration — 7-Day Backtest")
plt.xlabel("Time")
plt.ylabel("Average vibration (mm/s)")
plt.legend()
plt.grid(alpha=0.25)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12. Forecast the next 7 days
# MAGIC 
# MAGIC After validating the method, retrain on **all available hourly observations** and forecast the next 168 hours.
# MAGIC 
# MAGIC These future values are model estimates, not actual observed sensor readings.

# COMMAND ----------

final_model = ExponentialSmoothing(
    target,
    trend="add",
    damped_trend=True,
    seasonal="add",
    seasonal_periods=24,
    initialization_method="estimated",
)

final_fit = final_model.fit(optimized=True, use_brute=False)
future_forecast = final_fit.forecast(FORECAST_HOURS)

future_df = pd.DataFrame({
    "forecast_timestamp": future_forecast.index,
    "forecast_vibration_mm_s": future_forecast.values,
})

future_df.head(10)

# COMMAND ----------

plt.figure(figsize=(14, 5))

recent = target.iloc[-24 * 14:]

plt.plot(recent.index, recent.values, label="Last 14 days actual")
plt.plot(
    future_df["forecast_timestamp"],
    future_df["forecast_vibration_mm_s"],
    label="Next 7 days forecast"
)

plt.title("A-001 — Next 7 Days Vibration Forecast")
plt.xlabel("Time")
plt.ylabel("Average vibration (mm/s)")
plt.legend()
plt.grid(alpha=0.25)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 13. Optional multivariate teaching example
# MAGIC 
# MAGIC A common question is:
# MAGIC 
# MAGIC > Can temperature, pressure, flow and electrical current help predict vibration?
# MAGIC 
# MAGIC Yes, but there is an important forecasting principle:
# MAGIC 
# MAGIC **For a true future forecast, future values of those explanatory variables must also be known or forecast.**
# MAGIC 
# MAGIC So this section uses the other sensor variables for a **historical one-hour-ahead backtest**, where their values are available. It is a useful introduction to multivariate ML, but it should not be presented as a seven-day future forecast unless the future input variables are also modeled.

# COMMAND ----------

from sklearn.linear_model import LinearRegression

ml = hourly.copy()

# Lagged vibration features: information that would already be known.
ml["vibration_lag_1h"] = ml["avg_vibration_mm_s"].shift(1)
ml["vibration_lag_24h"] = ml["avg_vibration_mm_s"].shift(24)

# Predict the NEXT hour's vibration.
ml["target_next_hour"] = ml["avg_vibration_mm_s"].shift(-1)

feature_cols = [
    "vibration_lag_1h",
    "vibration_lag_24h",
    "avg_temperature_c",
    "avg_pressure_bar",
    "avg_flow_rate_m3_h",
    "avg_electrical_current_a",
    "avg_ambient_temperature_c",
]

ml = ml.dropna(subset=feature_cols + ["target_next_hour"]).copy()

split = len(ml) - (24 * 7)

X_train = ml.iloc[:split][feature_cols]
y_train = ml.iloc[:split]["target_next_hour"]

X_test = ml.iloc[split:][feature_cols]
y_test = ml.iloc[split:]["target_next_hour"]

lr = LinearRegression()
lr.fit(X_train, y_train)

ml_pred = lr.predict(X_test)

print("Multivariate one-hour-ahead MAE:",
      round(mean_absolute_error(y_test, ml_pred), 4))
print("Multivariate one-hour-ahead RMSE:",
      round(np.sqrt(mean_squared_error(y_test, ml_pred)), 4))

# COMMAND ----------

importance = pd.DataFrame({
    "feature": feature_cols,
    "coefficient": lr.coef_,
}).sort_values("coefficient", key=np.abs, ascending=False)

importance

# COMMAND ----------

# MAGIC %md
# MAGIC ## 14. Connect the forecast back to projects and risks

# COMMAND ----------

project_risk = pd.read_sql_query(
    '''
    SELECT *
    FROM a001_project_risk_360
    ORDER BY project_id, risk_id
    ''',
    conn
)

project_risk[[
    "asset_id",
    "project_id",
    "project_name",
    "project_status",
    "risk_id",
    "risk_category",
    "probability",
    "impact",
    "exposure_score",
    "evidence_basis"
]].head(40)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 15. Daily data: when would I use it?
# MAGIC 
# MAGIC Use the daily view if the class is very new to time series.
# MAGIC 
# MAGIC It gives roughly one observation per day for one year. A sensible exercise would be:
# MAGIC 
# MAGIC - target: `avg_vibration_mm_s`
# MAGIC - holdout: last 30 days
# MAGIC - forecast horizon: next 30 days
# MAGIC - seasonal pattern: weekly (`seasonal_periods=7`)
# MAGIC 
# MAGIC The trade-off is that daily aggregation hides within-day changes that may matter for an industrial sensor.

# COMMAND ----------

daily = pd.read_sql_query(
    "SELECT * FROM a001_sensor_daily ORDER BY reading_date",
    conn
)
daily["reading_date"] = pd.to_datetime(daily["reading_date"])

# A complete day contains 1,440 one-minute readings.
# The first and last calendar dates are partial because the one-year
# sensor window starts/ends during the day.
daily_complete = daily[daily["minute_readings"] == 1440].copy()

print("All calendar-date rows:", len(daily))
print("Complete 24-hour days:", len(daily_complete))
daily[["reading_date", "minute_readings"]].iloc[[0, -1]]

# COMMAND ----------

# MAGIC %md
# MAGIC # Recommended class storyline
# MAGIC 
# MAGIC 1. **Meet the asset:** A-001 is a high-criticality pump.
# MAGIC 2. **See raw IoT scale:** one-minute data contains 525,600 rows.
# MAGIC 3. **Aggregate intelligently:** use 8,760 hourly observations.
# MAGIC 4. **Validate data quality:** regular intervals, no duplicated timestamps, complete hours.
# MAGIC 5. **Explore vibration:** visualize the year-long pattern.
# MAGIC 6. **Explain train/test:** never evaluate on the same observations used for fitting.
# MAGIC 7. **Create a baseline:** same hour yesterday.
# MAGIC 8. **Fit Holt-Winters:** level + trend + 24-hour seasonality.
# MAGIC 9. **Evaluate:** compare MAE and RMSE against the baseline.
# MAGIC 10. **Forecast:** next seven days / 168 hours.
# MAGIC 11. **Add enterprise context:** inspect work orders, inspections, maintenance, project and risk records.
# MAGIC 12. **Introduce multivariate ML:** use other sensor variables for historical next-step prediction, while explaining the future-covariate limitation.
# MAGIC 
# MAGIC ### Core teaching message
# MAGIC 
# MAGIC **Machine learning does not replace the operational story.**
# MAGIC 
# MAGIC The sensor model tells us what may happen next.  
# MAGIC The asset, work-order, inspection, project, risk and document data tell us **why the forecast matters and what humans should do with it**.

# COMMAND ----------
