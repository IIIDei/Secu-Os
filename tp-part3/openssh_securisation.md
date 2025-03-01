# OpenSSH - Sécurisation du serveur SSH

## Objectif  
Configurer OpenSSH pour renforcer la sécurité et limiter l’accès au serveur :  
- Modifier le port d’écoute  
- Désactiver l’authentification par mot de passe  
- Interdire l’accès root  
- Restreindre les connexions à un utilisateur spécifique  
- Forcer l’utilisation des clés SSH  

## 🔧 Configuration  

### Modifications du fichier `/etc/ssh/sshd_config`  
```bash
sudo nano /etc/ssh/sshd_config
```
Modifications apportées :
```
# Changer le port d'écoute
Port 2222

# Désactiver l'accès root
PermitRootLogin no

# Désactiver l'authentification par mot de passe
PasswordAuthentication no

# Désactiver l'authentification par challenge
ChallengeResponseAuthentication no

# Forcer l'utilisation des clés SSH
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Limiter les connexions à un utilisateur spécifique
AllowUsers it4
```

### 🔥 Mise à jour du pare-feu  
Après modification du port SSH, il est essentiel de mettre à jour le pare-feu :
```bash
sudo firewall-cmd --permanent --remove-port=22/tcp
sudo firewall-cmd --permanent --add-port=2222/tcp
sudo firewall-cmd --reload
```

### 📌 Création et configuration de l’utilisateur SSH  
Création d’un utilisateur dédié avec un accès restreint via clé SSH :  
```bash
sudo useradd -m -s /bin/bash it4 
sudo mkdir -p /home/it4/.ssh 
sudo nano /home/it4/.ssh/authorized_keys
```
Ajout de la clé publique :
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIn29vGuYAyEcmwkSS4pmpgxjsVSgs5n/1qF2DfP0vBZ it4@nowhere
```
Modification des permissions :
```bash
sudo chown -R it4:it4 /home/it4/.ssh 
sudo chmod 700 /home/it4/.ssh
sudo chmod 600 /home/it4/.ssh/authorized_keys
```

### 🔄 Redémarrage du service SSH  
```bash
sudo systemctl restart sshd
sudo systemctl enable sshd
```

## 🔑 Génération et ajout d’une clé SSH  
Sur la machine cliente :
```bash
ssh-keygen -t ed25519 -C "it4@windows"
```
Ajout de la nouvelle clé publique au fichier `authorized_keys` :
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB3P8Cd7P1lwX3v+... it4@windows
```
