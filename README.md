# LogiDesk - Promex
 
> Situation Professionnelle 2 - Client lourd / Épreuve E6 BTS SIO SLAM - Session 2026
 
Application desktop de gestion des commandes fournisseurs développée pour **Promex**, PME de distribution de matériel professionnel basée à Villejuif (94).
 
---
 
## Contexte
 
Le service achat de Promex gérait ses commandes fournisseurs via des fichiers Excel, sans suivi structuré ni historique fiable. LogiDesk centralise la gestion des commandes dans une application desktop installée sur les postes du service achat, s'appuyant sur la même base de données que WebStock (SP1) pour garantir la cohérence des données.
 
---
 
## Stack technique
 
| Élément | Détail |
|---|---|
| **Langage** | Python 3.12 |
| **Framework GUI** | PySide6 |
| **Base de données** | MySQL 8.0 |
| **Connecteur BDD** | mysql-connector-python |
| **IDE** | VS Code / PyCharm |
| **Versioning** | Git / GitHub |
 
---
 
## Fonctionnalités
 
- Authentification avec gestion des rôles (Acheteur / Administrateur)
- CRUD complet sur les fournisseurs
- Création et suivi des commandes fournisseurs
- Gestion des lignes de commande (ajout / suppression)
- Modification du statut d'une commande (En cours / Validée / Livrée)
- Gestion des utilisateurs réservée à l'administrateur
 
---

 
### Dépendances
 
```
PySide6>=6.6.0
mysql-connector-python>=8.3.0
```
 
---
 
## Comptes de test
 
| Rôle | Email | Mot de passe |
|---|---|---|
| Administrateur | admin@promex.fr | admin123 |
| Acheteur | acheteur@promex.fr | user123 |
 
---
 
## Base de données
 
LogiDesk utilise la base **promex_db**, partagée avec WebStock (Situation Pro 1).
 
| Table | Description |
|---|---|
| `utilisateurs` | Comptes et rôles |
| `fournisseurs` | Référentiel fournisseurs |
| `commandes` | En-têtes de commandes fournisseurs |
| `lignes_commande` | Détail des lignes par commande |
 
> Les tables `categories`, `produits` et `mouvements_stock` sont présentes dans promex_db mais gérées par WebStock (SP1).
 
---
 
## Architecture
 
Le projet suit le mod_le **MVC** adapté à PySide6 :
 
- **Modèles** : classes Python gérant l'accès aux données via mysql-connector-python
- **Vues** : classes PySide6 (QWidget, QMainWindow, QDialog) gérant l'interface graphique
- **Contrôleurs** : logique métier entre les modèles et les vues
- **Database** : classe Singleton assurant une instance unique de connexion MySQL
- **Signaux / Slots** : mécanisme PySide6 pour la communication entre composants
 
 
## Projet associé
 
| Situation | Repo | Description |
|---|---|---|
| SP1 | [WebStock_Promex](https://github.com/Su-Kaveh/WebStock_Promex) | Client léger — Gestion des stocks (PHP / MySQL) |
 
---
