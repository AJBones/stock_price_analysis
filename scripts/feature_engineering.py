import numpy as np
import pandas as pd

ftse100_path = "../data/raw/ftse_100_historic_prices.csv"
ftse250_path = "../data/raw/ftse_250_historic_prices.csv"
ftse100 = pd.read_csv(ftse100_path)
ftse250 = pd.read_csv(ftse250_path)

ftse100["Date"] = pd.to_datetime(ftse100["Date"])
ftse250["Date"] = pd.to_datetime(ftse250["Date"])
for data in [ftse100, ftse250]:
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.month
    data["DOM"] = data["Date"].dt.day
    data["Day"] = data["Date"].dt.dayofweek
    data["Week"] = data["Date"].dt.isocalendar().week
    data["DOY"] = data["Date"].dt.dayofyear

ftse100Cons = ftse100["Company"].unique()
ftse250Cons = ftse250["Company"].unique()

LAG_PERIODS = [1, 2, 7, 14]
ROLLING_WINDOWS = [7, 30]
FEATURES_TO_LAG = ["Close", "Open", "High", "Low", "Volume"]

ftse100_lagged = []
for company in ftse100Cons:
    subset = ftse100.loc[ftse100["Company"] == company]
    for lag in LAG_PERIODS:
        for feature in FEATURES_TO_LAG:
            subset.loc[:, f"{feature}_lag_{lag}"] = subset[feature].shift(lag)
    # Rolling mean features
    for window in ROLLING_WINDOWS:
        for feature in FEATURES_TO_LAG:
            subset.loc[:, f"{feature}_rolling_mean_{window}"] = (
                subset[feature].shift(1).rolling(window=window).mean()
            )
    subset = subset.dropna()
    ftse100_lagged.append(subset)

ftse100_proc = pd.concat(ftse100_lagged, ignore_index=True)
ftse100_proc.to_csv("../data/processed/ftse100_historic_prices.csv", index=False)

ftse250_lagged = []
for company in ftse250Cons:
    subset = ftse250.loc[ftse250["Company"] == company]
    for lag in LAG_PERIODS:
        for feature in FEATURES_TO_LAG:
            subset.loc[:, f"{feature}_lag_{lag}"] = subset[feature].shift(lag)
    # Rolling mean features
    for window in ROLLING_WINDOWS:
        for feature in FEATURES_TO_LAG:
            subset.loc[:, f"{feature}_rolling_mean_{window}"] = (
                subset[feature].shift(1).rolling(window=window).mean()
            )
    subset = subset.dropna()
    ftse250_lagged.append(subset)

ftse250_proc = pd.concat(ftse250_lagged, ignore_index=True)
ftse250_proc.to_csv("../data/processed/ftse250_historic_prices.csv", index=False)
