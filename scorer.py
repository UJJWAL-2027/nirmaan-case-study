import pandas as pd
import numpy as np
import os

# Try importing sentence_transformers; fallback if not available
try:
    from sentence_transformers import SentenceTransformer, util
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    MODEL = None

RUBRIC_XLSX = os.path.join(os.path.dirname(__file__), "Case study for interns.xlsx")

def load_rubric():
    if not os.path.exists(RUBRIC_XLSX):
        raise FileNotFoundError(f"Rubric file not found: {RUBRIC_XLSX}")
    df = pd.read_excel(RUBRIC_XLSX)
    df = df.rename(columns={c: c.strip() for c in df.columns})
    return df.to_dict(orient="records")

def keyword_score(transcript, keywords):
    if not keywords:
        return 0.0, []
    found = []
    t = transcript.lower()
    kws = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    for kw in kws:
        if kw in t:
            found.append(kw)
    if len(kws) == 0:
        return 0, found
    return len(found) / len(kws), found

def length_score(transcript, min_w, max_w):
    words = len(transcript.split())
    if min_w and words < min_w:
        return 0.0, words
    if max_w and words > max_w:
        excess = words - max_w
        return max(0.0, 1 - (excess / max_w)), words
    return 1.0, words

def semantic_score(transcript, description):
    if not MODEL or not description:
        return 0.5
    try:
        emb1 = MODEL.encode(transcript, convert_to_tensor=True)
        emb2 = MODEL.encode(description, convert_to_tensor=True)
        sim = util.cos_sim(emb1, emb2).item()
        return (sim + 1) / 2
    except Exception:
        return 0.5

def score_transcript(transcript):
    rubric = load_rubric()
    per_criterion = []
    total_weight = sum([r.get("weight", 1) for r in rubric])
    overall_raw = 0.0

    for r in rubric:
        desc = str(r.get("description", ""))
        kw = str(r.get("keywords", "")) if not pd.isna(r.get("keywords", "")) else ""
        weight = float(r.get("weight", 1) or 1)
        min_w = int(r.get("min_words", 0) or 0)
        max_w = int(r.get("max_words", 0) or 0)

        kw_score, found = keyword_score(transcript, kw)
        len_score, _ = length_score(transcript, min_w, max_w)
        sem_score = semantic_score(transcript, desc)

        combined = (0.4 * kw_score) + (0.3 * sem_score) + (0.3 * len_score)

        per_criterion.append({
            "criterion": r.get("criterion", "Unnamed"),
            "weight": weight,
            "keyword_score": round(kw_score, 3),
            "semantic_score": round(sem_score, 3),
            "length_score": round(len_score, 3),
            "combined_score_0_1": round(combined, 3),
            "found_keywords": found
        })

        overall_raw += combined * weight

    final_score = (overall_raw / total_weight) * 100
    return {
        "overall_score_0_100": round(final_score, 2),
        "per_criterion": per_criterion
    }
