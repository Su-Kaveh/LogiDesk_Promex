from config.database import Database


class Commande:
    def __init__(self):
        self.db = Database.get_instance()

    def get_all(self):
        return self.db.query("""
            SELECT c.*, f.raison_sociale AS fournisseur,
                   u.nom AS utilisateur_nom, u.prenom AS utilisateur_prenom
            FROM commandes c
            LEFT JOIN fournisseurs f ON c.id_fournisseur = f.id_fournisseur
            LEFT JOIN utilisateurs u ON c.id_utilisateur = u.id_utilisateur
            ORDER BY c.date_commande DESC
        """)

    def get_by_id(self, id_commande):
        result = self.db.query("""
            SELECT c.*, f.raison_sociale AS fournisseur,
                   u.nom AS utilisateur_nom, u.prenom AS utilisateur_prenom
            FROM commandes c
            LEFT JOIN fournisseurs f ON c.id_fournisseur = f.id_fournisseur
            LEFT JOIN utilisateurs u ON c.id_utilisateur = u.id_utilisateur
            WHERE c.id_commande = %s
        """, (id_commande,))
        return result[0] if result else None

    def create(self, data):
        return self.db.execute("""
            INSERT INTO commandes
            (numero_commande, date_commande, date_livraison_prevue, statut, id_fournisseur, id_utilisateur)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['numero_commande'], data['date_commande'], data['date_livraison_prevue'],
              data['statut'], data['id_fournisseur'], data['id_utilisateur']))

    def update_statut(self, id_commande, statut):
        return self.db.execute(
            "UPDATE commandes SET statut = %s WHERE id_commande = %s",
            (statut, id_commande)
        )

    def delete(self, id_commande):
        return self.db.execute(
            "DELETE FROM commandes WHERE id_commande = %s",
            (id_commande,)
        )

    def get_last_numero(self):
        result = self.db.query(
            "SELECT numero_commande FROM commandes ORDER BY id_commande DESC LIMIT 1"
        )
        if result:
            last = result[0]['numero_commande']
            year = last.split('-')[1]
            num  = int(last.split('-')[2]) + 1
            return f"CMD-{year}-{num:03d}"
        from datetime import date
        return f"CMD-{date.today().year}-001"
