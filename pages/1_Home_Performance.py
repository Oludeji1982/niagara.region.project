import streamlit as st
import plotly.express as px
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
if raw is None:
    st.error("Run dashboard first")
    st.stop()

df = prepare_data(raw)
df = apply_filters(df)

top = df.groupby("Major Group")["Total Amount"].sum().nlargest(10).index
df = df[df["Major Group"].isin(top)]

if df.empty:
    st.warning("No data available")
    st.stop()

st.markdown("## **Home Performance**")

home = df.groupby("Home")["Total Amount"].sum().reset_index()

fig = px.bar(
    home,
    x="Home",
    y="Total Amount",
    text="Total Amount",
    color="Total Amount",
    color_continuous_scale="Greens"
)

fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)