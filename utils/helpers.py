from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

font_path = os.path.join(os.path.dirname(__file__), "NotoSans-Regular.ttf")
if not os.path.exists(font_path):
    import requests
    url = "https://github.com/googlefonts/noto-fonts/blob/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf?raw=true"
    r = requests.get(url)
    with open(font_path, "wb") as f:
        f.write(r.content)

pdfmetrics.registerFont(TTFont("NotoSans", font_path))

def generate_pdf_bytes(results: list) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "NotoSans"
    story = []

    for i, res in enumerate(results, 1):
        story.append(Paragraph(f"Clause {i}: {res['clause']}", styles["Normal"]))
        story.append(Paragraph(f"Language: {res.get('language', 'Unknown')}", styles["Normal"]))
        story.append(Paragraph(f"Ownership: {res.get('ownership', 'Unknown')}", styles["Normal"]))
        story.append(Paragraph(f"Exclusivity: {res.get('exclusivity', 'Unknown')}", styles["Normal"]))
        story.append(Paragraph(f"Risk Level: {res.get('risk', 'Unknown')}", styles["Normal"]))
        story.append(Paragraph(f"Risk Score: {res.get('score', 'Unknown')}/100", styles["Normal"]))
        story.append(Paragraph(f"Reason: {res.get('reason','')}", styles["Normal"]))
        story.append(Paragraph(f"Suggested Fix: {res.get('suggestion','')}", styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
