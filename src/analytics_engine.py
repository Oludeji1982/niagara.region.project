import pandas as pd


# ----------------------------------
# FOOD WASTE HEATMAP MODEL
# ----------------------------------

def food_waste_model(df):

    waste = df.groupby(
        ["Home","Major Group"]
    )["Total Quantity"].sum().reset_index()

    waste["Waste Score"] = waste["Total Quantity"] / waste["Total Quantity"].max()

    heatmap = waste.pivot_table(
        index="Home",
        columns="Major Group",
        values="Waste Score",
        fill_value=0
    )

    return heatmap


# ----------------------------------
# SKU REDUCTION ENGINE
# ----------------------------------

def sku_reduction_engine(df):

    sku = df.groupby(
        ["Major Group","Brand Name"]
    ).agg({
        "Total Amount":"sum",
        "Total Quantity":"sum"
    }).reset_index()

    sku["Unit Cost"] = sku["Total Amount"] / sku["Total Quantity"]

    cheapest = sku.loc[
        sku.groupby("Major Group")["Unit Cost"].idxmin()
    ]

    return sku, cheapest


# ----------------------------------
# SUPPLIER COST OPTIMIZATION
# ----------------------------------

def supplier_optimization(df):

    supplier = df.groupby(
        ["Distribution Item","Distributor"]
    ).agg({
        "Unit Price":"mean"
    }).reset_index()

    cheapest_supplier = supplier.loc[
        supplier.groupby("Distribution Item")["Unit Price"].idxmin()
    ]

    return supplier, cheapest_supplier

    def procurement_advisor(df):

    advice = []

    sku = df.groupby(
        ["Distribution Item","Brand Name"]
    ).agg({
        "Total Amount":"sum",
        "Total Quantity":"sum",
        "Unit Price":"mean"
    }).reset_index()

    for item in sku["Distribution Item"].unique():

        subset = sku[sku["Distribution Item"] == item]

        if len(subset) < 2:
            continue

        cheapest = subset.loc[subset["Unit Price"].idxmin()]
        expensive = subset.loc[subset["Unit Price"].idxmax()]

        savings = (
            expensive["Unit Price"] - cheapest["Unit Price"]
        ) * expensive["Total Quantity"]

        if savings > 0:

            advice.append({
                "Item": item,
                "Current Brand": expensive["Brand Name"],
                "Recommended Brand": cheapest["Brand Name"],
                "Potential Savings": round(savings,2)
            })

    advice_df = pd.DataFrame(advice).sort_values(
        "Potential Savings",
        ascending=False
    )

    return advice_df