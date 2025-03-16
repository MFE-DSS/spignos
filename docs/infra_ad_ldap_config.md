## 1. Gestion de GLPI et IIS

GLPI - Gestion et Configuration

GLPI (Gestion Libre de Parc Informatique) est utilisé pour la gestion des actifs IT et le suivi des tickets de support. Voici les actions effectuées :

Installation et Configuration de GLPI sur SRV-WEB

Téléchargement et installation de GLPI sur SRV-WEB (192.168.10.21).

Configuration de MariaDB comme base de données, accessible via localhost sur le port 3306.

Définition des accès et configurations de droits utilisateurs.

Problèmes rencontrés et résolutions

Erreurs 403 et 500 : Problème de définition de port entre SRV-DC (192.168.10.2) et SRV-WEB (192.168.10.21).

Résolution en ajustant les règles de pare-feu et permissions IIS.

### IIS - Internet Information Services

Modules activés et nécessaires

Développement d'application CGI pour exécuter les scripts PHP nécessaires.

Activation et configuration de PHP Manager pour assurer la bonne exécution des fichiers PHP.

Configuration des Handlers Mapping pour le support FastCGI avec PHP.

## 2. Configuration DNS pour SPIGNOS.LOCAL

### Types d'Entrées DNS et Utilisation

NS (Name Server) : Définit les serveurs DNS autoritaires pour le domaine.

SOA (Start of Authority) : Définit le serveur DNS principal et les paramètres de zone.

Hôte A : Associe un nom de domaine à une ou plusieurs adresses IP.

MX (Mail Exchange) : Définit les serveurs de messagerie du domaine.

### Configuration Spécifique à SPIGNOS.LOCAL

Entrée Hôte A pour spignos.local associée à plusieurs adresses IP pour redondance.

DNS primaire sur SRV-DC (192.168.10.2) avec résolution des requêtes pour le domaine interne.

Accès configuré pour l'intégration avec LDAP (voir section suivante).

## 3. Installation et Configuration de MariaDB

Installation sur SRV-WEB (192.168.10.21)

Téléchargement et installation de MariaDB.

Configuration de l'accès local via localhost:3306.

Création de bases de données pour stockage des informations GLPI.

Vérification que la base GLPI est bien créée et accessible.

## 4. Intégration LDAP avec Active Directory

### Configuration LDAP dans GLPI

Serveur LDAP : 192.168.10.2

Port : 389

BaseDN : OU=IT,DC=spignos,DC=local

Compte Bind : CN=Feldmann Martin,OU=IT,DC=spignos,DC=local

Filtre de connexion :

(&(objectClass=user)(objectCategory=person)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))

Processus de Synchronisation

Vérification des utilisateurs via OU=IT,DC=spignos,DC=local.

Attribution automatique des permissions et rôles via LDAP.

Vérification du fonctionnement en exécutant un test depuis GLPI.

Problèmes rencontrés et Résolutions

Connexion LDAP inactive : Vérification des droits et du compte utilisé pour le bind.

Synchronisation incomplète : Ajustement du filtre LDAP pour récupérer tous les utilisateurs.

## 5. Réinitialisation de FortiOS et Implications

Suite à une expiration de la période d’essai, un factory reset a été exécuté sur FortiGate. Conséquences :

Suppression de toutes les configurations réseau et firewall.

Nécessité de reconfigurer les interfaces, règles et NAT.

Perte des certificats et configurations DNS internes.

## 6. Exposition de la DMZ et Configuration DHCP

Architecture de la DMZ

Interface externe (WAN) : Gère l’accès public à Spignos.com.

Interface interne (LAN/DMZ) : Sécurise les échanges avec SRV-WEB et les bases de données.

Configuration du DHCP

Plage DHCP : 192.168.40.1 - 192.168.40.254.

Attribue dynamiquement des IPs aux machines internes et aux serveurs en DMZ.

## 7. VLAN et Haute Disponibilité (HA)

Utilisation de VLAN pour segmenter les réseaux internes et éviter les conflits d’adresses.

Mise en place de Haute Disponibilité (HA) pour assurer la résilience des services en cas de panne.

## 8. Benchmark NAS/DAS vs SAN pour SPIGNOS
todo

## 9. Configuration FortiOS pour le Firewall

Ajout des règles pour DMZ ↔ LAN ↔ WAN :

DMZ ➝ LAN : Accès aux bases PostgreSQL et MariaDB.

LAN ➝ DMZ : Exposition du site web.

WAN ➝ DMZ : Sécurisation des accès publics.

## 10. Gestion des Pare-feux Windows

Désactiver les pare-feux Domaine et Privé.

Garder actif le pare-feu Public pour protéger les accès externes.

Configurer des règles de ports spécifiques pour les services critiques.
