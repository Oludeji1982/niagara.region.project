from src.filters import apply_filters

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

import streamlit as st
from src.analytics_engine import procurement_advisor

st.title("AI Procurement Advisor")

df = st.session_state["data"]

if df.empty:
    st.warning("No data available")
    st.stop()

advice = procurement_advisor(df)

st.subheader("AI Recommendations")

if advice.empty:
    st.success("No optimization opportunities detected")
else:
    st.dataframe(advice)

    st.subheader("Top Savings Insights")

    for _, row in advice.head(5).iterrows():

        st.info(
            f"Switching from {row['Current Brand']} to {row['Recommended Brand']} "
            f"for {row['Item']} could save ${row['Potential Savings']:,.0f}"
        )