import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data
from src.analytics_engine import detect_anomalies

raw = st.session_state.get("raw_data")
if raw is None:
    st.error("Run dashboard first")
    st.stop()

df = prepare_data(raw)
df = apply_filters(df)

if df.empty:
    st.warning("No data available")
    st.stop()

st.markdown("# **Executive Dashboard**")

# ---------------- KPI ----------------
total_spend = df["Total Amount"].sum()
avg_cost = df["Cost_per_KG"].mean()

# savings
group = df.groupby("Major Group").agg({
    "Cost_per_KG":"mean",
    "Total Quantity":"sum"
}).reset_index()

savings = (group["Cost_per_KG"].max() - group["Cost_per_KG"].min()) * group["Total Quantity"].sum()
savings = min(savings, total_spend * 0.25)  # realistic cap

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Spend", f"${total_spend:,.0f}")

col2.markdown(f"""
<div style='background:#d4edda;padding:15px;border-radius:10px'>
<b>💸 Savings Opportunity</b><br>${savings:,.0f}
</div>
""", unsafe_allow_html=True)

color = "#f8d7da" if avg_cost > df["Cost_per_KG"].median() else "#d4edda"

col3.markdown(f"""
<div style='background:{color};padding:15px;border-radius:10px'>
<b>📉 Cost per KG</b><br>${avg_cost:.2f}
</div>
""", unsafe_allow_html=True)

# ---------------- ALERTS ----------------
alerts = detect_anomalies(df)
for a in alerts:
    st.warning(a)

# ---------------- TOP 10 PIE ----------------
top = df.groupby("Major Group")["Total Amount"].sum().reset_index()
top = top.sort_values("Total Amount", ascending=False).head(10)

fig = px.pie(
    top,
    names="Major Group",
    values="Total Amount",
    color_discrete_sequence=px.colors.sequential.Greens
)

fig.update_traces(textinfo='percent+label')

st.plotly_chart(fig, use_container_width=True)

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
    
# GENERATE REPORT
report_file = generate_report(df)

# DOWNLOAD BUTTON
with open(report_file, "rb") as f:
    st.download_button(
        label="📄 Download Executive Report",
        data=f,
        file_name="Niagara_Procurement_Report.pdf",
        mime="application/pdf"
    )