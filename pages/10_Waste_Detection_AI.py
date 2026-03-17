from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import plotly.express as px
from src.ai_models import waste_detection_model

st.title("AI Waste Detection System")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

waste = waste_detection_model(df)

st.subheader("Detected Inefficiencies")

st.dataframe(waste)

st.subheader("High Waste Areas")

fig = px.scatter(
    waste,
    x="Total Quantity",
    y="Unit Cost",
    color="Waste Flag",
    size="Waste Severity",
    hover_data=["Home", "Major Group"],
    title="Waste Detection Analysis"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("AI Insights")

high_waste = waste[waste["Waste Flag"] == True]

for _, row in high_waste.head(5).iterrows():
    st.warning(
        f"{row['Home']} is overspending on {row['Major Group']} "
        f"(Unit Cost: ${row['Unit Cost']:.2f})"
    )