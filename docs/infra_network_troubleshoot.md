# 🔧 Spignos Network & Infrastructure Troubleshooting Guide

## 📌 Introduction
Ce guide est une **cheat sheet complète** pour la gestion et la résolution des problèmes d'infrastructure et de réseau de Spignos. Il couvre **la configuration réseau, le déploiement des services, les problèmes de connectivité, le routage, le NAT, la gestion des conteneurs Docker/Kubernetes, ainsi que le dépannage avancé des DNS et des connexions réseau**.

## 📂 Table des Matières
1. **📡 Configuration Réseau de Base**
2. **📊 Vérification des Routes & Connectivité**
3. **🌍 Dépannage du NAT & Accès Internet**
4. **🔎 Résolution des Problèmes DNS**
5. **📦 Déploiement Docker & Kubernetes**
6. **📁 Gestion des Logs & Monitoring**
7. **🛠 Historique des Fixes et RCA (Root Cause Analysis)**

---

## 1️⃣ 📡 Configuration Réseau de Base

### 🖥️ **SRV-DC (Windows Server 2022 - Active Directory & DNS)**
#### ➜ **Fixer l'adresse IP et la passerelle :**
```powershell
New-NetIPAddress -InterfaceAlias "Ethernet0" -IPAddress 192.168.10.2 -PrefixLength 24 -DefaultGateway 192.168.10.254
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" -ServerAddresses ("192.168.10.1", "8.8.8.8")
```

#### ➜ **Vérifier la configuration actuelle :**
```powershell
ipconfig /all
route print
```

#### ➜ **Tester la connexion vers la passerelle :**
```powershell
ping 192.168.10.254
```

---

## 2️⃣ 📊 Vérification des Routes & Connectivité

### **🛜 Vérifier la table de routage sur FortiGate :**
```bash
get router info routing-table all
```

### **🖧 Tester la connectivité entre SRV-DC et FortiGate :**
```powershell
ping 192.168.10.254  # Vérifier la passerelle FortiGate
Test-NetConnection -ComputerName 8.8.8.8 -Port 53  # Tester le DNS
tracert 8.8.8.8  # Vérifier le chemin réseau
```

### **📡 Vérifier les sessions réseau sur FortiGate :**
```bash
diagnose sys session list | grep 192.168.10.2
```

---

## 3️⃣ 🌍 Dépannage du NAT & Accès Internet

### **🔄 Vérifier que le NAT fonctionne sur FortiGate :**
```bash
diagnose firewall snat list
```

### **🛠 Ajouter un pool NAT manuel si nécessaire :**
```bash
config firewall ippool
    edit "SNAT_POOL"
    set startip 192.168.1.114
    set endip 192.168.1.114
    set type overload
next
end
```

### **🔍 Capturer les paquets pour identifier le blocage :**
```bash
diagnose sniffer packet any 'host 192.168.10.2' 4
```

---

## 4️⃣ 🔎 Résolution des Problèmes DNS

### **🧩 Tester la résolution DNS sur SRV-DC :**
```powershell
nslookup google.com
Resolve-DnsName google.com
```

### **🛠 Changer le serveur DNS si la résolution échoue :**
```powershell
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" -ServerAddresses ("8.8.8.8", "1.1.1.1")
```

### **📡 Vérifier les DNS sur FortiGate :**
```bash
get system dns
```

---

## 5️⃣ 📦 Déploiement Docker & Kubernetes

### **💾 Vérifier l'installation de Docker :**
```bash
docker --version
systemctl status docker
```

### **🚀 Lancer les conteneurs Docker :**
```bash
docker-compose up -d
```

### **🔄 Vérifier Kubernetes :**
```bash
kubectl get pods -A
kubectl get services -A
kubectl describe pod <pod_name>
```

### **🌐 Vérifier l'exposition des services :**
```bash
kubectl get ingress
```

---

## 6️⃣ 📁 Gestion des Logs & Monitoring

### **📝 Logs FortiGate :**
```bash
diagnose debug enable
diagnose debug console timestamp enable
diagnose debug application sslvpn -1
```

### **🔍 Logs Kubernetes :**
```bash
kubectl logs -f <pod_name>
```

### **📡 Logs Docker :**
```bash
docker logs <container_id>
```

---

## 7️⃣ 🛠 Historique des Fixes et RCA (Root Cause Analysis)

| 📅 Date | 🔍 Problème | 🛠 Solution | ✅ Résolu |
|---------|------------|------------|-----------|
| 08/02/25 | SRV-DC ne ping pas Internet | Vérification NAT & ajout d'une règle SNAT | ✅ Oui |
| 09/02/25 | Kubernetes pods ne se lancent pas | Correction de l'image du conteneur et des permissions | ✅ Oui |
| 10/02/25 | DNS ne résout pas les noms de domaine | Modification des entrées DNS dans FortiGate | ✅ Oui |

---

### 📢 **Derniers conseils :**
- Vérifie toujours la **passerelle par défaut** des machines 🖥️
- Teste **les DNS et le NAT** en cas de problème de connectivité 🌍
- Garde une **trace des correctifs** pour éviter de refaire les mêmes erreurs 🛠️

---

📌 **Ce document évoluera au fil du temps pour s’adapter aux nouvelles problématiques et solutions apportées à l’infrastructure de Spignos.** 🚀

