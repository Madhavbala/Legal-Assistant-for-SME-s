import streamlit as st

from core.parser import get_input_text
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm
from utils.helpers import export_pdf

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Legal Assistant for SMEs",
    layout="wide"
)

st.title("📄 Legal Contract Risk Analyzer")

# --------------------------------------------------
# Input Section
# --------------------------------------------------
st.subheader("Upload Contract or Paste Text")

uploaded_file = st.file_uploader(
    "Upload contract file",
    type=["pdf", "docx", "txt"]  # DO NOT add "doc"
)

pasted_text = st.text_area(
    "Or paste contract text here",
    height=250,
    placeholder="Paste contract text here..."
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------
analyze_clicked = st.button(
    "Analyze Contract",
    use_container_width=True
)

# --------------------------------------------------
# Main Logic
# --------------------------------------------------
if analyze_clicked:

    if not uploaded_file and not pasted_text.strip():
        st.error("Please upload a file or paste contract text.")
        st.stop()

    # 1. Extract text + detect language
    raw_text, lang = get_input_text(uploaded_file, pasted_text)

    if not raw_text.strip():
        st.error("Could not extract any readable text.")
        st.stop()

    st.success(f"Language detected: {lang}")

    # 2. Clause splitting
    clauses = split_clauses(raw_text, lang)

    if not clauses:
        st.error("No clauses detected in the document.")
        st.stop()

    st.info(f"Total clauses detected: {len(clauses)}")

    # 3. Analyze each clause with LLM
    results = []

    with st.spinner("Analyzing clauses..."):
        for idx, clause in enumerate(clauses, start=1):
            analysis = analyze_clause_with_llm(clause, lang)
            results.append({
                "clause_no": idx,
                "clause_text": clause,
                "analysis": analysis
            })

    # 4. Display results
    st.subheader("Clause Analysis Results")

    for r in results:
        with st.expander(f"Clause {r['clause_no']}"):
            st.markdown("**Clause Text:**")
            st.write(r["clause_text"])

            st.markdown("**Risk Analysis:**")
            st.write(r["analysis"])

    # 5. Export PDF
    pdf_bytes = export_pdf(results)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="contract_risk_report.pdf",
        mime="application/pdf"
    )
