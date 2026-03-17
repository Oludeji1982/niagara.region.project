from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Procurement Risk")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

dist_spend = df.groupby("Distributor")["Total Amount"].sum()

st.subheader("Supplier Concentration")

fig, ax = plt.subplots()

dist_spend.sort_values(ascending=False).plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Distributor")
ax.set_ylabel("Spend ($)")
ax.set_title("Spend by Distributor")

st.pyplot(fig)