from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Procurement Optimization")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

group_cost = df.groupby("Major Group").agg({
    "Total Amount":"sum",
    "Total Quantity":"sum"
})

group_cost["Unit Cost"] = group_cost["Total Amount"] / group_cost["Total Quantity"]

benchmark = group_cost["Unit Cost"].min()

group_cost["Potential Savings"] = (
    group_cost["Unit Cost"] - benchmark
) * group_cost["Total Quantity"]

group_cost = group_cost.sort_values("Potential Savings",ascending=False)

st.subheader("Optimization Opportunities")

fig, ax = plt.subplots()

group_cost["Potential Savings"].head(10).plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Major Group")
ax.set_ylabel("Savings ($)")
ax.set_title("Potential Procurement Savings")

st.pyplot(fig)