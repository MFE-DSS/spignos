# Commandes utiles pour automatiser les tâches fréquentes
.PHONY: data train evaluate clean

# Prétraitement des données
data:
    python spignos/dataset.py

# Entraînement des modèles
train:
    python spignos/modeling/train.py

# Évaluation des modèles
evaluate:
    python spignos/evaluation/metrics.py

# Nettoyage des données intermédiaires
clean:
    rm -rf data/interim/*
