
### Active Directory & ADDS

**ADDS (Active Directory Domain Services)** est le rôle principal de l’Active Directory installé sur **SRV-DC** (contrôleur de domaine) :

- Gère les **identités utilisateurs**, groupes, ordinateurs.
- Fonctionne sur les protocoles **LDAP** et **Kerberos**.
- Permet la **centralisation des authentifications**.

### Qu'est-ce que LDAP ?
LDAP (Lightweight Directory Access Protocol) est un protocole utilisé pour **interroger** et **modifier** les services d’annuaire.
Il permet :
- de rechercher un utilisateur ou un groupe dans un domaine (ex. : `spignos.local`)
- d’effectuer des authentifications via des applications tierces (ex : GLPI)

### Accès à l’annuaire LDAP dans SPIGNOS
Ton annuaire LDAP est configuré ainsi :
- **Serveur LDAP** : `192.168.10.2` (SRV-DC)
- **BaseDN** : `OU=IT,DC=spignos,DC=local`
- **Port** : 389 (LDAP standard non chiffré)
- **Bind DN** : Utilisateur avec droits pour interroger l’AD (`CN=Feldmann Martin,...`)

### Intégration dans les applications
Ex : GLPI utilise l’AD pour synchroniser les comptes utilisateurs :
- Authentification unique (SSO possible)
- Attributions automatiques de rôles dans l’interface GLPI

---

## 2. 🌐 DMZ & Exposition Sécurisée de Services

### Pourquoi utiliser une DMZ ?
La **DMZ** (Demilitarized Zone) est une **zone tampon** réseau :
- Elle expose **les services web** au public (ex : spignos.com)
- Elle **protège le LAN** d’un accès direct

### Dans SPIGNOS :
| Zone | Contenu | Exemple |
|------|---------|---------|
| LAN | Données internes, AD, PostgreSQL | `SRV-DC`, `SRV-DB` |
| DMZ | Services exposés | `VPS (spignos.com)` |
| WAN | Accès Internet | OVH, Utilisateurs externes |

Le FortiGate :
- filtre les flux entre WAN ↔ DMZ ↔ LAN via des **policies**
- expose via **VIP** les services Django depuis DMZ (VPS)

---

## 3. 🔏 HTTPS et Certificats avec Certbot

### Pourquoi HTTPS ?
- Chiffre les échanges client ⇄ serveur
- Assure l’identité du site
- Requis pour de nombreux navigateurs modernes

### Utilisation de **Certbot**
Certbot est un client ACME pour générer automatiquement des certificats **Let’s Encrypt**.

#### Installation :
```bash
sudo apt install certbot python3-certbot-apache
```

#### Génération automatique d’un certificat HTTPS :
```bash
sudo certbot --apache -d spignos.com -d www.spignos.com
```

Cela :
- Configure automatiquement Apache pour utiliser HTTPS
- Installe le certificat SSL/TLS Let’s Encrypt

### 🔁 Renouvellement automatique
```bash
sudo crontab -e
```
Ajouter :
```
0 0 1 * * certbot renew --quiet
```

---

## 4. 🔗 Intégration Django avec HTTPS

Même si Django peut servir du HTTPS, en production tu utilises :
- **Gunicorn** comme serveur WSGI
- **Nginx ou Apache** en reverse proxy

### Lien entre Apache (ou Nginx) et Django :
- Apache (ou Nginx) gère HTTPS (avec Certbot)
- Il **reverse-proxy** les requêtes vers Gunicorn (port local, socket)

### Configuration Apache pour Django (extrait) :
```apache
<VirtualHost *:443>
    ServerName spignos.com
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/spignos.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/spignos.com/privkey.pem

    ProxyPass / http://unix:/run/gunicorn.sock|http://127.0.0.1:8000/
    ProxyPassReverse / http://unix:/run/gunicorn.sock|http://127.0.0.1:8000/
</VirtualHost>
```

### Django à configurer pour HTTPS :
Dans `settings.py` :
```python
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

---
