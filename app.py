import streamlit as st
from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.ip_rules import is_ip_clause, infer_ip_meaning
from core.llm_engine import analyze_clause_with_llm
from core.risk_engine import calculate_ip_risk
from core.audit import log_audit
from utils.helpers import generate_pdf_bytes

st.set_page_config(page_title="Legal Assistant for SMEs", layout="wide")

st.header("Legal Assistant for SMEs")

mode = st.radio("Choose input method", ["Paste IP Clause", "Upload Contract File"], horizontal=True)

raw_text = get_input_text(mode)

analyze_clicked = st.button("Analyze Contract")

if analyze_clicked:
    if not raw_text or len(raw_text.strip()) < 10:
        st.error("Please provide valid IP clause or contract text.")
        st.stop()

    lang = detect_language(raw_text)
    st.info(f"Detected language: {lang}")

    clauses = split_clauses(raw_text)
    st.success(f"Total clauses detected: {len(clauses)}")

    results = []

    for i, clause in enumerate(clauses, 1):
        st.markdown(f"### Clause {i}")
        st.write(clause)

        if is_ip_clause(clause):
            rule_result = infer_ip_meaning(clause)
            llm_result = analyze_clause_with_llm(clause, lang)

            combined_result = {
                "ownership": rule_result.get("ownership", "Unknown"),
                "exclusivity": rule_result.get("exclusivity", "Unknown"),
                "risk_reason": llm_result.get("risk_reason", ""),
                "suggested_fix": llm_result.get("suggested_fix", "")
            }

            risk, score = calculate_ip_risk(combined_result)

            st.write("Ownership:", combined_result["ownership"])
            st.write("Exclusivity:", combined_result["exclusivity"])
            st.write("Risk Level:", risk)
            st.write("Reason / Explanation:", combined_result["risk_reason"])
            st.write("Safer Alternative / Suggestion:", combined_result["suggested_fix"])
            st.write("Risk Score:", score)

            results.append({
                "clause": clause,
                "analysis": combined_result,
                "risk": risk,
                "score": score
            })
        else:
            st.write("No IP-related risk found in this clause.")

    if results:
        if st.button("Export PDF Report"):
            pdf_bytes = generate_pdf_bytes(results)
            st.download_button("Download PDF", pdf_bytes, file_name="ip_risk_report.pdf")
        
        log_audit(results)
        st.success("Audit log updated")
