from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(filename, title, summary, bullets):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(title, styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(summary, styles["BodyText"]))
    content.append(Spacer(1, 12))

    for bullet in bullets:
        content.append(Paragraph(f"• {bullet}", styles["BodyText"]))
        content.append(Spacer(1, 8))

    doc.build(content)