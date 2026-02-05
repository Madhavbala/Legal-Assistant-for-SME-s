import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm, calculate_risk_score
from utils.helpers import export_pdf

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="Legal Contract Risk Analyzer",
    layout="wide"
)

st.title("📄 Legal Contract Risk Analyzer")

# ----------------------------
# Input Section
# ----------------------------
st.subheader("Upload Contract or Paste Text")

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
        type=["pdf", "docx", "doc", "txt"]
    )
else:
    pasted_text = st.text_area(
        "Paste contract text here",
        height=250
    )

# ----------------------------
# Analyze Button
# ----------------------------
analyze_clicked = st.button(
    "Analyze Contract",
    use_container_width=True
)

# ----------------------------
# Processing
# ----------------------------
if analyze_clicked:

    raw_text = get_input_text(
        mode=mode,
        uploaded_file=uploaded_file,
        pasted_text=pasted_text
    )

    if not raw_text.strip():
        st.error("No text found. Please upload a valid file or paste text.")
        st.stop()

    # 1. Language detection
    lang = detect_language(raw_text)
    st.success(f"Language detected: {lang}")

    # 2. Clause splitting
    clauses = split_clauses(raw_text)

    if not clauses:
        st.error("No clauses detected.")
        st.stop()

    st.info(f"Total clauses detected: {len(clauses)}")

    # 3. Clause analysis
    results = []

    st.subheader("Clause Analysis Results")

    for idx, clause in enumerate(clauses, start=1):

        st.markdown(f"### Clause {idx}")
        st.write(clause)

        analysis = analyze_clause_with_llm(clause, lang)

        risk_score = calculate_risk_score(analysis)

        # --- Friendly UI (NO JSON) ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Ownership", analysis.get("ownership", "Unknown"))

        with col2:
            st.metric("Exclusivity", analysis.get("exclusivity", "Unknown"))

        with col3:
            st.metric("Risk Score", f"{risk_score}/100")

        if risk_score >= 70:
            st.error("High Risk Clause")
        elif risk_score >= 40:
            st.warning("Medium Risk Clause")
        else:
            st.success("Low Risk Clause")

        st.markdown("**Reason / Explanation:**")
        st.write(analysis.get("risk_reason", "N/A"))

        st.markdown("**Safer Alternative / Suggestion:**")
        st.write(analysis.get("suggested_fix", "N/A"))

        st.divider()

        results.append({
            "clause": clause,
            "analysis": analysis,
            "risk_score": risk_score
        })

    # ----------------------------
    # PDF Export
    # ----------------------------
    pdf_bytes = export_pdf(results)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="contract_risk_report.pdf",
        mime="application/pdf"
    )
