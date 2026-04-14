FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# 🔥 Instalar dependencias + eventlet
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install eventlet

COPY . .

# Crear carpeta de llaves
RUN mkdir -p /app/keys

# Generar llaves
RUN python generate_keys.py

EXPOSE 5000

# 🔥 Ejecutar con Python normal (usarás allow_unsafe_werkzeug en código)
CMD ["python", "run.py"]
