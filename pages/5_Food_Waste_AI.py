import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
df = prepare_data(raw)
df = apply_filters(df)

st.markdown("## **Food Waste Heatmap**")

waste = df.groupby(["Home","Major Group"])["Total Quantity"].sum().reset_index()

fig = px.density_heatmap(
    waste,
    x="Major Group",
    y="Home",
    z="Total Quantity",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig, use_container_width=True)