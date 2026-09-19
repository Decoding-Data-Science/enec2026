# Nuclear Enterprise 360 V2.2 — Compact Data Dictionary

## Core tables

| Object | Rows | Purpose |
|---|---:|---|
| `assets` | 128 | enterprise asset master |
| `systems` | 16 | systems containing assets |
| `units` | 4 | synthetic organisational/plant units |
| `sensor_readings` | 47,540 | preserved general sensor history |
| `sensor_readings_a001_1min` | 525,600 | one full year of one-minute A-001 readings |
| `asset_health_scores` | 11,520 | historical asset-health scoring |
| `work_orders` | 1,500 | work requests and status/history |
| `inspections` | 600 | inspection records |
| `maintenance_history` | 900 | synthetic maintenance history |
| `projects` | 29 | enterprise projects |
| `project_assets` | 30 | project-to-asset bridge |
| `risks` | 423 | project risks |
| `risk_assets` | 4 | direct risk-to-asset links |
| `actions` | 807 | mitigation/actions |
| `documents` | 42 | structured document register |
| `document_chunks` | 59 | pre-built synthetic chunks |
| `document_entity_links` | 22 | document-to-entity relationships |
| `a001_source_documents` | 9 | authoritative A-001 RAG corpus metadata |
| `a001_source_document_links` | 18 | links from corpus documents to entities |
| `agent_runs` | 50 | synthetic agent-run audit history |
| `agent_tool_calls` | 90 | synthetic tool-call traces |
| `human_approvals` | 35 | synthetic human-review decisions |

## Teaching views

| View | Rows | Teaching use |
|---|---:|---|
| `a001_sensor_hourly` | 8,760 | primary Day 1 forecasting dataset |
| `asset_360` | 128 | current asset evidence summary |
| `asset_project_map` | 30 | asset-to-project navigation |
| `asset_project_risk_map` | 432 | project and direct asset-risk context |
| `a001_project_risk_360` | 33 | A-001-specific project/risk view |
| `a001_event_timeline` | 49 | chronological A-001 story |
| `a001_document_evidence` | 18 | document evidence linked to A-001 |
| `project_risk_360` | 29 | project risk summary |

## Recommended beginner path

`assets` → `a001_sensor_hourly` → `asset_360` → work/inspection history → project/risk context → A-001 documents → RAG → governed agent.
