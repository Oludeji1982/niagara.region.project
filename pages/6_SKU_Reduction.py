import streamlit as st

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

st.markdown("## **SKU Reduction**")

sku = df.groupby(["Major Group","Brand Name"]).agg({
    "Cost_per_KG":"mean",
    "Total Quantity":"sum"
}).reset_index()

st.dataframe(sku.sort_values("Cost_per_KG", ascending=False))