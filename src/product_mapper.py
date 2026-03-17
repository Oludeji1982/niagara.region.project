def classify_product(text):

    text = str(text).lower()

    mapping = {
        "ground coffee": "Ground Coffee",
        "liquid coffee": "Frozen Liquid Coffee",
        "skim": "Skim Milk",
        "2%": "2% Milk",
        "beef patty": "Beef Patties"
    }

    for keyword, category in mapping.items():

        if keyword in text:
            return category

    return "Other"