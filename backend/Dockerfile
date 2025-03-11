FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les dépendances
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le backend
COPY . /app/

# Vérifier que les fichiers sont bien copiés
RUN ls -la /app/spignosapi
RUN ls -la /app/spignosapi/spignosapi

# Définir PYTHONPATH et DJANGO_SETTINGS_MODULE
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=spignosapi.spignosapi.settings

# Exposer le port de l'API
EXPOSE 8000

# Lancer Gunicorn avec le bon chemin de module
CMD ["gunicorn", "--chdir", "/app", "--bind", "0.0.0.0:8000", "spignosapi.spignosapi.wsgi:application"]
