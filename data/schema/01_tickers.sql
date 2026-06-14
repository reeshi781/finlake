-- Input ticker list (seeded from data/raw/company_master.csv)

CREATE TABLE IF NOT EXISTS tickers (
    ticker      VARCHAR(32) PRIMARY KEY,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
