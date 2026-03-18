import streamlit as st

def apply_filters(df):

    st.sidebar.markdown("## **Filters**")

    # ---------------- REMOVE INVALID HOMES ----------------
    df = df[
        ~df["Home"].isin([
            "Riordon Street Shelter",
            "Summer Street Shelter"
        ])
    ]

    # ---------------- DROPDOWNS ----------------
    home = st.sidebar.multiselect(
        "🏠 Select Home",
        sorted(df["Home"].dropna().unique())
    )

    category = st.sidebar.multiselect(
        "📦 Select Category",
        sorted(df["Major Group"].dropna().unique())
    )

    brand = st.sidebar.multiselect(
        "🏷 Select Brand",
        sorted(df["Brand Name"].dropna().unique())
    )

    supplier = st.sidebar.multiselect(
        "🚚 Select Supplier",
        sorted(df["Distributor"].dropna().unique())
    )

    # ---------------- RANGE SLIDERS ----------------

    # COST PER KG
    if "Cost_per_KG" in df.columns:
        min_cost = float(df["Cost_per_KG"].min())
        max_cost = float(df["Cost_per_KG"].max())

        cost_range = st.sidebar.slider(
            "💰 Cost per KG Range",
            min_cost,
            max_cost,
            (min_cost, max_cost)
        )

        df = df[
            (df["Cost_per_KG"] >= cost_range[0]) &
            (df["Cost_per_KG"] <= cost_range[1])
        ]

    # TOTAL SPEND
    min_spend = float(df["Total Amount"].min())
    max_spend = float(df["Total Amount"].max())

    spend_range = st.sidebar.slider(
        "💵 Total Spend Range",
        min_spend,
        max_spend,
        (min_spend, max_spend)
    )

    df = df[
        (df["Total Amount"] >= spend_range[0]) &
        (df["Total Amount"] <= spend_range[1])
    ]

    # QUANTITY
    if "Total Quantity" in df.columns:
        min_qty = float(df["Total Quantity"].min())
        max_qty = float(df["Total Quantity"].max())

        qty_range = st.sidebar.slider(
            "📊 Quantity Range",
            min_qty,
            max_qty,
            (min_qty, max_qty)
        )

        df = df[
            (df["Total Quantity"] >= qty_range[0]) &
            (df["Total Quantity"] <= qty_range[1])
        ]

    # ---------------- APPLY DROPDOWNS ----------------
    if home:
        df = df[df["Home"].isin(home)]

    if category:
        df = df[df["Major Group"].isin(category)]

    if brand:
        df = df[df["Brand Name"].isin(brand)]

    if supplier:
        df = df[df["Distributor"].isin(supplier)]

    return df