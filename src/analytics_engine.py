import pandas as pd

# ================= ANOMALY DETECTION =================
def detect_anomalies(df):

    alerts = []

    if "Cost_per_KG" not in df.columns:
        return alerts

    avg_cost = df["Cost_per_KG"].mean()

    high_cost = df[df["Cost_per_KG"] > avg_cost * 2]

    if not high_cost.empty:
        alerts.append(f"⚠️ {len(high_cost)} products priced >2x average")

    supplier_spend = df.groupby("Distributor")["Total Amount"].sum()

    if not supplier_spend.empty:
        max_supplier = supplier_spend.max()
        total = supplier_spend.sum()

        if max_supplier / total > 0.4:
            alerts.append("🔴 Supplier concentration risk (>40%)")

    if (df["Cost_per_KG"] == 0).sum() > 0:
        alerts.append("🟠 Zero-cost items detected (data issue)")

    return alerts


# ================= SUPPLIER RISK =================
def supplier_risk(df):

    supplier = df.groupby("Distributor")["Total Amount"].sum().reset_index()

    total = supplier["Total Amount"].sum()

    supplier["Share"] = supplier["Total Amount"] / total

    supplier["Risk"] = supplier["Share"].apply(
        lambda x: "HIGH" if x > 0.30 else ("MEDIUM" if x > 0.15 else "LOW")
    )

    return supplier