# 🐳 To-Do List: Déploiement Docker du Backend Spignos

## 📌 1️⃣ Installer les dépendances Docker
Si Docker n'est pas installé sur votre machine, suivez les instructions officielles :
- **Ubuntu** : https://docs.docker.com/engine/install/ubuntu/
- **Windows** : https://docs.docker.com/desktop/install/windows-install/

Vérifier l'installation :
```bash
docker --version
```

## 📌 2️⃣ Construire l'image Docker du backend
Lancer la commande suivante depuis le répertoire racine du projet :
```bash
docker build -t spignos-backend -f backend/Dockerfile .
```
Explication :
- `-t spignos-backend` : Nom de l’image Docker.
- `-f backend/Dockerfile` : Spécifie le chemin du Dockerfile.

## 📌 3️⃣ Lancer le conteneur en local
Exécuter le conteneur avec :
```bash
docker run -p 8000:8000 spignos-backend
```
Explication :
- `-p 8000:8000` : Redirige le port 8000 du conteneur vers la machine hôte.
- `spignos-backend` : Nom du conteneur construit.

Tester l'API sur : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📌 4️⃣ Vérifier les logs du conteneur
Si besoin, voir ce qui se passe en live :
```bash
docker logs -f <container_id>
```
Obtenir l'ID du conteneur en cours d'exécution :
```bash
docker ps
```

## 📌 5️⃣ Supprimer un conteneur ou une image
- **Arrêter un conteneur actif** :
  ```bash
  docker stop <container_id>
  ```
- **Supprimer un conteneur** :
  ```bash
  docker rm <container_id>
  ```
- **Supprimer une image** :
  ```bash
  docker rmi spignos-backend
  ```

## 📌 6️⃣ Pousser l'image vers Docker Hub (optionnel)
Créer un compte sur [https://hub.docker.com/](https://hub.docker.com/) puis :
```bash
docker tag spignos-backend <votre-utilisateur>/spignos-backend
```
Se connecter et envoyer l’image :
```bash
docker login
docker push <votre-utilisateur>/spignos-backend
```

## 📌 7️⃣ Déployer avec Docker Compose (optionnel)
Si plusieurs services sont utilisés (ex: PostgreSQL, Redis...), ajouter un `docker-compose.yaml` :
```bash
docker-compose up -d
```
---
✅ **Votre backend Spignos tourne maintenant en conteneur Docker !** 🚀
