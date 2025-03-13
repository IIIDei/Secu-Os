# Part II : Observe

## Contexte

Dans cette partie, nous explorons l'observation des *syscalls* (appels système) exécutés par des programmes sous Linux. L'objectif est d'utiliser des outils comme `strace` et `sysdig` pour comprendre comment un programme interagit avec le noyau.

## Outils utilisés

- `strace` : permet de tracer les *syscalls* effectués par un processus en cours d'exécution.
- `sysdig` : outil plus moderne et puissant permettant une capture et une analyse avancées des *syscalls*.

## 1. Analyse avec `strace`

### Tracer l'exécution de `ls`

Nous avons utilisé `strace` pour tracer l'exécution de la commande `ls` dans un dossier contenant des fichiers.

Commande :
```bash
strace -e write ls test/
```

Résultat :
```bash
write(1, "a.c  b.c  c.c\n", 14a.c  b.c  c.c
) = 14
+++ exited with 0 +++
```

Le *syscall* `write` est utilisé pour afficher les résultats de `ls` dans le terminal.

---

### Tracer l'exécution de `cat`

Nous avons tracé l'exécution de `cat` sur un fichier contenant du texte.

Préparation du fichier :
```bash
echo "hello" > myfile.txt
```

Commande :
```bash
strace -e open,write cat myfile.txt
```

Résultat :
```bash
write(1, "hello\n", 6) = 6
+++ exited with 0 +++
```

- Le *syscall* `open` est utilisé pour ouvrir le fichier.
- Le *syscall* `write` est utilisé pour écrire le contenu du fichier dans le terminal.

---

### Tracer l'exécution de `curl example.org`

Nous avons tracé l'exécution de `curl` pour observer les *syscalls* effectués.

Commande :
```bash
strace -c curl example.org
```

Extrait des résultats :
```bash
% time     seconds  usecs/call     calls    errors syscall
25.65    0.007975          56       141           mmap
12.10    0.003762          78        48           fstat
11.26    0.003502          56        62        14 openat
11.15    0.003468          65        53           rt_sigaction
...
```

- `openat` permet d'ouvrir un fichier ou une ressource réseau.
- `mmap` est utilisé pour mapper des fichiers en mémoire.
- `fstat` récupère des informations sur un fichier.

---

## 2. Analyse avec `sysdig`

### Tracer `ls`

Commande :
```bash
sudo sysdig proc.name=ls and evt.type=write
```

Résultat :
```bash
ls (23072.23072) > write fd=1(<f>/dev/pts/1) size=114
ls (23072.23072) < write res=114 data=strace_cat.txt  strace_curl.txt  sysdig-0.39.0-x86_64.rpm
```

Le *syscall* `write` affiche les résultats dans le terminal.

---

### Tracer `cat`

Commande pour suivre l'écriture dans le terminal :
```bash
sudo sysdig proc.name=cat and evt.type=write
```

Résultat :
```bash
cat (23084.23084) > write fd=1(<f>/dev/pts/1) size=6
cat (23084.23084) < write res=6 data=hello.
```

Commande pour suivre l'ouverture du fichier :
```bash
sudo sysdig proc.name=cat and evt.type=openat
```

Résultat :
```bash
cat (23133.23133) > openat dirfd=-100(AT_FDCWD) name=myfile.txt flags=1(O_RDONLY) mode=0
cat (23133.23133) < openat fd=3(<f>/home/dei/myfile.txt) dirfd=-100(AT_FDCWD) name=myfile.txt flags=1(O_RDONLY) mode=0
```

Le *syscall* `openat` est utilisé pour ouvrir `myfile.txt`.

---

### Tracer tous les *syscalls* d'un utilisateur

Commande :
```bash
sudo sysdig user.name=dei
```

Cela affiche en temps réel tous les *syscalls* effectués par l'utilisateur `dei`.

---

### Capture des *syscalls* de `curl`

Commande pour enregistrer les *syscalls* dans un fichier :
```bash
sudo sysdig -w curl.scap proc.name=curl
```

Fichier généré : `curl.scap`, ajouté au dépôt Git.

--- 

📌 **Fichier joint** : `curl.scap` (capture des *syscalls* de `curl`).
