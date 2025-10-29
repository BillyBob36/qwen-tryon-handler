# Dockerfile pour Qwen-Image-Edit sur RunPod
# Optimisé pour RTX 4090 (24GB VRAM)

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
    transformers>=4.37.0 \
    accelerate>=0.26.0 \
    torch>=2.1.0 \
    torchvision \
    pillow>=10.0.0 \
    runpod>=1.6.0 \
    qwen-vl-utils \
    sentencepiece \
    protobuf

# Créer le répertoire de travail
WORKDIR /app

# Copier le handler
COPY handler.py /app/handler.py

# Pré-télécharger le modèle (optionnel mais recommandé)
# Décommentez les lignes suivantes pour pré-télécharger le modèle
# RUN python -c "from transformers import Qwen2VLForConditionalGeneration, AutoProcessor; \
#     processor = AutoProcessor.from_pretrained('Qwen/Qwen2-VL-7B-Instruct', trust_remote_code=True); \
#     model = Qwen2VLForConditionalGeneration.from_pretrained('Qwen/Qwen2-VL-7B-Instruct', trust_remote_code=True)"

# Créer les répertoires de cache
RUN mkdir -p /runpod-volume/transformers-cache /runpod-volume/huggingface

# Exposer le port (pour référence)
EXPOSE 8000

# Commande de démarrage
CMD ["python", "-u", "/app/handler.py"]
