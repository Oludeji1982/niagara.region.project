import streamlit as st
from src.filters import apply_filters
from src.data_prep import prepare_data

raw = st.session_state.get("raw_data")
if raw is None:
    st.stop()

df = prepare_data(raw)
df = apply_filters(df)

st.title("AI Procurement Advisor")

top = df.groupby("Major Group")["Total Amount"].sum().nlargest(10).index

df = df[df["Major Group"].isin(top)]

sku = df.groupby(["Major Group","Brand Name"]).agg({
    "Cost_per_KG":"mean",
    "Total Quantity":"sum"
}).reset_index()

for g in sku["Major Group"].unique():

    sub = sku[sku["Major Group"] == g]

    if len(sub) < 2:
        continue

    cheap = sub.loc[sub["Cost_per_KG"].idxmin()]
    exp = sub.loc[sub["Cost_per_KG"].idxmax()]

    savings = (exp["Cost_per_KG"] - cheap["Cost_per_KG"]) * exp["Total Quantity"]

    if savings > 500:

        st.error(f"""
🔴 **{g}**

Drop **{exp['Brand Name']}**  
Switch to **{cheap['Brand Name']}**

💰 Save: ${savings:,.0f}

Reason:
- Higher cost/kg (${exp['Cost_per_KG']:.2f})
- Same category alternative cheaper
- High usage amplifies loss
""")