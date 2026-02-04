import streamlit as st
from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.ip_rules import is_ip_clause
from core.llm_engine import analyze_clause_with_llm
from core.risk_engine import calculate_ip_risk
from core.audit import log_audit
from utils.helpers import generate_pdf_bytes
import json

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Legal Assistant for SMEs", layout="wide")
st.title("Legal Assistant for SMEs")

# ------------------ INPUT ------------------
mode = st.radio("Choose input method", ["Paste IP Clause", "Upload Contract File"], horizontal=True)
raw_text = get_input_text(mode)
analyze_clicked = st.button("Analyze Contract")

# ------------------ PROCESS ------------------
if analyze_clicked:
    if not raw_text or len(raw_text.strip()) < 10:
        st.error("Please provide valid IP clause or contract text.")
        st.stop()

    lang = detect_language(raw_text)
    st.info(f"Detected language: {lang}")
    clauses = split_clauses(raw_text)
    st.success(f"Total clauses detected: {len(clauses)}")

    results = []

    # ------------------ CLAUSE ANALYSIS ------------------
    for i, clause in enumerate(clauses, 1):
        with st.container():
            st.markdown(f"### Clause {i}")
            st.write(clause)

            if is_ip_clause(clause):
                st.warning("Intellectual Property Risk Detected")
                llm_result = analyze_clause_with_llm(clause, lang)
                risk, score = calculate_ip_risk(llm_result)

                col1, col2, col3 = st.columns(3)
                col1.metric("Ownership", llm_result["ownership"])
                col2.metric("Exclusivity", llm_result["exclusivity"])
                col3.metric("Risk Level", risk)

                # ------------------ FRIENDLY OUTPUT ------------------
                try:
                    reason_data = json.loads(llm_result["risk_reason"])
                except Exception:
                    reason_data = {"RiskExplanation": llm_result["risk_reason"],
                                   "SaferAlternative": llm_result.get("suggested_fix", "")}

                st.markdown("**Reason / Explanation:**")
                st.write(reason_data.get("RiskExplanation", ""))

                st.markdown("**Safer Alternative / Suggestion:**")
                st.write(reason_data.get("SaferAlternative", llm_result.get("suggested_fix", "")))

                st.markdown(f"**Risk Score:** {score}/100")

                results.append({
                    "clause": clause,
                    "analysis": llm_result,
                    "risk": risk,
                    "score": score
                })
            else:
                st.success("No IP-related risk found in this clause.")

    # ------------------ EXPORT & AUDIT ------------------
    if results:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Export PDF Report"):
                pdf_bytes = generate_pdf_bytes(results)
                st.download_button(
                    "Download PDF",
                    pdf_bytes,
                    file_name="ip_risk_report.pdf",
                    mime="application/pdf"
                )

        with col2:
            # Audit log auto-update
            log_audit(results)
            st.success("Audit log updated")
