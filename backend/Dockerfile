FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les dépendances pour optimiser le cache
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet Django
COPY . /app/

# Vérifier que `spignosapi/spignosapi/wsgi.py` est bien copié
RUN ls -la /app/spignosapi/spignosapi

# Définir PYTHONPATH pour éviter les erreurs d'importation
ENV PYTHONPATH=/spignos/spignosapi


ENV DJANGO_SETTINGS_MODULE=spignosapi.spignosapi.settings

# Exposer le port de l'API
EXPOSE 8000
# Lancer Gunicorn avec le bon chemin de module
CMD ["gunicorn", "--chdir", "/app/spignosapi", "--bind", "0.0.0.0:8000", "spignosapi.wsgi:application"]
