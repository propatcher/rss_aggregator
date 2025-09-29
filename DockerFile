FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "until pg_isready -h db -p 5432 -U user; do echo 'Waiting for database...'; sleep 2; done && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]