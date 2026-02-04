import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.ip_rules import is_ip_clause
from core.llm_engine import analyze_clause_with_llm
from core.risk_engine import calculate_ip_risk
from core.audit import log_audit
from utils.helpers import export_pdf

st.set_page_config(
    page_title="GenAI Legal Assistant for SMEs",
    layout="wide"
)

st.title("GenAI Legal Assistant for SMEs")
st.write("Contract IP risk analysis using rules and LLM")

mode = st.radio(
    "Choose input method",
    ["Paste IP Clause", "Upload Contract File"],
    horizontal=True
)

raw_text = get_input_text(mode)

analyze_clicked = st.button("Analyze Contract", use_container_width=True)

if analyze_clicked:

    if not raw_text or len(raw_text.strip()) < 10:
        st.error("Please provide valid contract text.")
        st.stop()

    lang = detect_language(raw_text)
    st.info(f"Detected language: {lang}")

    clauses = split_clauses(raw_text)
    st.success(f"Total clauses detected: {len(clauses)}")

    results = []

    for i, clause in enumerate(clauses, 1):

        st.subheader(f"Clause {i}")
        st.write(clause)

        if is_ip_clause(clause):

            llm_result = analyze_clause_with_llm(clause, lang)
            risk, score = calculate_ip_risk(llm_result)

            st.write("Ownership:", llm_result["ownership"])
            st.write("Exclusivity:", llm_result["exclusivity"])
            st.write("Risk level:", risk)
            st.write("Reason:", llm_result["risk_reason"])
            st.write("Suggested fix:", llm_result["suggested_fix"])
            st.write("Risk score:", score)

            result_entry = {
                "clause": clause,
                "analysis": llm_result,
                "risk": risk,
                "score": score
            }

            results.append(result_entry)

            log_audit(result_entry)

        else:
            st.write("No IP-related risk found in this clause.")

        st.divider()

    if results:
        if st.button("Export PDF", use_container_width=True):
            pdf_path = export_pdf(results)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    data=f,
                    file_name="ip_risk_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
