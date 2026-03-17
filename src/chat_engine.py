import pandas as pd

def simple_chat(df, query):

    query = query.lower()

    if "spend" in query:
        return f"Total spend is ${df['Total Amount'].sum():,.0f}"

    elif "highest" in query:
        top = df.groupby("Major Group")["Total Amount"].sum().idxmax()
        return f"Highest spending category is {top}"

    elif "cheapest" in query:
        cheapest = df.loc[df["Unit Price"].idxmin()]
        return f"Cheapest item is {cheapest['Distribution Item']} at ${cheapest['Unit Price']:.2f}"

    else:
        return "Try asking about spend, highest category, or cheapest item."