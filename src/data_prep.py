import pandas as pd

def prepare_data(df):

    if df is None:
        return df

    df = df.copy()

    # ---------------- REMOVE INVALID HOMES ----------------
    df = df[~df["Home"].isin([
        "Riordon Street Shelter",
        "Summer Street Shelter"
    ])]

    # ---------------- STANDARDIZE COST ----------------
    if "Standardized Weight (KG)" in df.columns:
        df["Cost_per_KG"] = df["Total Amount"] / df["Standardized Weight (KG)"]
    else:
        df["Cost_per_KG"] = df["Unit Price"]

    # ---------------- CLEAN BAD VALUES ----------------
    df = df[df["Cost_per_KG"] > 0]

    return df