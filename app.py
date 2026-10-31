from pathlib import Path
import pandas as pd
import streamlit as st
from src.ranker import rank_profiles

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "profiles.csv"
st.set_page_config(page_title="School Influencer Discovery | EDXSO", page_icon="🎓", layout="wide")
st.title("🎓 School Influencer Discovery Tool")
st.caption("EDXSO AI Intern Assignment · Explainable profile discovery MVP")

@st.cache_data
def load_data():
    return pd.read_csv(DATA).fillna("")

profiles = load_data()
with st.sidebar:
    st.header("Discovery settings")
    top_n = st.slider("Number of profiles to show", 5, min(25, len(profiles)), 20)
    st.caption(f"Dataset: {len(profiles)} sourced public professional records")
    st.markdown("**Data access**\n\nNo LinkedIn login, scraping, CAPTCHA bypass, or restricted data access is used.")

st.subheader("1. Add a reference professional")
mode = st.radio("Input method", ["Paste profile details (recommended)", "Use a dataset example"], horizontal=True)
if mode == "Use a dataset example":
    labels = {f"{r['name']} — {r['current_role']}, {r['organisation']}": i for i, r in profiles.iterrows()}
    selected = st.selectbox("Choose reference", list(labels))
    ref_row = profiles.iloc[labels[selected]]
    reference = " ".join(str(ref_row[c]) for c in ["current_role", "organisation", "location", "experience_indicators", "profile_text"])
    ref_url = str(ref_row["linkedin_url"])
else:
    ref_url = st.text_input("LinkedIn profile URL (optional)", placeholder="https://www.linkedin.com/in/...")
    reference = st.text_area("Paste publicly accessible profile headline, role, About and experience text", height=180,
        placeholder="Example: School consultant advising K-12 school groups on growth, admissions, operations, CBSE affiliation and teacher development...")
    st.caption("The URL is recorded for reference only. The app does not fetch LinkedIn content; paste text you are authorised to use.")

st.subheader("2. Discover and rank similar professionals")
if st.button("Analyze and discover profiles", type="primary", use_container_width=True):
    if len(reference.strip()) < 25:
        st.error("Please provide at least 25 characters of profile context, or select a dataset example.")
    else:
        candidate_rows = profiles.to_dict("records")
        # Exclude the reference person when a known LinkedIn URL or dataset example is used.
        if ref_url:
            candidate_rows = [r for r in candidate_rows if str(r.get("linkedin_url", "")).strip().lower() != ref_url.strip().lower()]
        results = rank_profiles(reference, candidate_rows, top_n=top_n)
        st.session_state["results"] = results
        st.session_state["reference_url"] = ref_url

if "results" in st.session_state:
    results = st.session_state["results"]
    st.success(f"Ranked {len(results)} candidate profiles from the sourced test corpus.")
    st.info("Scores are relative relevance indicators, not probabilities or endorsements. Review source evidence before outreach.")
    for rank, p in enumerate(results, 1):
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"**#{rank} · {p['name']}**")
                st.write(f"{p['current_role']} · {p['organisation']} · {p['location']}")
                st.write(p["match_explanation"])
                st.caption("Indicators: " + str(p["experience_indicators"]))
                if p.get("linkedin_url"):
                    st.markdown(f"[LinkedIn profile]({p['linkedin_url']})")
                st.markdown(f"[Evidence source]({p['source_url']}) · {p['source_type']}")
            with c2:
                st.metric("Relevance", f"{p['relevance_score']:.1f}/100")
                st.caption(f"TF-IDF: {p['lexical_similarity']:.2f}")
    export = pd.DataFrame(results)
    st.download_button("Download ranked results (CSV)", export.to_csv(index=False).encode("utf-8"),
                       "edxso_ranked_profiles.csv", "text/csv")

with st.expander("How the AI/ML ranking works"):
    st.markdown("""
    1. **Profile representation:** combines role, organisation, location, experience indicators and profile text.
    2. **TF-IDF:** word and bigram features represent professional context; cosine similarity measures textual proximity.
    3. **Context features:** rule-based signals identify school leadership, consulting/advisory, school groups, education networks and teacher development.
    4. **Hybrid score:** 68% TF-IDF similarity + 24% overlap of reference context signals + 8% candidate signal coverage.
    5. **Explanation:** displays the overlapping context categories and the source-backed experience indicators.

    This is an explainable baseline ranking model, not a trained neural network. It is suitable for an MVP and can be validated with human relevance labels before production.
    """)
with st.expander("Dataset and responsible-use notes"):
    st.write("The included corpus contains publicly documented school-ecosystem professionals. Source links are supplied per record. LinkedIn URLs are included only where verified in the source corpus; unavailable URLs are left blank rather than guessed.")
    st.write("Some directory entries provide only a name, title and organisation, so their profile text is intentionally brief. The tool must not infer unverified experience, contact details or relationships.")
    st.write("For production, use an authorised CRM, licensed provider, user-submitted profile data, or official public biographies with provenance and refresh dates.")
