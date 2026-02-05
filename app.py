# app.py

import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm, calculate_risk_score

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Legal AI Assistant", layout="wide")
st.title("📄 Legal Contract Risk Analyzer")

# ----------------------------
# Input Section
# ----------------------------
mode = st.radio(
    "Choose input method",
    ["Paste Text"],
    horizontal=True
)

pasted_text = st.text_area(
    "Paste contract text here",
    height=300
)

analyze_clicked = st.button("Analyze Contract", use_container_width=True)

# ----------------------------
# Processing
# ----------------------------
if analyze_clicked and pasted_text.strip():

    raw_text = get_input_text(mode, pasted_text)
    language = detect_language(raw_text)

    st.info(f"Detected language: {language}")

    clauses = split_clauses(raw_text)

    results = []
    for clause in clauses:
        result = analyze_clause_with_llm(clause, language)
        results.append(result)

    # ----------------------------
    # Risk Score
    # ----------------------------
    risk_score = calculate_risk_score(results)

    st.subheader("📊 Overall Risk Score")
    st.progress(risk_score / 100)
    st.write(f"**Risk Score:** {risk_score} / 100")

    # ----------------------------
    # Clause Results
    # ----------------------------
    st.subheader("🧩 Clause Analysis")

    for idx, r in enumerate(results, start=1):
        with st.expander(f"Clause {idx} — Risk: {r['risk_level']}"):
            st.write(r["clause"])
            st.write("**Analysis:**")
            st.write(r["analysis"])

else:
    st.warning("Please paste contract text before clicking Analyze.")
