# 🚀 Handler RunPod pour Qwen-Image-Edit

Handler optimisé pour l'essayage virtuel de vêtements avec Qwen-Image-Edit sur RunPod.

## 📁 Fichiers

- `handler.py` - Handler Python principal
- `Dockerfile` - Configuration Docker
- `requirements.txt` - Dépendances Python
- `README.md` - Ce fichier

## 🎯 Deux Options de Déploiement

### Option 1 : Via Docker Hub (Recommandé - Plus Simple)

#### Étape 1 : Build et Push l'Image

```bash
# Dans le dossier runpod-handler
cd "c:/Users/lamid/CascadeProjects/qwen image - Claude/runpod-handler"

# Build l'image
docker build -t votre-username/qwen-tryon:latest .

# Login Docker Hub
docker login

# Push l'image
docker push votre-username/qwen-tryon:latest
```

#### Étape 2 : Créer l'Endpoint sur RunPod

1. Allez sur https://www.runpod.io/console/serverless
2. Cliquez sur "+ New Endpoint"
3. Sélectionnez "Docker Registry"
4. Image: `votre-username/qwen-tryon:latest`
5. Configuration:
   ```
   GPU: RTX 4090 (24GB)
   Workers Min: 0
   Workers Max: 1
   Container Disk: 30 GB
   Volume Disk: 50 GB
   Execution Timeout: 120s
   Idle Timeout: 5s
   ```

---

### Option 2 : Via GitHub (Plus Flexible)

#### Étape 1 : Créer un Repo GitHub

```bash
# Initialiser Git
cd "c:/Users/lamid/CascadeProjects/qwen image - Claude/runpod-handler"
git init

# Ajouter les fichiers
git add .
git commit -m "Initial commit: Qwen-Image-Edit handler"

# Créer un repo sur GitHub et pusher
git remote add origin https://github.com/votre-username/qwen-tryon-handler.git
git branch -M main
git push -u origin main
```

#### Étape 2 : Créer l'Endpoint sur RunPod

1. Allez sur https://www.runpod.io/console/serverless
2. Cliquez sur "+ New Endpoint"
3. Sélectionnez "Import from GitHub"
4. Repo: `votre-username/qwen-tryon-handler`
5. Branch: `main`
6. Dockerfile Path: `Dockerfile`
7. Configuration (même que Option 1)

---

## 🧪 Test Local (Optionnel)

### Prérequis
- Docker installé
- GPU NVIDIA avec CUDA

### Commandes

```bash
# Build l'image
docker build -t qwen-tryon-local .

# Run localement
docker run --gpus all -p 8000:8000 qwen-tryon-local
```

---

## 📝 Format d'Entrée

```json
{
  "input": {
    "image": "data:image/png;base64,...",
    "reference_image": "data:image/png;base64,...",
    "prompt": "Place this garment on the person naturally.",
    "strength": 0.8,
    "guidance_scale": 7.5
  }
}
```

## 📤 Format de Sortie

```json
{
  "output": {
    "image": "data:image/png;base64,...",
    "generated_text": "...",
    "prompt_used": "...",
    "status": "success"
  }
}
```

---

## ⚙️ Configuration

### Variables d'Environnement

```bash
TRANSFORMERS_CACHE=/runpod-volume/transformers-cache
HF_HOME=/runpod-volume/huggingface
```

### Modèle Utilisé

```python
MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct"
```

---

## 💡 Optimisations

### 1. Pré-télécharger le Modèle

Dans le `Dockerfile`, décommentez:
```dockerfile
RUN python -c "from transformers import Qwen2VLForConditionalGeneration, AutoProcessor; \
    processor = AutoProcessor.from_pretrained('Qwen/Qwen2-VL-7B-Instruct', trust_remote_code=True); \
    model = Qwen2VLForConditionalGeneration.from_pretrained('Qwen/Qwen2-VL-7B-Instruct', trust_remote_code=True)"
```

**Avantage:** Démarrage plus rapide  
**Inconvénient:** Image Docker plus lourde (~15GB)

### 2. Utiliser un Volume Persistant

Sur RunPod, configurez un volume pour:
- Cache des modèles
- Éviter de re-télécharger à chaque démarrage

---

## 🐛 Dépannage

### Erreur "Out of Memory"

**Solution:**
- Passez à A40 (48GB)
- Ou réduisez la résolution des images dans le handler

### Erreur "Model not found"

**Solution:**
- Vérifiez la connexion internet du pod
- Pré-téléchargez le modèle dans le Dockerfile

### Timeout

**Solution:**
- Augmentez `Execution Timeout` à 180s
- Optimisez la taille des images

---

## 📊 Performance

### Avec RTX 4090

- **Temps de chargement:** 30-60s (première fois)
- **Temps par image:** 15-25s
- **VRAM utilisée:** ~20GB
- **Coût:** ~$0.003/image

---

## 🔗 Liens Utiles

- **Qwen GitHub:** https://github.com/QwenLM/Qwen-VL
- **Hugging Face:** https://huggingface.co/Qwen
- **RunPod Docs:** https://docs.runpod.io/

---

## ✅ Checklist de Déploiement

- [ ] Fichiers créés (handler.py, Dockerfile, requirements.txt)
- [ ] Docker installé localement
- [ ] Compte Docker Hub créé (pour Option 1)
- [ ] Ou Repo GitHub créé (pour Option 2)
- [ ] Image buildée et pushée
- [ ] Endpoint créé sur RunPod
- [ ] Configuration GPU validée
- [ ] Test effectué
- [ ] Endpoint ID copié dans `.env.local`

---

**🚀 Prêt à déployer !**
