# app.py

import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm, calculate_risk_score

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Legal AI Assistant", layout="wide")
st.title("📄 Legal Contract Risk Analyzer")

# ----------------------------
# Input mode
# ----------------------------
mode = st.radio(
    "Choose input method",
    ["Upload File", "Paste Text"],
    horizontal=True
)

uploaded_file = None
pasted_text = ""

if mode == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload contract file",
        type=["pdf", "docx", "txt"]
    )
else:
    pasted_text = st.text_area(
        "Paste contract text here",
        height=300
    )

analyze_clicked = st.button("Analyze Contract", use_container_width=True)

# ----------------------------
# Processing
# ----------------------------
if analyze_clicked:

    # Decide what to send to parser
    input_source = uploaded_file if mode == "Upload File" else pasted_text

    raw_text = get_input_text(input_source)

    if not raw_text.strip():
        st.error("No text found in the input.")
        st.stop()

    language = detect_language(raw_text)
    st.info(f"Detected language: {language}")

    clauses = split_clauses(raw_text)

    results = []
    for clause in clauses:
        results.append(
            analyze_clause_with_llm(clause, language)
        )

    # ----------------------------
    # Risk Score
    # ----------------------------
    risk_score = calculate_risk_score(results)

    st.subheader("📊 Overall Risk Score")
    st.progress(risk_score / 100)
    st.write(f"**Risk Score:** {risk_score} / 100")

    # ----------------------------
    # Clause Analysis
    # ----------------------------
    st.subheader("🧩 Clause Analysis")

    for i, r in enumerate(results, 1):
        with st.expander(f"Clause {i} — Risk: {r['risk_level']}"):
            st.write(r["clause"])
            st.write("**Analysis**")
            st.write(r["analysis"])
