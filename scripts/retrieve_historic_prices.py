import argparse
import pandas as pd
import yfinance as yf
from datetime import date


def retrieve_data(input=pd.DataFrame, start_date=str, end_date=str, output=str):
    """
    Retrieves the historic stock prices for the given tickers.
    """
    price_data = pd.DataFrame()

    for i in range(len(input)):
        ticker = input.loc[i, "Ticker"] + ".L"
        response = yf.download(ticker, start=start_date, end=end_date)
        data = response.loc[:, ["Close", "Open", "High", "Low", "Volume"]]
        data.columns = data.columns.droplevel(1)
        data["Company"] = input.loc[i, "Company"]
        data["Ticker"] = input.loc[i, "Ticker"]
        data["Sector"] = input.loc[i, "FTSE industry classification benchmark sector"]
        data.reset_index(inplace=True)
        price_data = pd.concat([price_data, data], axis=0, ignore_index=True)
    price_data.to_csv(output, index=False)


def main():
    parser = argparse.ArgumentParser(description="Stock price retriever script")
    parser.add_argument("-i", "--input")
    parser.add_argument("-s", "--start", default="2025-01-01")
    parser.add_argument("-e", "--end", default=date.today().strftime("%Y-%m-%d"))
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    # TODO: Get the below working without getting the 403 forbidden error. Spend some time on this. In the meantime, just
    # use a direct grab of the Wikipedia table as a CSV file.
    # Get list of tickers for FTSE 250 index from Wikipedia
    # ftse250_tickers = pd.read_html('https://en.wikipedia.org/wiki/FTSE_250_Index')[2]
    # ftse_100_path = "../data/raw/ftse_100.csv"
    # ftse_100 = pd.read_csv(ftse_100_path)
    # ftse_250_path = "../data/raw/ftse_250.csv"
    # ftse_250 = pd.read_csv(ftse_250_path)
    input = pd.read_csv(args.input)
    retrieve_data(input, args.start, args.end, args.output)


if __name__ == "__main__":
    main()
