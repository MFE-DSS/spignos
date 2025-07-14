# Makefile pour SPIGNOS

VENV=.venv/bin
MANAGE=python manage.py

# === MAKEFILE - SPIGNOS DJANGO BACKEND ===

.PHONY: help install migrate run swagger swagger-json clean clean-pyc

# 🔹 Aide
help:
	@echo "🚀 Commandes disponibles :"
	@echo "  make install        # Installe les dépendances"
	@echo "  make migrate        # Gère les migrations Django"
	@echo "  make run            # Lance le serveur Django"
	@echo "  make swagger        # Génère Swagger YAML + JSON"
	@echo "  make swagger-json   # Génère uniquement Swagger JSON"
	@echo "  make clean-pyc      # Supprime les .pyc et __pycache__"

# 🔹 Installation des dépendances
install:
	pip install -r requirements.txt

# 🔹 Migrations Django
migrate:
	python manage.py makemigrations
	python manage.py migrate

# 🔹 Lancement du serveur Django
run:
	@echo "🚀 Lancement du serveur Django..."
	python manage.py runserver

# 🔹 Génération Swagger YAML + JSON
swagger:
	python manage.py spectacular --file schema.yaml
	python manage.py spectacular --file schema.json

# 🔹 Génération Swagger JSON uniquement
swagger-json:
	python manage.py spectacular --file schema.json

# 🔹 Nettoyage des fichiers Python compilés
clean-pyc:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
