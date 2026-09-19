# ENEC 2026 — AI for Coders & Software Engineers

A four-day, instructor-led, hands-on enterprise AI programme built around one connected synthetic scenario: **Asset A-001, a cooling-water pump**.

The programme uses **Databricks** as the primary hands-on environment and progressively connects enterprise data, machine learning, Generative AI, Retrieval-Augmented Generation (RAG), AI agents, governed workflows and a final integrated application.

> **Training notice:** every asset, document, procedure, observation and dataset in this repository is synthetic and designed only for training. Nothing here is operational engineering guidance.

## Capability journey

```text
A-001
  ↓
Databricks & Enterprise Data
  ↓
Machine Learning / Forecasting
  ↓
Generative AI
  ↓
Enterprise RAG
  ↓
AI Agents
  ↓
Skills + Memory + Progressive Disclosure
  ↓
Governed / Multi-Agent Workflows
  ↓
Integrated Enterprise AI Application
  ↓
Human Review & Oversight
```

## Repository map

| Folder | Purpose |
|---|---|
| [Day_1_Databricks_Data_ML](Day_1_Databricks_Data_ML/) | Databricks foundations, enterprise data exploration, vibration forecasting and optional anomaly detection |
| [Day_2_GenAI_RAG](Day_2_GenAI_RAG/) | LLM foundations, document ingestion, chunking, embeddings, retrieval, authority filtering and RAG |
| [Day_3_Agentic_AI](Day_3_Agentic_AI/) | Tool use, SQL + RAG agents, skills, progressive disclosure, memory and governed agent patterns |
| [Day_4_Integrated_Capstone](Day_4_Integrated_Capstone/) | End-to-end integration, governed orchestration, capstone, evaluation and participant demos |
| [data](data/) | V2.2 database package, data dictionary, validation script and quick-start SQL |
| [resources](resources/) | Programme agenda, participant setup, instructor run-of-show, slides/archive catalog and additional references |
| [reference](reference/) | Earlier complete Databricks kit retained for instructor/reference use |

## The single enterprise story

Participants work with **A-001** throughout the programme.

Structured sources include:
- asset master and health information
- sensor readings
- inspections and maintenance history
- work orders
- projects and risks
- document metadata and links

Unstructured sources include:
- enterprise reliability policy
- operating guide
- approved, superseded and draft procedures
- troubleshooting guide
- condition-monitoring report
- work order
- field-condition report

The teaching point is not simply to retrieve the most similar or newest information. The system must reason about **authority, approval status, evidence quality, provenance and human oversight**.

## Recommended Databricks setup

Primary target:
- Catalog: `workspace`
- Schema: `nuclear_enterprise_360`
- Volume: `training_files`
- Volume path: `/Volumes/workspace/nuclear_enterprise_360/training_files`

Recommended workspace folders:
```text
/Workspace/Nuclear_Enterprise_360/
├── A001 Documents/
├── Agent_Skills/
└── Notebooks/
```

## Start here

### Participants
1. Read [resources/PARTICIPANT_SETUP.md](resources/PARTICIPANT_SETUP.md).
2. Download/extract the V2.2 data package from [data](data/).
3. Import the Day 1 notebooks into Databricks.
4. Run `00_Setup_Nuclear_Enterprise_360.py`.
5. Follow the README inside each day folder.

### Instructor
1. Read [resources/INSTRUCTOR_RUN_OF_SHOW.md](resources/INSTRUCTOR_RUN_OF_SHOW.md).
2. Validate V2.2 with `data/verify_v2_2.py`.
3. Keep the pre-staged Databricks environment as the live-demo fallback.
4. Use the slide archive in `resources/slides/`.
5. Keep the same A-001 narrative across all four days.

## Current data version

The **primary training database is V2.2 Clean Beginner Version**, created 16 September 2026.

Core forecasting flow:
- raw: `sensor_readings_a001_1min` — 525,600 rows
- teaching view: `a001_sensor_hourly` — 8,760 hourly rows
- recommended target: `avg_vibration_mm_s`
- recommended forecast horizon: 7 days / 168 hours

See [data/README.md](data/README.md) for details.

## Design principles

- One connected scenario rather than unrelated daily examples.
- Practical application before deep platform administration or theory.
- Build capability progressively; do not reveal the full architecture too early.
- Keep **data**, **knowledge**, **tools**, **skills**, **memory** and **authority** conceptually separate.
- Treat relevance and authority as different questions: **relevant does not automatically mean trusted**.
- Preserve uncertainty and evidence gaps.
- Human reviewers retain final operational authority.

## Programme outcome

By the end of Day 4, participants should be able to explain and demonstrate how a governed enterprise AI application can combine:
- structured enterprise data
- predictive ML outputs
- trusted organisational documents
- RAG with source attribution
- tools and agent routing
- workflow state and memory
- governance, auditability and human review

---

**Decoding Data Science — Learn by Building**  
ENEC 2026 synthetic enterprise AI training repository.
