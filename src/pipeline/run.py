"""Run full ETL: read tickers → extract → save staging file → load to PostgreSQL."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.extract.company_details import extract_companies
from src.load.company_master import upsert_company_master
from src.load.tickers import read_tickers

PROCESSED_CSV = PROJECT_ROOT / "data" / "processed" / "company_master.csv"


def run(save_csv: bool = True, delay: float = 0.5) -> int:
    tickers = read_tickers()
    print(f"Found {len(tickers)} tickers")

    companies = extract_companies(tickers, delay=delay)
    if not companies:
        print("No companies extracted.")
        return 0

    if save_csv:
        PROCESSED_CSV.parent.mkdir(parents=True, exist_ok=True)
        import pandas as pd

        pd.DataFrame(companies).to_csv(PROCESSED_CSV, index=False)
        print(f"Saved staging file: {PROCESSED_CSV}")

    return upsert_company_master(companies)


if __name__ == "__main__":
    run()
