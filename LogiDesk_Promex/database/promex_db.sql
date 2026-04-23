-- ============================================================
--  promex_db — Base de données Promex
--  BTS SIO SLAM — Épreuve E6 — Session 2026
--  Auteur : Kaveh Ostad
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- Création de la base
-- ------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS promex_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE promex_db;

-- ------------------------------------------------------------
-- Table : utilisateurs
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS utilisateurs (
  id_utilisateur INT          NOT NULL AUTO_INCREMENT,
  nom            VARCHAR(100) NOT NULL,
  prenom         VARCHAR(100) NOT NULL,
  email          VARCHAR(150) NOT NULL UNIQUE,
  mot_de_passe   VARCHAR(255) NOT NULL,
  role           ENUM('admin', 'commercial', 'acheteur') NOT NULL DEFAULT 'commercial',
  created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_utilisateur)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table : categories
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
  id_categorie INT          NOT NULL AUTO_INCREMENT,
  libelle      VARCHAR(100) NOT NULL,
  description  TEXT,
  PRIMARY KEY (id_categorie)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table : produits
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS produits (
  id_produit    INT            NOT NULL AUTO_INCREMENT,
  reference     VARCHAR(50)    NOT NULL UNIQUE,
  designation   VARCHAR(200)   NOT NULL,
  description   TEXT,
  prix_unitaire DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  stock_actuel  INT            NOT NULL DEFAULT 0,
  stock_minimum INT            NOT NULL DEFAULT 5,
  id_categorie  INT            NOT NULL,
  PRIMARY KEY (id_produit),
  CONSTRAINT fk_produit_categorie
    FOREIGN KEY (id_categorie) REFERENCES categories (id_categorie)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table : fournisseurs
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fournisseurs (
  id_fournisseur INT          NOT NULL AUTO_INCREMENT,
  raison_sociale VARCHAR(150) NOT NULL,
  contact        VARCHAR(100),
  telephone      VARCHAR(20),
  email          VARCHAR(150),
  adresse        TEXT,
  PRIMARY KEY (id_fournisseur)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table : commandes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS commandes (
  id_commande          INT         NOT NULL AUTO_INCREMENT,
  numero_commande      VARCHAR(50) NOT NULL UNIQUE,
  date_commande        DATE        NOT NULL,
  date_livraison_prevue DATE,
  statut               ENUM('en_cours', 'validee', 'livree', 'annulee') NOT NULL DEFAULT 'en_cours',
  id_fournisseur       INT         NOT NULL,
  id_utilisateur       INT         NOT NULL,
  PRIMARY KEY (id_commande),
  CONSTRAINT fk_commande_fournisseur
    FOREIGN KEY (id_fournisseur) REFERENCES fournisseurs (id_fournisseur)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_commande_utilisateur
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table : lignes_commande
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lignes_commande (
  id_ligne          INT            NOT NULL AUTO_INCREMENT,
  quantite_commandee INT           NOT NULL DEFAULT 1,
  prix_unitaire     DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  id_commande       INT            NOT NULL,
  id_produit        INT            NOT NULL,
  PRIMARY KEY (id_ligne),
  CONSTRAINT fk_ligne_commande
    FOREIGN KEY (id_commande) REFERENCES commandes (id_commande)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_ligne_produit
    FOREIGN KEY (id_produit) REFERENCES produits (id_produit)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Table : mouvements_stock
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mouvements_stock (
  id_mouvement   INT          NOT NULL AUTO_INCREMENT,
  type_mouvement ENUM('entree', 'sortie') NOT NULL,
  quantite       INT          NOT NULL,
  motif          TEXT,
  date_mouvement DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_produit     INT          NOT NULL,
  id_utilisateur INT          NOT NULL,
  PRIMARY KEY (id_mouvement),
  CONSTRAINT fk_mouvement_produit
    FOREIGN KEY (id_produit) REFERENCES produits (id_produit)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_mouvement_utilisateur
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs (id_utilisateur)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
--  DONNÉES DE TEST (jeux d'essai)
-- ============================================================

-- ------------------------------------------------------------
-- Utilisateurs
-- NB : mots de passe en clair — vulnérabilité volontaire v1
-- ------------------------------------------------------------
INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES
  ('Dupont',   'Marc',    'marc.dupont@promex.fr',    'admin123',  'admin'),
  ('Martin',   'Sophie',  'sophie.martin@promex.fr',  'user123',   'commercial'),
  ('Benali',   'Karim',   'karim.benali@promex.fr',   'user123',   'acheteur'),
  ('Leroy',    'Julie',   'julie.leroy@promex.fr',    'user123',   'commercial');

-- ------------------------------------------------------------
-- Catégories
-- ------------------------------------------------------------
INSERT INTO categories (libelle, description) VALUES
  ('Outillage',          'Outils manuels et électroportatifs'),
  ('Fournitures bureau', 'Papeterie, consommables, mobilier'),
  ('Équipements sécu',   'EPI, signalisation, protection individuelle'),
  ('Informatique',       'Matériel et périphériques informatiques');

-- ------------------------------------------------------------
-- Produits
-- ------------------------------------------------------------
INSERT INTO produits (reference, designation, description, prix_unitaire, stock_actuel, stock_minimum, id_categorie) VALUES
  ('OUT-001', 'Perceuse visseuse 18V',    'Perceuse sans fil avec 2 batteries',  89.90,  12,  5, 1),
  ('OUT-002', 'Marteau 500g',             'Marteau à tête acier forgée',          14.50,  30,  8, 1),
  ('OUT-003', 'Niveau laser croix',       'Portée 15m, précision ±0.3mm',         59.00,   8,  4, 1),
  ('BUR-001', 'Ramette papier A4 80g',    '500 feuilles blanc',                    4.90, 120, 20, 2),
  ('BUR-002', 'Stylos bille bleu x10',    'Boîte de 10 stylos',                    3.20,  85, 15, 2),
  ('BUR-003', 'Classeur A4 8cm',          'Classeur à levier dos 80mm',            5.80,  45, 10, 2),
  ('SEC-001', 'Casque chantier blanc',    'Conforme EN 397',                       12.00,  20,  6, 3),
  ('SEC-002', 'Gants protection T9',      'Gants anti-coupure niveau B',            8.50,  35, 10, 3),
  ('SEC-003', 'Gilet haute visibilité',   'Classe 2, taille unique',               6.90,  25,  8, 3),
  ('INF-001', 'Souris optique USB',       'Souris filaire 1000 DPI',              12.90,  18,  5, 4),
  ('INF-002', 'Clé USB 32Go',             'USB 3.0, lecture 80MB/s',               9.90,  40, 10, 4),
  ('INF-003', 'Câble RJ45 5m cat6',       'Câble réseau blindé',                   6.50,  22,  6, 4);

-- ------------------------------------------------------------
-- Fournisseurs
-- ------------------------------------------------------------
INSERT INTO fournisseurs (raison_sociale, contact, telephone, email, adresse) VALUES
  ('ToolPro Distribution', 'Jean Moreau',    '01 45 23 67 89', 'contact@toolpro.fr',   '12 rue de l\'Industrie, 75010 Paris'),
  ('BureauPlus',           'Anne Petit',     '01 38 92 45 11', 'commande@bureauplus.fr','5 avenue Foch, 92100 Boulogne'),
  ('SafeEquip',            'Pierre Lambert', '01 64 77 32 08', 'info@safeequip.fr',    '8 bd de la Sécurité, 94200 Ivry'),
  ('TechSupply',           'Lucie Bernard',  '01 55 43 21 90', 'vente@techsupply.fr',  '3 rue des Lilas, 93100 Montreuil');

-- ------------------------------------------------------------
-- Commandes
-- ------------------------------------------------------------
INSERT INTO commandes (numero_commande, date_commande, date_livraison_prevue, statut, id_fournisseur, id_utilisateur) VALUES
  ('CMD-2025-001', '2025-11-03', '2025-11-10', 'livree',   1, 3),
  ('CMD-2025-002', '2025-11-15', '2025-11-25', 'livree',   2, 3),
  ('CMD-2025-003', '2025-12-01', '2025-12-10', 'validee',  3, 3),
  ('CMD-2026-001', '2026-01-08', '2026-01-20', 'en_cours', 1, 3),
  ('CMD-2026-002', '2026-01-15', '2026-01-28', 'en_cours', 4, 3);

-- ------------------------------------------------------------
-- Lignes de commande
-- ------------------------------------------------------------
INSERT INTO lignes_commande (quantite_commandee, prix_unitaire, id_commande, id_produit) VALUES
  -- CMD-2025-001 (ToolPro)
  (10, 89.90, 1, 1),
  (20, 14.50, 1, 2),
  -- CMD-2025-002 (BureauPlus)
  (50,  4.90, 2, 4),
  (30,  3.20, 2, 5),
  (20,  5.80, 2, 6),
  -- CMD-2025-003 (SafeEquip)
  (15, 12.00, 3, 7),
  (20,  8.50, 3, 8),
  -- CMD-2026-001 (ToolPro)
  (5,  59.00, 4, 3),
  (10, 14.50, 4, 2),
  -- CMD-2026-002 (TechSupply)
  (10, 12.90, 5, 10),
  (20,  9.90, 5, 11),
  (10,  6.50, 5, 12);

-- ------------------------------------------------------------
-- Mouvements de stock
-- ------------------------------------------------------------
INSERT INTO mouvements_stock (type_mouvement, quantite, motif, date_mouvement, id_produit, id_utilisateur) VALUES
  ('entree', 10, 'Réception commande CMD-2025-001', '2025-11-10 09:30:00', 1,  3),
  ('entree', 20, 'Réception commande CMD-2025-001', '2025-11-10 09:30:00', 2,  3),
  ('sortie',  3, 'Livraison client chantier Lyon',  '2025-11-12 14:00:00', 1,  2),
  ('entree', 50, 'Réception commande CMD-2025-002', '2025-11-25 10:00:00', 4,  3),
  ('sortie', 15, 'Consommation interne bureau',     '2025-11-28 11:30:00', 4,  2),
  ('entree', 30, 'Réception commande CMD-2025-002', '2025-11-25 10:00:00', 5,  3),
  ('entree', 15, 'Réception commande CMD-2025-003', '2025-12-10 08:45:00', 7,  3),
  ('sortie',  5, 'Distribution équipe terrain',     '2025-12-12 09:00:00', 7,  2),
  ('entree', 20, 'Réception commande CMD-2025-003', '2025-12-10 08:45:00', 8,  3),
  ('sortie',  8, 'Distribution équipe sécurité',    '2026-01-05 10:15:00', 8,  2);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- Vérification rapide
-- ============================================================
-- SELECT 'utilisateurs'    AS table_name, COUNT(*) AS nb FROM utilisateurs
-- UNION SELECT 'categories',     COUNT(*) FROM categories
-- UNION SELECT 'produits',       COUNT(*) FROM produits
-- UNION SELECT 'fournisseurs',   COUNT(*) FROM fournisseurs
-- UNION SELECT 'commandes',      COUNT(*) FROM commandes
-- UNION SELECT 'lignes_commande',COUNT(*) FROM lignes_commande
-- UNION SELECT 'mouvements_stock',COUNT(*) FROM mouvements_stock;
