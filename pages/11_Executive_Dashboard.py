from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import plotly.express as px
from src.executive_engine import (
    generate_executive_summary,
    scenario_simulator,
    generate_ai_recommendations
)

st.set_page_config(layout="wide")

st.title("Executive Dashboard")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

# -------------------------------
# EXECUTIVE SUMMARY
# -------------------------------

st.markdown("## Executive Summary")

summary = generate_executive_summary(df)

st.markdown(f"""
<div style='background-color:#006b3c;padding:20px;border-radius:10px'>
<p style='color:white;font-size:16px'>{summary}</p>
</div>
""", unsafe_allow_html=True)


# -------------------------------
# KPI ROW
# -------------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Spend", f"${df['Total Amount'].sum():,.0f}")
col2.metric("Avg Unit Price", f"${df['Unit Price'].mean():.2f}")
col3.metric("Total Quantity", f"{df['Total Quantity'].sum():,.0f}")


# -------------------------------
# SCENARIO SIMULATOR
# -------------------------------

st.markdown("## Scenario Simulator")

reduction = st.slider("Reduce Quantity (%)", 0, 30, 10)

result = scenario_simulator(df, reduction)

col1, col2, col3 = st.columns(3)

col1.metric("Original Spend", f"${result['Original Spend']:,.0f}")
col2.metric("New Spend", f"${result['New Spend']:,.0f}")
col3.metric("Savings", f"${result['Savings']:,.0f}")


# -------------------------------
# VISUALIZATION
# -------------------------------

st.markdown("## Spend by Major Group")

group = df.groupby("Major Group")["Total Amount"].sum().reset_index()

fig = px.bar(
    group,
    x="Major Group",
    y="Total Amount",
    color="Total Amount",
    title="Spending Distribution",
)

st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# AI RECOMMENDATIONS
# -------------------------------

st.markdown("## AI Recommendations")

recommendations = generate_ai_recommendations(df)

for rec in recommendations:
    st.warning(rec)

    from src.report_engine import generate_pdf

if st.button("Export Executive Report"):

    file = generate_pdf(summary)

    with open(file, "rb") as f:
        st.download_button(
            "Download Report",
            f,
            file_name="LTC_Report.pdf"
        )