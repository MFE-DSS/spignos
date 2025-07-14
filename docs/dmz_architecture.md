# 🔒 Documentation Firewall Policies - Projet SPIGNOS

## 🔗 Objectif

Garantir la communication **sécurisée** entre toutes les zones de l'infrastructure SPIGNOS :

- **LAN** (Serveurs internes)
- **DMZ** (Services exposés)
- **WAN** (Internet)
- **VPS externe** (Cloud OVH - 51.68.71.173)

En respectant les **meilleures pratiques de sécurité**, **NAT** et **contrôle de flux**.

---

## 🔒 Table des Firewall Policies définies

| ID | Nom                       | Source      | Destination        | Services                  | Direction | NAT | Remarques                             |
| -- | ------------------------- | ----------- | ------------------ | ------------------------- | --------- | --- | ------------------------------------- |
| 1  | LAN_TO_WAN                 | LAN (port2) | WAN (port3)         | HTTP, HTTPS, DNS, NTP     | ➡️        | ✅   | Navigation Internet LAN               |
| 2  | WAN_TO_LAN                 | WAN (port3) | LAN (port2)         | Established Sessions Only | ⇄         | ❌   | Retours de sessions LAN vers Internet |
| 3  | LAN_TO_VPS                 | LAN (port2) | VPS (51.68.71.173)  | PostgreSQL (5432), HTTPS  | ➡️        | ✅   | Accès à la DB/VPS                     |
| 4  | VPS_TO_LAN (optionnel)      | VPS (WAN)   | SRV-DB (LAN)        | PostgreSQL (5432)         | ➡️ limité | ❌   | Ouverture spécifique et maîtrisée     |
| 5  | DMZ_TO_LAN                 | DMZ         | LAN                 | LDAP, PostgreSQL, DNS     | ⇄         | ❌   | Échanges de service internes          |
| 6  | LAN_TO_DMZ                 | LAN         | DMZ                 | SSH, PostgreSQL           | ⇄         | ❌   | Administration LAN vers DMZ           |
| 7  | VIP_WEB (WAN to DMZ/VPS)    | WAN (port3) | VIP_DMZ ou VPS      | HTTP, HTTPS               | ➡️        | ❌   | Publication site web/API publique     |
| 8  | ADMIN_ACCESS               | LAN (port2) | LAN, DMZ, VPS       | SSH, RDP, WinRM           | ⇄         | ❌   | Accès privilégié sécurisé             |
| 9  | DENY_ALL                   | ANY         | ANY                 | ALL                       | ⇄         | ❌   | Blocage total hors règles définies     |

---

## 📊 Schéma textuel des flux autorisés

```plaintext
[ Internet (WAN) ]
    ⇄ VIP_WEB (HTTP/HTTPS) ⇄ [ DMZ (WordPress, Django VPS) ]

[ LAN (192.168.10.0/24) ]
    ➡️ LAN_TO_WAN ➡️ [ Internet ]
    ⇄ LAN_TO_DMZ / DMZ_TO_LAN ⇄
    ➡️ LAN_TO_VPS ➡️ VPS
    ⇄ ADMIN_ACCESS SSH/RDP ⇄ LAN/DMZ/VPS

[ DMZ (192.168.40.0/24) ]
    ⇄ DMZ ⇄ LAN (LDAP, PostgreSQL)
```

---

# 🛠️ Particularités et Enjeux Techniques

## 1⃣ LAN_TO_WAN / WAN_TO_LAN

- **LAN_TO_WAN** : Permet à tes serveurs internes (SRV-DC, SRV-WEB, SRV-DB) de se connecter vers Internet pour des mises à jour ou accès API extérieurs.
- **WAN_TO_LAN** : Restreint uniquement aux réponses des connexions initiées.

**Objectif** : ✔️ Navigation Internet contrôlée sans exposition du LAN.

---

## 2⃣ LAN_TO_VPS / VPS_TO_LAN

- **LAN_TO_VPS** : Permet à Django et services internes de consommer PostgreSQL/API exposés par le VPS.
- **VPS_TO_LAN** (optionnel) : Limité à PostgreSQL ou services nécessaires.

**Objectif** : ✔️ Sécuriser l'accès aux bases de données distribuées.

---

## 3⃣ DMZ_TO_LAN / LAN_TO_DMZ

- Échanges LDAP (authentification Active Directory)
- Accès PostgreSQL LAN à partir des services en DMZ (WordPress, Django API)
- Résolutions DNS internes

**Objectif** : ✔️ Permettre aux applications publiques d'utiliser les ressources internes en évitant les expositions non nécessaires.

---

## 4⃣ VIP_WEB (WAN to DMZ)

- VIP (Virtual IP) pour exposer uniquement le domaine spignos.com via HTTP/HTTPS.
- Redirige vers ton VPS ou service DMZ tout en utilisant Cloudflare et FortiGate pour filtrer.

**Objectif** : ✔️ Publier spignos.com sans exposer directement l'adresse IP LAN.

---

## 5⃣ ADMIN_ACCESS

- SSH pour l'administration Linux (SRV-WEB, SRV-DB)
- RDP pour l'administration Windows (SRV-DC)
- WinRM pour automatisation (Ansible, Scripts)

**Objectif** : ✔️ Système d'administration contrôlé et audité.

---

## 6⃣ DENY_ALL

- Aucune communication autorisée si elle n'est pas définie explicitement.

**Objectif** : ✔️ Appliquer la politique de "Zero Trust".

---

# 📊 Enjeux de Sécurité Avancés

- **Isolation DMZ/LAN** : Empêcher un service compromis dans la DMZ d'accéder librement au LAN.
- **VPS externe** : Être traité comme un poste externe contrôlé même s'il sert ton domaine.
- **Logs & Monitoring** : Activer la journalisation sur toutes les policies critiques.
- **VPN d'administration** : Privilégier des tunnels VPN pour l'administration à distance.
