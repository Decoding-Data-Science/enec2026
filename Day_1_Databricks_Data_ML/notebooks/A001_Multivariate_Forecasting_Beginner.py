# Databricks notebook source
# MAGIC %md
# MAGIC # A-001 Beginner Multivariate Forecasting
# MAGIC 
# MAGIC ## Business objective
# MAGIC Use one year of **hourly A-001 sensor data** to forecast the next **7 days (168 hours)**.
# MAGIC 
# MAGIC The main business question is:
# MAGIC 
# MAGIC > **Is A-001's vibration likely to continue rising, so the maintenance/reliability team can plan inspection or servicing earlier?**
# MAGIC 
# MAGIC This notebook is intentionally beginner-friendly. It does **not** make an automatic maintenance or shutdown decision.
# MAGIC 
# MAGIC ### What makes this multivariate?
# MAGIC We use several sensor signals together:
# MAGIC 
# MAGIC - Vibration — our main business signal
# MAGIC - Temperature
# MAGIC - Pressure
# MAGIC - Flow rate
# MAGIC - Electrical current
# MAGIC - Ambient temperature
# MAGIC 
# MAGIC The model forecasts all six signals together so it can keep forecasting multiple hours into the future.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Simple process
# MAGIC 
# MAGIC **Hourly data → clean → create time-based features → train → test on last 7 days → forecast next 7 days**
# MAGIC 
# MAGIC We use **Ridge Regression**, which is a regularized linear regression model.
# MAGIC 
# MAGIC Why Ridge?
# MAGIC - easy to explain
# MAGIC - fast to train
# MAGIC - works well with correlated sensor variables
# MAGIC - gives a strong foundation before introducing more advanced models

# COMMAND ----------

import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Change this path only if your database is stored elsewhere.
DB_PATH = "/Workspace/Nuclear_Enterprise_360/nuclear_enterprise_360_v2_2_clean.db"

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(
        f"Database not found at {DB_PATH}. "
        "Upload the V2.2 database and update DB_PATH."
    )

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query(
    "SELECT * FROM a001_sensor_hourly ORDER BY hour_timestamp",
    conn
)

df["hour_timestamp"] = pd.to_datetime(df["hour_timestamp"])

print("Rows:", len(df))
print("Start:", df["hour_timestamp"].min())
print("End:", df["hour_timestamp"].max())
df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Choose the variables
# MAGIC 
# MAGIC We forecast six hourly variables together.
# MAGIC 
# MAGIC Our **main target for the business story is vibration** (`avg_vibration_mm_s`).

# COMMAND ----------

VARIABLES = [
    "avg_vibration_mm_s",
    "avg_temperature_c",
    "avg_pressure_bar",
    "avg_flow_rate_m3_h",
    "avg_electrical_current_a",
    "avg_ambient_temperature_c",
]

df[["hour_timestamp"] + VARIABLES].head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Quick data-quality check
# MAGIC 
# MAGIC Before modeling, check:
# MAGIC - missing values
# MAGIC - duplicate timestamps
# MAGIC - whether the hourly timeline is complete

# COMMAND ----------

print("Duplicate timestamps:", df["hour_timestamp"].duplicated().sum())
print("\nMissing values:")
print(df[VARIABLES].isna().sum())

expected_hours = pd.date_range(
    df["hour_timestamp"].min(),
    df["hour_timestamp"].max(),
    freq="h"
)

missing_hours = expected_hours.difference(df["hour_timestamp"])
print("\nMissing hourly timestamps:", len(missing_hours))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Visualize A-001 vibration
# MAGIC 
# MAGIC This is the first chart students should see.
# MAGIC 
# MAGIC The question is not just *"what is the latest value?"*  
# MAGIC The question is *"what pattern has developed over time?"*

# COMMAND ----------

