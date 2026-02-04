# utils/helpers.py
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

# Ensure reports directory exists
REPORT_DIR = os.path.join(os.getcwd(), "data", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def export_pdf(results):
    """
    Generate a professional PDF report for IP clauses.
    Saves locally and returns a BytesIO object for download.
    """
    # File name
    filename = f"ip_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(REPORT_DIR, filename)

    # Buffer for Streamlit download
    buffer = BytesIO()
    doc = SimpleDocTemplate(file_path, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ClauseHeader', fontSize=12, leading=14, spaceAfter=6,
                              textColor=colors.HexColor('#333333'), fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name='ClauseBody', fontSize=10, leading=12, spaceAfter=10,
                              textColor=colors.HexColor('#444444')))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=14, leading=16, spaceAfter=12,
                              textColor=colors.HexColor('#222222'), fontName="Helvetica-Bold"))

    elements = []

    # Title
    elements.append(Paragraph("Risk Report", styles['Title']))
    elements.append(Spacer(1, 12))

    for idx, item in enumerate(results, 1):
        analysis = item.get("analysis", {})
        ownership = analysis.get("ownership", "Unknown")
        exclusivity = analysis.get("exclusivity", "Unknown")
        risk_reason = analysis.get("risk_reason", "No reason provided")
        suggested_fix = analysis.get("suggested_fix", "No suggestion available")
        risk = item.get("risk", "Unknown")
        score = item.get("score", 0)

        # Clause header
        elements.append(Paragraph(f"Clause {idx}", styles['ClauseHeader']))

        # Clause text
        elements.append(Paragraph(item["clause"], styles['ClauseBody']))

        # Risk table
        data = [
            ["Ownership", ownership],
            ["Exclusivity", exclusivity],
            ["Risk Level", risk],
            ["Risk Score", f"{score}/100"]
        ]
        table = Table(data, colWidths=[100, 350])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 6))

        # Risk reason
        elements.append(Paragraph("<b>Why this is risky:</b>", styles['ClauseHeader']))
        elements.append(Paragraph(risk_reason, styles['ClauseBody']))

        # Suggested fix
        elements.append(Paragraph("<b>Suggested Fix :</b>", styles['ClauseHeader']))
        elements.append(Paragraph(suggested_fix, styles['ClauseBody']))

        # Page break after each clause
        elements.append(PageBreak())

    # Build PDF locally
    doc.build(elements)

    # Load into BytesIO for Streamlit download
    with open(file_path, "rb") as f:
        buffer.write(f.read())
    buffer.seek(0)

    return file_path, buffer
