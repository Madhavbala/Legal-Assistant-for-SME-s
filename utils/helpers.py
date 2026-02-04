from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf_bytes(results: list):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    for i, res in enumerate(results, 1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Clause {i}")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(60, y, res["clause"])
        y -= 20

        c.drawString(60, y, f"Ownership: {res['analysis']['ownership']}")
        y -= 15
        c.drawString(60, y, f"Exclusivity: {res['analysis']['exclusivity']}")
        y -= 15
        c.drawString(60, y, f"Risk: {res['risk']} | Score: {res['score']}/100")
        y -= 15

        try:
            reason_data = json.loads(res["analysis"]["risk_reason"])
            c.drawString(60, y, "Reason:")
            y -= 15
            c.drawString(70, y, reason_data.get("RiskExplanation", ""))
            y -= 20
            c.drawString(60, y, "Suggested Alternative:")
            y -= 15
            c.drawString(70, y, reason_data.get("SaferAlternative", ""))
            y -= 30
        except:
            c.drawString(60, y, "Reason: " + res["analysis"]["risk_reason"])
            y -= 30

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer.read()
