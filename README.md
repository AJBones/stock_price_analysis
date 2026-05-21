# stock_price_analysis
Exploratory data analysis project working on forecasting stocks and shares prices from historical data.

This project is mainly for self directed learning and is unlikely to yield anything that could be used for
real stock price prediction. The aims of this project are for me to learn some common forecasting and time 
series prediction methods, ideally do some data engineering by retrieving data from a range of different
sources and combining them for data analysis, and finally just to have some fun with data outside of my
usually work.

Data can be retrieved using the script `retrieve_historic_prices.py` on the command line. This is just a
wrapper around the Yahoo finance API - it gets a list of tickers from a CSV file (there are two included
in the repo listing FTSE 100 and FTSE 250 companies and their tickers. By default, it gets data from 
1st January 2015 until the current date, but these can be specified. It will save these to the specified 
csv file.

Example usage: `python retrieve_historic_prices.py -i ../data/raw/ftse_100.csv -o "../data/processed/ftse100_historic_prices.csv"`

The rest of the notebooks will include some exploratory analysis and visualisations. Long term aim is to
use the notebook code to create applications that users can interact with.

