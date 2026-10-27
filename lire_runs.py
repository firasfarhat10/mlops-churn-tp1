import mlflow

# Tous les runs de l'expérience, en tableau pandas, triés par f1 décroissant
runs = mlflow.search_runs(
    experiment_names=["churn-prediction"],
    order_by=["metrics.f1 DESC"])

colonnes = ["tags.mlflow.runName", "params.n_estimators", "params.max_depth",
            "metrics.accuracy", "metrics.f1"]
print(runs[colonnes].to_string(index=False))

# La première ligne = le meilleur run
meilleur = runs.iloc[0]
print()
print("Meilleur run :", meilleur["tags.mlflow.runName"], "| id :", meilleur["run_id"][:8], "...")