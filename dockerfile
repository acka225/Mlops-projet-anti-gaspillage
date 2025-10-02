# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code
COPY . .

# Création des dossiers nécessaires
RUN mkdir -p data models

# Exposition des ports
EXPOSE 8000 8501

# Commande par défaut (peut être overridé par docker-compose)
CMD ["python", "src/api_flask_correct.py"]