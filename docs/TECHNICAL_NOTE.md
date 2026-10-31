# Technical Note — EDXSO School Influencer Discovery MVP

## 1. Objective
Build an MVP that accepts one school-ecosystem professional as a reference, analyses professional context, ranks similar professionals, and explains each result. The implementation follows the assignment's reference → analysis → discovery → ranking → results flow.

## 2. Architecture
- **UI:** Streamlit (`app.py`) for reference input, dataset example selection, result cards and CSV export.
- **Data:** curated CSV corpus (`data/profiles.csv`) with per-record source URL and source type.
- **Ranking:** scikit-learn TF-IDF vectorisation and cosine similarity, augmented by interpretable context signals (`src/ranker.py`).
- **Output:** relevance score, lexical similarity, context overlap, matching rationale and evidence link.

## 3. Data retrieval and compliance
The bundled dataset is a static curated public-source test corpus, not a live LinkedIn scrape. It includes publicly documented professionals from institutional biographies, professional association directories and two public LinkedIn profile pages. Each row has a provenance URL. LinkedIn URLs are blank where they could not be verified. No login, CAPTCHA, authentication bypass, private data, or restricted endpoints are used. The reference LinkedIn URL is not fetched; the user pastes profile text they are authorised to process.

The corpus has 25 records, but evidence depth varies. Association directory records can contain only role and organisation. The system deliberately does not manufacture missing details. This satisfies an end-to-end demonstration with a clearly identified test corpus; it is not proof of live discovery across all LinkedIn members.

## 4. AI/ML method
1. Concatenate current role, organisation, location, experience indicators and profile text.
2. Convert text to TF-IDF features using unigrams and bigrams, English stop-word removal and sublinear term frequency.
3. Compute cosine similarity between reference and each candidate.
4. Extract five interpretable professional context categories: school leadership, consulting/advisory, school groups, education networks and teacher development.
5. Calculate a hybrid score:

   `score = 100 × (0.68 × TF-IDF cosine + 0.24 × context overlap + 0.08 × candidate signal coverage)`

   Context overlap is the fraction of active reference categories also present in the candidate. Candidate coverage is the fraction of the five categories detected in the candidate.
6. Explain the match with shared categories and the source-backed experience indicators.

The score is a relative ranking heuristic, not a calibrated probability or an endorsement. A production system should tune weights using a labelled dataset and evaluate Precision@K, Recall@K, NDCG@K and inter-rater agreement.

## 5. Ranking and relevance
The model combines lexical similarity with professional context so that a principal, school-group operator, consultant or education-network leader can rank well even when their exact wording differs. The source evidence is shown beside each candidate so a reviewer can validate the match.

## 6. Limitations
- Static dataset; no real-time or arbitrary LinkedIn discovery.
- Uneven public biography detail and incomplete LinkedIn URL coverage.
- TF-IDF is a lexical baseline and does not understand deep semantics like a transformer embedding model.
- Rule-based context signals can miss synonyms and need expert review.
- Similarity does not establish influence, personal relationships, willingness to engage or suitability for outreach.

## 7. Production path
Use a licensed/authorised people-data API, the organisation's CRM, user-submitted profile exports with permission, or public institutional biographies. Store source, retrieval date, permitted purpose and retention period. Add deduplication, freshness checks, human review, opt-out/removal handling and audit logs. Validate ranking with human-labelled examples before use.

## 8. Local setup
See the root `README.md`. Dependencies are listed in `requirements.txt`; no secrets or API keys are required.
