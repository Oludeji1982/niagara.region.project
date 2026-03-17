from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Product Benchmark")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

product_price = df.groupby("Distribution Item")["Unit Price"].mean()

st.subheader("Average Product Price")

fig, ax = plt.subplots()

product_price.sort_values(ascending=False).head(15).plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Product")
ax.set_ylabel("Unit Price")
ax.set_title("Most Expensive Products")

st.pyplot(fig)