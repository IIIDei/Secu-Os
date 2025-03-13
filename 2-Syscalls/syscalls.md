# Syscalls - Part I : Learn

## Introduction
Dans cette partie, nous allons explorer les concepts fondamentaux liés aux programmes et aux appels système (*syscalls*). Un programme est un fichier exécutable, qui interagit avec le système via des appels système fournis par le noyau.

Nous utiliserons plusieurs outils pour analyser ces programmes et observer les *syscalls* qu'ils utilisent.

## 1. Anatomy of a program

### A. `file`
La commande `file` permet de déterminer le type d'un fichier. Voici les résultats pour différents fichiers :

```bash
file /bin/ls
```
```
/bin/ls: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=1afdd52081d4b8b631f2986e26e69e0b275e159c, for GNU/Linux 3.2.0, stripped
```

```bash
file /usr/sbin/ip
```
```
/usr/sbin/ip: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=77a2f5899f0529f27d87bb29c6b84c535739e1c7, for GNU/Linux 3.2.0, stripped
```

```bash
wget -O test.mp3 https://samplelib.com/lib/preview/mp3/sample-3s.mp3
file test.mp3
```
```
test.mp3: Audio file with ID3 version 2.4.0, contains:MPEG ADTS, layer III, v1, 64 kbps, 44.1 kHz, Stereo
```

### B. `readelf`
La commande `readelf` permet d'obtenir des informations sur les fichiers ELF.

#### **Affichage du header ELF de `ls`**
```bash
readelf -h /bin/ls
```
```
Entry point address:               0x6b10
```

#### **Affichage des sections ELF de `ls`**
```bash
readelf -S /bin/ls
```
```
[15] .text PROGBITS 0000000000004d50 00004d50
```
La section `.text` commence à l'adresse `0x4d50`.

### C. `ldd`
La commande `ldd` permet d'afficher les bibliothèques dynamiques qu'un programme utilise.

```bash
ldd /bin/ls
```
```
linux-vdso.so.1 (0x00007ffed5198000)
libselinux.so.1 => /lib64/libselinux.so.1 (0x00007ff6dd2e3000)
libcap.so.2 => /lib64/libcap.so.2 (0x00007ff6dd2d9000)
libc.so.6 => /lib64/libc.so.6 (0x00007ff6dd000000)
libpcre2-8.so.0 => /lib64/libpcre2-8.so.0 (0x00007ff6dd23d000)
/lib64/ld-linux-x86-64.so.2 (0x00007ff6dd33a000)
```
La Glibc utilisée est : **`libc.so.6`**

## 2. Syscalls basics

### A. Syscall list
Un *syscall* est une fonction appelée par un programme pour interagir avec le noyau Linux. Vous pouvez trouver la liste complète des *syscalls* sur [cette table](https://filippo.io/linux-syscall-table/).

Voici quelques *syscalls* utiles :

| %rax | Name | Manual | Entry point |
| --- | --- | --- | --- |
| 0 | read | [read(2)](https://manpages.debian.org/unstable/manpages-dev/read.2.en.html) | [sys_read](https://github.com/search?q=repo%3Atorvalds%2Flinux+%2FSYSCALL_DEFINE%5B%5E%2C%5D*%5Cbread%5Cb%2F&type=code) |
| 1 | write | [write(2)](https://manpages.debian.org/unstable/manpages-dev/write.2.en.html) | [sys_write](https://github.com/search?q=repo%3Atorvalds%2Flinux+%2FSYSCALL_DEFINE%5B%5E%2C%5D*%5Cbwrite%5Cb%2F&type=code) |
| 59 | execve | [execve(2)](https://manpages.debian.org/unstable/manpages-dev/execve.2.en.html) | [sys_execve](https://github.com/search?q=repo%3Atorvalds%2Flinux+%2FSYSCALL_DEFINE%5B%5E%2C%5D*%5Cbexecve%5Cb%2F&type=code) |

### B. `objdump`
La commande `objdump` permet de désassembler un programme et voir son code en assembleur.

#### **Recherche des appels `call` dans `ls`**
```bash
objdump -d /bin/ls | grep 'call'
```
```
4014:       ff d0                   callq  *%rax
4d51:       e8 da f9 ff ff          callq  4730 abort@plt
4e4b:       e8 20 fa ff ff          callq  4870 bindtextdomain@plt
```

#### **Recherche des *syscalls* dans `ls`**
```bash
objdump -d /bin/ls | grep 'syscall'
```
```
(Aucun *syscall* direct dans `ls` car ils sont effectués via la Glibc)
```

#### **Recherche des *syscalls* dans la Glibc**
```bash
objdump -d /lib64/libc.so.6 | grep 'syscall'
```
```
295f4:       0f 05                   syscall
3e969:       0f 05                   syscall
423f5:       0f 05                   syscall
```

#### **Recherche du *syscall* `close()` dans la Glibc**
```bash
objdump -d /lib64/libc.so.6 | grep -B 10 '0f 05' | grep 'close'
```
```
00000000000fe220 <__close>:
fe22e:       75 10                   jne    fe240 <__close+0x20>
```

