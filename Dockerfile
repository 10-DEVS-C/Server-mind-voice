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

RUN touch .env

RUN echo "MONGO_URI=mongodb+srv://IsaacChino:Chino2@cluster0.riazwh1.mongodb.net/Mi_Proyecto?appName=Cluster0" >> .env
RUN echo "VITE_GEMINI_API_KEY=AIzaSyCHC97lp8JvPNDBVmE1YJeKHNpuhZdB2cY" >> .env

EXPOSE 5000

# 🔥 Ejecutar con Python normal (usarás allow_unsafe_werkzeug en código)
CMD ["python", "run.py"]
