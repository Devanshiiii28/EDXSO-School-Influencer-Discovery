# 5–10 Minute Demo Script

## 0:00–1:00 — Problem and objective
Explain that school-network outreach requires identifying principals, former principals, school owners, consultants, education entrepreneurs and professionals connected to multiple schools. The MVP ranks sourced public profiles against one reference profile.

## 1:00–2:00 — Show the interface
Open the Streamlit app. Point out the reference input, dataset example option, number-of-results control and responsible-use note. Clarify that the LinkedIn URL is not scraped; profile text is pasted by the user.

## 2:00–3:00 — Run a reference example
Select Kiran Dalal or paste a school consultant/principal profile summary. Click **Analyze and discover profiles**. Explain the input representation: role, organisation, location and experience indicators.

## 3:00–5:00 — Explain ranking
Show ranked candidates and relevance scores. Explain TF-IDF cosine similarity, the five professional-context signals and the 68/24/8 hybrid score. Open an evidence source link to demonstrate traceability.

## 5:00–6:30 — Inspect results
Compare candidates with school leadership, school-group operations, consulting, education networks and teacher-development indicators. Explain that scores are relative, not probabilities, and sparse records need manual validation.

## 6:30–7:30 — Export
Download the ranked CSV and show that it includes score, explanation, profile URL where verified and evidence source.

## 7:30–9:00 — Architecture and limitations
Show `src/ranker.py`, `data/profiles.csv`, `source_register.csv` and the technical note. Explain no LinkedIn scraping or access-control bypass; the static dataset is a test corpus. Discuss authorised data-provider/CRM integration as the production path.

## Closing
The MVP demonstrates the complete workflow using traceable public-source data and an explainable ML baseline. Next step: collect human relevance labels and evaluate Precision@20/NDCG@20 before production rollout.
