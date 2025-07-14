# 📚 Documentation Technique : VIP & Firewall Policy pour SPIGNOS - FortiGate 7.0.13

## 📌 Objectif

Mettre en place l'**exposition publique** de `spignos.com` sur un VPS OVH, **protégé** par une VIP FortiGate en respectant la **séparation LAN / DMZ / WAN**.

Ce document compile toutes les configurations FortiGate et la logique d'infrastructure associée.

---

# 🛠️ 1. Création des objets réseau

## ➡️ 1.1 Address Object - VPS

- **Nom** : `ADDR_VPS_SPIGNOS`
- **Type** : `IP/Netmask`
- **Adresse IP** : `51.68.71.173/32`
- **Interface** : `Any`
- **Commentaire** : VPS Spignos (OVH)

## ➡️ 1.2 VIP Object - Site Web

- **Nom** : `VIP_SPIGNOS_WEB`
- **Interface WAN** : `WAN (port3)`
- **External IP Address** : (Ton IPv4 publique WAN, ex : `92.184.xx.xx`)
- **Mapped IP Address** : `51.68.71.173`
- **Port Forwarding** : Désactivé
- **Commentaire** : Redirection HTTP/HTTPS vers VPS OVH

---

# 📜 2. Création des Firewall Policies

| ID | Nom                     | Source         | Destination         | Service                  | Direction | NAT | Commentaire                            |
|:--:|--------------------------|----------------|---------------------|---------------------------|-----------|-----|----------------------------------------|
| 1  | LAN_TO_WAN               | LAN (port2)     | WAN (port3)          | HTTP, HTTPS, DNS, NTP     | ➡️        | ✅   | Navigation Internet pour LAN           |
| 2  | WAN_TO_LAN               | WAN (port3)     | LAN (port2)          | Established Sessions Only | ⇄         | ❌   | Retours TCP vers LAN                   |
| 3  | LAN_TO_VPS_DB            | LAN (port2)     | ADDR_VPS_SPIGNOS     | PostgreSQL (5432)         | ➡️        | ✅   | Django LAN vers DB VPS                 |
| 4  | VPS_TO_LAN_DB (optionnel) | WAN (port3)     | SRV-DB (LAN)         | PostgreSQL (5432)         | ➡️        | ❌   | Retour restreint depuis VPS            |
| 5  | VIP_WEB                  | WAN (port3)     | VIP_SPIGNOS_WEB      | HTTP, HTTPS               | ➡️        | ❌   | Exposition publique de spignos.com     |
| 6  | ADMIN_ACCESS             | LAN (port2)     | LAN, DMZ, VPS        | SSH, RDP, WinRM           | ⇄         | ❌   | Accès d'administration sécurisé        |
| 7  | DENY_ALL                 | Any             | Any                  | ALL                       | ⇄         | ❌   | Blocage général hors règles explicites |

---

# 📊 3. Schéma d'infrastructure (UML Markdown)

```plaintext
             [ Internet (WAN) - Public IP ]
                        |
               +--------+---------+
               | VIP_SPIGNOS_WEB  |
               +--------+---------+
                        |
                 [ VPS OVH - 51.68.71.173 ]
                        |
          +-------------+-------------+
          |                           |
 [ Service Web/API Django ]    [ WordPress (optionnel) ]
          |
          v
  [ Accès PostgreSQL - SRV-DB (LAN) ]

LAN (192.168.10.0/24) --> accès SSH/DB vers VPS
LAN (192.168.10.0/24) --> Internet via LAN_TO_WAN

+---------------------------+
|        Firewall FortiOS    |
| - VIP
| - Firewall Policies        |
| - NAT & Monitoring         |
+---------------------------+
```

---

# ⚙️ 4. Détails par élément

## 4.1 VIP (Virtual IP)
- Masque l'adresse réelle du VPS derrière l'IP publique de ton FortiGate.
- Permet d'appliquer contrôle, logs, et filtrage HTTP/HTTPS.

## 4.2 PostgreSQL Distant
- Django reste hébergé sur VPS.
- La base PostgreSQL reste protégée sur ton LAN (SRV-DB).

## 4.3 Sécurité avancée
- **Deny All** : Politique par défaut.
- **Admin Access** : Ouvert uniquement depuis LAN sécurisé.
- **Journalisation** : Activée sur toutes les policies sensibles.
- **Cloudflare** : Protection supplémentaire DNS et HTTPS.
