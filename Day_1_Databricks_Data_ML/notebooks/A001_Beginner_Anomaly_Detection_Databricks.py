# Databricks notebook source
# MAGIC %md
# MAGIC # A001 Beginner AI Project
# MAGIC ## Is the pump reading Normal or Abnormal?
# MAGIC
# MAGIC One-variable beginner project:
# MAGIC **Vibration → Decision Tree → Normal / Abnormal**
# MAGIC
# MAGIC This is anomaly detection/classification, not actual failure prediction.

# COMMAND ----------

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix

# COMMAND ----------

DB_PATH = "/Volumes/workspace/v2_nuclear_enterprise_360/v2_nuclear_enterprise_360/nuclear_enterprise_360_v2_2_clean.db"

conn = sqlite3.connect(DB_PATH)

query = '''
SELECT
    reading_timestamp,
    asset_id,
    vibration_mm_s,
    anomaly_flag
FROM sensor_readings
WHERE asset_id = 'A-001'
ORDER BY reading_timestamp
'''

df = pd.read_sql_query(query, conn)
conn.close()

print("Rows loaded:", len(df))
display(df.head(10))

# COMMAND ----------

print("Normal vs abnormal readings:")
print(df["anomaly_flag"].value_counts())

# COMMAND ----------

df["reading_timestamp"] = pd.to_datetime(df["reading_timestamp"])

plt.figure(figsize=(12, 4))
plt.plot(df["reading_timestamp"], df["vibration_mm_s"])
plt.xlabel("Time")
plt.ylabel("Vibration (mm/s)")
plt.title("A-001 Vibration Readings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

X = df[["vibration_mm_s"]]
y = df["anomaly_flag"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# COMMAND ----------

model = DecisionTreeClassifier(max_depth=1, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# COMMAND ----------

accuracy = accuracy_score(y_test, predictions)
cm = confusion_matrix(y_test, predictions)

print("Accuracy:", round(accuracy * 100, 2), "%")
print("Confusion Matrix:")
print(cm)

# COMMAND ----------

threshold = model.tree_.threshold[0]

print(f"The model learned a vibration split of approximately {threshold:.2f} mm/s")
print(f"If vibration <= {threshold:.2f} mm/s → NORMAL")
print(f"If vibration >  {threshold:.2f} mm/s → ABNORMAL")

# COMMAND ----------

plt.figure(figsize=(10, 5))
plot_tree(
    model,
    feature_names=["vibration_mm_s"],
    class_names=["Normal", "Abnormal"],
    filled=False,
    rounded=True
)
plt.title("A-001 Beginner Decision Tree")
plt.show()

# COMMAND ----------

new_readings = pd.DataFrame({
    "vibration_mm_s": [1.2, 3.0, 4.8, 5.2, 5.5]
})

new_readings["prediction"] = model.predict(new_readings)
new_readings["meaning"] = new_readings["prediction"].map({
    0: "NORMAL",
    1: "ABNORMAL"
})

display(new_readings)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Business meaning
# MAGIC An abnormal prediction does **not** mean the pump has failed.
# MAGIC
# MAGIC It means the vibration reading looks like historical readings that were marked abnormal.
# MAGIC
# MAGIC **Prediction → inspect A-001 → review documents/work orders → human decision**