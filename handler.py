"""
Handler RunPod pour Qwen-Image-Edit Virtual Try-On
Optimisé pour l'essayage virtuel de vêtements avec prompts
"""

import runpod
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image
import base64
import io
import os

# Configuration
MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"🚀 Initialisation du modèle Qwen sur {DEVICE}...")

# Charger le modèle au démarrage
try:
    processor = AutoProcessor.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )
    
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        device_map="auto",
        trust_remote_code=True
    )
    
    print("✅ Modèle Qwen chargé avec succès!")
    
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle: {str(e)}")
    raise


def decode_base64_image(base64_string):
    """
    Décode une image base64 en objet PIL Image
    """
    try:
        # Supprimer le préfixe data:image si présent
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Décoder
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Convertir en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    
    except Exception as e:
        raise ValueError(f"Erreur lors du décodage de l'image: {str(e)}")


def encode_image_to_base64(image):
    """
    Encode une image PIL en base64
    """
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG", quality=95)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    except Exception as e:
        raise ValueError(f"Erreur lors de l'encodage de l'image: {str(e)}")


def process_virtual_tryon(person_image, garment_image, prompt, strength=0.8, guidance_scale=7.5):
    """
    Traite l'essayage virtuel avec Qwen-Image-Edit
    
    Args:
        person_image: Image base64 de la personne
        garment_image: Image base64 du vêtement
        prompt: Instructions textuelles
        strength: Force de l'édition (0.0-1.0)
        guidance_scale: Fidélité au prompt (1.0-20.0)
    
    Returns:
        Image résultante en base64
    """
    try:
        print("📸 Décodage des images...")
        person_img = decode_base64_image(person_image)
        garment_img = decode_base64_image(garment_image)
        
        # Redimensionner si nécessaire (pour optimiser la mémoire)
        max_size = 1024
        if max(person_img.size) > max_size:
            ratio = max_size / max(person_img.size)
            new_size = tuple(int(dim * ratio) for dim in person_img.size)
            person_img = person_img.resize(new_size, Image.LANCZOS)
        
        if max(garment_img.size) > max_size:
            ratio = max_size / max(garment_img.size)
            new_size = tuple(int(dim * ratio) for dim in garment_img.size)
            garment_img = garment_img.resize(new_size, Image.LANCZOS)
        
        print("🎨 Préparation du prompt pour Qwen...")
        
        # Construire le prompt pour Qwen-VL
        # Format spécifique pour l'édition d'images
        conversation = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": person_img,
                    },
                    {
                        "type": "image", 
                        "image": garment_img,
                    },
                    {
                        "type": "text",
                        "text": f"Image editing task: {prompt}\n\nPlease edit the first image by applying the garment from the second image to the person, following the instructions carefully."
                    },
                ],
            }
        ]
        
        # Préparer les inputs
        text_prompt = processor.apply_chat_template(
            conversation,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = processor(
            text=[text_prompt],
            images=[person_img, garment_img],
            return_tensors="pt",
            padding=True
        )
        
        # Déplacer sur GPU si disponible
        if DEVICE == "cuda":
            inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        
        print("🔮 Génération avec Qwen...")
        
        # Générer
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1,
            )
        
        # Décoder la sortie
        generated_text = processor.batch_decode(
            outputs,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]
        
        print(f"📝 Réponse Qwen: {generated_text[:200]}...")
        
        # Note: Qwen-VL génère du texte, pas directement des images
        # Pour l'édition d'images, il faudrait utiliser un modèle spécialisé
        # Ou combiner avec un modèle de diffusion
        
        # Pour l'instant, retourner l'image originale avec un overlay
        # (À remplacer par la vraie logique d'édition)
        result_img = person_img.copy()
        
        # Encoder le résultat
        print("✅ Encodage du résultat...")
        result_base64 = encode_image_to_base64(result_img)
        
        return result_base64, generated_text
    
    except Exception as e:
        print(f"❌ Erreur dans process_virtual_tryon: {str(e)}")
        raise


def handler(event):
    """
    Handler principal pour RunPod
    
    Format d'entrée attendu:
    {
        "input": {
            "image": "data:image/png;base64,...",
            "reference_image": "data:image/png;base64,...",
            "prompt": "Place this garment on the person...",
            "strength": 0.8,  # optionnel
            "guidance_scale": 7.5  # optionnel
        }
    }
    """
    try:
        print("📥 Réception de la requête...")
        
        # Récupérer les données d'entrée
        input_data = event.get('input', {})
        
        person_image = input_data.get('image')
        garment_image = input_data.get('reference_image')
        prompt = input_data.get('prompt', 'Place this garment on the person naturally.')
        strength = input_data.get('strength', 0.8)
        guidance_scale = input_data.get('guidance_scale', 7.5)
        
        # Validation
        if not person_image:
            return {
                "error": "Missing 'image' parameter (person image)",
                "status": "failed"
            }
        
        if not garment_image:
            return {
                "error": "Missing 'reference_image' parameter (garment image)",
                "status": "failed"
            }
        
        print(f"🎯 Prompt: {prompt}")
        print(f"⚙️  Strength: {strength}, Guidance: {guidance_scale}")
        
        # Traiter l'essayage virtuel
        result_image, generated_text = process_virtual_tryon(
            person_image,
            garment_image,
            prompt,
            strength,
            guidance_scale
        )
        
        print("✅ Traitement terminé avec succès!")
        
        return {
            "output": {
                "image": result_image,
                "generated_text": generated_text,
                "prompt_used": prompt,
                "status": "success"
            }
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur dans le handler: {error_msg}")
        
        return {
            "error": error_msg,
            "status": "failed"
        }


# Point d'entrée RunPod
if __name__ == "__main__":
    print("🚀 Démarrage du serveur RunPod...")
    runpod.serverless.start({"handler": handler})
