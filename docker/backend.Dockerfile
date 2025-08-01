# backend.Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY data/ ./data
COPY local_db/ ./local_db
COPY .env .env


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
