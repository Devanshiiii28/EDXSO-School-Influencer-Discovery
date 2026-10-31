"""Explainable hybrid ranking for school-ecosystem profile discovery."""
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROLE_TERMS = {
    "school_leadership": ["principal", "head of school", "school director", "director principal", "headmaster"],
    "consulting_advisory": ["consultant", "advisor", "advisory", "consulting", "resource person"],
    "school_group": ["group of schools", "school group", "trustee", "chairman", "managing director", "founder", "co-founder"],
    "education_network": ["network", "multiple schools", "sahodaya", "association", "npsc", "cbse", "ncert"],
    "teacher_development": ["teacher training", "teacher development", "capacity building", "faculty development"],
}

def _clean(text):
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()

def _signals(text):
    t = _clean(text)
    return {k: int(any(term in t for term in terms)) for k, terms in ROLE_TERMS.items()}

def rank_profiles(reference_text, profiles, top_n=20):
    """Rank rows with TF-IDF cosine similarity plus interpretable role-context overlap."""
    ref = _clean(reference_text)
    docs = [ref] + [ _clean(" ".join(str(row.get(c, "")) for c in
             ["current_role", "organisation", "location", "experience_indicators", "profile_text"]))
             for row in profiles ]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True,
                                 stop_words="english", max_features=12000)
    matrix = vectorizer.fit_transform(docs)
    lexical = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    ref_sig = _signals(ref)
    results = []
    for i, row in enumerate(profiles):
        candidate_text = docs[i + 1]
        cand_sig = _signals(candidate_text)
        active = [k for k, v in ref_sig.items() if v]
        overlap = sum(ref_sig[k] and cand_sig[k] for k in active) / max(1, len(active))
        candidate_coverage = sum(cand_sig.values()) / len(cand_sig)
        # lexical/context balance reduces dependence on literal keyword overlap.
        score = 100 * (0.68 * lexical[i] + 0.24 * overlap + 0.08 * candidate_coverage)
        shared = [k.replace("_", " ") for k in active if cand_sig[k]]
        if not shared:
            shared = ["school-education professional context"]
        explanation = "Matches on " + ", ".join(shared[:4]) + ". "
        if row.get("experience_indicators"):
            explanation += "Evidence: " + str(row["experience_indicators"])[:220]
        results.append({**row, "relevance_score": round(float(score), 1),
                        "lexical_similarity": round(float(lexical[i]), 3),
                        "context_overlap": round(float(overlap), 3),
                        "match_explanation": explanation})
    return sorted(results, key=lambda x: x["relevance_score"], reverse=True)[:top_n]
