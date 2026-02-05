import streamlit as st

from core.parser import get_input_text
from core.language import detect_language
from core.clause_splitter import split_clauses
from core.llm_engine import analyze_clause_with_llm, calculate_risk_score
from utils.helpers import export_pdf

# -------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Legal Contract Risk Analyzer",
    layout="wide"
)

st.title("📄 Legal Contract Risk Analyzer")
st.caption("Upload a contract or paste text to identify legal risks")

# -------------------------------------------------
# Input Mode
# -------------------------------------------------
mode = st.radio(
    "Choose input method",
    ["Upload File", "Paste Text"],
    horizontal=True
)

uploaded_file = None
pasted_text = None

if mode == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload contract file",
        type=["pdf", "docx", "doc", "txt"]
    )
else:
    pasted_text = st.text_area(
        "Paste contract text here",
        height=300
    )

# -------------------------------------------------
# Analyze Button
# -------------------------------------------------
analyze_clicked = st.button(
    "🔍 Analyze Contract",
    use_container_width=True
)

if analyze_clicked:

    # 1️⃣ Extract text safely
    raw_text = get_input_text(uploaded_file, pasted_text)

    if not raw_text or len(raw_text.strip()) < 50:
        st.error("Please upload a valid contract or paste sufficient text.")
        st.stop()

    # 2️⃣ Detect language
    lang = detect_language(raw_text)
    st.success(f"Language detected: {lang.capitalize()}")

    # 3️⃣ Split clauses
    clauses = split_clauses(raw_text)

    if not clauses:
        st.error("No clauses detected in the document.")
        st.stop()

    st.info(f"Total clauses detected: {len(clauses)}")

    # 4️⃣ Analyze each clause
    results = []

    for clause in clauses:
        analysis = analyze_clause_with_llm(clause, lang)
        analysis["clause"] = clause

        # Add numeric risk score
        analysis["risk_score"] = calculate_risk_score(analysis)

        results.append(analysis)

    # -------------------------------------------------
    # Display Results (CLIENT FRIENDLY – NO JSON)
    # -------------------------------------------------
    st.subheader("🧩 Clause Risk Analysis")

    for i, r in enumerate(results, 1):
        with st.expander(
            f"Clause {i} — Risk Score: {r['risk_score']}/100",
            expanded=False
        ):
            st.markdown("### 📄 Clause Text")
            st.write(r["clause"])

            st.markdown("### ⚠️ Risk Summary")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Ownership", r["ownership"].capitalize())

            with c2:
                st.metric("Exclusivity", r["exclusivity"].capitalize())

            with c3:
                st.metric("Favors", r["favor"].capitalize())

            st.markdown("### 🧠 Why this is risky")
            st.write(r["risk_reason"])

            st.markdown("### ✅ Recommended Fix")
            st.write(r["suggested_fix"])

    # -------------------------------------------------
    # PDF Export
    # -------------------------------------------------
    pdf_bytes = export_pdf(results)

    st.download_button(
        label="📥 Download Risk Report (PDF)",
        data=pdf_bytes,
        file_name="contract_risk_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
