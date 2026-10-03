-- db/markets_schema.sql
CREATE TABLE IF NOT EXISTS markets.price_history (
    ticker VARCHAR(20),
    trade_date DATE,
    open_price NUMERIC(15, 6),
    high_price NUMERIC(15, 6),
    low_price NUMERIC(15, 6),
    close_price NUMERIC(15, 6),
    volume BIGINT,
    PRIMARY KEY (ticker, trade_date)
);

-- Index the date column since time-series queries rely heavily on date ranges
CREATE INDEX IF NOT EXISTS idx_markets_date ON markets.price_history(trade_date);