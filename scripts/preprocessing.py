import pandas as pd
from datetime import date


def fill_dates(
    df=pd.DataFrame, date_col=str, target_col=str, format=str, series_end=date
):
    """
    Used for filling in gaps when a feature logs specific instances for example
    changes in Bank of England base rate, but the data needs to be extended so
    that the date column is continuous, and the value is populated from the raw
    change data.
    """
    try:
        df[date_col] = pd.to_datetime(df[date_col], format=format)
    except pd._libs.tslibs.parsing.DateParseError:
        print("Please check columns and provided date format and try again.")
    start = df[date_col].min()
    end = df[date_col].max()
    df.sort_values(by=date_col, inplace=True)
    dates = pd.date_range(start, end)
    vals = []
    # Calculate the difference between each dates and then add the value that many times
    # to the list
    for i in range(0, len(df) - 1):
        diff = (df.loc[i + 1, date_col] - df.loc[i, date_col]).days
        vals.append([df.loc[i, target_col]] * diff)
    # Fill in from the final dataframe value until the specified end_date
    if series_end > df.loc[len(df) - 1, date_col]:
        diff = (series_end - df.loc[len(df) - 1, date_col]).days
        vals.append(df.loc[len(df) - 1, target_col] * diff)
        vals.append([df.loc[i, target_col]] * diff)
    flat_vals = [x for xs in vals for x in xs]
    out = pd.DataFrame(date_col=dates, target_col=vals)
    return out
