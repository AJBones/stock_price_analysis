CREATE DATABASE IF NOT EXISTS stock_prices;
-- Company dimension table
CREATE TABLE dim_company (
    company_id BIGINT NOT NULL AUTO_INCREMENT,
    company_name VARCHAR(250) NOT NULL,
    company_ticker VARCHAR(10) NOT NULL,
    sector VARCHAR(250) NOT NULL,
    exchange VARCHAR(250) NOT NULL,
    is_active BOOLEAN,
    PRIMARY KEY (company_id),
    UNIQUE KEY idx_ticker (company_ticker)
);
-- Date dimension table
CREATE TABLE dim_date (
    date_id INT NOT NULL,
    calendar_date DATE NOT NULL,
    year YEAR NOT NULL,
    quarter TINYINT NOT NULL,
    month TINYINT NOT NULL,
    day_of_week TINYINT NOT NULL,
    is_trading_day BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (date_id),
    UNIQUE KEY idx_calendar_date (calendar_date)
);
-- Daily prices fact table
CREATE TABLE fact_daily_prices (
    fact_id BIGINT NOT NULL AUTO_INCREMENT,
    company_id BIGINT NOT NULL,
    date_id INT NOT NULL,
    open_price DECIMAL(12, 2) NOT NULL,
    high_price DECIMAL(12, 2) NOT NULL,
    low_price DECIMAL(12, 2) NOT NULL,
    close_price DECIMAL(12, 2) NOT NULL,
    volume BIGINT NOT NULL,
    daily_return DECIMAL(8,4) NOT NULL,
    created_at_utc TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (fact_id),
    UNIQUE KEY idx_company_date (company_id, date_id),
    CONSTRAINT fk_fact_company FOREIGN KEY (company_id) REFERENCES dim_company (company_id),
    CONSTRAINT fk_fact_date FOREIGN KEY (date_id) REFERENCES dim_date (date_id)    
);
