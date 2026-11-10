# 1. Image de base : un Linux minimal avec Python 3.11 (ta version locale)
FROM python:3.11-slim

# 2. Dossier de travail dans l'image
WORKDIR /app

# 3. D'abord SEULEMENT la liste des bibliothèques, puis l'installation
#    Cette couche est mise en cache tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Ensuite le code et le modèle (ils changent plus souvent)
COPY app.py .
COPY model/ model/

# 5. Valeur par défaut : charger le modèle depuis le dossier model
ENV MODEL_URI=model
ENV PYTHONUNBUFFERED=1

# 6. Documenter le port utilisé par l'API (information, ne publie rien)
EXPOSE 8000

# 7. Commande lancée au démarrage du conteneur
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]