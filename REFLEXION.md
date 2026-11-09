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
