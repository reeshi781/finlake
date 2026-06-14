# de_project

Local data engineering pipeline: ticker list → yfinance extract → PostgreSQL.

## Structure

```
data/raw/          Input tickers (CSV)
data/processed/    Staging extract output (CSV)
data/schema/       Table DDL + seed SQL
src/extract/       Fetch data from APIs (yfinance)
src/load/          Database init, reads, and writes
src/pipeline/      Orchestration (extract + load)
src/config/        DB connection settings
src/transform/     Future transforms (Spark/pandas)
```

## Setup

```bash
cp .env.example .env
docker compose up -d
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python src/load/init_db.py
```

## Run pipeline

Full flow (read tickers from DB → extract → staging CSV → PostgreSQL):

```bash
PYTHONPATH=. python src/pipeline/run.py
```

Load only from an existing staging file:

```bash
PYTHONPATH=. python src/load/load_company_master.py
```

## TablePlus connection

| Field    | Value        |
|----------|--------------|
| Host     | `localhost`  |
| Port     | `5432`       |
| Database | `de_project` |
| User     | `de_user`    |
| Password | `de_pass`    |
