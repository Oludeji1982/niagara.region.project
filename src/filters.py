import streamlit as st

def apply_filters(df):

    st.sidebar.header("Filters")

    homes = st.sidebar.multiselect(
        "Home",
        sorted(df["Home"].unique()),
        default=sorted(df["Home"].unique()),
        key="home_filter_global"
    )

    distributors = st.sidebar.multiselect(
        "Distributor",
        sorted(df["Distributor"].unique()),
        default=sorted(df["Distributor"].unique()),
        key="dist_filter_global"
    )

    groups = st.sidebar.multiselect(
        "Major Group",
        sorted(df["Major Group"].unique()),
        default=sorted(df["Major Group"].unique()),
        key="group_filter_global"
    )

    filtered = df[
        (df["Home"].isin(homes)) &
        (df["Distributor"].isin(distributors)) &
        (df["Major Group"].isin(groups))
    ]

    return filtered
    