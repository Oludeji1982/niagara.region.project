import pandas as pd
from sklearn.ensemble import RandomForestRegressor


# ----------------------------------------
# DEMAND FORECASTING AI
# ----------------------------------------

def demand_forecast_model(df):

    data = df.copy()

    # Create time index (proxy since no date column)
    data["time_index"] = range(len(data))

    grouped = data.groupby(
        ["Home", "Major Group"]
    ).agg({
        "Total Quantity": "sum",
        "time_index": "mean"
    }).reset_index()

    X = grouped[["time_index"]]
    y = grouped["Total Quantity"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    grouped["Predicted Next Demand"] = model.predict(X) * 1.05  # slight growth assumption

    return grouped[[
        "Home",
        "Major Group",
        "Total Quantity",
        "Predicted Next Demand"
    ]]


# ----------------------------------------
# WASTE DETECTION AI
# ----------------------------------------

def waste_detection_model(df):

    waste = df.groupby(
        ["Home", "Major Group"]
    ).agg({
        "Total Quantity": "sum",
        "Total Amount": "sum"
    }).reset_index()

    waste["Unit Cost"] = waste["Total Amount"] / waste["Total Quantity"]

    # Detect outliers (inefficient spending)
    threshold = waste["Unit Cost"].mean() + waste["Unit Cost"].std()

    waste["Waste Flag"] = waste["Unit Cost"] > threshold

    waste["Waste Severity"] = (
        waste["Unit Cost"] - waste["Unit Cost"].mean()
    )

    return waste.sort_values("Waste Severity", ascending=False)