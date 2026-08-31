import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class PDFReportBuilder:
    @staticmethod
    def build_pdf(report_data: dict) -> bytes:
        """
        Takes the aggregated report payload and renders a formal PDF byte stream.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = styles['Heading1']
        title_style.alignment = 1 # Center
        
        h2_style = styles['Heading2']
        h2_style.textColor = colors.HexColor("#0C2340")
        
        normal_style = styles['Normal']
        
        flag_ai_style = ParagraphStyle(
            'FlagAI',
            parent=normal_style,
            textColor=colors.darkblue,
            leftIndent=10
        )
        
        flag_officer_style = ParagraphStyle(
            'FlagOfficer',
            parent=normal_style,
            textColor=colors.darkgreen,
            leftIndent=10
        )
        
        elements = []
        
        # Header
        elements.append(Paragraph(f"GovFlow Compliance Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Metadata
        elements.append(Paragraph(f"<b>Tender ID:</b> {report_data['tender_id']}", normal_style))
        elements.append(Paragraph(f"<b>Bidder ID:</b> {report_data['bidder_id']}", normal_style))
        elements.append(Paragraph(f"<b>Legal Name:</b> {report_data['legal_name']}", normal_style))
        elements.append(Paragraph(f"<b>Generated At:</b> {datetime.utcnow().isoformat()}Z", normal_style))
        elements.append(Spacer(1, 24))
        
        # Flags Section
        elements.append(Paragraph("Compliance Findings", h2_style))
        elements.append(Spacer(1, 12))
        
        for idx, flag in enumerate(report_data['flags'], 1):
            # Flag Title
            elements.append(Paragraph(f"<b>{idx}. {flag['title']}</b> (Rule: {flag['rule']})", normal_style))
            
            # AI Recommendation block
            ai = flag['ai_recommendation']
            ai_text = f"<b>AI Finding:</b> {ai['status']} - {ai['reason']}<br/><i>Notes:</i> {ai['confidence_notes']}"
            elements.append(Paragraph(ai_text, flag_ai_style))
            
            # Officer Decision block
            officer = flag['officer_decision']
            if officer:
                off_text = f"<b>Officer Decision:</b> {officer['status']}<br/><i>Notes:</i> {officer['notes']}<br/><i>By:</i> {officer['officer_id']} at {officer['timestamp']}"
                elements.append(Paragraph(off_text, flag_officer_style))
            else:
                elements.append(Paragraph("<b>Officer Decision:</b> Pending Review", flag_officer_style))
                
            # Evidence block
            elements.append(Spacer(1, 6))
            if flag['evidence']:
                evidence_data = [["Document ID", "Page", "Snippet"]]
                for anchor in flag['evidence']:
                    evidence_data.append([
                        anchor.get('documentId', 'Unknown'),
                        str(anchor.get('pageNumber', 1)),
                        str(anchor.get('snippet', ''))[:50] + "..."
                    ])
                
                t = Table(evidence_data, colWidths=[200, 50, 250])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F4F8")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
                ]))
                elements.append(t)
            
            elements.append(Spacer(1, 18))
            
        if not report_data['flags']:
            elements.append(Paragraph("No compliance flags found for this bidder.", normal_style))
            
        doc.build(elements)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
