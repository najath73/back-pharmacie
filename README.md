# API de Gestion de Pharmacies
## Description
Cette API est développée avec FastAPI et MongoDB (Beanie) pour gérer un système de pharmacies. Elle permet de :
- Gérer les pharmacies et leurs produits
- Passer et gérer des commandes
- Gérer les utilisateurs avec différents rôles (admin, gestionnaire de pharmacie, utilisateur simple)
  ## Prérequis
- Python 3.7+
- FastAPI
- Uvicorn (pour le serveur)
- MongoDB (utilisé avec Beanie pour la gestion des documents)

  ## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/najath73/back-pharmacie.git
   cd back-pharmacie


2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv env
   source env/bin/activate   # Sur Windows: env\Scripts\activate

3. Installez les dépendances du projet :
   ```bash
   pip install -r requirements.txt

## Lancement du serveur
4. Pour démarrer le serveur FastAPI en local avec Uvicorn :
   ```bash
   uvicorn main:app --reload
Le serveur sera disponible à l'adresse http://127.0.0.1:8000.



## Documentation API

Une fois le serveur démarré, vous pouvez accéder à la documentation interactive Swagger à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)






 





