import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm
from core.risk_engine import calculate_ip_risk
from core.audit import log_audit
from utils.helpers import export_pdf  # Corrected import

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="GenAI Legal Assistant for SMEs",
    layout="wide"
)

# ------------------ HEADER ------------------
st.markdown(
    """
    <h1 style="text-align:center;">GenAI Legal Assistant for SMEs</h1>
    <p style="text-align:center;color:gray;">
    Intellectual Property risk analysis using AI and rules
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ------------------ INPUT ------------------
st.subheader("Contract Input")

mode = st.radio(
    "Choose input method",
    ["Paste IP Clause", "Upload Contract File"],
    horizontal=True
)

raw_text = get_input_text(mode)

analyze_clicked = st.button("Analyze Contract", use_container_width=True)

# ------------------ PROCESS ------------------
if analyze_clicked:

    if not raw_text or len(raw_text.strip()) < 10:
        st.error("Please provide valid contract text.")
        st.stop()

    # Language detection
    lang = detect_language(raw_text)
    st.info(f"Detected language: {lang}")

    clauses = split_clauses(raw_text)
    st.success(f"Total clauses detected: {len(clauses)}")

    results = []

    st.markdown("---")
    st.subheader("Clause-wise Analysis")

    # ------------------ ANALYSIS LOOP ------------------
    for idx, clause in enumerate(clauses, 1):

        st.markdown(
            f"""
            <div style="border:1px solid #ddd;padding:12px;border-radius:6px;">
            <b>Clause {idx}</b><br>
            {clause}
            </div>
            """,
            unsafe_allow_html=True
        )

        # LLM analysis with safe try/except
        try:
            llm_result = analyze_clause_with_llm(clause, lang)
        except Exception as e:
            llm_result = {
                "ownership": "unclear",
                "exclusivity": "unclear",
                "favor": "unclear",
                "risk_reason": f"LLM error: {str(e)}",
                "suggested_fix": "Manual legal review recommended."
            }

        # Safe defaults
        ownership = llm_result.get("ownership", "Unknown")
        exclusivity = llm_result.get("exclusivity", "Unknown")
        risk_reason = llm_result.get("risk_reason", "Not specified")
        suggested_fix = llm_result.get("suggested_fix", "No suggestion available")

        # English translation for PDF (Hindi-safe)
        llm_result.setdefault(
            "english_translation",
            llm_result.get("translated_clause", clause)
        )

        risk, score = calculate_ip_risk(llm_result)

        # Risk indicator
        if score >= 30:
            st.warning("Intellectual Property risk detected")
        else:
            st.success("No significant Intellectual Property risk detected")

        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Ownership", ownership)
        col2.metric("Exclusivity", exclusivity)
        col3.metric("Risk Level", risk)

        st.markdown("Reason for risk")
        st.write(risk_reason)

        st.markdown("Recommended alternative")
        st.write(suggested_fix)

        st.markdown(f"Risk score: {score}/100")
        st.markdown("---")

        results.append({
            "clause": clause,
            "analysis": {
                "ownership": ownership,
                "exclusivity": exclusivity,
                "risk_reason": risk_reason,
                "suggested_fix": suggested_fix,
                "english_translation": llm_result["english_translation"]
            },
            "risk": risk,
            "score": score
        })

    # ------------------ AUTO AUDIT LOG ------------------
    log_audit(results, language=lang)

    # ------------------ EXPORT ------------------
    if results:
        st.subheader("Export")

        # Use correct helpers.py function
        pdf_path, pdf_buffer = export_pdf(results)

        st.success("PDF generated and audit log updated")

        st.download_button(
            label="Download PDF report",
            data=pdf_buffer,
            file_name="ip_risk_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.info("Enter contract text and click Analyze Contract to continue.")
