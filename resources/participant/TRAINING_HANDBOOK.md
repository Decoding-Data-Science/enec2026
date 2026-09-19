# Participant Handbook — AI for Coders & Software Engineers

This is the repository version of the printable participant handout. It is designed to support the full **3.5 days of guided learning + final half-day team capstone**.

> All A-001 data, documents, observations and scenarios are synthetic training material.

## Programme journey

```text
A-001
  -> Databricks & Enterprise Data
  -> Machine Learning / Forecasting
  -> Generative AI
  -> Enterprise RAG
  -> AI Tools & Agents
  -> Skills + Memory + Progressive Disclosure
  -> Governed / Multi-Agent Workflows
  -> Integrated Enterprise AI Application
  -> Human Review & Oversight
```

## Day 1 — Databricks, Enterprise Data & Machine Learning

### Outcomes

- Set up the Databricks workspace.
- Understand catalog, schema, tables and Volumes.
- Load the V2.2 SQLite training database.
- Explore A-001 using SQL/Python.
- Build a simple vibration forecasting workflow.
- Interpret MAE and prediction limits.

### Core notebooks

1. `00_Setup_Nuclear_Enterprise_360.py`
2. `01_SQL_and_Delta_Foundations.py`
3. `A001_Forecasting_Databricks_Notebook.py`

### Key teaching dataset

- `a001_sensor_hourly`
- 8,760 hourly rows
- target: `avg_vibration_mm_s`
- forecast horizon: 168 hours / 7 days

### Day 1 question

**Is prediction enough to make a maintenance decision?**

No. Prediction is analytical evidence; enterprise decisions also require approved procedures, work context, recent observations and human judgement.

---

## Day 2 — Generative AI & RAG

### Outcomes

- Explain LLMs, prompts, tokens, context and hallucinations.
- Understand chunking, embeddings and semantic retrieval.
- Build a grounded A-001 RAG flow.
- Use metadata, approval status and versioning.
- Produce cited answers.

### RAG flow

```text
Documents
  -> Text extraction
  -> Chunking
  -> Embeddings
  -> Retrieval
  -> Metadata / authority filtering
  -> LLM
  -> Grounded answer + sources
```

### Governance trap

For the inspection procedure:

- V1 = SUPERSEDED
- V2 = APPROVED / current
- V3D = DRAFT

**Newest or most similar does not automatically mean authoritative.**

---

## Day 3 — Agentic AI & Governed Agent Patterns

### Outcomes

- Explain LLM vs RAG vs agent.
- Build a bounded SQL capability.
- Combine SQL and RAG tools.
- Route questions to the correct capability.
- Understand tools, skills, knowledge, memory and progressive disclosure.
- Explain human-in-the-loop and multi-agent patterns.

### Three teaching skills

| Skill | Evidence | Purpose |
|---|---|---|
| `asset_summary` | SQL | Return current structured facts |
| `approved_procedure` | RAG | Identify current approved guidance |
| `reliability_review` | SQL + RAG | Prepare an evidence-backed human-review briefing |

### Core rule

A smarter agent does not justify weaker permissions.

---

## Day 4 — Integration + Capstone

### First half: integration

Combine:

- structured data
- sensor / ML evidence
- approved document evidence
- agent tools
- workflow controls
- human review

### Second half: team capstone

**Business question:**

> What does the available evidence say about A-001, what should a qualified reviewer pay attention to, and what is the appropriate human next step?

### Required final output

1. Situation
2. Structured evidence
3. Predictive / analytical evidence
4. Document evidence
5. Assessment
6. Evidence gaps / uncertainty
7. Recommended human next step
8. Sources used

### Evaluation

Five dimensions, each scored 1–5:

1. Problem understanding
2. Data use
3. AI / RAG use
4. Evidence & explainability
5. Governance & human oversight

Maximum score: **25**

---

## Five questions to repeat throughout the programme

1. What do we know from the data?
2. What can we predict?
3. What does the organisation know?
4. What should the AI application do with that information?
5. Where must a human remain responsible?

## Participant setup

Start here:

- [START_HERE.md](../../START_HERE.md)
- [Participant Setup Guide](SETUP_GUIDE.md)

## Repository

https://github.com/Decoding-Data-Science/enec2026

## Release / data pack

https://github.com/Decoding-Data-Science/enec2026/releases/tag/enec-2026-final

Download:

`ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

The printable PDF handbook is also provided separately by the instructor.
