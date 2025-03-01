# TP Filtrage des paquets - Partie 1

## 🔥 Configuration restrictive de firewalld

Nous avons mis en place une configuration restrictive du pare-feu avec les règles suivantes :
- Seuls les ports utiles sont ouverts.
- Seul le réseau `10.1.1.0/24` est autorisé en entrée.
- Le service SSH a été retiré et remplacé par l'ouverture explicite du port `22/tcp`.

### 🔎 Vérification de la configuration avec `firewall-cmd`

Commande exécutée :

```bash
sudo firewall-cmd --list-all
```

Résultat obtenu :

```
target: default
icmp-block-inversion: no
interfaces: enp0s3 enp0s8
sources:
services: cockpit dhcpv6-client ftp
ports: 22/tcp
protocols:
forward: yes
masquerade: no
forward-ports:
source-ports:
icmp-blocks:
rich rules:
```

### ✅ Analyse des résultats

- **Interfaces actives** : `enp0s3` et `enp0s8`.
- **Services autorisés** : `cockpit`, `dhcpv6-client`, `ftp` (si cela ne correspond pas aux attentes, il faudra ajuster).
- **Ports ouverts** : `22/tcp` est bien autorisé.
- **Masquerade désactivé** : Aucun NAT n'est activé.  
