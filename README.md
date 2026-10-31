# EDXSO — School Influencer Discovery Tool

A Streamlit MVP for discovering and ranking school-education professionals from a reference profile. It follows the assignment workflow: **Reference Profile → AI Analysis → Similar Profile Discovery → Ranking → Results**.

## Quick start (Windows PowerShell)

```powershell
cd edxso_school_influencer_mvp
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`). Do not upload `.venv/` or `__pycache__/` to GitHub.

## Use the MVP

1. Choose **Paste profile details** and paste profile text you are authorised to use, or choose **Use a dataset example**.
2. Click **Analyze and discover profiles**.
3. Review ranked candidates, score, matching context, LinkedIn link (where verified), and evidence source.
4. Download the ranked CSV.

The LinkedIn URL field is metadata only. This app does not automatically access LinkedIn or scrape profiles. Paste the reference profile's text manually.

## ML method

The ranker uses scikit-learn TF-IDF with word/bigram features and cosine similarity, combined with interpretable professional-context signals. Final score = 0.68 × lexical similarity + 0.24 × reference-signal overlap + 0.08 × candidate-signal coverage, scaled to 100. It is a baseline similarity/ranking approach, not a probability. Details are in `docs/TECHNICAL_NOTE.md`.

## Dataset

`data/profiles.csv` contains 25 sourced public professional records. Each row includes a source URL and source type. LinkedIn URLs are populated only when a matching public profile URL was verified; otherwise the field is blank. This is a **curated public-source test corpus**, not a comprehensive or live LinkedIn index. Several association-directory records have limited biography detail; the app does not invent missing facts. `data/source_register.csv` lists source pages.

## Deploy

### Streamlit Community Cloud
1. Push this folder to a GitHub repository (exclude `.venv/`, `.streamlit/secrets.toml`, caches and local exports).
2. In Streamlit Community Cloud, create an app from the repository.
3. Set main file path to `app.py`.
4. Deploy. No API key or secret is required for this offline-dataset MVP.

### GitHub
```powershell
git init
git add .
git commit -m "Build EDXSO school influencer discovery MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/edxso-school-influencer-discovery.git
git push -u origin main
```

## Project structure

```text
app.py
requirements.txt
src/ranker.py
data/profiles.csv
data/source_register.csv
docs/TECHNICAL_NOTE.md
docs/DEMO_SCRIPT.md
```

## Limitations and next steps

- The corpus is a static test dataset; it does not discover arbitrary new LinkedIn profiles live.
- Some records have sparse public source data; ranking quality depends on input and evidence completeness.
- Scores need evaluation against human-labelled relevant/irrelevant pairs before business use.
- Production discovery requires an authorised data provider or user-submitted/consented data, provenance tracking, refresh policy, deduplication, and review controls.
- Do not use this tool to infer sensitive traits or scrape restricted platforms.
