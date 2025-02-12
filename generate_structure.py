import os


def create_project_structure(base_path):
    structure = {
        os.path.join("backend", "app"): ["main.py", "models.py", "config.py", "utils.py"],
        os.path.join("backend", "app", "routers"): ["chat.py"],
        "backend": ["requirements.txt", "Dockerfile"],
        os.path.join("frontend", "src"): ["App.js", "ChatInterface.js"],
        "frontend": ["package.json", "Dockerfile"],
        os.path.join("infrastructure", "k8s"): ["backend-deployment.yaml", "frontend-deployment.yaml", "ingress.yaml"],
        "infrastructure": ["docker-compose.yaml"],
        os.path.join(".github", "workflows"): ["deploy.yml"],
        "": ["README.md", "LICENSE", "Makefile", "pyproject.toml", "generate_structure.py"]
    }

    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")  # Crée un fichier vide


if __name__ == "__main__":
    base_path = os.getcwd()  # Utilisation du répertoire racine actuel
    create_project_structure(base_path)
    print(f"Structure du projet créée sous {base_path}")
