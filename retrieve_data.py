import pandas as pd
import yfinance as yf

#TODO: Complete list of companies in the FTSE250 index
ticker = "^FTMC"

data = yf.download(ticker, start='2015-01-01', end='2025-12-29')

#TODO: Get the below working without getting the 403 forbidden error. Spend some time on this. In the meantime, just
# use a direct grab of the Wikipedia table as a CSV file.
# Get list of tickers for FTSE 250 index from Wikipedia
# ftse250_tickers = pd.read_html('https://en.wikipedia.org/wiki/FTSE_250_Index')[2]
ftse_path = '../data/ftse_250.csv'
ftse_250 = pd.read_csv(ftse_path)

# Time to retrieve the data for each of the constituents for modelling
price_data = pd.DataFrame()
start_date = '2015-01-01'
end_date = '2025-12-30'
for i in range(len(ftse_250)):
    ticker = ftse_250.loc[i, 'Ticker'] + '.L'
    response = yf.download(ticker, start=start_date, end=end_date)
    data = response.loc[:,['Close', 'Open', 'High', 'Low', 'Volume']]
    data.columns = data.columns.droplevel(1)
    print(data.head())
    print(data.columns)
    data['Company'] = ftse_250.loc[i, 'Company']
    data['Ticker'] = ftse_250.loc[i, 'Ticker']
    data['Sector'] = ftse_250.loc[i, 'FTSE Industry Classification Benchmark sector']
    data.reset_index(inplace=True)
    print(data.columns)
    price_data = pd.concat([price_data, data], axis=0, ignore_index=True)
price_data.to_csv('../data/ftse_250_historic_prices.csv')
    
