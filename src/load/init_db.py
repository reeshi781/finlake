"""Seed tickers and verify PostgreSQL connection."""

import csv
import time
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from src.config.db import get_database_url

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TICKERS_CSV = PROJECT_ROOT / "data" / "raw" / "company_master.csv"
SCHEMA_PATH = PROJECT_ROOT / "data" / "schema" / "schema.sql"


def wait_for_db(engine, retries: int = 30, delay_seconds: float = 2.0) -> None:
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready.")
            return
        except OperationalError:
            print(f"Waiting for database... ({attempt}/{retries})")
            time.sleep(delay_seconds)
    raise RuntimeError("Database did not become ready.")


def init_db(seed_tickers: bool = True) -> None:
    engine = create_engine(get_database_url())
    wait_for_db(engine)

    with engine.begin() as conn:
        conn.execute(text(SCHEMA_PATH.read_text()))

        if seed_tickers and TICKERS_CSV.exists():
            with TICKERS_CSV.open(newline="") as f:
                tickers = [row["ticker"] for row in csv.DictReader(f)]

            conn.execute(
                text(
                    "INSERT INTO tickers (ticker) VALUES (:ticker) "
                    "ON CONFLICT (ticker) DO NOTHING"
                ),
                [{"ticker": ticker} for ticker in tickers],
            )
            print(f"Seeded {len(tickers)} tickers into tickers table.")

    print("Schema applied successfully.")


if __name__ == "__main__":
    init_db()
