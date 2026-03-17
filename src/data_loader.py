import pandas as pd


def load_purchases(path):

    df = pd.read_csv(path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Standardize column names
    df = df.rename(columns={
        "Total Amount": "TotalAmount",
        "Total Quantity": "TotalQuantity",
        "Brand Name": "BrandName",
        "Unit Price": "UnitPrice",
        "Major Group": "MajorGroup"
    })

    return df


def load_production(path):

    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    return df