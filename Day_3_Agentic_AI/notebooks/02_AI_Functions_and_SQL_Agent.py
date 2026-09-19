# Databricks notebook source
# MAGIC %md
# MAGIC # Day 3 — Governed SQL Tool + Agent Routing
# MAGIC
# MAGIC **Outcome:** turn structured enterprise data into a bounded callable capability that an agent can use safely.

# COMMAND ----------

from textwrap import dedent

CATALOG = spark.sql("SELECT current_catalog()").first()[0]
SCHEMA = "nuclear_enterprise_360"
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql(f"USE SCHEMA `{SCHEMA}`")

ASSET_VIEW = f"`{CATALOG}`.`{SCHEMA}`.asset_360"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. A bounded SQL tool
# MAGIC
# MAGIC The language model does **not** receive unrestricted database credentials.
# MAGIC The application exposes a small, testable function.

# COMMAND ----------

def asset_summary_tool(asset_id: str = "A-001") -> dict:
    if asset_id != "A-001":
        raise ValueError("This training tool is scoped to synthetic asset A-001.")

    row = spark.sql(f"""
        SELECT asset_id, asset_name, asset_type, criticality, status,
               health_score, risk_level, recommended_action,
               open_work_orders, high_priority_open_work,
               follow_up_findings, latest_inspection_date
        FROM {ASSET_VIEW}
        WHERE asset_id = 'A-001'
        LIMIT 1
    """).first()

    return row.asDict() if row else {}

asset_summary_tool()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Add another structured capability

# COMMAND ----------

def recent_sensor_summary_tool(hours: int = 168) -> list[dict]:
    if hours < 1 or hours > 336:
        raise ValueError("Training horizon must be between 1 and 336 hours.")

    rows = spark.sql(f"""
        SELECT hour_timestamp, avg_vibration_mm_s, max_vibration_mm_s,
               avg_temperature_c, avg_discharge_pressure_bar
        FROM a001_sensor_hourly
        ORDER BY hour_timestamp DESC
        LIMIT {int(hours)}
    """).collect()

    return [r.asDict() for r in rows]

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Deterministic routing first
# MAGIC
# MAGIC Begin with predictable routing. Model-driven planning can be discussed later.

# COMMAND ----------

def choose_structured_tool(question: str) -> str:
    q = question.lower()

    if any(term in q for term in ["vibration", "sensor", "trend", "temperature", "pressure"]):
        return "recent_sensor_summary"

    return "asset_summary"

# COMMAND ----------

def run_structured_agent(question: str):
    tool = choose_structured_tool(question)

    if tool == "recent_sensor_summary":
        evidence = recent_sensor_summary_tool(hours=168)
    else:
        evidence = asset_summary_tool()

    return {
        "question": question,
        "selected_tool": tool,
        "evidence": evidence,
        "authority": "decision-support only; final operational decisions remain with a qualified human",
    }

run_structured_agent("What is the current health summary for A-001?")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Tool contract
# MAGIC
# MAGIC A useful enterprise tool contract states:
# MAGIC
# MAGIC - allowed input
# MAGIC - allowed data scope
# MAGIC - expected output
# MAGIC - failure behaviour
# MAGIC - authority boundary
# MAGIC - audit/provenance fields
# MAGIC
# MAGIC The next step is to combine this structured-data capability with the governed RAG capability from Day 2.
