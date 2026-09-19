# ENEC 2026 — Participant Start Here

Welcome to the four-day **AI for Coders & Software Engineers** programme.

Everything in this repository is synthetic training material. The programme follows one connected enterprise scenario around **Asset A-001**.

## 1. What you need

- GitHub access to this repository
- Databricks access
- a modern browser
- the companion **V2.2 Data + PDF Corpus** download from the repository Releases page

The source notebooks, readable A-001 documents, skills, evaluation files and guides are already in this repository.

## 2. Clone or download the repository

Recommended for Databricks: clone/import this GitHub repository into a Databricks Git folder.

Repository:

`https://github.com/Decoding-Data-Science/enec2026`

The Day 2/3 notebooks can automatically locate the repository's readable A-001 document mirrors and skill files when the repository is cloned into Databricks.

## 3. Download the database pack

From **GitHub → Releases**, download:

`ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`

Extract it locally. It contains:

- `nuclear_enterprise_360_v2_2_clean.db`
- the original nine A-001 PDF documents
- V2.2 release notes

## 4. Upload the database to Databricks

Run:

`Day_1_Databricks_Data_ML/notebooks/00_Setup_Nuclear_Enterprise_360.py`

The notebook creates:

```text
Catalog: current catalog (normally workspace)
Schema: nuclear_enterprise_360
Volume: training_files
```

Upload the extracted database to:

```text
/Volumes/workspace/nuclear_enterprise_360/training_files/nuclear_enterprise_360_v2_2_clean.db
```

Then rerun the setup notebook from the upload-check cell.

## 5. A-001 documents

You have two options.

### Easiest — use the repo documents
Readable Markdown mirrors of all nine A-001 documents are under:

`Day_2_GenAI_RAG/documents/a001/`

The updated RAG notebooks can use these directly when the repo is cloned into Databricks.

### Original PDFs
The companion data pack contains the original PDFs. If your exercise specifically requires PDF ingestion, upload them into:

`/Workspace/Nuclear_Enterprise_360/A001 Documents/`

## 6. Agent skills

The four skill files are already in:

`Day_3_Agentic_AI/skills/`

The updated Day 3 notebooks can locate them automatically from the cloned repo.

Fallback manual Databricks location:

`/Workspace/Nuclear_Enterprise_360/02_Agent_Skills/`

## 7. Follow the four days

1. [Day 1 — Databricks, Data & ML](Day_1_Databricks_Data_ML/)
2. [Day 2 — GenAI & RAG](Day_2_GenAI_RAG/)
3. [Day 3 — Agentic AI](Day_3_Agentic_AI/)
4. [Day 4 — Integrated Capstone](Day_4_Integrated_Capstone/)

## 8. Training boundary

The A-001 case, database, documents, observations and predictions are synthetic.

The exercises teach decision support, evidence provenance, document authority, auditability and human oversight. They are not operational engineering instructions.
