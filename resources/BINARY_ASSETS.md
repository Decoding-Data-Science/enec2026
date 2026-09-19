# Binary Training Assets

The repository source tree contains all text-based notebooks, code, Markdown guides, SQL helpers, skill files and evaluation CSVs.

The remaining large/original binary training materials are distributed as two companion GitHub Release packs. The repository itself contains notebooks, code, guides, skills, evaluation CSVs and readable mirrors of all nine A-001 documents.

## Pack 1 — Data + A-001 PDF corpus

**Recommended filename:** `ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

Contents:
- `nuclear_enterprise_360_v2_2_clean.db`
- nine A-001 enterprise RAG PDFs
- V2.2 release notes

Why packaged:
- the extracted SQLite database is about 120 MB, above GitHub's normal 100 MB single-file limit
- the compressed pack is about 24 MB and is suitable as a training download / GitHub Release asset

## Pack 2 — Slides + trainer materials

**Recommended filename:** `ENEC_2026_Slides_and_Trainer_Materials.zip`

Recovered materials include:
- ENEC Day 1 intro/training decks
- A-001 multivariate forecasting deck
- Databricks enterprise/workshop decks
- SQL & Delta foundations deck
- AI functions / governed SQL agent deck
- enterprise RAG / cited answers deck
- governed RAG & hybrid retrieval masterclass deck
- skills / progressive disclosure / memory deck
- governed Agentic AI capstone decks
- Agentic AI workshop steps
- Databricks setup trainer runbook
- participant setup guide (DOCX/PDF)

## Recommended publishing method

Attach both ZIPs to a GitHub Release named something like:

`ENEC 2026 Training Materials — Final`

Then keep this source repository as the version-controlled teaching reference and the Release assets as the binary download layer.


## Repository-native fallback

Participants can browse all nine A-001 documents directly under:

`Day_2_GenAI_RAG/documents/a001/`

Those are readable Markdown mirrors. The Release pack contains the original PDFs.

## Owner action

The connected GitHub integration cannot upload Release assets or change repository visibility. The two final manual publishing actions are documented in [OWNER_FINAL_STEPS.md](OWNER_FINAL_STEPS.md).
