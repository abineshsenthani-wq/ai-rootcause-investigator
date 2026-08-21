import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from typing import Dict, Any

class ReportService:
    """Generates PDF investigation reports from analytical evidence."""

    @staticmethod
    def generate_pdf_report(evidence: Dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1e1b4b")
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#64748b")
        )

        heading2_style = ParagraphStyle(
            "Heading2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#2563eb"),
            spaceBefore=10,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            "BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155")
        )

        story = []

        # Title Header
        story.append(Paragraph("AI ROOT-CAUSE INVESTIGATION REPORT", title_style))
        story.append(Paragraph("Evidence-Grounded Business Anomaly Analysis", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=15))

        # 1. Executive Summary
        story.append(Paragraph("1. Executive Summary", heading2_style))
        summary_text = evidence.get("summary", "Investigation completed.")
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 10))

        # 2. Calculated Facts
        story.append(Paragraph("2. Direct Calculated Facts", heading2_style))
        for fact in evidence.get("facts", []):
            story.append(Paragraph(f"• {fact}", body_style))
        story.append(Spacer(1, 10))

        # 3. Ranked Potential Contributing Factors
        story.append(Paragraph("3. Potential Contributing Factors (Ranked)", heading2_style))
        factors = evidence.get("potential_factors", [])
        if factors:
            table_data = [["Rank", "Factor / Slice", "Evidence Score", "Status"]]
            for i, f in enumerate(factors[:5], 1):
                table_data.append([
                    str(i),
                    f.get("factor_name", ""),
                    f"{f.get('evidence_score', 0)}/100",
                    f.get("evidence_label", "")
                ])

            t = Table(table_data, colWidths=[40, 260, 110, 110])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
            ]))
            story.append(t)
        story.append(Spacer(1, 12))

        # 4. Recommendations
        story.append(Paragraph("4. Recommended Next Steps", heading2_style))
        for rec in evidence.get("recommendations", []):
            story.append(Paragraph(f"• {rec}", body_style))
        story.append(Spacer(1, 10))

        # 5. Methodological Limitations
        story.append(Paragraph("5. Methodology & Limitations", heading2_style))
        for lim in evidence.get("limitations", []):
            story.append(Paragraph(f"• {lim}", body_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
