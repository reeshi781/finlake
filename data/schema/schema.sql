-- Full schema (used by init_db.py)
-- Per-table files: 01_tickers.sql, 02_company_master.sql

CREATE TABLE IF NOT EXISTS tickers (
    ticker      VARCHAR(32) PRIMARY KEY,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS company_master (
    ticker             VARCHAR(32) PRIMARY KEY,
    company_name       TEXT,
    short_name         TEXT,
    sector             TEXT,
    industry           TEXT,
    country            TEXT,
    city               TEXT,
    currency           VARCHAR(16),
    exchange           TEXT,
    website            TEXT,
    logo_url           TEXT,
    employee_count     DOUBLE PRECISION,
    market_cap         BIGINT,
    enterprise_value   BIGINT,
    business_summary   TEXT,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_company_master_sector ON company_master (sector);
CREATE INDEX IF NOT EXISTS idx_company_master_country ON company_master (country);
