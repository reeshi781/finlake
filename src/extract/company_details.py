"""Read tickers from DB, extract company details via yfinance, upsert into company_master."""

import sys
import warnings
from pathlib import Path
from time import sleep

import yfinance as yf
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.db import get_database_url

warnings.filterwarnings("ignore")

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


def get_logo_url(ticker: str) -> str:
    return f"https://financialmodelingprep.com/image-stock/{ticker}.png"


def read_tickers() -> list[str]:
    engine = create_engine(get_database_url())
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT ticker FROM tickers")).fetchall()
    return [row[0] for row in rows]


def get_company_details(ticker: str) -> dict:
    info = yf.Ticker(ticker).info
    return {
        "ticker": ticker,
        "company_name": info.get("longName"),
        "short_name": info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "city": info.get("city"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        "website": info.get("website"),
        "logo_url": get_logo_url(ticker),
        "employee_count": info.get("fullTimeEmployees"),
        "market_cap": info.get("marketCap"),
        "enterprise_value": info.get("enterpriseValue"),
        "business_summary": info.get("longBusinessSummary"),
    }


def get_company_details_from_list(
    tickers: list[str],
    delay: float = 0.5,
) -> list[dict]:
    companies = []
    for ticker in tickers:
        print(f"Processing {ticker}")
        try:
            companies.append(get_company_details(ticker))
            if delay > 0:
                sleep(delay)
        except Exception as exc:
            print(f"Failed: {ticker} — {exc}")
    return companies


def save_company_details(companies: list[dict]) -> int:
    if not companies:
        print("No companies to save.")
        return 0

    engine = create_engine(get_database_url())
    with engine.begin() as conn:
        conn.execute(UPSERT_SQL, companies)

    print(f"Saved {len(companies)} rows to company_master")
    return len(companies)


def main() -> None:
    tickers = read_tickers()
    print(f"Found {len(tickers)} tickers")
    companies = get_company_details_from_list(tickers)
    save_company_details(companies)


if __name__ == "__main__":
    main()
