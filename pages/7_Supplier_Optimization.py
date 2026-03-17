from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
from src.analytics_engine import supplier_optimization

st.title("Supplier Cost Optimization Model")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

supplier, cheapest_supplier = supplier_optimization(df)

st.subheader("Supplier Price Comparison")

st.dataframe(supplier)

st.subheader("Cheapest Supplier by Product")

st.dataframe(cheapest_supplier)

st.success(
"Switching to the cheapest supplier for identical products can significantly reduce procurement costs."
)