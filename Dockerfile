# Dockerfile pour Virtual Try-On Handler sur RunPod
# Version simplifiée et légère

FROM python:3.10-slim

# Définir les variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
ENV HF_HOME=/runpod-volume/huggingface

# Mettre à jour et installer les dépendances système
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    pillow>=10.0.0 \
    runpod>=1.6.0

# Créer le répertoire de travail
WORKDIR /app

# Copier le handler
COPY handler.py /app/handler.py

# Créer les répertoires de cache
RUN mkdir -p /runpod-volume

# Exposer le port (pour référence)
EXPOSE 8000

# Commande de démarrage
CMD ["python", "-u", "/app/handler.py"]
