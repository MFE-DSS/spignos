# 🔄 Migration WordPress → Django sur VPS OVH (spignos.com)

Ce document résume les commandes importantes utilisées lors de l’installation de WordPress, et propose une **réadaptation complète pour déployer Django** dans le même environnement (Ubuntu 24.04 sur VPS OVH).

---

## 📦 Étapes WordPress : Rappel des Commandes Importantes

```bash
# Structure des répertoires web
cd /var/www
ls
cd html

# Déplacement des fichiers
sudo mv ~/wordpress /var/www/html/
sudo chown -R www-data:www-data /var/www/html/wordpress
sudo chmod -R 775 /var/www/html/wordpress

# Installation PHP + Apache
sudo apt install php8.3 libapache2-mod-php8.3

# Edition de php.ini
sudo nano /etc/php/8.3/apache2/php.ini

# Installation MariaDB (alternative MySQL)
sudo apt install mariadb-server
sudo mysql -u root -p

# Création base de données WordPress
CREATE DATABASE wordpress;

# Configuration Apache
cd /etc/apache2/sites-available/
sudo cp 000-default.conf spignos.com.conf
sudo nano spignos.com.conf

# Activation du site et rechargement
sudo a2ensite spignos.com.conf
sudo a2dissite 000-default.conf
sudo systemctl reload apache2

# Installation HTTPS avec Certbot
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d spignos.com
```

---

## 🚀 Réadaptation pour le Déploiement Django

### 1️⃣ Préparer le VPS

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git nginx
```

### 2️⃣ Cloner ton projet Django

```bash
cd /var/www/
git clone git@github.com:MFE-DSS/spignos.git
cd spignos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Configurer Gunicorn

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Contenu :

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/spignos
ExecStart=/var/www/spignos/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock spignos.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 4️⃣ Configurer NGINX pour Django

```bash
sudo nano /etc/nginx/sites-available/spignos
```

Contenu :

```nginx
server {
    listen 80;
    server_name spignos.com www.spignos.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/spignos;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/spignos /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 5️⃣ HTTPS avec Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d spignos.com -d www.spignos.com
```

---

## 📝 Notes supplémentaires

- Pour PostgreSQL, configure la base sur SRV-WEB ou SRV-DB.
- Vérifie que Django a bien accès à PostgreSQL via `settings.py`.

---
