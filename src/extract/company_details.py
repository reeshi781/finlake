"""Extract company details from yfinance (no database writes)."""

import warnings
from time import sleep

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")


def get_logo_url(ticker: str) -> str:
    return f"https://financialmodelingprep.com/image-stock/{ticker}.png"


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


def extract_companies(
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


def extract_to_dataframe(
    tickers: list[str],
    delay: float = 0.5,
) -> pd.DataFrame:
    return pd.DataFrame(extract_companies(tickers, delay=delay))
