import streamlit as st
import plotly.express as px

import os

logo_path = os.path.join("assets", "logo.png")

if os.path.exists(logo_path):
    st.image(logo_path, width=80)
else:
    st.warning("Logo not found — check assets/logo.png")

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