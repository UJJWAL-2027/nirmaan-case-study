\
    import pandas as pd
    import numpy as np
    import os

    # Try importing sentence_transformers; code handles absence gracefully.
    try:
        from sentence_transformers import SentenceTransformer, util
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        MODEL = None

    RUBRIC_XLSX = os.path.join(os.path.dirname(__file__), "Case study for interns.xlsx")

    def load_rubric():
        # Expects columns: criterion, description, keywords (comma separated), weight, min_words, max_words
        if not os.path.exists(RUBRIC_XLSX):
            raise FileNotFoundError(f"Rubric file not found at {RUBRIC_XLSX}")
        df = pd.read_excel(RUBRIC_XLSX)
        # normalize expected column names
        df = df.rename(columns={c: c.strip() for c in df.columns})
        return df.to_dict(orient="records")

    def keyword_score(transcript, keywords):
        if not keywords:
            return 0.0, []
        found = []
        t = transcript.lower()
        for kw in [k.strip().lower() for k in keywords.split(",") if k.strip()]:
            if kw in t:
                found.append(kw)
        score = len(found) / max(1, len([k for k in keywords.split(",") if k.strip()]))
        return score, found

    def length_score(transcript, min_w, max_w):
        words = len(transcript.split())
        if min_w and words < min_w:
            return 0.0, words
        if max_w and words > max_w:
            # penalize proportionally
            over = words - max_w
            # simple linear penalty
            return max(0.0, 1 - (over / max_w)), words
        return 1.0, words

    def semantic_score(transcript, description):
        if not MODEL or not description:
            # fallback: return 0.5 for neutral if model missing
            return 0.5
        try:
            emb1 = MODEL.encode(transcript, convert_to_tensor=True)
            emb2 = MODEL.encode(description, convert_to_tensor=True)
            sim = util.cos_sim(emb1, emb2).item()
            # map similarity (-1..1) to 0..1
            return float((sim + 1) / 2)
        except Exception as e:
            return 0.5

    def score_transcript(transcript):
        rubric = load_rubric()
        per_criterion = []
        total_weight = sum([r.get("weight", 1) for r in rubric])
        overall_raw = 0.0
        words = len(transcript.split())

        for r in rubric:
            desc = str(r.get("description", ""))
            kw = str(r.get("keywords", "")) if not pd.isna(r.get("keywords", "")) else ""
            weight = float(r.get("weight", 1) or 1)
            min_w = int(r.get("min_words", 0) or 0)
            max_w = int(r.get("max_words", 0) or 0)

            kw_score, found = keyword_score(transcript, kw)
            len_score, wcount = length_score(transcript, min_w, max_w)
            sem_score = semantic_score(transcript, desc)

            # combine: simple weighted average of the three signals
            combined = (0.4 * kw_score) + (0.3 * sem_score) + (0.3 * len_score)
            per_criterion.append({
                "criterion": r.get("criterion", "Unnamed"),
                "weight": weight,
                "keyword_score": round(kw_score, 3),
                "found_keywords": found,
                "semantic_score": round(sem_score, 3),
                "length_score": round(len_score, 3),
                "combined_score_0_1": round(combined, 3),
            })
            overall_raw += combined * weight

        overall_norm = (overall_raw / max(1, total_weight)) * 100
        return {
            "overall_score_0_100": round(overall_norm, 2),
            "words": words,
            "per_criterion": per_criterion
        }
