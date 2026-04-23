from config.database import Database


class LigneCommande:
    def __init__(self):
        self.db = Database.get_instance()

    def get_by_commande(self, id_commande):
        return self.db.query("""
            SELECT lc.*, p.designation AS produit, p.reference
            FROM lignes_commande lc
            LEFT JOIN produits p ON lc.id_produit = p.id_produit
            WHERE lc.id_commande = %s
            ORDER BY lc.id_ligne
        """, (id_commande,))

    def create(self, data):
        return self.db.execute("""
            INSERT INTO lignes_commande (quantite_commandee, prix_unitaire, id_commande, id_produit)
            VALUES (%s, %s, %s, %s)
        """, (data['quantite_commandee'], data['prix_unitaire'],
              data['id_commande'], data['id_produit']))

    def delete(self, id_ligne):
        return self.db.execute(
            "DELETE FROM lignes_commande WHERE id_ligne = %s",
            (id_ligne,)
        )
