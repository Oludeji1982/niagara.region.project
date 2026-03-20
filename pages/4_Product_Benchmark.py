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

st.markdown("## **Product Benchmark**")

category = st.selectbox("Select Category", sorted(df["Major Group"].unique()))

sub = df[df["Major Group"] == category]

prod = sub.groupby("Brand Name")["Cost_per_KG"].mean().reset_index()

fig = px.bar(
    prod.sort_values("Cost_per_KG", ascending=False).head(10),
    x="Brand Name",
    y="Cost_per_KG",
    text="Cost_per_KG",
    color="Cost_per_KG"
)

fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)