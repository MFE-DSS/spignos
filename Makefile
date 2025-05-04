# ----------- Variables -------------
PYTHON=python
DJANGO_MANAGE=manage.py

# -------------- Commandes principales ---------------

run:
	@echo "🚀 Lancement du serveur Django..."
	$(PYTHON) $(DJANGO_MANAGE) runserver

migrate:
	$(PYTHON) $(DJANGO_MANAGE) migrate

makemigrations:
	$(PYTHON) $(DJANGO_MANAGE) makemigrations

black:
	@echo "🎨 Formatage avec black..."
	black .

lint:
	@echo "🔍 Lint avec flake8..."
	flake8 .

test:
	@echo "🧪 Tests unitaires..."
	$(PYTHON) $(DJANGO_MANAGE) test

swagger:
	@echo "📄 Génération de la documentation Swagger YAML et JSON..."
	$(PYTHON) $(DJANGO_MANAGE) spectacular --file schema.yaml
	$(PYTHON) $(DJANGO_MANAGE) spectacular --file schema.json

# -------------- Nettoyage standard ---------------

clean:
	@echo "🧹 Nettoyage des fichiers Python compilés..."
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -type d -exec rm -r {} + || true

# -------------- Nettoyage HARD ---------------

clean-hard: clean
	@echo "🔥 Nettoyage HARD : __pycache__, fichiers temporaires, .migrations inutilisées..."
	# Supprimer tous les fichiers de migration sauf le 0001 (le premier qui crée les tables)
	find . -path "*/migrations/*.py" -not -name "__init__.py" -not -name "0001_initial.py" -delete || true
	find . -path "*/migrations/*.pyc" -delete || true
	# Supprimer les fichiers temporaires cachés (.DS_Store, etc.)
	find . -name '.DS_Store' -delete || true
	# Supprimer les caches de PyCharm ou autres éditeurs si jamais inclus
	rm -rf .idea/ || true
	rm -rf .vscode/ || true
	rm -rf backend/.pytest_cache/ || true
