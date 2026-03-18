import pandas as pd

def reduce_dmi_df(df):
    df = df.copy()

    # Tider: object -> datetime
    df["created"] = pd.to_datetime(df["created"])
    df["observed"] = pd.to_datetime(df["observed"])

    # Få unikke værdier -> category
    df["parameterId"] = df["parameterId"].astype("category")

    # Taltyper gøres mindre
    df["coordsx"] = df["coordsx"].astype("float32")
    df["coordsy"] = df["coordsy"].astype("float32")
    df["value"] = df["value"].astype("float32")
    df["stationId"] = pd.to_numeric(df["stationId"], downcast="integer")

    return df

