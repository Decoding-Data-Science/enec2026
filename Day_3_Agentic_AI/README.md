# Day 3 — Agentic AI & Governed Agent Patterns

## Goal

Extend the Day 2 RAG application into an agent that can choose between structured data and document knowledge, then introduce reusable skills, progressive disclosure, memory, governance and multi-agent patterns.

## Start with a question RAG alone cannot answer well

Example:

> What was happening in A-001's data, what does the current approved procedure say, and what should be prepared for human reliability review?

That requires more than document retrieval.

It may require:
- SQL / structured data
- RAG / document evidence
- calculations or analysis
- tool selection
- workflow state
- a bounded synthesis step

## Core mental model

```text
User question
    ↓
Agent / Router
    ↓
Choose capability
 ┌───────┬──────────┬────────────┐
 SQL     RAG      Analysis     Other approved tools
 └───────┴──────────┴────────────┘
    ↓
Evidence packet
    ↓
Bounded synthesis
    ↓
Human review
```

## Core assets

### Structured / agent foundations
- `notebooks/02_AI_Functions_and_SQL_Agent.py`
- `notebooks/ENEC_A001_SQL_RAG_Hybrid_Agent_Educational_Notebook_v2_Skills.ipynb`

### Skills, progressive disclosure & memory
- `notebooks/ENEC_A001_Progressive_Disclosure_Skills_Notebook.ipynb`
- `notebooks/02_A001_Skills_Progressive_Disclosure_Memory_Databricks_Qwen.ipynb`
- `skills/skills_catalog.md`
- `skills/asset_summary.md`
- `skills/approved_procedure.md`
- `skills/reliability_review.md`

## Six concepts to keep separate

| Layer | Meaning |
|---|---|
| Tools | What the agent can call |
| Skills | How to perform a reusable business capability |
| Knowledge | Evidence the agent retrieves |
| Memory | Context intentionally retained |
| Progressive disclosure | Load only what the current task needs |
| Governance | What the system is allowed to do |

## Three teaching skills

### asset_summary
SQL only. Return bounded structured facts.

### approved_procedure
RAG only. Identify current approved authority and reject draft/superseded material as current guidance.

### reliability_review
SQL + RAG + bounded synthesis. Prepare an evidence-backed human-review briefing.

## Multi-agent section

Teach multi-agent systems as an architectural option, not a goal.

A useful pattern:

```text
Supervisor
  ├── Data specialist
  ├── Knowledge specialist
  ├── Analysis specialist
  └── Reporting specialist
          ↓
      Human review
```

Use a multi-agent architecture when specialised roles, permissions, tools or audit boundaries justify the added complexity.

**Do not use multiple agents when one governed agent with a few tools is enough.**

## End-of-day outcome

Participants should understand:
- tool calling
- agent routing
- SQL and RAG as separate enterprise capabilities
- reusable skills
- progressive disclosure
- session/workflow memory
- human-in-the-loop controls
- why agent authority must remain bounded


## Participant skill/document setup

The updated notebooks first try to locate resources from the cloned repository:

- documents: `Day_2_GenAI_RAG/documents/a001/`
- skills: `Day_3_Agentic_AI/skills/`

If the repository is not available as a Databricks Git folder, use the fallback workspace locations:

- `/Workspace/Nuclear_Enterprise_360/A001 Documents/`
- `/Workspace/Nuclear_Enterprise_360/02_Agent_Skills/`
