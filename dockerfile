# Etapa 1: Build
FROM python:3.11-slim as build

# Setează variabile de mediu pentru producție
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalează dependințele de sistem necesare
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Creează și setează directorul de lucru
WORKDIR /app

# Copiază fișierele requirements în imagine
COPY requirements.txt /app/

# Instalează dependințele Python
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiază codul sursă în imagine
COPY . /app/

# Etapa 2: Producție
FROM python:3.11-slim

# Setează variabile de mediu pentru producție
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalează dependințele de sistem necesare pentru runtime
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

# Creează și setează directorul de lucru
WORKDIR /app

# Copiază fișierele instalate în etapa de build
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app

# Expune portul aplicației
EXPOSE 8000

# Comanda pentru rularea aplicației
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "etf_predictor.wsgi:application", "--workers=3"]
