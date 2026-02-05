import streamlit as st

from core.parser import get_input_text
from core.clause_splitter import split_clauses
from core.ip_rules import is_ip_clause
from core.llm_engine import analyze_clause_with_llm
from core.risk_engine import calculate_ip_risk
from core.audit import log_audit
from utils.helpers import export_pdf


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Legal Assistant for SMEs",
    layout="wide"
)

st.title("Legal Assistant for SMEs")
st.write("Analyze intellectual property risks in contracts")


# ---------------- INPUT SECTION ----------------
st.subheader("Input")

mode = st.radio(
    "Choose input method",
    ["Paste IP Clause", "Upload Contract File"],
    horizontal=True
)

uploaded_file = None
pasted_text = ""

if mode == "Paste IP Clause":
    pasted_text = st.text_area(
        "Enter IP clause or contract text",
        height=220
    )
else:
    uploaded_file = st.file_uploader(
        "Upload contract file",
        type=["pdf", "docx", "doc", "txt"]
    )

analyze_clicked = st.button("Analyze Contract", use_container_width=True)


# ---------------- ANALYSIS ----------------
if analyze_clicked:

    raw_text, lang = get_input_text(uploaded_file, pasted_text)

    if not raw_text or len(raw_text.strip()) < 10:
        st.error("Please provide valid contract text")
        st.stop()

    st.info(f"Detected language: {lang}")

    clauses = split_clauses(raw_text)

    st.success(f"Total clauses detected: {len(clauses)}")

    results = []

    st.subheader("Analysis Results")

    for idx, clause in enumerate(clauses, start=1):

        st.markdown(f"### Clause {idx}")
        st.write(clause)

        if is_ip_clause(clause):

            st.warning("Intellectual Property Risk Detected")

            llm_result = analyze_clause_with_llm(clause, lang)

            risk_label, score = calculate_ip_risk(llm_result)

            col1, col2, col3 = st.columns(3)
            col1.metric("Ownership", llm_result["ownership"])
            col2.metric("Exclusivity", llm_result["exclusivity"])
            col3.metric("Risk Level", risk_label)

            st.markdown("Reason / Explanation")
            st.write(llm_result["risk_reason"])

            st.markdown("Safer Alternative / Suggestion")
            st.write(llm_result["suggested_fix"])

            st.write(f"Risk Score: {score}/100")

            results.append({
                "clause": clause,
                "analysis": llm_result,
                "risk": risk_label,
                "score": score
            })

        else:
            st.success("No IP-related risk found in this clause")

        st.markdown("---")

    # ---------------- AUDIT LOG ----------------
    if results:
        log_audit(raw_text, results)
        st.success("Audit log updated")

    # ---------------- PDF EXPORT ----------------
    if results:
        pdf_bytes = export_pdf(results)

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="ip_risk_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.info("Enter contract text and click Analyze Contract to continue")
