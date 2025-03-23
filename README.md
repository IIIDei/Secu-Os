# Secu OS

## Objectif du projet

- **Mise en place de services** sous Linux (gestion des utilisateurs, NFS, FTP, Ansible, etc.)  
- **Sécurisation des services** via des techniques de *service hardening* (filtrage de *syscalls* avec `seccomp`, configuration avancée de `systemd`, etc.)

---

## 🔹 Contenu

### 🧩 1 Linux-Basics – Configuration de base des services Linux

1. **Configuration des utilisateurs et groupes**  
   - Création et gestion des utilisateurs/groupes  
   - Définition des permissions et restrictions  

2. **Partage de fichiers avec NFS**  
   - Installation et configuration d'un serveur NFS  
   - Montage des répertoires clients  

3. **Automatisation avec Ansible**  
   - Déploiement automatisé des configurations  
   - Utilisation des playbooks Ansible  

4. **Sécurisation et gestion des accès**  
   - Paramétrage du pare-feu et des permissions  
   - Application des bonnes pratiques de sécurité  

5. **Mise en place d'un serveur FTP sécurisé**  
   - Installation et configuration de vsftpd  
   - Sécurisation avec TLS  
   - Test d'accès avec les utilisateurs  

---

### 🛡️ 2 Syscalls – Service Hardening et Seccomp

Objectif : appliquer des techniques de **service hardening** pour limiter les actions système qu'un programme peut exécuter (filtrage des *syscalls* via `seccomp`), et sécuriser une application vulnérable.

1. **Observation des syscalls système**  
   - Utilisation de `strace` pour tracer l'activité système d'un programme  
   - Observation en situation normale et sous exploitation  

2. **Application de `seccomp` via systemd**  
   - Limitation des *syscalls* autorisés dans un service  
   - Analyse et adaptation du fichier `.service` pour chaque cas  

3. **Cas pratique – sécurisation de NGINX**  
   - Installation et démarrage de NGINX  
   - Tracing de son activité  
   - Application d’un profil de filtrage *syscalls* via `systemd`  

4. **Cas pratique – sécurisation d’une application vulnérable**  
   - Utilisation d’une calculatrice TCP vulnérable (`calc.py`)  
   - Création d’un service `calculatrice.service`  
   - Exploitation de la vulnérabilité  
   - Application du hardening (droits, *syscalls*)  

Les fichiers de tracing et de service sont organisés dans les dossiers :  
- `observe_files/`  
- `service_hardening_files/`  
- `shitty_app_files/`

---

## 🔗 Références

- Documentation officielle :  
  - [vsftpd](https://security.appspot.com/vsftpd.html)  
  - [NFS](https://wiki.debian.org/NFS)  
  - [Ansible](https://docs.ansible.com/)  
  - [Systemd - Service Hardening](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)  
  - [strace](https://strace.io/)  
  - [seccomp](https://man7.org/linux/man-pages/man2/seccomp.2.html)
