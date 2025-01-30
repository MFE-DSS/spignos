import os

# Structures pour différents use cases
PROJECT_TEMPLATES = {
    "time_series": {
        "data": ["raw", "interim", "processed", "external"],
        "models/time_series": ["__init__.py", "train.py", "predict.py"],
        "notebooks": [],
        "spignos": ["__init__.py", "config.py", "dataset.py", "features.py"],
        "spignos/modeling": ["__init__.py", "train.py", "predict.py"],
        "spignos/evaluation": ["__init__.py", "metrics.py"],
        "spignos/visualization": ["__init__.py", "plots.py"],
        "tests": ["__init__.py", "test_time_series.py"],
    },
    "classification": {
        "data": ["raw", "interim", "processed", "external"],
        "models/classification": ["__init__.py", "train.py", "predict.py"],
        "notebooks": [],
        "spignos": ["__init__.py", "config.py", "dataset.py", "features.py"],
        "spignos/modeling": ["__init__.py", "train.py", "predict.py"],
        "spignos/evaluation": ["__init__.py", "metrics.py"],
        "spignos/visualization": ["__init__.py", "plots.py"],
        "tests": ["__init__.py", "test_classification.py"],
    },
    "custom": {
        "data": ["raw", "interim", "processed", "external"],
        "models/custom_model": ["__init__.py", "train.py", "predict.py"],
        "notebooks": [],
        "spignos": ["__init__.py", "config.py", "dataset.py", "features.py"],
        "spignos/modeling": ["__init__.py", "train.py", "predict.py"],
        "spignos/evaluation": ["__init__.py", "metrics.py"],
        "spignos/visualization": ["__init__.py", "plots.py"],
        "tests": ["__init__.py", "test_custom.py"],
    },
}

# Contenu de base pour les fichiers générés automatiquement
FILE_TEMPLATES = {
    "__init__.py": "# Initialisation du package\n",
    "config.py": "# Configuration globale du projet\nCONFIG = {}\n",
    "train.py": """# Script de formation du modèle
def train_model():
    print('Training the model...')
""",
    "predict.py": """# Script de prédiction
def predict(data):
    print(f'Predicting with input: {data}')
    return "dummy_prediction"
""",
    "metrics.py": """# Calcul des métriques d'évaluation
def calculate_metrics():
    print('Calculating evaluation metrics...')
""",
    "plots.py": """# Génération des graphiques
def generate_plot():
    print('Generating plots...')
""",
    "test_time_series.py": """import pytest

def test_time_series():
    assert True, "Exemple de test de série temporelle"
""",
    "test_classification.py": """import pytest

def test_classification():
    assert True, "Exemple de test pour les modèles de classification"
""",
    "test_custom.py": """import pytest

def test_custom():
    assert True, "Exemple de test pour le cas d'usage personnalisé"
""",
}


def create_structure(use_case, base_path):
    if use_case not in PROJECT_TEMPLATES:
        print(f"Cas d'usage non reconnu : {use_case}")
        return

    structure = PROJECT_TEMPLATES[use_case]

    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):  # Éviter d'écraser les fichiers existants
                with open(file_path, "w") as f:
                    content = FILE_TEMPLATES.get(file_name, "# Fichier généré automatiquement\n")
                    f.write(content)
    print(f"Structure du projet {use_case} générée avec succès.")


if __name__ == "__main__":
    print("Choisissez le cas d'usage pour votre projet :")
    print("1 - time_series")
    print("2 - classification")
    print("3 - custom")

    choice = input("Entrez le numéro correspondant au cas d'usage : ").strip()
    use_case = {"1": "time_series", "2": "classification", "3": "custom"}.get(choice, "custom")

    base_path = os.getcwd()  # Génère la structure dans le répertoire actuel
    create_structure(use_case, base_path)
