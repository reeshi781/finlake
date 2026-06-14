"""Load company data from CSV/Parquet into PostgreSQL."""

import argparse
from pathlib import Path

import pandas as pd

from src.load.company_master import COMPANY_MASTER_COLUMNS, upsert_company_master

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "company_master.csv"


def load_company_master(data_path: Path) -> int:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    if data_path.suffix == ".parquet":
        df = pd.read_parquet(data_path)
    else:
        df = pd.read_csv(data_path)

    expected = set(COMPANY_MASTER_COLUMNS)
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in data file: {sorted(missing)}")

    records = df[COMPANY_MASTER_COLUMNS].to_dict(orient="records")
    return upsert_company_master(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load company_master data from file")
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to CSV or Parquet file",
    )
    args = parser.parse_args()
    load_company_master(args.path)


if __name__ == "__main__":
    main()
