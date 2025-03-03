FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les dépendances
COPY backend/requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet Django
COPY backend /app/backend

# Vérifier le contenu de `/app/backend`
RUN ls -la /app/backend/spignosapi/spignosapi

# Définir PYTHONPATH et DJANGO_SETTINGS_MODULE
ENV PYTHONPATH=/app/backend
ENV DJANGO_SETTINGS_MODULE=spignosapi.spignosapi.settings


# Exposer le port de l'API
EXPOSE 8000

# Lancer Gunicorn avec le bon chemin de module
CMD ["gunicorn", "--chdir", "/app/backend", "--bind", "0.0.0.0:8000", "spignosapi.spignosapi.wsgi:application"]
