def prepared_total(df):

    return df["TotalToPrepare"].sum()


def served_total(df):

    return df["Portions"].sum()


def waste_estimate(df):

    return prepared_total(df) - served_total(df)


def waste_rate(df):

    waste = waste_estimate(df)

    prepared = prepared_total(df)

    return waste / prepared