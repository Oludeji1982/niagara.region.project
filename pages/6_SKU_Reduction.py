from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
from src.analytics_engine import sku_reduction_engine

st.title("SKU Reduction Recommendation Engine")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

sku, cheapest = sku_reduction_engine(df)

st.subheader("All SKUs")

st.dataframe(sku)

st.subheader("Recommended SKU Standardization")

st.dataframe(cheapest)

st.info(
"Recommendation: Standardize purchasing on the lowest unit-cost brand within each Major Group."
)