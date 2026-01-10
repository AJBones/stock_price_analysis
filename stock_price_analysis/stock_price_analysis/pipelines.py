import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DynamicCyclicalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, date_column):
        self.date_column = date_column

    def fit(self, X, y=None):
        return self  # Nothing to learn from the data

    def transform(self, X):
        X_out = X.copy()
        dates = pd.to_datetime(X_out[self.date_column])

        # 1. Day of Month (Dynamic Max: 28, 29, 30, or 31)
        days_in_month = dates.dt.days_in_month
        X_out["day_month_sin"] = np.sin(2 * np.pi * dates.dt.day / days_in_month)
        X_out["day_month_cos"] = np.cos(2 * np.pi * dates.dt.day / days_in_month)

        # 2. Day of Year (Dynamic Max: 365 or 366)
        days_in_year = dates.dt.is_leap_year.map({True: 366, False: 365})
        X_out["day_year_sin"] = np.sin(2 * np.pi * dates.dt.dayofyear / days_in_year)
        X_out["day_year_cos"] = np.cos(2 * np.pi * dates.dt.dayofyear / days_in_year)

        # 3. Month (Fixed Max: 12)
        X_out["month_sin"] = np.sin(2 * np.pi * dates.dt.month / 12)
        X_out["month_cos"] = np.cos(2 * np.pi * dates.dt.month / 12)

        # TODO: Add encoding for day of week

        # Drop the original date column to keep it clean for sklearn
        return X_out.drop(columns=[self.date_column])
