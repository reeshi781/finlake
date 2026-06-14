# Copy to .env before starting Docker
cp .env.example .env

# Start PostgreSQL + pgAdmin
docker compose up -d

# Install Python deps (from project root)
source .venv/bin/activate
pip install -r requirements.txt

# Seed tickers + apply schema
PYTHONPATH=. python src/load/init_db.py

# Extract company details from DB tickers → company_master table
PYTHONPATH=. python src/extract/company_details.py

# Stop containers
docker compose down
