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

fig3, ax3 = plt.subplots()import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Niagara Region LTC Food Supply Intelligence",
    layout="wide"
)

st.title("Niagara Region LTC Food Supply Intelligence Dashboard")

st.write(
"""
This dashboard analyzes purchasing, menu demand, production, and supply chain
patterns across Niagara Region Long Term Care Homes.
"""
)

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

@st.cache_data
def load_data():

    purchases = pd.read_csv("data/Fact_Purchases.csv")
    production = pd.read_csv("data/Fact_Production.csv")
    homes = pd.read_csv("data/Dim_Homes.csv")

    purchases["Date"] = pd.to_datetime(purchases["Date"], errors="coerce")
    production["Date"] = pd.to_datetime(production["Date"], errors="coerce")

    return purchases, production, homes


purchases, production, homes = load_data()

st.success("Dataset Loaded")

# ----------------------------------------
# OVERVIEW METRICS
# ----------------------------------------

st.header("Operational Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Spend", f"${purchases['TotalAmount'].sum():,.0f}")

with col2:
    st.metric("Total Products", purchases["ItemName"].nunique())

with col3:
    waste = production["TotalToPrepare"].sum() - production["Portions"].sum()
    st.metric("Estimated Waste", int(waste))

with col4:
    st.metric("Total Suppliers", purchases["Distributor"].nunique())

# ----------------------------------------
# SPEND BY HOME
# ----------------------------------------

st.header("Spend by LTC Home")

spend_home = purchases.groupby("Facility")["TotalAmount"].sum()

fig, ax = plt.subplots()

spend_home.plot(kind="bar", ax=ax)

ax.set_ylabel("Total Spend")

st.pyplot(fig)

# ----------------------------------------
# SUPPLIER SPENDING
# ----------------------------------------

st.header("Supplier Spend Analysis")

supplier = purchases.groupby("Distributor")["TotalAmount"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()

supplier.head(10).plot(kind="bar", ax=ax2)

ax2.set_title("Top Suppliers")

st.pyplot(fig2)

# ----------------------------------------
# TOP PRODUCTS
# ----------------------------------------

st.header("Top Purchased Products")

top_items = purchases.groupby("ItemName")["TotalQty"].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()

top_items.plot(kind="barh", ax=ax3)

st.pyplot(fig3)

# ----------------------------------------
# SKU REDUCTION ANALYSIS
# ----------------------------------------

st.header("SKU Consolidation Opportunities")

sku_counts = purchases.groupby("Category")["ItemName"].nunique()

fig4, ax4 = plt.subplots()

sku_counts.plot(kind="bar", ax=ax4)

ax4.set_title("SKUs by Category")

st.pyplot(fig4)

# ----------------------------------------
# WASTE ANALYSIS
# ----------------------------------------

st.header("Food Waste Analysis")

production["Waste"] = production["TotalToPrepare"] - production["Portions"]

waste_by_item = production.groupby("Item")["Waste"].sum()

fig5, ax5 = plt.subplots()

waste_by_item.sort_values(ascending=False).head(10).plot(kind="bar", ax=ax5)

ax5.set_title("Top Waste Items")

st.pyplot(fig5)

# ----------------------------------------
# PRICE INFLATION
# ----------------------------------------

st.header("Food Price Inflation")

purchases["Month"] = purchases["Date"].dt.to_period("M")

price_trend = purchases.groupby("Month")["UnitPrice"].mean()

fig6, ax6 = plt.subplots()

price_trend.plot(marker="o", ax=ax6)

ax6.set_title("Average Unit Price Trend")

st.pyplot(fig6)

# ----------------------------------------
# PURCHASING FREQUENCY
# ----------------------------------------

st.header("Purchasing Frequency")

purchase_freq = purchases["ItemName"].value_counts().head(10)

fig7, ax7 = plt.subplots()

purchase_freq.plot(kind="bar", ax=ax7)

st.pyplot(fig7)

# ----------------------------------------
# HOME PURCHASING PATTERNS
# ----------------------------------------

st.header("Purchasing Patterns by LTC Home")

home_items = purchases.groupby(["Facility","ItemName"])["TotalQty"].sum()

st.dataframe(home_items.head(20))

# ----------------------------------------
# AI DEMAND FORECASTING
# ----------------------------------------

st.header("AI Food Demand Forecast")

df = purchases.copy()

df["Month"] = df["Date"].dt.month

X = df[["Month"]]
y = df["TotalQty"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

model = RandomForestRegressor()

model.fit(X_train, y_train)

prediction = model.predict([[12]])

st.metric("Predicted Demand Next Month", int(prediction[0]))

# ----------------------------------------
# MENU CATEGORY DISTRIBUTION
# ----------------------------------------

st.header("Meal Category Distribution")

meal_counts = production["Meal"].value_counts()

fig8, ax8 = plt.subplots()

sns.barplot(
    x=meal_counts.index,
    y=meal_counts.values,
    ax=ax8
)

st.pyplot(fig8)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.write("---")

st.write("Project Team")

st.write(
"""
- Oludeji Fashoro – Data Loader & Cleaning
- Team Members – Supply Analytics
"""
)

trend.plot(marker="o", ax=ax3)

st.pyplot(fig3)