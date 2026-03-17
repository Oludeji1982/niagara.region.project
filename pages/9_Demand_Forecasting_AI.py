from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import plotly.express as px
from src.ai_models import demand_forecast_model

st.title("AI Demand Forecasting")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

forecast = demand_forecast_model(df)

st.subheader("Predicted Food Demand (Next Cycle)")

st.dataframe(forecast)

fig = px.bar(
    forecast.head(20),
    x="Major Group",
    y="Predicted Next Demand",
    color="Home",
    title="Predicted Demand by Food Category",
)

st.plotly_chart(fig, use_container_width=True)

st.info(
"AI predicts future food demand based on historical purchasing patterns to reduce over-ordering."
)