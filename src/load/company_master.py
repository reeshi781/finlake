"""Shared upsert logic for company_master table."""

from sqlalchemy import create_engine, text

from src.config.db import get_database_url

COMPANY_MASTER_COLUMNS = [
    "ticker",
    "company_name",
    "short_name",
    "sector",
    "industry",
    "country",
    "city",
    "currency",
    "exchange",
    "website",
    "logo_url",
    "employee_count",
    "market_cap",
    "enterprise_value",
    "business_summary",
]

UPSERT_SQL = text(
    """
    INSERT INTO company_master (
        ticker, company_name, short_name, sector, industry, country, city,
        currency, exchange, website, logo_url, employee_count,
        market_cap, enterprise_value, business_summary
    ) VALUES (
        :ticker, :company_name, :short_name, :sector, :industry, :country, :city,
        :currency, :exchange, :website, :logo_url, :employee_count,
        :market_cap, :enterprise_value, :business_summary
    )
    ON CONFLICT (ticker) DO UPDATE SET
        company_name = EXCLUDED.company_name,
        short_name = EXCLUDED.short_name,
        sector = EXCLUDED.sector,
        industry = EXCLUDED.industry,
        country = EXCLUDED.country,
        city = EXCLUDED.city,
        currency = EXCLUDED.currency,
        exchange = EXCLUDED.exchange,
        website = EXCLUDED.website,
        logo_url = EXCLUDED.logo_url,
        employee_count = EXCLUDED.employee_count,
        market_cap = EXCLUDED.market_cap,
        enterprise_value = EXCLUDED.enterprise_value,
        business_summary = EXCLUDED.business_summary,
        updated_at = NOW()
    """
)


def upsert_company_master(records: list[dict]) -> int:
    if not records:
        print("No records to upsert.")
        return 0

    engine = create_engine(get_database_url())
    with engine.begin() as conn:
        conn.execute(UPSERT_SQL, records)

    print(f"Upserted {len(records)} rows into company_master")
    return len(records)
