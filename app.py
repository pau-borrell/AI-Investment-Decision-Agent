"""Local portfolio walkthrough: streamlit run app.py."""
import json
import pandas as pd
import streamlit as st
from src.demo import run_offline_demo, DEFAULT_PORTFOLIO, DEFAULT_QUERY

st.set_page_config(page_title="Portfolio-aware Investment Agent", page_icon="📊", layout="wide")
st.title("Portfolio-aware Investment Agent")
st.caption("Offline analytics walkthrough · synthetic metadata · no model or market downloads")
st.info("This mode computes portfolio metrics and lexical retrieval. It does not generate an AI recommendation.")
with st.form("portfolio"):
    text = st.text_area("Holdings as a JSON mapping (amounts or weights in one currency)",
                        json.dumps(DEFAULT_PORTFOLIO, indent=2), height=160)
    question = st.text_input("Research question", DEFAULT_QUERY)
    submitted = st.form_submit_button("Analyze portfolio")
if submitted or "result" not in st.session_state:
    try:
        result = run_offline_demo(json.loads(text), question)
        st.session_state["result"] = result
    except (ValueError, TypeError) as exc:
        st.error(str(exc))
        st.stop()
result = st.session_state["result"]
analysis = result["portfolio_analysis"]
st.warning(result["notice"])
a, b, c = st.columns(3)
a.metric("Position HHI", f'{analysis["diversification"]["score"]:.3f}')
b.metric("Effective positions", f'{analysis["diversification"]["effective_positions"]:.2f}')
c.metric("Known sector/cash weight", f'{analysis["sector_known_weight"]:.1%}')
st.caption("Position HHI measures allocation across positions. It does not account for ETF constituent overlap.")
left, right = st.columns(2)
left.subheader("Portfolio weights")
left.bar_chart(pd.Series(analysis["portfolio_weights"], name="Weight"))
right.subheader("Sector look-through")
right.bar_chart(pd.Series(analysis["sector_exposure"], name="Weight"))
for warning in analysis["warnings"]:
    st.warning(warning)
st.subheader("Retrieved educational snippets")
for chunk in result["retrieved_chunks"]:
    with st.expander(chunk["metadata"]["source"]):
        st.write(chunk["text"])
        st.caption(f'Lexical source ID: {chunk["id"]}')
if not result["retrieved_chunks"]:
    st.write("No matching passages. The walkthrough does not invent evidence.")
st.download_button("Download analysis JSON", json.dumps(result, indent=2, allow_nan=False),
                   "portfolio_analysis.json", "application/json")
st.caption("For local Mistral generation, follow the live-agent setup in README.md.")
