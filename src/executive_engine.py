import pandas as pd


# -----------------------------------
# EXECUTIVE SUMMARY ENGINE
# -----------------------------------

def generate_executive_summary(df):

    total_spend = df["Total Amount"].sum()
    avg_price = df["Unit Price"].mean()

    highest_group = df.groupby("Major Group")["Total Amount"].sum().idxmax()
    highest_home = df.groupby("Home")["Total Amount"].sum().idxmax()

    summary = f"""
    Total procurement spend is ${total_spend:,.0f}. 
    The highest spending category is {highest_group}. 
    {highest_home} is the highest spending LTC home. 
    Average unit price is ${avg_price:.2f}.
    """

    return summary


# -----------------------------------
# SCENARIO SIMULATOR
# -----------------------------------

def scenario_simulator(df, reduction_percent=10):

    scenario = df.copy()

    scenario["Adjusted Quantity"] = scenario["Total Quantity"] * (1 - reduction_percent / 100)

    scenario["Adjusted Spend"] = scenario["Adjusted Quantity"] * scenario["Unit Price"]

    original_spend = df["Total Amount"].sum()
    new_spend = scenario["Adjusted Spend"].sum()

    savings = original_spend - new_spend

    return {
        "Original Spend": original_spend,
        "New Spend": new_spend,
        "Savings": savings
    }


# -----------------------------------
# AI RECOMMENDATION ENGINE
# -----------------------------------

def generate_ai_recommendations(df):

    recommendations = []

    group_cost = df.groupby("Major Group").agg({
        "Total Amount":"sum",
        "Total Quantity":"sum"
    })

    group_cost["Unit Cost"] = group_cost["Total Amount"] / group_cost["Total Quantity"]

    high_cost = group_cost.sort_values("Unit Cost", ascending=False).head(5)

    for group, row in high_cost.iterrows():

        recommendations.append(
            f"Reduce spending in {group}. Current unit cost is ${row['Unit Cost']:.2f}, which is above average."
        )

    return recommendations