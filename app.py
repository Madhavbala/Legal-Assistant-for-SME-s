# app.py

import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm
from utils.helpers import export_pdf

st.set_page_config(page_title="Legal Contract Risk Analyzer", layout="wide")

st.title("📄 Legal Contract Risk Analyzer")

# ---------------- INPUT ---------------- #

mode = st.radio(
    "Upload Contract or Paste Text",
    ["Upload File", "Paste Text"],
    horizontal=True,
)

raw_text = get_input_text(mode)

analyze_clicked = st.button("Analyze Contract", use_container_width=True)

# ---------------- ANALYSIS ---------------- #

if analyze_clicked and raw_text.strip():

    # 1. Language detection
    lang = detect_language(raw_text)
    st.success(f"Language detected: {lang}")

    # 2. Clause splitting
    clauses = split_clauses(raw_text)

    # remove junk clauses
    clauses = [c for c in clauses if len(c.strip()) > 30]

    if not clauses:
        st.error("No valid clauses detected.")
        st.stop()

    st.success(f"Total clauses detected: {len(clauses)}")

    results = []

    st.header("Clause Analysis Results")

    for idx, clause in enumerate(clauses, start=1):

        st.subheader(f"Clause {idx}")
        st.markdown("**Clause Text:**")
        st.write(clause)

        analysis = analyze_clause_with_llm(clause, lang)

        # Display clean output (NO JSON DUMP)
        st.markdown("### Risk Summary")
        st.markdown(f"""
- **Ownership:** {analysis["ownership"]}
- **Exclusivity:** {analysis["exclusivity"]}
- **Favor:** {analysis["favor"]}
""")

        st.markdown("**Why this is risky:**")
        st.write(analysis["risk_reason"])

        st.markdown("**Suggested Fix:**")
        st.write(analysis["suggested_fix"])

        results.append({
            "clause": clause,
            "analysis": analysis
        })

        st.divider()

    # ---------------- PDF EXPORT ---------------- #

    pdf_bytes = export_pdf(results)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="contract_risk_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

elif analyze_clicked:
    st.warning("Please upload a file or paste contract text.")
