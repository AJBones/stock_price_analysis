import argparse
import datetime
import os

import pandas as pd
import yfinance as yf


def retrieve_data(input_df=pd.DataFrame, start_date=str, end_date=str):
    """Retrieves historic stock prices and standardises column formats to load into database"""
    all_prices = []

    for _, row in input_df.iterrows():
        raw_ticker = str(row["Ticker"]).strip()
        # Ensure LSE ticker extension (.L) is present
        yf_ticker = raw_ticker if raw_ticker.endswith(".L") else f"{raw_ticker}.L"

        try:
            response = yf.download(
                yf_ticker,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=False
            )

            if response.empty:
                continue

            # Flatten MultiIndex columns if present
            if isinstance(response.columns, pd.MultiIndex):
                response.columns = response.columns.get_level_values(0)
            
            data = response[["Open", "High", "Low", "Close", "Volume"]].copy()
            data.reset_index(inplace=True)

            data["company_ticker"] = raw_ticker
            data["company_name"] = row["Company"]
            data["sector"] = row.get("FTSE industry classification benchmark sector", "Unknown")
            data["exchange"] = "LSE"

            all_prices.append(data)

        except Exception as e:
            print(f"Error fetching data for {raw_ticker}: {e}")
        
    if not all_prices:
        return pd.DataFrame()

    combined_df = pd.concat(all_prices, axis=0, ignore_index=True)

    # Name columns to enable loading
    combined_df.rename(
        columns={
            "Date": "calendar_date",
            "Open": "open_price",
            "High": "high_price",
            "Low": "low_price",
            "Close": "close_price",
            "Volume": "volume"
        },
        inplace=True
    )
    # Calculate daily return percentage
    combined_df["daily_return"] = (
        (combined_df["close_price"] - combined_df["open_price"]) / combined_df["open_price"]
    ).round(4)

    return combined_df

    
def main():
    parser = argparse.ArgumentParser(description="Stock price retriever script")
    parser.add_argument("-i", "--input", required=True, help="Path to input ticker CSV")
    parser.add_argument("-s", "--start", default="1990-04-01")
    parser.add_argument("-e", "--end", default=datetime.datetime.now(tz=datetime.timezone.utc).date().strftime("%Y-%m-%d"))
    parser.add_argument("-o", "--output-dir", default="data/landing")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    
    input_df = pd.read_csv(args.input)
    price_df = retrieve_data(input_df, args.start, args.end)

    if not price_df.empty:
        # Add timestamp when writing file for logging
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"stock_extract_{timestamp}.csv"
        filepath = os.path.join(args.output_dir, filename)
        
        price_df.to_csv(filepath, index=False)
        print(f"Successfully landed raw extract to: {filepath}")
    else:
        print("No data retrieved.")


if __name__ == "__main__":
    main()