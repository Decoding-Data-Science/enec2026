# Instructor Run of Show

## The one sentence to keep the programme coherent

> We are taking one synthetic enterprise asset, A-001, and progressively making the application more capable — first with data, then prediction, then organisational knowledge, then tools and agents, while keeping evidence and human authority visible.

## Recurring teaching pattern

For every major concept use:

1. **WHY** — what enterprise problem are we solving?
2. **WHAT** — explain the concept visually and simply.
3. **HOW** — run the notebook/code.
4. **SO WHAT** — relate it back to A-001 and enterprise decision-making.

## Day 1

### Open
Introduce A-001 and the full capability journey before touching Databricks.

### First half
- workspace / notebook orientation
- catalog → schema → table / Volume
- upload and setup
- explore key tables
- SQL/Python
- show where documents live

### Second half
- sensor trend
- hourly aggregation
- vibration target
- baseline / simple model
- MAE
- forecast
- interpretation

### Transition
Ask: **Is prediction enough to make a maintenance decision?**

Use the missing organisational context to lead into Day 2.

## Day 2

### First half
Keep LLM theory practical.

Demonstrate that the model cannot know which A-001 procedure is currently approved unless enterprise evidence is supplied.

### Second half
Build:
PDF → chunks → embeddings → retrieval → metadata/authority filter → LLM → cited answer.

Emphasise:
**relevant ≠ authoritative**.

### Transition
Ask a question that needs both database facts and document guidance. Use that limitation to motivate agents.

## Day 3

Start with:
**An agent is an LLM-driven application that can choose approved tools to complete a bounded task.**

Teach one governed agent before multi-agent systems.

Recommended sequence:
1. SQL tool
2. RAG tool
3. hybrid question
4. skills
5. progressive disclosure
6. memory/state
7. governance / human review
8. multi-agent architecture discussion

Do not introduce multiple agents just because the term is fashionable. Make the architectural trade-off explicit.

## Day 4

Introduce very little new theory.

Show the integrated architecture and give participants the A-001 capstone.

Expected final reasoning structure:
- what happened?
- what does the data show?
- what does ML suggest?
- what do approved documents say?
- what supports the conclusion?
- what is missing?
- what must a human decide?

## Five questions to repeat across all four days

1. What do we know from the data?
2. What can we predict?
3. What does the organisation know?
4. What should the AI application do with that information?
5. Where must a human remain responsible?

## Live-delivery priority

If time gets tight, protect these outcomes:
1. Day 1 setup works.
2. One forecasting notebook works.
3. One RAG notebook works.
4. One SQL + RAG agent works.
5. One integrated capstone path works.

Slides support the notebooks; the notebooks are the hands-on product.
