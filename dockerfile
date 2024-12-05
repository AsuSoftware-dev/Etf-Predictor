# Folosește o imagine oficială Python
FROM python:3.11-slim

# Setează directorul de lucru în container
WORKDIR /app

# Copiază fișierele proiectului în container
COPY . /app

# Instalează dependințele
RUN pip install --no-cache-dir -r requirements.txt

# Expune portul 8000 (portul standard Django)
EXPOSE 8000

# Comanda pentru a porni serverul Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
