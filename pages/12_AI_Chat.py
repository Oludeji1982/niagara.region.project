import streamlit as st
from src.chat_engine import simple_chat
from src.filters import apply_filters

st.title("AI Chat Assistant")

raw = st.session_state.get("raw_data")
df = apply_filters(raw)

if df.empty:
    st.warning("No data available")
    st.stop()

query = st.text_input("Ask a question about your data")

if query:
    response = simple_chat(df, query)
    st.success(response)