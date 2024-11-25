from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image
import os
import unicodedata
from io import BytesIO

from models.product import Product
from utils.services import fetch_products

# Initialize the API router with a prefix and tags
router = APIRouter(tags=["prescription"])

def remove_accents(input_str):
    # Normalise la chaîne de caractères et enlève les accents
    return ''.join(
        char for char in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(char) != 'Mn'
    )
# Fonction pour extraire le texte à partir d'une image
def extract_text_from_image(image_data):
    """Fonction pour extraire du texte à partir d'une image"""
    try:
        # Convertir l'image binaire en objet Image PIL
        image = Image.open(BytesIO(image_data))
        # Utiliser pytesseract pour extraire du texte
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture de l'image : {e}")

@router.post("/process_prescription/")
async def process_prescription(file: UploadFile = File(...)):
    """Route pour traiter une ordonnance à partir d'une image téléchargée"""
    
    # Lire le contenu du fichier téléchargé
    image_data = await file.read()
    
    if not image_data:
        raise HTTPException(status_code=400, detail="Aucun fichier téléchargé.")
    
    # Extraire le texte de l'image
    extracted_text = extract_text_from_image(image_data)
    
    if not extracted_text:
        raise HTTPException(status_code=404, detail="Aucun texte n'a été extrait de l'image.")
    
    # Traitement simple pour extraire les "produits" (séparer par des espaces et newlines)
    words_in_image = extracted_text.replace("\n", " ").split(" ")
    # Supprimer les valeurs dupliquées dans la liste des produits
    words_in_image = list(set(words_in_image))
    # Supprimer les caractères spéciaux et les valeurs vides de la liste des produits
    words_in_image = [remove_accents(word) for word in words_in_image if word.isalnum()]
    class ProductNameProjection(BaseModel):
        name: str
    products_name = await Product.find({}, projection_model=ProductNameProjection).to_list()
    products_name = ' '.join([product.name for product in products_name])
    products_name = products_name.replace("\n", " ").split(" ")
    products_name = list(set(products_name))
    products_name = [ remove_accents(name) for name in products_name if name.isalnum()]
    products_name = [name.lower() for name in products_name]

    print(products_name)

    # Filtrer les produits qui ne sont pas dans la base de données
    products_in_image = [word for word in words_in_image if word in products_name]
    if not products_in_image:
        return JSONResponse(status_code=404, content={"message": "Aucun produit trouvé dans l'image."})
    found_products = []
    for product in products_in_image:
        # Remplacer cette ligne par la logique de recherche dans votre base de données
        # Exemple : found_product = database.find_product_by_name(product)
        found_product = await fetch_products(product)
        if found_product:
            found_products.append(found_product)

    # Répondre avec la liste des produits trouvés dans la base de données
    return found_products

