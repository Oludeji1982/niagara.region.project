import streamlit as st
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
df = prepare_data(raw)
df = apply_filters(df)

st.markdown("## **AI Chat Assistant**")

query = st.text_input("Ask about procurement")

if query:

    if "spend" in query:
        st.success(f"${df['Total Amount'].sum():,.0f}")

    elif "expensive" in query:
        row = df.loc[df["Cost_per_KG"].idxmax()]
        st.success(f"{row['Brand Name']} highest cost")

    else:
        st.info("Try: spend, expensive")