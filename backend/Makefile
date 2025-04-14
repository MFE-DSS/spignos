# Makefile pour SPIGNOS

VENV=.venv/bin
MANAGE=python manage.py

run:
	@echo "🚀 Lancement du serveur Django..."
	@$(VENV)/$(MANAGE) runserver

swagger-json:
	@echo "📄 Génération du schéma Swagger (JSON)..."
	@$(VENV)/$(MANAGE) spectacular --file schema.json

swagger-yaml:
	@echo "📄 Génération du schéma Swagger (YAML)..."
	@$(VENV)/$(MANAGE) spectacular --file schema.yaml

swagger: swagger-json swagger-yaml

test-llm:
	@echo "🧪 Test du modèle LLM local..."
	@$(VENV)/python scripts/test_llm.py

download-model:
	@echo "📥 Téléchargement du modèle local..."
	@$(VENV)/python scripts/download_model.py

clean-pyc:
	@echo "🧹 Suppression des fichiers .pyc et __pycache__..."
	find . -type d -name "__pycache__" -exec rm -r {} + ; find . -name "*.pyc" -delete
