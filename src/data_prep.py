import pandas as pd

def prepare_data(df):

    # REMOVE unwanted homes
    df = df[~df["Home"].isin(["Riordon Street Shelter", "Summer Street Shelter"])]

    # COST PER KG SAFE LOGIC
    if "Standardized Weight (KG)" in df.columns:
        df = df[df["Standardized Weight (KG)"] > 0]
        df["Cost_per_KG"] = df["Total Amount"] / df["Standardized Weight (KG)"]

    elif "BaseWeightKG" in df.columns:
        df = df[df["BaseWeightKG"] > 0]
        df["Cost_per_KG"] = df["Total Amount"] / df["BaseWeightKG"]

    else:
        df["Cost_per_KG"] = df["Unit Price"]

    return df