def detect_anomalies(df):

    alerts = []

    avg = df["Cost_per_KG"].mean()

    if (df["Cost_per_KG"] > avg * 2).sum() > 10:
        alerts.append("🔴 High cost inefficiency detected")

    supplier = df.groupby("Distributor")["Total Amount"].sum()
    if not supplier.empty:
        if supplier.max() / supplier.sum() > 0.4:
            alerts.append("🔴 Supplier concentration risk")

    if (df["Cost_per_KG"] == 0).sum() > 0:
        alerts.append("🟠 Zero-cost data issue")

    return alerts