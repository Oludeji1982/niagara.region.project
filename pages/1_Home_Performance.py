from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Home Performance Overview")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

home_spend = df.groupby("Home")["Total Amount"].sum()

col1,col2,col3 = st.columns(3)

col1.metric("Total Spend", f"${df['Total Amount'].sum():,.0f}")

cost_per_resident = df["Total Amount"].sum()/df["Total Quantity"].sum()

col2.metric("Cost per Resident per Day", f"${cost_per_resident:.2f}")

col3.metric("Homes Analyzed", len(home_spend))

st.subheader("Home-Level Spend Comparison")

fig, ax = plt.subplots()

home_spend.sort_values(ascending=False).plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Home")
ax.set_ylabel("Spend ($)")
ax.set_title("Spend by LTC Home")

st.pyplot(fig)