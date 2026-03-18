import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
df = prepare_data(raw)
df = apply_filters(df)

st.markdown("## **Demand Forecasting**")

forecast = df.groupby(["Home","Major Group"])["Total Quantity"].mean().reset_index()
forecast["Forecast"] = forecast["Total Quantity"] * 1.1

fig = px.bar(
    forecast,
    x="Major Group",
    y="Forecast",
    color="Home"
)

st.plotly_chart(fig, use_container_width=True)