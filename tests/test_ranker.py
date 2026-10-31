import pandas as pd
from src.ranker import rank_profiles


def test_returns_ranked_profiles_with_explanations():
    profiles = pd.read_csv("data/profiles.csv").fillna("").to_dict("records")
    results = rank_profiles(
        "Former school principal and education consultant supporting school groups, CBSE affiliation and teacher training",
        profiles,
        top_n=20,
    )
    assert len(results) == 20
    assert results[0]["relevance_score"] >= results[-1]["relevance_score"]
    assert all("match_explanation" in row and row["source_url"] for row in results)
