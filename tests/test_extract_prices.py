from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from scripts.extract_prices import main, retrieve_data


# --- retrieve_data tests ---
@pytest.fixture
def sample_input_df():
    return pd.DataFrame({
        "Ticker": ["ULVR", "BATS"],
        "Company": ["Unilever", "British American Tobacco"],
        "FTSE industry classification benchmark sector": ["Consumer Staples", "Consumer Staples"]
    })

@patch("scripts.extract_prices.yf.download")
def test_retrieve_data_ticker_normalization(mock_download, sample_input_df):
    mock_download.return_value = pd.DataFrame({
        "Date": "2023-01-01", "Open": [100], "High": [105], "Low": [95], "Close": [102], "Volume": [1000]
    })
    
    result = retrieve_data(sample_input_df, "2023-01-01", "2023-01-02")
    
    # Check ticker normalization
    assert "ULVR.L" in result["company_ticker"].values  # ULVR → ULVR.L
    assert "BATS.L" in result["company_ticker"].values  # BATS → BATS.L

@patch("scripts.extract_prices.yf.download")
def test_retrieve_data_column_renaming(mock_download, sample_input_df):
    mock_download.return_value = pd.DataFrame({
        "Open": [100], "High": [105], "Low": [95], "Close": [102], "Volume": [1000]}, index=pd.to_datetime(["2023-01-01"]))
    
    result = retrieve_data(sample_input_df, "2023-01-01", "2023-01-02")
    
    assert list(result.columns) == [
        "index", "open_price", "high_price", "low_price", 
        "close_price", "volume", "company_ticker", "company_name", 
        "sector", "exchange", "daily_return"
    ]

@patch("scripts.extract_prices.yf.download")
def test_retrieve_data_daily_return_calc(mock_download, sample_input_df):
    mock_download.return_value = pd.DataFrame({
        "Open": [100], "High": [105], "Low": [95], "Close": [105], "Volume": [1000]
    }, index=pd.to_datetime(["2023-01-01"]))
    
    result = retrieve_data(sample_input_df, "2023-01-01", "2023-01-02")
    assert result["daily_return"].iloc[0] == 0.05  # (105-100)/100

def test_retrieve_data_empty_input():
    result = retrieve_data(pd.DataFrame(), "2023-01-01", "2023-01-02")
    assert result.empty

@patch("scripts.extract_prices.yf.download")
def test_retrieve_data_multiindex_columns(mock_download, sample_input_df):
    mock_download.return_value = pd.DataFrame(
        {("Open", "adj"): [100], ("Close", "adj"): [105]},
        index=pd.to_datetime(["2023-01-01"])
    )
    result = retrieve_data(sample_input_df, "2023-01-01", "2023-01-02")
    assert not isinstance(result.columns, pd.MultiIndex)

# --- main() tests ---
@patch("scripts.extract_prices.argparse.ArgumentParser")
@patch("scripts.extract_prices.os.makedirs")
@patch("scripts.extract_prices.pd.read_csv")
@patch("scripts.extract_prices.retrieve_data")
@patch("scripts.extract_prices.datetime.datetime")
def test_main_success(mock_datetime, mock_retrieve, mock_read_csv, mock_makedirs, mock_parser):
    # Setup mocks
    mock_args = MagicMock()
    mock_args.input = "input.csv"
    mock_args.start = "2023-01-01"
    mock_args.end = "2023-01-02"
    mock_args.output_dir = "data/landing"
    mock_parser.return_value.parse_args.return_value = mock_args
    mock_read_csv.return_value = pd.DataFrame({"Ticker": ["UU."], "Company": ["Unilever"]})
    mock_retrieve.return_value = pd.DataFrame({"calendar_date": ["2023-01-01"]})
    mock_datetime.now.return_value.strftime.return_value = "20230101_120000"
    
    with patch("scripts.extract_prices.pd.DataFrame.to_csv") as mock_to_csv:
        main()
        mock_to_csv.assert_called_once()
        mock_makedirs.assert_called_once_with("data/landing", exist_ok=True)

@patch("scripts.extract_prices.argparse.ArgumentParser")
def test_main_missing_input(mock_parser):
    mock_parser.return_value.parse_args.side_effect = SystemExit
    with pytest.raises(SystemExit):
        main()