import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import *
from src.data_cleaner import *
from src.purchasing_analysis import *
from src.production_analysis import *
from src.inflation_analysis import *

st.set_page_config(
    page_title="Niagara Region LTC Supply Intelligence",
    layout="wide"
)

st.title("Niagara Region LTC Purchasing & Supply Dashboard")

purchases = load_purchases("data/Fact_Purchases.csv")
production = load_production("data/Fact_Production.csv")

purchases = clean_purchases(purchases)
production = clean_production(production)

# Overview metrics

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Food Spend", f"${total_spend(purchases):,.0f}")

with col2:
    st.metric("SKU Count", sku_count(purchases))

with col3:
    st.metric("Waste Estimate", waste_estimate(production))

# Supplier spend

st.header("Supplier Spend")

supplier = spend_by_supplier(purchases)

fig, ax = plt.subplots()

supplier.head(10).plot(kind="bar", ax=ax)

st.pyplot(fig)

# Top items

st.header("Top Purchased Products")

items = top_products(purchases)

fig2, ax2 = plt.subplots()

items.plot(kind="barh", ax=ax2)

st.pyplot(fig2)

# Inflation trend

st.header("Food Price Inflation")

trend = price_trend(purchases)

fig3, ax3 = plt.subplots()

trend.plot(marker="o", ax=ax3)

st.pyplot(fig3)