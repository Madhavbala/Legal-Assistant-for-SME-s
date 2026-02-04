import streamlit as st
import re
from typing import List, Dict

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="SME Legal IP Risk Assistant", layout="wide")

# ===============================
# SIMPLE LANGUAGE DETECTION
# ===============================
def detect_language(text: str) -> str:
    if re.search(r'[\u0900-\u097F]', text):
        return "Hindi"
    return "English"

# ===============================
# CLAUSE SPLITTER
# ===============================
def split_clauses(text: str) -> List[str]:
    clauses = re.split(r'\n+|(?<=\.)\s+', text)
    return [c.strip() for c in clauses if len(c.strip()) > 10]

# ===============================
# IP CLAUSE DETECTION (RULE BASED)
# ===============================
def is_ip_clause(text: str) -> bool:
    keywords = [
        "intellectual property",
        "ip rights",
        "ownership",
        "work made for hire",
        "shall vest",
        "exclusive rights",
        "copyright",
        "patent",
        "trademark"
    ]
    text_lower = text.lower()
    return any(k in text_lower for k in keywords)

# ===============================
# IP RISK ANALYSIS (NO LLM)
# ===============================
def analyze_ip_clause(clause: str) -> Dict:
    text = clause.lower()

    ownership = "Unclear"
    exclusivity = "Unclear"
    risk = "Low"
    score = 20
    reason = []
    fix = []

    if "shall vest" in text or "exclusive" in text:
        ownership = "Company"
        exclusivity = "Exclusive"
        risk = "High"
        score = 75
        reason.append("Clause assigns all IP exclusively to the company.")
        fix.append("Limit IP ownership to work created specifically for this engagement.")

    if "all intellectual property" in text:
        risk = "High"
        score = max(score, 80)
        reason.append("Scope of IP is overly broad.")
        fix.append("Define IP scope clearly (background IP vs project IP).")

    if ownership == "Unclear":
        reason.append("IP ownership is not clearly defined.")
        fix.append("Explicitly state who owns newly created IP.")

    return {
        "ownership": ownership,
        "exclusivity": exclusivity,
        "risk": risk,
        "score": score,
        "reason": " ".join(reason),
        "fix": " ".join(fix)
    }

# ===============================
# UI
# ===============================
st.title("📜 SME Legal IP Risk Assistant")

contract_text = st.text_area(
    "Paste contract clause(s) here",
    height=200,
    placeholder="Paste legal text here..."
)

if st.button("Analyze"):
    if not contract_text.strip():
        st.warning("Please enter contract text.")
        st.stop()

    language = detect_language(contract_text)
    clauses = split_clauses(contract_text)

    st.markdown(f"**Detected language:** {language}")
    st.markdown(f"**Total clauses detected:** {len(clauses)}")

    for i, clause in enumerate(clauses, start=1):
        st.markdown("---")
        st.subheader(f"Clause {i}")
        st.write(clause)

        if is_ip_clause(clause):
            result = analyze_ip_clause(clause)

            st.markdown(f"**Ownership:** {result['ownership']}")
            st.markdown(f"**Exclusivity:** {result['exclusivity']}")
            st.markdown(f"**Risk level:** {result['risk']}")
            st.markdown(f"**Risk score:** {result['score']}")

            st.markdown("**Reason:**")
            st.write(result["reason"])

            st.markdown("**Suggested fix:**")
            st.write(result["fix"])
        else:
            st.info("No intellectual property risk detected in this clause.")
