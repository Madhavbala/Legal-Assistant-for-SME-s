from fpdf import FPDF
from io import BytesIO

def generate_pdf_bytes(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Use Arial Unicode for Hindi text
    pdf.add_font("ArialUnicode", "", "Arial.ttf", uni=True)
    pdf.set_font("ArialUnicode", size=12)

    for i, res in enumerate(results, 1):
        pdf.multi_cell(0, 8, f"Clause {i}: {res['clause']}")
        pdf.ln(2)
        analysis = res["analysis"]
        pdf.multi_cell(0, 8, f"Ownership: {analysis['ownership']}")
        pdf.multi_cell(0, 8, f"Exclusivity: {analysis['exclusivity']}")
        pdf.multi_cell(0, 8, f"Risk Level: {res['risk']}")
        pdf.multi_cell(0, 8, f"Reason: {analysis['risk_reason']}")
        pdf.multi_cell(0, 8, f"Safer Alternative: {analysis['suggested_fix']}")
        pdf.multi_cell(0, 8, f"Risk Score: {res['score']}/100")
        pdf.ln(5)

    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes.read()
