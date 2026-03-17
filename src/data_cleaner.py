import pandas as pd


def clean_purchases(df):

    # Rename columns to consistent names used in the analytics code
    df = df.rename(columns={
        "Home": "Facility",
        "Distribution Item": "ItemName",
        "Operations Category": "Category",
        "Major Group": "MajorGroup",
        "Brand Name": "BrandName",
        "Pack Size": "PackSize",
        "Total Quantity": "TotalQty",
        "Total Amount": "TotalAmount",
        "Unit Price": "UnitPrice"
    })

    # Convert numeric columns safely
    for col in ["TotalAmount", "UnitPrice", "TotalQty"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def clean_production(df):

    df = df.rename(columns={
        "Total To Prepare": "TotalToPrepare",
        "Total to Prepare": "TotalToPrepare",
        "Item": "ItemName"
    })

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "TotalToPrepare" in df.columns:
        df["TotalToPrepare"] = pd.to_numeric(df["TotalToPrepare"], errors="coerce")

    if "Portions" in df.columns:
        df["Portions"] = pd.to_numeric(df["Portions"], errors="coerce")

    return df


def clean_menu_cost(df):

    if "Total" in df.columns:
        df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

    return df