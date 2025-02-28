FROM python:3.10

# Définir le répertoire de travail du conteneur
WORKDIR /app

# Copier les dépendances
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet Django
COPY . /app/

# Vérifier la présence des fichiers
RUN ls -la /app
RUN ls -la /app/spignosapi/spignosapi

# Exposer le port (si nécessaire)
EXPOSE 8000

# Lancer Gunicorn avec le bon chemin
CMD ["gunicorn", "--chdir", "/app", "--bind", "0.0.0.0:8000", "spignosapi.wsgi:application"]
