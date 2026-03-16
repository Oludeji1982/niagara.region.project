def total_spend(df):

    return df["Total Amount"].sum()


def spend_by_home(df):

    return (
        df.groupby("Facility")["Total Amount"]
        .sum()
        .sort_values(ascending=False)
    )


def spend_by_supplier(df):

    return (
        df.groupby("Distributor")["Total Amount"]
        .sum()
        .sort_values(ascending=False)
    )


def sku_count(df):

    return df["Item Name"].nunique()


def top_products(df):

    return (
        df.groupby("Item Name")["Total Qty"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )