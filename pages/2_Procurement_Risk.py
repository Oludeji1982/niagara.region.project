import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
df = prepare_data(raw)
df = apply_filters(df)

st.title("Procurement Risk")

supplier = df.groupby("Distributor")["Total Amount"].sum().reset_index()

supplier["Share"] = supplier["Total Amount"] / supplier["Total Amount"].sum()

supplier["Risk"] = supplier["Share"].apply(
    lambda x: "HIGH" if x > 0.3 else "LOW"
)

high_only = st.toggle("Show only high-risk suppliers")

if high_only:
    supplier = supplier[supplier["Risk"] == "HIGH"]

fig = px.bar(
    supplier,
    x="Distributor",
    y="Total Amount",
    text="Total Amount",
    color="Risk"
)

fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)