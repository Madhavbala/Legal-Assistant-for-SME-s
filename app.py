import streamlit as st
from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.ip_rules import is_ip_clause
from core.llm_engine import analyze_clause_with_llm
from core.risk_engine import calculate_ip_risk
from core.audit import log_audit
from utils.helpers import generate_pdf_bytes

st.set_page_config(
    page_title="GenAI Legal Assistant for SMEs",
    layout="wide"
)

st.title("GenAI Legal Assistant for SMEs")
st.write("Analyze contract text for Intellectual Property risks")

mode = st.radio(
    "Choose input method",
    ["Paste Text", "Upload File"],
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

    st.subheader("Analysis Results")

    for i, clause in enumerate(clauses, 1):
        st.markdown(f"Clause {i}")
        st.write(clause)

        if is_ip_clause(clause):
            llm_result = analyze_clause_with_llm(clause, lang)
            risk, score = calculate_ip_risk(llm_result)

            col1, col2, col3 = st.columns(3)
            col1.metric("Ownership", llm_result.get("ownership", "Unknown"))
            col2.metric("Exclusivity", llm_result.get("exclusivity", "Unknown"))
            col3.metric("Risk Level", risk)

            st.write("Reason")
            st.write(llm_result.get("risk_reason", ""))

            st.write("Suggested Alternative")
            st.write(llm_result.get("suggested_fix", ""))

            st.write(f"Risk Score: {score}/100")

            result = {
                "clause": clause,
                "language": lang,
                "ownership": llm_result.get("ownership"),
                "exclusivity": llm_result.get("exclusivity"),
                "risk": risk,
                "score": score,
                "reason": llm_result.get("risk_reason"),
                "suggestion": llm_result.get("suggested_fix"),
            }

            results.append(result)
            log_audit(result)
        else:
            st.write("No IP-related risk found in this clause.")

        st.divider()

    if results:
        pdf_bytes = generate_pdf_bytes(results)

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="ip_risk_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("Provide contract text and click Analyze Contract.")
