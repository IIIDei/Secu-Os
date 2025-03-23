# Syscalls - Part IV : My Shitty App

## But et contexte
Dans cette partie, le but est de prendre le contrôle sur une application Python vulnérable, la transformer en service systemd, la durcir (hardening) via un utilisateur dédié et un filtrage `seccomp` des appels systèmes (syscalls). Nous devons également tester cette application via `netcat`, l'exploiter pour obtenir un shell root, puis appliquer un hardening pour bloquer cette exploitation.

---

## 1. Test de l'application

### 🌟 Installation et test initial
- Application téléchargée et placée dans `/opt/calc.py`
- Lancement manuel avec :
```bash
python3 /opt/calc.py
```
- Ouverture du port firewall 13337 (réseau interne)
- Connexion avec `netcat` depuis mon PC Windows :
```powershell
.\ncat.exe --crlf 10.1.1.11 13337
```
- Test : envoi de `6+6` → réponse correcte `12` → Fonctionnement OK

---

## 2. Création du service systemd

### Fichier `/etc/systemd/system/calculatrice.service` :
```ini
[Unit]
Description=Super serveur calculatrice

[Service]
ExecStart=/usr/bin/python3 /opt/calc.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Commandes effectuées :
```bash
sudo systemctl daemon-reload
sudo systemctl start calculatrice
sudo systemctl status calculatrice
```

### 🚀 Résultat :
- Service actif et fonctionnel
- Test avec `netcat` toujours opérationnel (calculs OK)

---

## 3. Exploitation (Hack)

### Payload utilisé depuis netcat :
```
__import__('os').system('/bin/bash')
```

### Effet :
- Shell root obtenu (dû à `eval()` vulnérable)
- Commande `ps aux | grep bash` : présence du shell root visible

---

## 4. Hardening

### 🔒 A. Création utilisateur dédié
```bash
sudo useradd --no-create-home --shell /sbin/nologin calculatrice
sudo chown calculatrice:calculatrice /opt/calc.py
sudo chmod 700 /opt/calc.py
```

### 🏛️ Modification du `.service` :
```ini
[Unit]
Description=Super serveur calculatrice

[Service]
ExecStart=/usr/bin/python3 /opt/calc.py
Restart=always
User=calculatrice

[Install]
WantedBy=multi-user.target
```

### 🌟 Vérification :
```bash
ps aux | grep calc.py
# Retour : utilisateur "calculatrice" actif
```

---

### 🛡️ B. Filtrage des syscalls

### 1. Tracing normal :
```bash
sudo strace -f -o strace_calc_normal.txt /usr/bin/python3 /opt/calc.py
```
- Connexion via `netcat` et calcul `3+3`
- Arrêt avec `CTRL+C`
- Extraction syscalls :
```bash
cat strace_calc_normal.txt | grep -oP '^[0-9]+\s+\K\w+' | sort | uniq
```
- Liste obtenue : `read`, `write`, `recvfrom`, `sendto`, `openat`, `mmap`, `futex`, etc.

### 2. Tracing exploitation :
```bash
sudo strace -f -o strace_calc_hack.txt /usr/bin/python3 /opt/calc.py
```
- Connexion netcat + envoi du payload exploit
- Extraction : identifié `execve` lors de l'exploit ✔️

### 3. Mise en place `seccomp` dans le `.service` :
```ini
SystemCallFilter=~execve
```

### 🌟 Test post-hardening :
- Connexion normale = OK
- Exploit = 💥 crash du service avec code `SYS/core-dump` → **Filtrage efficace**

---

## 📌 **Fichier joint**
- `strace_calc_normal.txt` : tracing normal
- `strace_calc_hack.txt` : tracing exploitation
- `calculatrice.service` : service avec hardening

---
