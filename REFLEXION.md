# Réflexion — TP2

1. Quel est le meilleur des 3 modèles ? Peut-on le prouver ?
   -> Pas encore avec certitude. Git conserve chaque essai dans un commit séparé
   (e047c98 = Essai 1, e6b2d24 = Essai 2, a236195 = Essai 3), avec un message
   qui explique ce qui a changé : on sait exactement quel code correspond à quel
   essai. Mais Git ne garde pas les scores : ils ne sont visibles que dans les
   sorties du notebook, et il faut ouvrir chaque version pour les comparer.
   De plus, l'écart entre les essais (0.99 contre 1.0) ne porte que sur un seul
   client sur 100, avec seulement 5 clients qui partent dans le jeu de test :
   c'est trop faible pour conclure.

2. Peut-on redonner exactement le modèle de l'Essai 1 ?
   -> Oui pour le code : `git checkout e047c98 -- churn_model.ipynb` restaure le
   notebook exact de l'Essai 1 (testé à l'Étape 7). Non pour le modèle lui-même :
   model.pkl est dans le .gitignore, donc absent de l'historique. Il faut
   réexécuter le notebook ; grâce aux graines fixées (random_state=42), on
   retrouve le même modèle, à condition d'avoir les mêmes versions des
   bibliothèques.

3. Un camarade peut-il reproduire notre travail sur une autre machine ?
   -> En partie. `git clone` lui donne le code, les données (churn_data.csv) et
   tout l'historique des essais (vérifié avec le dossier TP1-collegue). Mais
   venv/ et model.pkl ne sont pas transmis : il doit recréer son environnement
   et réentraîner le modèle. Et rien ne fixe les versions de Python et des
   bibliothèques (pas de requirements.txt figé) : son résultat peut donc
   différer.

## TP3 — avec MLflow

1. Quel est le meilleur des 3 modèles ? Peut-on le prouver ?
   -> Oui. Chaque essai est un run MLflow avec ses paramètres et ses 4 métriques
   (accuracy, precision, recall, f1). Le tri par f1, dans l'interface ou avec
   `mlflow.search_runs(order_by=["metrics.f1 DESC"])`, donne un classement daté
   et conservé : essai-1 et essai-3 à égalité (f1 = 0.889), essai-2 nettement
   derrière (f1 = 0.333). À performance égale, je retiens essai-3, le plus simple
   (il n'a pas besoin de la colonne salaire).
   Le f1 a révélé ce que l'accuracy cachait : essai-2 affiche 0.96 d'accuracy
   mais ne détecte qu'un seul départ sur 5 (recall = 0.2). Nuance : avec 5 clients
   qui partent dans le test, un seul client mal classé fait varier fortement ces
   chiffres ; ils orientent le choix plus qu'ils ne le prouvent.

2. Peut-on redonner exactement le modèle de l'Essai 1 ?
   -> Oui. Chaque run conserve son propre modèle dans ses artifacts : plus rien
   n'est écrasé. `mlflow.sklearn.load_model("runs:/<run_id>/model")` le recharge
   sans réentraînement (testé avec charger_modele.py).

3. Un camarade peut-il reproduire notre travail sur une autre machine ?
   -> En partie. Git lui donne le code et les données, et chaque run MLflow
   enregistre les versions des bibliothèques (requirements.txt et
   python_env.yaml dans les artifacts du modèle). Mais mlflow.db et mlruns/
   restent sur ma machine : il doit relancer les scripts pour obtenir ses propres
   runs, et son environnement n'est pas garanti identique. Ce dernier point sera
   traité avec Docker (TP5-6).

## TP4 — avec le Registry et l'API

1. Comment désigner officiellement le modèle à utiliser ?
   -> Avec le Model Registry de MLflow. Le meilleur run (essai-3) est enregistré
   sous un nom stable, churn-model (version 1), et l'alias « champion » pointe
   vers cette version. Le modèle se charge ensuite par
   `models:/churn-model@champion`, sans connaître ni son numéro de version ni
   son identifiant de run. Chaque version reste reliée à son run d'origine : on
   sait toujours d'où vient le modèle officiel et avec quels réglages.

2. Comment une application peut-elle utiliser le modèle ?
   -> Par une requête web à l'API FastAPI : POST /predict avec un client au
   format JSON, la réponse contient la prédiction (churn = 1 ou 0). Le client
   n'a besoin ni de scikit-learn, ni de MLflow (testé avec test_api.py). Les
   données sont validées par Pydantic : un âge « abc » ou un abonnement « Gold »
   est refusé avec un code 422 avant d'atteindre le modèle.

3. Que se passe-t-il quand on change de champion ?
   -> On déplace l'alias en une ligne (`set_registered_model_alias`), puis on
   redémarre l'API, qui ne charge le modèle qu'au démarrage. Ni le code de l'API
   ni celui des applications clientes ne change. Je l'ai testé avec
   deplacer_alias.py : promotion vers la version 2 (essai-2), puis retour
   arrière vers la version 1.
   Limite : l'API refait à la main l'encodage de l'entraînement (get_dummies) ;
   si l'encodage changeait, il faudrait aussi modifier l'API. Et le Registry
   reste dans mlflow.db, sur ma machine.
