import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

def generate_pdf_report(password_mask: str, health_score: dict, entropy: float, crack_times: dict, recommendations: list) -> bytes:
    """
    Generates a professional vector PDF security report for the analyzed password.
    Returns PDF file binary bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Title & Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#00f2fe'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#a0aec0'),
        spaceAfter=15
    )
    
    heading2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#1a202c'),
        spaceBefore=15,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#2d3748'),
        leading=14
    )

    story = []

    # Title Banner
    story.append(Paragraph("PSWX AI PASSWORD SECURITY AUDIT REPORT", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | System Version v1.0.0", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#00f2fe"), spaceAfter=15))

    # Executive Overview Box
    score_val = health_score.get('score', 0)
    score_cat = health_score.get('category', 'N/A')
    
    overview_data = [
        [Paragraph("<b>Target Password (Masked):</b>", body_style), Paragraph(f"<code>{password_mask}</code>", body_style)],
        [Paragraph("<b>Health Score:</b>", body_style), Paragraph(f"<font color='{health_score.get('color', '#000')}'><b>{score_val} / 100 ({score_cat})</b></font>", body_style)],
        [Paragraph("<b>Shannon Entropy:</b>", body_style), Paragraph(f"<b>{entropy} bits</b>", body_style)],
    ]
    
    t_overview = Table(overview_data, colWidths=[180, 350])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 15))

    # Crack Time Resistance Matrix
    story.append(Paragraph("Estimated Resistance Against Attack Vectors", heading2_style))
    
    crack_data = [
        [Paragraph("<b>Attack Method</b>", body_style), Paragraph("<b>Estimated Crack Time</b>", body_style)],
        ["Online Rate Limited API", crack_times.get('online_attack', 'N/A')],
        ["Offline Fast Hash (MD5 / NTLM)", crack_times.get('fast_hash', 'N/A')],
        ["Offline Slow Hash (bcrypt / Argon2)", crack_times.get('slow_hash', 'N/A')],
        ["GPU Array Cluster (1 TH/s)", crack_times.get('gpu_cluster', 'N/A')]
    ]
    
    t_crack = Table(crack_data, colWidths=[260, 270])
    t_crack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#edf2f7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2d3748')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_crack)
    story.append(Spacer(1, 15))

    # Personalized Recommendations
    story.append(Paragraph("Actionable Recommendations", heading2_style))
    if recommendations:
        for rec in recommendations:
            bullet_text = f"• {rec}"
            story.append(Paragraph(bullet_text, body_style))
            story.append(Spacer(1, 3))
    else:
        story.append(Paragraph("• No significant security defects detected. Excellent password composition!", body_style))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("<i>Confidential & Privacy Protected: Plaintext password is never saved or logged by this platform.</i>", subtitle_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
