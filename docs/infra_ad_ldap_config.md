## 1. Gestion de GLPI et IIS
### GLPI - Gestion et Configuration

GLPI (Gestion Libre de Parc Informatique) est utilisé pour la gestion des actifs IT et le suivi des tickets de support. Voici les actions effectuées :

Installation et Configuration de GLPI sur SRV-WEB

Installation de GLPI sur SRV-WEB (192.168.10.21).

Configuration de MariaDB comme base de données, accessible via localhost sur le port 3306.

Configuration des permissions et accès utilisateurs.

Problèmes rencontrés et résolutions

Erreurs 403 et 500 : Problème de définition de ports entre SRV-DC (192.168.10.2) et SRV-WEB (192.168.10.21).

Résolution en ajustant les règles de pare-feu et permissions IIS.

### IIS - Internet Information Services

Modules activés et nécessaires

Module CGI pour exécuter les scripts PHP.

Activation et configuration de PHP Manager pour la bonne exécution des fichiers PHP.

Définition des Handlers Mapping pour le support FastCGI avec PHP.

## 2. Configuration DNS et gestion du réseau

Types d'Entrées DNS et leur Utilisation

NS (Name Server) : Serveurs DNS autoritaires pour le domaine.

SOA (Start of Authority) : Serveur DNS principal et paramètres de zone.

Hôte A : Association d'un nom de domaine à une ou plusieurs adresses IP.

MX (Mail Exchange) : Serveurs de messagerie du domaine.

### Configuration Spécifique à SPIGNOS.LOCAL

Entrée Hôte A pour spignos.local associée à plusieurs IPs.

DNS primaire sur SRV-DC (192.168.10.2) avec résolution des requêtes internes.

Accès configuré pour l'intégration avec LDAP.

## 3. Intégration LDAP avec Active Directory

Configuration LDAP dans GLPI

Serveur LDAP : 192.168.10.2

Port : 389

BaseDN : OU=IT,DC=spignos,DC=local

Compte Bind : CN=Feldmann Martin,OU=IT,DC=spignos,DC=local

Filtre de connexion :

(&(objectClass=user)(objectCategory=person)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))

Processus de Synchronisation

Vérification des utilisateurs via OU=IT,DC=spignos,DC=local.

Attribution automatique des permissions et rôles via LDAP.

Test de fonctionnement depuis GLPI.

Problèmes rencontrés et résolutions

Connexion LDAP inactive : Vérification des droits et du compte bind.

Synchronisation incomplète : Ajustement du filtre LDAP pour récupérer tous les utilisateurs.
