"""
Handler RunPod pour Virtual Try-On avec Qwen-Image-Edit-2509
"""

import runpod
import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image
import base64
import io
import os

print("🚀 Chargement de Qwen-Image-Edit-2509...")

# Charger le modèle Qwen-Image-Edit
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    pipe = AutoPipelineForImage2Image.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    )
    pipe = pipe.to(DEVICE)
    print(f"✅ Qwen-Image-Edit chargé sur {DEVICE}")
except Exception as e:
    print(f"❌ Erreur chargement modèle: {e}")
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
    Traitement avec Qwen-Image-Edit-2509
    """
    try:
        print("📸 Décodage des images...")
        person_img = decode_base64_image(person_image)
        garment_img = decode_base64_image(garment_image)
        
        # Convertir en RGB si nécessaire
        if person_img.mode != 'RGB':
            person_img = person_img.convert('RGB')
        if garment_img.mode != 'RGB':
            garment_img = garment_img.convert('RGB')
        
        # Redimensionner si trop grand (pour optimiser)
        max_size = 1024
        if max(person_img.size) > max_size:
            ratio = max_size / max(person_img.size)
            new_size = tuple(int(dim * ratio) for dim in person_img.size)
            person_img = person_img.resize(new_size, Image.LANCZOS)
        
        print(f"🎨 Génération avec Qwen-Image-Edit...")
        print(f"   Prompt: {prompt[:80]}...")
        print(f"   Strength: {strength}, Guidance: {guidance_scale}")
        
        # Générer avec Qwen-Image-Edit
        result_img = pipe(
            prompt=prompt,
            image=person_img,
            strength=strength,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
        ).images[0]
        
        print("✅ Génération terminée")
        result_base64 = encode_image_to_base64(result_img)
        
        return result_base64, f"Generated with Qwen-Image-Edit: {prompt}"
    
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
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
