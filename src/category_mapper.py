def classify_product(text):

    text = str(text).lower()

    if "ground coffee" in text:
        return "Ground Coffee"

    if "liquid coffee" in text:
        return "Frozen Liquid Coffee"

    if "skim" in text:
        return "Skim Milk"

    if "2%" in text:
        return "2% Milk"

    if "beef patty" in text:
        return "Beef Patties"

    return "Other"