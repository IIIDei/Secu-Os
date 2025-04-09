# Hardening des Systèmes avec Apparmor - Ubuntu 22.04

## 📄 Objectifs
Explorer le contrôle d’accès obligatoire sous Linux via **AppArmor**, dans une logique de sécurisation d’un serveur web sous Ubuntu.  
L’approche s’aligne avec la défense en profondeur et s’appuie sur des recommandations reconnues, comme le **CIS Benchmark**.

Objectifs spécifiques :
- Découvrir les modes et mécanismes d'AppArmor
- Sécuriser l'accès SSH et filtrer les flux réseau
- Créer et ajuster un profil AppArmor pour un binaire
- Appliquer les recommandations CIS pertinentes

---

## 🖥️ Contexte de la VM

- **Système** : Ubuntu 22.04 Desktop
- **Interface graphique** : activée
- **Accès Internet** : ✅
- **Administrable en SSH** : ✅
- **AppArmor** : installé, avec profils actifs
- **Utilisateur principal** : membre du groupe `sudo`
- **Apache2** : installé et actif par défaut

---

## 🔐 1. Sécurisation de l'administration

### 🔑 Configuration SSH (recommandations ANSSI)

Fichier : `/etc/ssh/sshd_config.d/custom.conf`

```conf
Port 7372
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile /home/%u/.ssh/authorized_keys
AllowAgentForwarding no
AllowTcpForwarding no
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 0
UseDNS no

Match User dei
    AuthorizedKeysFile /home/dei/.ssh/authorized_keys
```

- Clé publique ajoutée dans `~/.ssh/authorized_keys`
- Connexion possible sans mot de passe uniquement pour l’utilisateur autorisé ✅

### 🔥 Configuration du pare-feu `ufw`

```bash
sudo ufw allow 7372/tcp
sudo ufw enable
sudo ufw status
```

Sortie :

```bash
Status: active

To                         Action      From
--                         ------      ----
7372/tcp                   ALLOW       Anywhere                  
7372/tcp (v6)              ALLOW       Anywhere (v6)             
```

---

## 🌐 2. Installation d’Apache & AppArmor

### 🚀 Installation Apache

```bash
sudo apt install apache2 -y
sudo systemctl enable --now apache2
```

- Le site par défaut est accessible via navigateur ✅

### 🛡️ Vérification AppArmor

```bash
sudo aa-status
```

Sortie :

```bash
apparmor module is loaded.
39 profiles are loaded.
39 profiles are in enforce mode.
...
```

---

## 🔎 3. Exploration des modes AppArmor

### 📌 Modes disponibles

| Mode      | Description |
|-----------|-------------|
| **enforce** | Applique strictement les règles |
| **complain** | N’empêche pas l’exécution, mais journalise les violations |
| **unconfined** | Aucune restriction via AppArmor |

### ❓ Que se passe-t-il si le profil ne convient pas ?

> En mode `enforce`, toute action interdite par le profil AppArmor entraîne une erreur bloquante pour le programme concerné. Cela permet de contenir les comportements indésirables.

---

## ⚙️ 4. Création et ajustement d’un profil AppArmor

### 🛠️ Création d’un profil squelette pour `ls`

```bash
sudo aa-genprof /bin/ls
```

- L’outil permet de générer un profil à partir des comportements réels observés.
- Une fois en mode apprentissage (`complain`), on exécute diverses commandes `ls`.

Exemples :

```bash
ls
ls -al /tmp
ls /etc
```

Puis :

```bash
sudo aa-logprof
```

- On affine le profil généré en fonction des violations détectées.
- Une fois stable, on passe en mode `enforce` :

```bash
sudo aa-enforce /etc/apparmor.d/bin.ls
```

### ✅ Validation

- Les commandes `ls` classiques continuent à fonctionner
- En cas de souci, retour temporaire au mode `complain` :

```bash
sudo aa-complain /etc/apparmor.d/bin.ls
```

- Puis nouvel ajustement avec `aa-logprof`.

---

## 🔐 5. Durcissement avec le CIS Benchmark

- Référence : [CIS Ubuntu Linux 22.04 Benchmark](https://www.cisecurity.org/benchmark/ubuntu_linux)

### 🔎 Ajustements AppArmor recommandés (exemples)

- Vérification de l’état du service AppArmor :

```bash
sudo systemctl is-enabled apparmor
sudo systemctl status apparmor
```

- Suppression de profils inutiles ou non maintenus
- Activation permanente du mode `enforce` pour les services critiques :

```bash
sudo aa-enforce /etc/apparmor.d/*
```

- Vérification des journaux AppArmor :

```bash
sudo journalctl -t apparmor
```

---

## 🗂️ Structure de fichiers modifiés/créés

```
/etc/ssh/sshd_config.d/custom.conf
/etc/apparmor.d/bin.ls
/home/lucas/.ssh/authorized_keys
```

---

## ✅ Résultats finaux

| Élément                          | Statut |
|----------------------------------|--------|
| Accès SSH restreint              | ✅    |
| Port custom 7372 actif           | ✅    |
| AppArmor actif (39 profils)      | ✅    |
| Apache fonctionnel               | ✅    |
| Profil `ls` en mode enforce      | ✅    |
| Recommandations CIS appliquées   | ✅    |
