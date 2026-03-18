import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
df = prepare_data(raw)
df = apply_filters(df)

st.markdown("## **Supplier Optimization**")

supplier = df.groupby(["Distributor","Brand Name"])["Cost_per_KG"].mean().reset_index()

fig = px.scatter(
    supplier,
    x="Distributor",
    y="Cost_per_KG",
    color="Brand Name"
)

st.plotly_chart(fig, use_container_width=True)