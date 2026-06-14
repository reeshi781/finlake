"""Load extracted company data into PostgreSQL company_master table."""

import argparse
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from src.config.db import get_database_url

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "company_master.csv"

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


def load_company_master(data_path: Path) -> int:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    if data_path.suffix == ".parquet":
        df = pd.read_parquet(data_path)
    else:
        df = pd.read_csv(data_path)

    expected_columns = {
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
    }
    missing = expected_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in data file: {sorted(missing)}")

    records = df[list(expected_columns)].to_dict(orient="records")
    engine = create_engine(get_database_url())

    with engine.begin() as conn:
        conn.execute(UPSERT_SQL, records)

    print(f"Loaded {len(records)} rows into company_master from {data_path}")
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load company_master data into PostgreSQL")
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to CSV or Parquet file with company data",
    )
    args = parser.parse_args()
    load_company_master(args.path)


if __name__ == "__main__":
    main()