plt.figure(figsize=(14, 5))
plt.plot(df["hour_timestamp"], df["avg_vibration_mm_s"])
plt.title("A-001 Hourly Average Vibration")
plt.xlabel("Time")
plt.ylabel("Vibration (mm/s)")
plt.grid(alpha=0.25)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Understand the multivariate relationship
# MAGIC 
# MAGIC Correlation is **not causation**, but it helps us see which sensor variables move together.
# MAGIC 
# MAGIC This is exploration only; it does not prove that one sensor causes another.

# COMMAND ----------

df[VARIABLES].corr().round(2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Create beginner-friendly time-series features
# MAGIC 
# MAGIC A normal regression model does not automatically understand time.
# MAGIC 
# MAGIC We therefore give it a little memory:
# MAGIC 
# MAGIC - **1-hour lag**: what was the sensor value one hour ago?
# MAGIC - **24-hour lag**: what was it at the same time yesterday?
# MAGIC - **24-hour rolling mean**: what has been typical over the last day?
# MAGIC - **hour/day features**: help represent repeating time patterns
# MAGIC 
# MAGIC These features let a simple model learn **trend + recent history + daily seasonality**.

# COMMAND ----------

def make_training_features(data):
    model_df = data.copy()

    for col in VARIABLES:
        model_df[f"{col}_lag1"] = model_df[col].shift(1)
        model_df[f"{col}_lag24"] = model_df[col].shift(24)
        model_df[f"{col}_roll24"] = (
            model_df[col].shift(1).rolling(24).mean()
        )

    hour = model_df["hour_timestamp"].dt.hour
    day_of_week = model_df["hour_timestamp"].dt.dayofweek

    model_df["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    model_df["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    model_df["dow_sin"] = np.sin(2 * np.pi * day_of_week / 7)
    model_df["dow_cos"] = np.cos(2 * np.pi * day_of_week / 7)

    return model_df.dropna().reset_index(drop=True)

model_df = make_training_features(df)

FEATURES = (
    [f"{col}_lag1" for col in VARIABLES]
    + [f"{col}_lag24" for col in VARIABLES]
    + [f"{col}_roll24" for col in VARIABLES]
    + ["hour_sin", "hour_cos", "dow_sin", "dow_cos"]
)

print("Model rows:", len(model_df))
print("Number of input features:", len(FEATURES))
model_df[["hour_timestamp"] + FEATURES[:6]].head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Use a chronological train/test split
# MAGIC 
# MAGIC For time series, **do not randomly shuffle the data**.
# MAGIC 
# MAGIC We train on the earlier history and keep the **last 7 days = 168 hours** completely unseen for testing.

# COMMAND ----------

FORECAST_HOURS = 24 * 7

train = model_df.iloc[:-FORECAST_HOURS].copy()
test = model_df.iloc[-FORECAST_HOURS:].copy()

print("Training rows:", len(train))
print("Test rows:", len(test))
print("Test period:", test["hour_timestamp"].min(), "to", test["hour_timestamp"].max())

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Create a simple baseline
# MAGIC 
# MAGIC Before using machine learning, ask:
# MAGIC 
# MAGIC > What if tomorrow simply looks like yesterday?
# MAGIC 
# MAGIC The baseline repeats the final 24 hours of training for the next 7 days.
# MAGIC 
# MAGIC A useful ML model should improve on this simple rule.

# COMMAND ----------

last_24_vibration = train["avg_vibration_mm_s"].iloc[-24:].to_numpy()
baseline_vibration = np.tile(last_24_vibration, 7)

baseline_mae = mean_absolute_error(
    test["avg_vibration_mm_s"],
    baseline_vibration
)
baseline_rmse = np.sqrt(
    mean_squared_error(
        test["avg_vibration_mm_s"],
        baseline_vibration
    )
)

print(f"Baseline MAE : {baseline_mae:.3f}")
print(f"Baseline RMSE: {baseline_rmse:.3f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Train the multivariate Ridge model
# MAGIC 
# MAGIC The model learns:
# MAGIC 
# MAGIC **Past values of all six sensor variables → next-hour values of all six sensor variables**
# MAGIC 
# MAGIC `StandardScaler` puts the variables on comparable scales.
# MAGIC 
# MAGIC `Ridge` learns a regularized linear relationship and reduces instability when input variables are correlated.

# COMMAND ----------

model = make_pipeline(
    StandardScaler(),
    Ridge(alpha=1.0)
)

model.fit(
    train[FEATURES],
    train[VARIABLES]
)

print("Model trained.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Recursive 7-day forecast function
# MAGIC 
# MAGIC For one-hour-ahead prediction, the model uses recent known history.
# MAGIC 
# MAGIC For hour 2, it uses the prediction from hour 1.
# MAGIC 
# MAGIC For hour 3, it uses the previous predictions again.
# MAGIC 
# MAGIC This repeated process is called a **recursive forecast**.

# COMMAND ----------

def recursive_forecast(model, history_df, steps):
    history = history_df[["hour_timestamp"] + VARIABLES].copy().reset_index(drop=True)
    predictions = []

    next_time = history["hour_timestamp"].iloc[-1] + pd.Timedelta(hours=1)

    for _ in range(steps):
        feature_row = {}

        for col in VARIABLES:
            values = history[col].to_numpy()

            feature_row[f"{col}_lag1"] = values[-1]
            feature_row[f"{col}_lag24"] = values[-24]
            feature_row[f"{col}_roll24"] = values[-24:].mean()

        h = next_time.hour
        dow = next_time.dayofweek

        feature_row["hour_sin"] = np.sin(2 * np.pi * h / 24)
        feature_row["hour_cos"] = np.cos(2 * np.pi * h / 24)
        feature_row["dow_sin"] = np.sin(2 * np.pi * dow / 7)
        feature_row["dow_cos"] = np.cos(2 * np.pi * dow / 7)

        X_next = pd.DataFrame([feature_row])[FEATURES]
        y_next = model.predict(X_next)[0]

        new_row = {
            "hour_timestamp": next_time,
            **dict(zip(VARIABLES, y_next))
        }

        predictions.append(new_row)
        history = pd.concat(
            [history, pd.DataFrame([new_row])],
            ignore_index=True
        )

        next_time += pd.Timedelta(hours=1)

    return pd.DataFrame(predictions)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Backtest on the last 7 days
# MAGIC 
# MAGIC This is the honest test.
# MAGIC 
# MAGIC We pretend the final 7 days have not happened yet and recursively forecast them from the earlier history.

# COMMAND ----------

test_start = test["hour_timestamp"].min()

history_before_test = df[
    df["hour_timestamp"] < test_start
].copy()

backtest = recursive_forecast(
    model,
    history_before_test,
    FORECAST_HOURS
)

actual_test = df[
    df["hour_timestamp"].isin(backtest["hour_timestamp"])
].copy()

model_mae = mean_absolute_error(
    actual_test["avg_vibration_mm_s"],
    backtest["avg_vibration_mm_s"]
)

model_rmse = np.sqrt(
    mean_squared_error(
        actual_test["avg_vibration_mm_s"],
        backtest["avg_vibration_mm_s"]
    )
)

results = pd.DataFrame({
    "Model": ["Same hour yesterday", "Multivariate Ridge"],
    "MAE": [baseline_mae, model_mae],
    "RMSE": [baseline_rmse, model_rmse],
})

results.round(3)

# COMMAND ----------

# MAGIC %md
# MAGIC ### How to read the metrics
# MAGIC 
# MAGIC - **MAE**: average absolute forecast error
# MAGIC - **RMSE**: penalizes larger errors more strongly
# MAGIC - **Lower is better**
# MAGIC 
# MAGIC For this synthetic training dataset, the multivariate Ridge model should beat the simple daily-repeat baseline.

# COMMAND ----------

plt.figure(figsize=(14, 5))

plt.plot(
    actual_test["hour_timestamp"],
    actual_test["avg_vibration_mm_s"],
    label="Actual"
)

plt.plot(
    backtest["hour_timestamp"],
    backtest["avg_vibration_mm_s"],
    label="Multivariate forecast"
)

plt.title("A-001 Vibration — 7-Day Backtest")
plt.xlabel("Time")
plt.ylabel("Vibration (mm/s)")
plt.legend()
plt.grid(alpha=0.25)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Retrain on all available history
# MAGIC 
# MAGIC After we validate the method, we retrain using the complete year of available observations.

# COMMAND ----------

full_model_df = make_training_features(df)

final_model = make_pipeline(
    StandardScaler(),
    Ridge(alpha=1.0)
)

final_model.fit(
    full_model_df[FEATURES],
    full_model_df[VARIABLES]
)

future_7d = recursive_forecast(
    final_model,
    df,
    FORECAST_HOURS
)

future_7d.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 12. Forecast A-001 for the next 7 days
# MAGIC 
# MAGIC The chart combines the last 14 days of actual history with the next 7 days of predicted vibration.

# COMMAND ----------

recent_actual = df.tail(24 * 14)

plt.figure(figsize=(14, 5))

plt.plot(
    recent_actual["hour_timestamp"],
    recent_actual["avg_vibration_mm_s"],
    label="Recent actual"
)

plt.plot(
    future_7d["hour_timestamp"],
    future_7d["avg_vibration_mm_s"],
    label="Next 7 days forecast"
)

plt.title("A-001 — Next 7 Days Vibration Forecast")
plt.xlabel("Time")
plt.ylabel("Vibration (mm/s)")
plt.legend()
plt.grid(alpha=0.25)
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 13. Business interpretation — keep it simple
# MAGIC 
# MAGIC Compare the next 7-day forecast with the recent 7-day history.
# MAGIC 
# MAGIC We are **not inventing an engineering alarm threshold**.  
# MAGIC Instead, we ask whether the forecast is moving materially above or below the recent operating baseline.

# COMMAND ----------

recent_7d_mean = df["avg_vibration_mm_s"].tail(24 * 7).mean()
future_7d_mean = future_7d["avg_vibration_mm_s"].mean()

change_pct = (
    (future_7d_mean - recent_7d_mean)
    / recent_7d_mean
    * 100
)

print(f"Recent 7-day average vibration : {recent_7d_mean:.3f} mm/s")
print(f"Forecast 7-day average vibration: {future_7d_mean:.3f} mm/s")
print(f"Forecast change vs recent baseline: {change_pct:.1f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ## What should the business do with the forecast?
# MAGIC 
# MAGIC The forecast is an **early-warning input**, not an automatic maintenance command.
# MAGIC 
# MAGIC A practical workflow is:
# MAGIC 
# MAGIC 1. Forecast suggests whether vibration is likely to rise, stabilize or fall.
# MAGIC 2. Review A-001's recent work orders, inspections and maintenance history.
# MAGIC 3. Review the current approved procedure and supporting documents.
# MAGIC 4. A qualified maintenance/reliability person decides whether inspection or servicing should be brought forward.
# MAGIC 
# MAGIC ### Key training message
# MAGIC 
# MAGIC > **Machine learning predicts a likely future pattern. Humans combine that prediction with engineering evidence and business context to make the maintenance decision.**

# COMMAND ----------

# MAGIC %md
# MAGIC # Optional next step
# MAGIC 
# MAGIC After students understand this notebook, you can compare the simple Ridge model with:
# MAGIC 
# MAGIC - Holt-Winters
# MAGIC - Random Forest
# MAGIC - Gradient Boosting / XGBoost
# MAGIC - LSTM / deep learning
# MAGIC 
# MAGIC But for beginners, **Ridge + lag features + a chronological backtest** is a very strong starting point.

# COMMAND ----------
