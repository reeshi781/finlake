-- Enriched company data from yfinance extract

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
