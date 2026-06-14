"""Read ticker symbols from PostgreSQL."""

from sqlalchemy import create_engine, text

from src.config.db import get_database_url


def read_tickers() -> list[str]:
    engine = create_engine(get_database_url())
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT ticker FROM tickers")).fetchall()
    return [row[0] for row in rows]
