"""
Handler de test simple pour vérifier que RunPod fonctionne
"""

import runpod
from PIL import Image, ImageDraw
import base64
import io

print("✅ Handler de test démarré")


def decode_base64_image(base64_string):
    """Décode une image base64"""
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        raise ValueError(f"Erreur décodage: {str(e)}")


def encode_image_to_base64(image):
    """Encode une image en base64"""
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG", quality=95)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        raise ValueError(f"Erreur encodage: {str(e)}")


def handler(event):
    """Handler de test - retourne simplement un composite"""
    try:
        print("📥 Requête reçue")
        
        input_data = event.get('input', {})
        person_image = input_data.get('image')
        garment_image = input_data.get('reference_image')
        prompt = input_data.get('prompt', 'Test')
        
        if not person_image or not garment_image:
            return {"error": "Images manquantes", "status": "failed"}
        
        print("📸 Décodage...")
        person_img = decode_base64_image(person_image)
        garment_img = decode_base64_image(garment_image)
        
        print("🎨 Création composite...")
        result_img = person_img.copy()
        
        # Redimensionner le vêtement
        garment_resized = garment_img.resize(
            (person_img.width // 3, person_img.height // 3),
            Image.LANCZOS
        )
        
        # Coller le vêtement
        result_img.paste(
            garment_resized,
            (person_img.width // 3, person_img.height // 3)
        )
        
        # Ajouter texte
        draw = ImageDraw.Draw(result_img)
        draw.text((10, 10), "TEST HANDLER OK", fill=(0, 255, 0))
        
        print("✅ Encodage...")
        result_base64 = encode_image_to_base64(result_img)
        
        print("✅ Terminé!")
        
        return {
            "output": {
                "image": result_base64,
                "generated_text": f"Test OK: {prompt}",
                "prompt_used": prompt,
                "status": "success"
            }
        }
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return {"error": str(e), "status": "failed"}


if __name__ == "__main__":
    print("🚀 Démarrage handler de test...")
    runpod.serverless.start({"handler": handler})
