import pandas as pd


def clean_purchases(df):

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce")

    df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce")

    return df


def clean_production(df):

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df


def clean_menu_cost(df):

    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

    return df