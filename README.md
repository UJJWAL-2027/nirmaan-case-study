# Nirmaan AI Intern - Case Study Submission (Demo)

This repository contains a simple demo tool that accepts a transcript and produces
a rubric-based score (overall 0-100) and per-criterion feedback using a combination
of rule-based checks (keyword presence, length) and an optional semantic scoring
using `sentence-transformers`.

## Contents
- `app.py` - simple Flask web app (paste transcript, POST `/score`)
- `scorer.py` - scoring logic that reads the provided rubric Excel and computes scores
- `requirements.txt` - Python dependencies
- `Case study for interns.xlsx` - rubric provided (included)
- `Sample text for case study.txt` - sample transcript (included)
- `Nirmaan AI intern Case study instructions.pdf` - original instructions (included)

## Scoring formula (summary)
For each rubric criterion we compute:
- Keyword score (0-1) based on fraction of rubric keywords present in transcript.
- Length score (0-1) based on min/max word limits.
- Semantic score (0-1) as cosine similarity between transcript and criterion description (requires `sentence-transformers`).
- Combined per-criterion score = 0.4 * keyword + 0.3 * semantic + 0.3 * length
- Overall score (0-100) = weighted average across criteria using weights provided in the rubric.

## Tech Stack Used
-Backend::
Python 3.8+ – Primary language used for the scoring engine
Flask – Lightweight web framework to expose a simple scoring API

-NLP & Scoring::
Sentence-Transformers (MiniLM-L6-v2) – For semantic similarity scoring between transcript and rubric criteria
Pandas – To load and process the rubric Excel file
OpenPyXL – For Excel file parsing
NumPy – Numerical operations and intermediate calculations

-Application Logic::
Custom Rule-Based Scoring
Keyword matching
Length scoring (min/max words)
Weighted rubric-based score aggregation

-Hybrid Scoring Model::
Combines semantic + rule-based signals to produce an overall score from 0–100

## Run locally (short)
1. Create a virtualenv and activate it.
2. `pip install -r requirements.txt`
3. `python app.py`
4. Open http://localhost:8080 and paste a transcript, or POST to `/score` to get JSON response.

Full, exact run & deploy steps are in `RUN_LOCAL.md`.
