def price_trend(df):

    df["Month"] = df["Date"].dt.to_period("M")

    return (
        df.groupby("Month")["Unit Price"]
        .mean()
        .sort_index()
    )