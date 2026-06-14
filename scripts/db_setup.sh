#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

docker compose up -d

source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=. python src/load/init_db.py
PYTHONPATH=. python src/pipeline/run.py
