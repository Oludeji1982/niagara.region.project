import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
df = prepare_data(raw)
df = apply_filters(df)

top = df.groupby("Major Group")["Total Amount"].sum().nlargest(10).index
df = df[df["Major Group"].isin(top)]

st.markdown("## **Procurement Optimization**")

group = df.groupby("Major Group")["Cost_per_KG"].mean().reset_index()

fig = px.bar(
    group,
    x="Major Group",
    y="Cost_per_KG",
    text="Cost_per_KG",
    color="Cost_per_KG",
    color_continuous_scale="Reds"
)

fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)