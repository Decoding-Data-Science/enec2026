# Databricks notebook source
# MAGIC %md
# MAGIC # Day 1 — SQL, Delta Lake & A-001 Evidence Exploration
# MAGIC
# MAGIC **Outcome:** explore the connected enterprise dataset, inspect A-001 evidence, and understand why trustworthy AI starts with trustworthy data.

# COMMAND ----------

CATALOG = spark.sql("SELECT current_catalog()").first()[0]
SCHEMA = "nuclear_enterprise_360"

spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql(f"USE SCHEMA `{SCHEMA}`")

print(f"Using {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Explore the lakehouse

# COMMAND ----------

display(spark.sql("SHOW TABLES"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM assets
# MAGIC WHERE asset_id = 'A-001';

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Use the Asset 360 view

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT asset_id, asset_name, asset_type, criticality, status,
# MAGIC        health_score, risk_level, recommended_action,
# MAGIC        open_work_orders, high_priority_open_work,
# MAGIC        follow_up_findings, latest_inspection_date
# MAGIC FROM asset_360
# MAGIC WHERE asset_id = 'A-001';

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Explore the recommended hourly sensor dataset

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM a001_sensor_hourly
# MAGIC ORDER BY hour_timestamp
# MAGIC LIMIT 48;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Summarise A-001 vibration by day

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DATE(hour_timestamp) AS reading_date,
# MAGIC        ROUND(AVG(avg_vibration_mm_s), 3) AS avg_vibration_mm_s,
# MAGIC        ROUND(MAX(max_vibration_mm_s), 3) AS max_vibration_mm_s,
# MAGIC        ROUND(AVG(avg_temperature_c), 2) AS avg_temperature_c
# MAGIC FROM a001_sensor_hourly
# MAGIC GROUP BY DATE(hour_timestamp)
# MAGIC ORDER BY reading_date;

# COMMAND ----------

# MAGIC %md
# MAGIC Use the Databricks visualization control to plot `reading_date` against `avg_vibration_mm_s`.
# MAGIC
# MAGIC **Teaching question:** Does a rising trend prove a physical failure, or does it justify further review?

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Link the asset to projects and risks

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM asset_project_map
# MAGIC WHERE asset_id = 'A-001'
# MAGIC ORDER BY project_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT project_id, project_name, risk_id, risk_category,
# MAGIC        risk_scope, exposure_score, status
# MAGIC FROM asset_project_risk_map
# MAGIC WHERE asset_id = 'A-001'
# MAGIC ORDER BY project_id, risk_scope DESC, exposure_score DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Follow the A-001 timeline

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM a001_event_timeline
# MAGIC ORDER BY event_timestamp;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. See the document evidence bridge

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM a001_document_evidence
# MAGIC ORDER BY document_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ## End-of-lab reflection
# MAGIC
# MAGIC Prepare a five-line evidence briefing:
# MAGIC
# MAGIC 1. What does the structured data say?
# MAGIC 2. What trend is visible?
# MAGIC 3. What does the data **not** prove?
# MAGIC 4. What other evidence would you need?
# MAGIC 5. What should a qualified human review next?
