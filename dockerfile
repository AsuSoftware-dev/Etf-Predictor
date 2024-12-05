# Imaginea de bază Python
FROM python:3.11-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază requirements.txt și instalează dependințele
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiază codul aplicației în container
COPY . .

# Expune portul 8000 (folosit de gunicorn)
EXPOSE 8000

# Comanda de pornire folosind gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "etf_predictor.wsgi:application", "--workers=3"]
