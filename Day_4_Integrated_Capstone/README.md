# Day 4 — Integrated Enterprise AI Application, Capstone & Evaluation

## Goal

Bring the previous three days together into one inspectable enterprise AI workflow and finish with a practical A-001 capstone.

## Integration architecture

```text
                    USER
                      │
                      ▼
              Enterprise AI App
                      │
              Governed Orchestrator
        ┌─────────────┼──────────────┐
        │             │              │
        ▼             ▼              ▼
 Structured Data   RAG/Documents   ML Output
        │             │              │
        └─────────────┼──────────────┘
                      ▼
                Evidence Packet
                      │
                      ▼
                Draft Briefing
                      │
                      ▼
                Human Review
                      │
                      ▼
                Recorded Outcome
```

## Core capstone assets

- `notebooks/04_Agentic_AI_Capstone.py`
- `CAPSTONE_BRIEF.md`
- `EVALUATION_RUBRIC.md`
- `resources/Day_4_Enterprise_AI_Capstone_Lab.zip`

## Capstone mission

Participants work individually or in small groups.

They should investigate the synthetic A-001 case using:
- structured enterprise data
- sensor / ML evidence
- enterprise documents
- RAG
- agent/tool capabilities
- governance constraints

The final output should clearly separate:
1. observed facts
2. analytical/model output
3. approved written guidance
4. interpretation
5. evidence gaps / uncertainty
6. recommended human next step

## Governance rule

The application may prepare evidence and a review briefing.

It must not:
- diagnose a real physical failure
- issue equipment-control commands
- authorise maintenance
- close a work order
- treat a model output as approval
- approve its own recommendation

## Demonstration expectation

A strong demo should show:
- the business question
- the data/evidence used
- the tool/retrieval path
- the answer or briefing
- sources/citations
- limitations
- where the human reviewer remains responsible

## End-of-programme outcome

Participants should be able to explain how a modest enterprise dataset becomes a governed AI-enabled application by progressively adding prediction, knowledge retrieval, tools, agents, workflow controls and human oversight.
