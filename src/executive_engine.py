import pandas as pd

EXCLUDED_HOMES = ["Riordon Street Shelter", "Summer Street Shelter"]

def clean_data(df):
    df = df.copy()

    # Remove unwanted homes
    df = df[~df["Home"].isin(EXCLUDED_HOMES)]

    # Safe numeric conversion
    df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce")
    df["Total Quantity"] = pd.to_numeric(df["Total Quantity"], errors="coerce")

    # Cost per KG logic
    if "Standardized Weight (KG)" in df.columns:
        df["Standardized Weight (KG)"] = pd.to_numeric(df["Standardized Weight (KG)"], errors="coerce")
        df = df[df["Standardized Weight (KG)"] > 0]
        df["Cost_per_KG"] = df["Total Amount"] / df["Standardized Weight (KG)"]

    elif "BaseWeightKG" in df.columns:
        df["BaseWeightKG"] = pd.to_numeric(df["BaseWeightKG"], errors="coerce")
        df = df[df["BaseWeightKG"] > 0]
        df["Cost_per_KG"] = df["Total Amount"] / df["BaseWeightKG"]

    else:
        df["Cost_per_KG"] = df["Unit Price"]

    return df


def top10_groups(df):
    g = df.groupby("Major Group")["Total Amount"].sum().reset_index()
    return g.sort_values("Total Amount", ascending=False).head(10)


def savings_engine(df):
    sku = df.groupby(["Major Group","Brand Name"]).agg({
        "Cost_per_KG":"mean",
        "Total Quantity":"sum"
    }).reset_index()

    savings_total = 0
    insights = []

    for g in sku["Major Group"].unique():
        sub = sku[sku["Major Group"] == g]

        if len(sub) < 2:
            continue

        cheap = sub.loc[sub["Cost_per_KG"].idxmin()]
        exp = sub.loc[sub["Cost_per_KG"].idxmax()]

        savings = (exp["Cost_per_KG"] - cheap["Cost_per_KG"]) * exp["Total Quantity"]

        if savings > 500:
            savings_total += savings

            insights.append({
                "group": g,
                "drop": exp["Brand Name"],
                "keep": cheap["Brand Name"],
                "saving": savings
            })

    return savings_total, insights