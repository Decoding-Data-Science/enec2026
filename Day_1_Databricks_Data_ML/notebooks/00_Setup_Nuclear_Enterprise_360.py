# Databricks notebook source
# MAGIC %md
# MAGIC # Nuclear Enterprise 360 — Setup
# MAGIC
# MAGIC This notebook imports the portable SQLite training database into Unity Catalog managed Delta tables.
# MAGIC
# MAGIC **Safety boundary:** all data is synthetic. It does not represent a real nuclear facility, reactor, safety system, employee, procedure, or operational condition.
# MAGIC
# MAGIC ## Before running
# MAGIC 1. Attach this notebook to **Serverless** compute.
# MAGIC 2. Run the first setup cell to create the schema and volume.
# MAGIC 3. Upload `nuclear_enterprise_360.db` through **New → Add or upload data → Upload files to a volume**.
# MAGIC 4. Select the volume created by this notebook and rerun from the upload-check cell.

# COMMAND ----------

from pathlib import Path
import sqlite3
import pandas as pd
from pyspark.sql import functions as F

CATALOG = spark.sql("SELECT current_catalog()").first()[0]
SCHEMA = "nuclear_enterprise_360"
VOLUME = "training_files"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`")
spark.sql(f"CREATE VOLUME IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`.`{VOLUME}`")
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql(f"USE SCHEMA `{SCHEMA}`")

VOLUME_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"
DB_PATH = f"{VOLUME_PATH}/nuclear_enterprise_360.db"

print(f"Catalog: {CATALOG}")
print(f"Schema:  {SCHEMA}")
print(f"Upload the SQLite file to: {VOLUME_PATH}")
print(f"Expected file: {DB_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Upload check
# MAGIC If this cell reports that the file is missing, use the upload instructions above. Databricks Free Edition restricts outbound downloads, so UI upload is the reliable method.

# COMMAND ----------

if not Path(DB_PATH).exists():
    raise FileNotFoundError(
        f"Upload nuclear_enterprise_360.db to {VOLUME_PATH}, then rerun this cell."
    )
print(f"Found training database: {DB_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Convert SQLite tables to managed Delta tables
# MAGIC
# MAGIC The import is repeatable: rerunning it overwrites the training tables with their original synthetic state.

# COMMAND ----------

with sqlite3.connect(DB_PATH) as con:
    table_names = [
        row[0]
        for row in con.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
    ]

    import_results = []
    for table_name in table_names:
        pdf = pd.read_sql_query(f'SELECT * FROM "{table_name}"', con)
        pdf = pdf.astype(object).where(pd.notnull(pdf), None)
        sdf = spark.createDataFrame(pdf)
        target = f"`{CATALOG}`.`{SCHEMA}`.`{table_name}`"
        (
            sdf.write
            .format("delta")
            .mode("overwrite")
            .option("overwriteSchema", "true")
            .saveAsTable(target)
        )
        import_results.append((table_name, len(pdf), len(pdf.columns)))

display(spark.createDataFrame(import_results, ["table_name", "row_count", "column_count"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add lakehouse features
# MAGIC
# MAGIC The RAG source table uses Change Data Feed so it can later back a Delta Sync AI Search index.

# COMMAND ----------

spark.sql("ALTER TABLE document_chunks SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

spark.sql("""
CREATE OR REPLACE VIEW asset_360 AS
WITH latest_health AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY asset_id ORDER BY score_date DESC) AS rn
  FROM asset_health_scores
), open_work AS (
  SELECT asset_id,
         COUNT(*) AS open_work_orders,
         SUM(CASE WHEN priority IN ('HIGH','URGENT') THEN 1 ELSE 0 END) AS high_priority_open_work
  FROM work_orders
  WHERE status IN ('OPEN','IN_PROGRESS','DEFERRED')
  GROUP BY asset_id
), findings AS (
  SELECT asset_id,
         COUNT(*) AS follow_up_findings,
         MAX(inspection_date) AS latest_inspection_date
  FROM inspections
  WHERE follow_up_required = 1
  GROUP BY asset_id
)
SELECT a.asset_id, a.asset_name, a.asset_type, a.criticality, a.status,
       s.system_name, s.unit_id,
       h.health_score, h.risk_level, h.recommended_action,
       COALESCE(w.open_work_orders, 0) AS open_work_orders,
       COALESCE(w.high_priority_open_work, 0) AS high_priority_open_work,
       COALESCE(f.follow_up_findings, 0) AS follow_up_findings,
       f.latest_inspection_date
FROM assets a
JOIN systems s ON a.system_id = s.system_id
LEFT JOIN latest_health h ON a.asset_id = h.asset_id AND h.rn = 1
LEFT JOIN open_work w ON a.asset_id = w.asset_id
LEFT JOIN findings f ON a.asset_id = f.asset_id
""")

spark.sql("""
CREATE OR REPLACE VIEW project_risk_360 AS
SELECT p.project_id, p.project_name, p.status AS project_status,
       p.completion_pct, p.budget_usd,
       COUNT(DISTINCT CASE WHEN r.status IN ('OPEN','MITIGATING') THEN r.risk_id END) AS active_risks,
       MAX(CASE WHEN r.status IN ('OPEN','MITIGATING') THEN r.exposure_score END) AS maximum_exposure,
       COUNT(DISTINCT CASE WHEN a.status IN ('OPEN','IN_PROGRESS','OVERDUE') THEN a.action_id END) AS active_actions,
       COUNT(DISTINCT CASE WHEN a.status = 'OVERDUE' THEN a.action_id END) AS overdue_actions
FROM projects p
LEFT JOIN risks r ON p.project_id = r.project_id
LEFT JOIN actions a ON p.project_id = a.project_id
GROUP BY p.project_id, p.project_name, p.status, p.completion_pct, p.budget_usd
""")

print("Created asset_360 and project_risk_360 views.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation
# MAGIC The expected result is zero orphaned records and visible synthetic-data metadata.

# COMMAND ----------

validation = spark.sql("""
SELECT 'work_orders_without_asset' AS check_name, COUNT(*) AS issue_count
FROM work_orders w LEFT ANTI JOIN assets a ON w.asset_id = a.asset_id
UNION ALL
SELECT 'risks_without_project', COUNT(*)
FROM risks r LEFT ANTI JOIN projects p ON r.project_id = p.project_id
UNION ALL
SELECT 'chunks_without_document', COUNT(*)
FROM document_chunks c LEFT ANTI JOIN documents d ON c.document_id = d.document_id
""")
display(validation)
display(spark.table("dataset_metadata"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup complete
# MAGIC Continue to `01_SQL_and_Delta_Foundations`.