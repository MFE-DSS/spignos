📌 Créer un fichier explicatif

touch ~/PycharmProjects/spignos/docs/docker_concepts.md

📌 Ajoute ce contenu :

# 🐳 Comprendre les Concepts Docker
## 📌 Introduction
Docker permet de **containeriser des applications**, ce qui signifie les exécuter dans un environnement isolé et portable.

---

## 🚀 1️⃣ **Les Images et Conteneurs**
### 📌 Image Docker
Une **image** est un modèle en lecture seule utilisé pour créer des **conteneurs**.
Elle contient :
- Le système d'exploitation minimal
- Les dépendances (Python, Django, PostgreSQL…)
- Le code de l'application

**Exemple : Construire une image Docker**
```bash
docker build -t myapp:latest .

📌 Conteneur Docker

Un conteneur est une instance en cours d'exécution d'une image.

Exemple : Lancer un conteneur

docker run -d -p 8000:8000 myapp:latest

🔧 2️⃣ Docker Compose

Docker Compose permet de gérer plusieurs conteneurs dans un même fichier YAML.
📌 Exemple de docker-compose.yaml

version: '3.8'

services:
  web:
    image: python:3.10
    volumes:
      - ./app:/app
    ports:
      - "8000:8000"

Commandes Docker Compose

docker-compose up -d  # Démarrer en arrière-plan
docker-compose down   # Arrêter et supprimer les conteneurs
docker-compose logs   # Voir les logs
docker-compose ps     # Voir les conteneurs en cours d'exécution

⚡ 3️⃣ Gestion des Volumes

Les volumes Docker permettent de persister des données entre les redémarrages.

Créer un volume nommé

docker volume create myvolume

L'utiliser dans docker-compose.yaml

services:
  db:
    image: postgres
    volumes:
      - myvolume:/var/lib/postgresql/data
volumes:
  myvolume:

🛠 4️⃣ Debugging Docker
📌 Vérifier les logs

docker logs <container_id>

📌 Entrer dans un conteneur

docker exec -it <container_id> bash

📌 Vérifier les ports ouverts

docker ps

✅ 5️⃣ Optimisation et Sécurité
📌 Minimiser la taille des images

Utiliser une base plus légère :

FROM python:3.10-slim

📌 Nettoyer Docker régulièrement

docker system prune -a
docker volume prune -f

