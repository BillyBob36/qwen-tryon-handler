"""
Handler RunPod pour Virtual Try-On
Version simplifiée pour test - Retourne l'image de la personne avec overlay du vêtement
"""

import runpod
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import os

print("🚀 Initialisation du handler Virtual Try-On...")

# Handler prêt
print("✅ Handler initialisé avec succès!")


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
    Version simplifiée pour test - Composite simple des images
    """
    try:
        print("📸 Décodage des images...")
        person_img = decode_base64_image(person_image)
        garment_img = decode_base64_image(garment_image)
        
        print(f"🎨 Traitement avec prompt: {prompt[:50]}...")
        
        # Créer une image composite simple pour le test
        result_img = person_img.copy()
        
        # Redimensionner le vêtement pour le placer sur l'image
        garment_resized = garment_img.resize(
            (person_img.width // 3, person_img.height // 3),
            Image.LANCZOS
        )
        
        # Placer le vêtement en overlay semi-transparent
        result_img.paste(
            garment_resized,
            (person_img.width // 3, person_img.height // 3),
            garment_resized if garment_resized.mode == 'RGBA' else None
        )
        
        # Ajouter un texte pour indiquer que c'est un test
        draw = ImageDraw.Draw(result_img)
        text = "TEST - Virtual Try-On Handler Active"
        draw.text((10, 10), text, fill=(255, 255, 255))
        
        print("✅ Traitement terminé")
        result_base64 = encode_image_to_base64(result_img)
        
        return result_base64, f"Processed with prompt: {prompt}"
    
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
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
