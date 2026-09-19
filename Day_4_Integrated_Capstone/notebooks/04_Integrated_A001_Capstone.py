# Databricks notebook source
# MAGIC %md
# MAGIC # Day 4 — Integrated A-001 Enterprise AI Capstone
# MAGIC
# MAGIC This notebook provides a simple orchestration skeleton for the final training exercise.
# MAGIC It combines structured evidence, document evidence and a human-review boundary.

# COMMAND ----------

import json
from datetime import datetime, timezone

CATALOG = spark.sql("SELECT current_catalog()").first()[0]
SCHEMA = "nuclear_enterprise_360"
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql(f"USE SCHEMA `{SCHEMA}`")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Structured evidence tool

# COMMAND ----------

def query_structured_a001() -> dict:
    row = spark.sql("""
        SELECT asset_id, asset_name, criticality, status,
               health_score, risk_level, recommended_action,
               open_work_orders, high_priority_open_work,
               follow_up_findings, latest_inspection_date
        FROM asset_360
        WHERE asset_id = 'A-001'
        LIMIT 1
    """).first()
    return row.asDict() if row else {}

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Recent trend evidence

# COMMAND ----------

def query_recent_trend(hours: int = 168) -> list[dict]:
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
# MAGIC ## 3. Document-authority evidence
# MAGIC
# MAGIC The Day 2/3 RAG notebooks provide the full retrieval implementation.
# MAGIC This capstone helper shows the document metadata that must remain visible.

# COMMAND ----------

def approved_document_register() -> list[dict]:
    rows = spark.sql("""
        SELECT document_id, title, document_type,
               approval_status, version, issue_date
        FROM a001_source_documents
        WHERE approval_status = 'APPROVED'
        ORDER BY issue_date DESC
    """).collect()
    return [r.asDict() for r in rows]

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Policy boundary

# COMMAND ----------

PROHIBITED_TERMS = [
    "control the reactor",
    "change the setpoint",
    "bypass a safeguard",
    "automatic shutdown",
    "issue a control command",
    "emergency operating instruction",
]

def policy_guard(question: str) -> tuple[bool, str]:
    q = question.lower()
    if any(term in q for term in PROHIBITED_TERMS):
        return False, (
            "Request refused. This synthetic training application is limited to "
            "evidence review and decision support."
        )
    return True, "Allowed within the synthetic decision-support boundary."

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Build an evidence packet

# COMMAND ----------

def build_evidence_packet(question: str) -> dict:
    allowed, guard_message = policy_guard(question)

    packet = {
        "question": question,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "guard": guard_message,
        "status": "REFUSED" if not allowed else "READY_FOR_REVIEW",
    }

    if not allowed:
        return packet

    packet["structured_evidence"] = query_structured_a001()
    packet["recent_sensor_evidence"] = query_recent_trend(168)
    packet["approved_document_register"] = approved_document_register()
    packet["limitations"] = [
        "A forecast or trend is not a physical diagnosis.",
        "Retrieved text must be checked for document authority and version.",
        "Missing or conflicting evidence must be preserved.",
        "Final operational decisions remain with a qualified human reviewer.",
    ]

    return packet

# COMMAND ----------

question = (
    "Investigate synthetic asset A-001, identify the evidence that matters, "
    "and prepare the next human reliability-review step."
)

packet = build_evidence_packet(question)

print("Status:", packet["status"])
print("Guard:", packet["guard"])
print("Structured evidence:")
print(json.dumps(packet.get("structured_evidence", {}), indent=2, default=str))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Add Day 2/3 RAG evidence
# MAGIC
# MAGIC Use the governed RAG notebook/tool from Day 2/3 to retrieve the relevant approved chunks.
# MAGIC Add those chunks to the packet under a separate `document_evidence` key.
# MAGIC
# MAGIC Keep these source types separate:
# MAGIC
# MAGIC - structured facts
# MAGIC - sensor / ML evidence
# MAGIC - written organisational guidance
# MAGIC - model interpretation
# MAGIC
# MAGIC This separation is part of the governance design.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Human-review output
# MAGIC
# MAGIC Your final briefing should contain:
# MAGIC
# MAGIC 1. Situation
# MAGIC 2. Structured evidence
# MAGIC 3. Predictive / trend evidence
# MAGIC 4. Approved document evidence
# MAGIC 5. Uncertainty / evidence gaps
# MAGIC 6. Recommended human next step
# MAGIC 7. Sources
# MAGIC
# MAGIC The application may prepare this briefing. It does not authorise maintenance or control equipment.
