# Dockerfile pour Qwen-Image-Edit-2509 sur RunPod
# Virtual Try-On avec IA

FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

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
    torch>=2.0.0 \
    diffusers>=0.25.0 \
    transformers>=4.35.0 \
    accelerate>=0.25.0 \
    pillow>=10.0.0 \
    runpod>=1.6.0 \
    safetensors>=0.4.0

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
