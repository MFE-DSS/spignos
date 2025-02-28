FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier uniquement les dépendances pour optimiser le cache Docker
COPY backend/requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet backend dans /app/
COPY backend /app/

# Vérifier que spignosapi et manage.py sont bien copiés
RUN ls -la /app
RUN ls -la /app/spignosapi
RUN ls -la /app/spignosapi/spignosapi

# Lancer Gunicorn en pointant vers le bon chemin du projet Django
CMD ["gunicorn", "--chdir", "/app", "--bind", "0.0.0.0:8000", "spignosapi.wsgi:application"]
