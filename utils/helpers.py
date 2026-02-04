from io import BytesIO
from fpdf import FPDF

def generate_pdf_bytes(results):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "IP Risk Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)

    for idx, res in enumerate(results, 1):
        clause = res["clause"]
        analysis = res["analysis"]
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 8, f"Clause {idx}")
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, clause)
        pdf.ln(2)

        # Friendly output
        try:
            reason_data = json.loads(analysis.get("risk_reason", "{}"))
            explanation = reason_data.get("RiskExplanation", "")
            suggestion = reason_data.get("SaferAlternative", analysis.get("suggested_fix", ""))
        except Exception:
            explanation = analysis.get("risk_reason", "")
            suggestion = analysis.get("suggested_fix", "")

        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 8, "Reason / Explanation:")
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, explanation)
        pdf.ln(1)

        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 8, "Safer Alternative / Suggestion:")
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, suggestion)
        pdf.ln(2)

        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 8, f"Risk Score: {res.get('score', 0)}/100")
        pdf.ln(5)

    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes.getvalue()
