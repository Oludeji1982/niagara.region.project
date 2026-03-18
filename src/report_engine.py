from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(df, filename="executive_report.pdf"):

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)

    total_spend = df["Total Amount"].sum()
    avg_cost = df["Cost_per_KG"].mean()

    content = []

    content.append(Paragraph("Niagara LTC Procurement Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Total Spend: ${total_spend:,.0f}", styles["Normal"]))
    content.append(Paragraph(f"Average Cost per KG: ${avg_cost:.2f}", styles["Normal"]))

    doc.build(content)

    return filename