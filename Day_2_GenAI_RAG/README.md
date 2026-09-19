# Day 2 — Generative AI & Retrieval-Augmented Generation

## Goal

Explain how LLMs work at a practical level, demonstrate why a general model does not automatically know internal organisational knowledge, and build a grounded enterprise RAG workflow around the A-001 document set.

## First half — LLM foundations

Cover:
- traditional ML vs Generative AI
- Large Language Models
- prompts and instructions
- tokens and context
- foundation models
- model parameters
- prompt engineering
- structured outputs
- hallucinations and limitations
- enterprise considerations

A useful transition question:

> **Which inspection procedure is currently approved for A-001?**

A general LLM should not be expected to know that. The answer requires trusted enterprise evidence.

## Second half — enterprise RAG

Core flow:

```text
PDFs
  ↓
Text extraction
  ↓
Chunking
  ↓
Embeddings
  ↓
Vector / semantic retrieval
  ↓
Metadata + authority filtering
  ↓
Relevant context
  ↓
LLM
  ↓
Grounded answer + sources
```

## Core notebooks

- `notebooks/01_A001_Simple_SQL_RAG.ipynb` — beginner-friendly SQL + RAG
- `notebooks/03_RAG_and_Hybrid_Retrieval.py` — governed retrieval / hybrid reference implementation

## A-001 RAG corpus

See:
- `documents/a001/` — readable repository mirrors of the full nine-document corpus
- `evaluation/` — manifest and evaluation questions

The original PDFs are included in the companion GitHub Release data pack.

The corpus deliberately contains:
- an APPROVED current procedure
- a SUPERSEDED older procedure
- a newer DRAFT procedure
- operating guidance
- troubleshooting guidance
- condition report
- work order
- field observation
- enterprise reliability policy

This creates the central governance lesson:

> **Most similar ≠ newest ≠ approved ≠ authoritative.**

## Recommended retrieval settings for the beginner notebook

- PDF or Markdown source documents
- chunk size: 400
- overlap: 100
- top-k: 3

## Evaluation

Use:
- `evaluation/rag_corpus_manifest.csv`
- `evaluation/rag_eval_questions.csv`

The evaluation set checks direct retrieval, authority/version handling, observation limits, hybrid evidence and human-governance boundaries.

## End-of-day outcome

Participants should be able to explain:
- what a chunk is
- what an embedding represents
- why semantic search differs from keyword search
- why metadata and document authority matter
- how RAG grounds an LLM in enterprise evidence
- why citations/provenance are required for enterprise trust


## Participant document setup

**Repo-native:** if this repository is cloned into Databricks, the updated notebooks first look for `Day_2_GenAI_RAG/documents/a001/`.

**Original-PDF exercise:** download the companion data pack from GitHub Releases and upload the nine PDFs to:

`/Workspace/Nuclear_Enterprise_360/A001 Documents/`

See [documents/a001/README.md](documents/a001/README.md).
