CREATE DATABASE IF NOT EXISTS stock_prices;
CREATE TABLE dim_company (
    company_id INT NOT NULL,
    company_name VARCHAR(250) NOT NULL,
    company_ticker VARCHAR(5) NOT NULL,
    sector VARCHAR(250) NOT NULL,
    exchange VARCHAR(250) NOT NULL,
    is_active BOOLEAN,
    PRIMARY KEY (company_id)
);
CREATE TABLE dim_date (
    date_id INT NOT NULL,
    calendar_date DATE NOT NULL,
    year YEAR NOT NULL,
    quarter SMALLINT NOT NULL,
    month,
    day_of_week,
    is_trading_day BOOLEAN,
);
CREATE TABLE fact_daily_prices (
    fact_id INT NOT NULL,
    company_id INT NOT NULL,
    date_id INT NOT NULL,
    open_price INT NOT NULL,
    high_price INT NOT NULL,
    low_price INT NOT NULL,
    close_price INT NOT NULL,
    volume INT NOT NULL,
    daily_return INT NOT NULL,
    created_at_utc TIMESTAMP NOT NULL
);