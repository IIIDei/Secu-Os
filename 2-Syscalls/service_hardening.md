# Syscalls - Part III : Service Hardening

## **1. Objectif**
Dans cette partie, l'objectif est de mettre en place un filtrage des appels système (*syscalls*) grâce à **seccomp** afin de durcir la sécurité d'un service. Nous utiliserons **NGINX** comme exemple et appliquerons une politique de **moindre privilège** en limitant les appels système autorisés.

## **2. Contexte**
- Chaque programme interagit avec le système via des *syscalls* (ex: lecture/écriture de fichiers, exécution de processus, accès réseau, etc.).
- Un programme ne devrait avoir accès qu'aux *syscalls* strictement nécessaires à son fonctionnement.
- **seccomp** permet de filtrer les appels système qu'un processus peut effectuer.
- **systemd** permet d'appliquer un profil `seccomp` à un service via la directive `SystemCallFilter=`.

## **3. Installation et lancement de NGINX**

### **Installation de NGINX**
```bash
sudo dnf install nginx -y
```

### **Démarrage et vérification du service**
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### **Ouverture du port 80 (si nécessaire)**
```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
```

### **Vérification en accédant à la page Web**
- Ouvrir un navigateur et aller sur `http://localhost`
- Si le serveur fonctionne, la page par défaut d'NGINX s'affiche.

### **Arrêt du service pour le tracing**
```bash
sudo systemctl stop nginx
```

## **4. Tracing de NGINX**

### **Utilisation de `strace` pour capturer les syscalls**
```bash
sudo strace -f -o strace_nginx.txt -e trace=all /usr/sbin/nginx
```

### **Utilisation de `sysdig` pour capturer les syscalls**
```bash
sudo sysdig -w nginx.scap proc.name=nginx
```

### **Liste des syscalls observés**
D'après les traces obtenues, les *syscalls* suivants sont essentiels au bon fonctionnement d'NGINX :
- `execve`
- `setgid`, `setuid`
- `unlink`, `unlinkat`
- `ptrace` (peut être désactivé car lié au debugging)

## **5. Durcissement d'NGINX avec `seccomp`**

### **Modification du fichier de service**
Le fichier `nginx.service` a été modifié pour inclure un filtrage des *syscalls*.

#### **Fichier modifié : `/etc/systemd/system/nginx.service`**
```ini
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/bin/rm -f /run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/usr/sbin/nginx -s reload
KillSignal=SIGQUIT
TimeoutStopSec=5
KillMode=mixed
PrivateTmp=true

# Appliquer le filtrage seccomp
SystemCallAllow=unlink unlinkat execve setgid setuid
SystemCallFilter=~ptrace

[Install]
WantedBy=multi-user.target
```

### **Redémarrage du service avec les nouvelles règles**
```bash
sudo systemctl daemon-reload
sudo systemctl restart nginx
```

### **Vérification du bon fonctionnement**
```bash
sudo systemctl status nginx
```



---

### **📌 Fichiers**
- `nginx.service` : fichier de configuration modifié avec les règles `seccomp`
- `strace_nginx.txt` et `nginx.scap` : fichiers contenant les traces des syscalls
