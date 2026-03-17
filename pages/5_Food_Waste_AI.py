from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
import matplotlib.pyplot as plt
from src.analytics_engine import food_waste_model

st.title("Food Waste Intelligence")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

heatmap = food_waste_model(df)

st.subheader("Food Waste Heatmap by LTC Home")

fig, ax = plt.subplots()

cax = ax.imshow(heatmap, aspect="auto")

ax.set_xticks(range(len(heatmap.columns)))
ax.set_xticklabels(heatmap.columns, rotation=90)

ax.set_yticks(range(len(heatmap.index)))
ax.set_yticklabels(heatmap.index)

ax.set_xlabel("Food Category")
ax.set_ylabel("LTC Home")

fig.colorbar(cax)

st.pyplot(fig)