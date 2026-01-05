import pandas as pd
import yfinance as yf

# TODO: Get the below working without getting the 403 forbidden error. Spend some time on this. In the meantime, just
# use a direct grab of the Wikipedia table as a CSV file.
# Get list of tickers for FTSE 250 index from Wikipedia
# ftse250_tickers = pd.read_html('https://en.wikipedia.org/wiki/FTSE_250_Index')[2]
ftse_100_path = "../data/raw/ftse_100.csv"
ftse_100 = pd.read_csv(ftse_100_path)
ftse_250_path = "../data/raw/ftse_250.csv"
ftse_250 = pd.read_csv(ftse_250_path)

# Time to retrieve the data for each of the constituents for modelling
price_data_100 = pd.DataFrame()
price_data_250 = pd.DataFrame()
start_date = "2015-01-01"
end_date = "2025-12-31"
print("Getting data for FTSE 100 companies...")
for i in range(len(ftse_100)):
    ticker = ftse_100.loc[i, "Ticker"] + ".L"
    response = yf.download(ticker, start=start_date, end=end_date)
    data = response.loc[:, ["Close", "Open", "High", "Low", "Volume"]]
    data.columns = data.columns.droplevel(1)
    data["Company"] = ftse_100.loc[i, "Company"]
    data["Ticker"] = ftse_100.loc[i, "Ticker"]
    data["Sector"] = ftse_100.loc[i, "FTSE industry classification benchmark sector"]
    data.reset_index(inplace=True)
    price_data_100 = pd.concat([price_data_100, data], axis=0, ignore_index=True)
price_data_100.to_csv("../data/raw/ftse_100_historic_prices.csv", index=False)

print("Getting data for FTSE 250 companies...")
for i in range(len(ftse_250)):
    ticker = ftse_250.loc[i, "Ticker"] + ".L"
    response = yf.download(ticker, start=start_date, end=end_date)
    data = response.loc[:, ["Close", "Open", "High", "Low", "Volume"]]
    data.columns = data.columns.droplevel(1)
    data["Company"] = ftse_250.loc[i, "Company"]
    data["Ticker"] = ftse_250.loc[i, "Ticker"]
    data["Sector"] = ftse_250.loc[i, "FTSE Industry Classification Benchmark sector"]
    data.reset_index(inplace=True)
    price_data_250 = pd.concat([price_data_250, data], axis=0, ignore_index=True)
price_data_250.to_csv("../data/raw/ftse_250_historic_prices.csv", index=False)
