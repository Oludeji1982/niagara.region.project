import pandas as pd

def load_purchases(path):

    try:
        df = pd.read_csv(path)
        return df

    except Exception as e:
        print("Error loading purchases:", e)
        return None


def load_production(path):

    try:
        return pd.read_csv(path)

    except:
        return None


def load_menu_cost(path):

    try:
        return pd.read_csv(path)

    except:
        return None


def load_homes(path):

    try:
        return pd.read_csv(path)

    except:
        return None