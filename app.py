# ===== 1. Importer les bibliothèques =====
import os                              # lire les variables d'environnement
from typing import Literal
import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# ===== 2. Créer l'application =====
app = FastAPI(title="API Churn")

# ===== 3. Lire la configuration dans les variables d'environnement =====
# os.getenv("NOM", "valeur") : valeur de la variable, ou valeur par défaut si elle n'existe pas
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
MODEL_URI = os.getenv("MODEL_URI", "models:/churn-model@champion")

# ===== 4. Charger le champion UNE SEULE FOIS, au démarrage =====
# MODEL_URI peut être une adresse du Registry (models:/...) ou un simple dossier (model)
mlflow.set_tracking_uri(TRACKING_URI)
model = mlflow.sklearn.load_model(MODEL_URI)
print(f"Modèle chargé depuis : {MODEL_URI}")

# ===== 5. Décrire les données attendues =====
class Client(BaseModel):
    age: int
    salaire: float
    abonnement: Literal["Basique", "Standard", "Premium"]
    anciennete: float
    consommation: float

# ===== 6. Route /health =====
@app.get("/health")
def health():
    return {"status": "ok"}

# ===== 7. Route /predict =====
@app.post("/predict")
def predict(client: Client):
    ligne = pd.DataFrame([client.model_dump()])
    ligne = pd.get_dummies(ligne)
    ligne = ligne.reindex(columns=model.feature_names_in_, fill_value=0)
    resultat = int(model.predict(ligne)[0])
    return {"churn": resultat,
            "message": "Le client va partir" if resultat == 1 else "Le client reste"}