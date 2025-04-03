# Hardening des Systèmes avec SELinux - Rocky Linux 9

## 📄 Objectifs
Expérimenter les mécanismes de contrôle d'accès obligatoires (MAC) sous Linux via SELinux. Il s'inscrit dans une logique de durcissement de serveur web sur Rocky Linux 9.

Objectifs spécifiques :
- Découvrir le fonctionnement de SELinux
- Mettre en œuvre les bonnes pratiques d'administration sécurisée (SSH, firewall)
- Modifier un profil SELinux
- Appliquer le benchmark de sécurité CIS

---

## 🏗️ Contexte de la VM
- **Système** : Rocky Linux 9 (installation minimale)
- **Langue** : Anglais (clavier AZERTY)
- **Adresse IP** : `10.1.1.11/24`
- **Accès Internet** : ✅
- **Administrable en SSH** : ✅
- **SELinux** : installé et activé (passé de `permissive` à `enforcing` au cours du TP)
- **Utilisateur** : administrateur (ajouté dans le groupe wheel)

---

## 🔐 1. Sécurisation de l'administration
### 🔑 SSH sécurisé (selon recommandations de l’ANSSI)
- Fichier : `/etc/ssh/sshd_config`
- Modifications :
```bash
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```
- Clé publique copiée dans `~/.ssh/authorized_keys`
- Résultat : connexion SSH possible sans mot de passe, uniquement via clé ✅

### 🔥 Firewall (`firewalld`)
```bash
sudo firewall-cmd --list-all
```
- Seuls les services **ssh**, **cockpit** et **dhcpv6-client** sont autorisés.

## 🌐 2. Installation et configuration d'Apache
```bash
sudo dnf install httpd -y
sudo systemctl enable --now httpd
```
- Accès web via navigateur : fonctionne parfaitement ✅
- SELinux initialement désactivé, puis activé (`permissive` > `enforcing`)

## 🔎 3. SELinux : Exploration
### 📌 Modes disponibles
- `disabled` : SELinux désactivé.
- `permissive` : SELinux logue les alertes mais n’interfère pas.
- `enforcing` : SELinux applique les règles et bloque les accès non autorisés.

### 🔍 Contexte de sécurité
- Service Apache :
```bash
ps -eZ | grep httpd
```
→ `system_u:system_r:httpd_t:s0`

- Répertoire et fichier Apache :
```bash
ls -Zd /var/www/html/
```
→ `unconfined_u:object_r:httpd_sys_content_t:s0`

## 🧪 4. Changement du répertoire web et profil SELinux
### 🔁 Modification d’Apache
- Nouveau répertoire web : `/srv/srv/srv_1`
- Fichier ajouté : `index.html` avec `Hello from /srv/srv/srv_1/`

### 🔧 Modification de la configuration
```apache
DocumentRoot "/srv/srv/srv_1"
<Directory "/srv/srv/srv_1">
    AllowOverride None
    Require all granted
</Directory>
```

### 🔐 Activation du mode `enforcing`
```bash
sudo setenforce 1
sestatus
```
→ Résultat : page **403 Forbidden** ❌

### 📛 Diagnostic avec `sealert`
- Erreur : `httpd` ne peut pas accéder à un fichier avec le contexte `user_home_t`
- Solution :
```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/srv/srv/srv_1(/.*)?"
sudo restorecon -Rv /srv/srv/srv_1
```

### ✅ Résultat final
- Contexte :
```bash
ls -Z /srv/srv/srv_1
→ unconfined_u:object_r:httpd_sys_content_t:s0 index.html
```
- Affichage dans le navigateur : `Hello from /srv/srv/srv_1/` 🎉

## 🧱 5. Renforcement via CIS Benchmark
### 🔍 Vérifications et ajustements
- **Paquets vérifiés** :
```bash
rpm -q libselinux
rpm -q setroubleshoot
rpm -q mcstrans
```
→ `setroubleshoot` et `mcstrans` non installés ✅ (recommandé par CIS)

- **Mode SELinux** :
```bash
getenforce
→ Enforcing ✅
```
```bash
grep ^SELINUX= /etc/selinux/config
→ SELINUX=enforcing
```

- **Vérification de l’absence de processus dans le domaine `unconfined_service_t`**
```bash
ps -eZ | grep unconfined_service_t
→ Aucun processus
```
