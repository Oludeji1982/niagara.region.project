import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.filters import apply_filters

st.markdown("""
<style>
.main {
    background-color: #f5f7f6;
}

h1, h2, h3 {
    color: #004b2d;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 8px solid #006b3c;
}

.green-card {
    border-left: 8px solid #2ecc71 !important;
}

.red-card {
    border-left: 8px solid #e74c3c !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Niagara Region LTC Procurement Intelligence",
    layout="wide"
)

st.title("Niagara Region LTC Procurement Intelligence")

st.markdown("""
<div style='background-color:#006b3c;padding:15px;border-radius:10px'>
<h4 style='color:white'>Niagara Region LTC Food Supply Intelligence Platform</h4>
<p style='color:white'>
AI-powered procurement optimization, supplier intelligence, and food waste analytics
</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():

    purchases = pd.read_csv("data/Fact_Purchases.csv")
    homes = pd.read_csv("data/Dim_Homes.csv")

    purchases.columns = purchases.columns.str.strip()

    return purchases, homes


purchases, homes = load_data()

st.session_state["raw_data"] = purchases

filtered = apply_filters(purchases)

st.session_state["data"] = filtered
st.session_state["homes"] = homes

st.success(f"{len(filtered):,} records after filtering")

if filtered.empty:
    st.warning("No data matches the selected filters")
    st.stop()

# KPI METRICS

col1, col2, col3 = st.columns(3)

total_spend = filtered["Total Amount"].sum()
total_qty = filtered["Total Quantity"].sum()
avg_price = filtered["Unit Price"].mean()

# RULE: higher price = bad
price_color = "red-card" if avg_price > filtered["Unit Price"].median() else "green-card"

col1.markdown(f"""
<div class="stMetric">
<h5>Total Spend</h5>
<h2>${total_spend:,.0f}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="stMetric">
<h5>Total Quantity</h5>
<h2>{total_qty:,.0f}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="stMetric {price_color}">
<h5>Avg Unit Price</h5>
<h2>${avg_price:.2f}</h2>
</div>
""", unsafe_allow_html=True)

# MAJOR GROUP SAVINGS

group_savings = filtered.groupby("Major Group").agg({
    "Total Amount":"sum",
    "Total Quantity":"sum"
})

group_savings["Unit Cost"] = (
    group_savings["Total Amount"] /
    group_savings["Total Quantity"]
)

benchmark = group_savings["Unit Cost"].min()

group_savings["Potential Savings"] = (
    group_savings["Unit Cost"] - benchmark
) * group_savings["Total Quantity"]

group_savings = group_savings.sort_values(
    "Potential Savings",
    ascending=False
)

st.subheader("Savings Opportunity by Major Group")

fig, ax = plt.subplots()

group_savings["Potential Savings"].head(10).plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Major Group")
ax.set_ylabel("Potential Savings ($)")
ax.set_title("Procurement Savings Opportunity")

st.pyplot(fig)

st.markdown("""
<div style='background-color:#006b3c;padding:15px;border-radius:10px'>
<h4 style='color:white'>Niagara Region LTC Food Supply Intelligence Platform</h4>
<p style='color:white'>
This platform analyzes procurement spending, supplier efficiency,
SKU duplication, and food waste patterns across Niagara Region Long-Term Care homes.
</p>
</div>
""", unsafe_allow_html=True)

import plotly.express as px

st.subheader("Savings Opportunity by Major Group")

fig = px.bar(
    group_savings.head(10),
    x=group_savings.head(10).index,
    y="Potential Savings",
    labels={"x":"Major Group","Potential Savings":"Savings ($)"},
    title="Top Savings Opportunities",
    color="Potential Savings",
    color_continuous_scale="Greens"
)

st.plotly_chart(fig, use_container_width=True)