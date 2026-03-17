from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(summary, filename="report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Niagara LTC Procurement Report", styles["Title"]))
    content.append(Paragraph(summary, styles["BodyText"]))

    doc.build(content)

    return filename