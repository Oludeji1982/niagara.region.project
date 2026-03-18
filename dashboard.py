import streamlit as st
import pandas as pd

from src.data_prep import prepare_data
from src.filters import apply_filters

st.set_page_config(layout="wide")

st.title("Niagara LTC Procurement Intelligence")

# ---------------- LOAD ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Fact_Purchases.csv")
    return df

raw = load_data()
raw = prepare_data(raw)

# ---------------- APPLY FILTERS (ONLY HERE) ----------------
filtered = apply_filters(raw)

# ================= REPORT EXPORT =================
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(df):

    total_spend = df["Total Amount"].sum()
    avg_cost = df["Cost_per_KG"].mean()
    savings = total_spend * 0.15  # conservative estimate

    top_categories = (
        df.groupby("Major Group")["Total Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    doc = SimpleDocTemplate("dashboard_report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Niagara Region Procurement Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Total Spend:</b> ${total_spend:,.0f}", styles["Normal"]))
    content.append(Paragraph(f"<b>Average Cost per KG:</b> ${avg_cost:.2f}", styles["Normal"]))
    content.append(Paragraph(f"<b>Estimated Savings Opportunity:</b> ${savings:,.0f}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>Top Spend Categories:</b>", styles["Heading2"]))

    for cat, val in top_categories.items():
        content.append(Paragraph(f"{cat}: ${val:,.0f}", styles["Normal"]))

    content.append(Spacer(1, 15))

    content.append(Paragraph(
        "Executive Insight: Significant savings opportunities exist through supplier optimization, SKU consolidation, and cost-per-KG standardization.",
        styles["Italic"]
    ))

    doc.build(content)

    return "dashboard_report.pdf"
# ---------------- STORE ----------------
st.session_state["raw_data"] = raw
st.session_state["filtered_data"] = filtered

st.success(f"{len(filtered):,} records after filtering")