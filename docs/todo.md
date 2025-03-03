Sécurisation des services exposés :

Placer le serveur web Spignos.com dans une DMZ pour éviter tout accès direct à la base de données ou à d'autres services sensibles.

Empêcher un attaquant qui compromettrait le serveur web d'accéder au réseau LAN sécurisé.

Filtrage des connexions entrantes :

Seules les requêtes HTTPS sont autorisées à entrer dans la DMZ via le pare-feu FortiGate.

Utilisation de Cloudflare pour protéger le service contre les attaques DDoS et améliorer la disponibilité.

Routage et gestion des adresses IP publiques/privées :

Création d’une VIP sur FortiGate pour rediriger l’IP publique vers l’IP privée du serveur web en DMZ.

Exposition uniquement des ports nécessaires (exemple : 443 pour HTTPS).

📌 Mise en place :

Certificat Cloudflare

Générer un certificat Cloudflare pour le domaine Spignos.com.

Déployer ce certificat sur FortiGate pour activer le SSL Offloading et assurer une communication sécurisée.

Création de VIP sur FortiGate (Mapping IP publique <-> IP LAN)

Exemple de configuration pour rediriger le port 443 vers le serveur web interne 192.168.10.100 :

config firewall vip
    edit "VIP_Web_Server"
        set extip <IP_PUBLIQUE>
        set mappedip 192.168.10.100
        set extintf "port3"  # Interface WAN
        set portforward enable
        set extport 443
        set mappedport 443
    next
end

Création d’une Policy FortiGate pour autoriser l’accès

config firewall policy
    edit 10
        set srcintf "port3"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "VIP_Web_Server"
        set action accept
        set schedule "always"
        set service "HTTPS"
        set nat enable
    next
end

3️⃣ Schéma Macro des Enjeux Réseaux

Le schéma suivant représente la segmentation de l’infrastructure avec une DMZ, une gestion du pare-feu FortiGate et l’isolation des bases de données en LAN.

📌 Composants clés :

DMZ : Exposition du service web Spignos.com via FortiGate.

FortiGate : Gestion du NAT, des VIP et des policies firewall.

LAN : Sécurisation des bases de données PostgreSQL.

Kubernetes Cluster : Gestion des conteneurs backend et API.

Docker Containers : Orchestration des microservices.

Firewall Rules : Filtrage des connexions entrantes et sortantes.

📌 Principales Connexions :

Internet ↔ Cloudflare ↔ FortiGate VIP ↔ Serveur Web DMZ

Serveur Web ↔ Backend API (Kubernetes/Docker)

Backend API ↔ Base de données PostgreSQL (LAN sécurisé)

Kubernetes Load Balancer ↔ Gestion des requêtes API

Gestion des logs et monitoring via des outils internes (Prometheus, Grafana, etc.)

