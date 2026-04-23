from config.database import Database


class Fournisseur:
    def __init__(self):
        self.db = Database.get_instance()

    def get_all(self):
        return self.db.query(
            "SELECT * FROM fournisseurs ORDER BY raison_sociale"
        )

    def get_by_id(self, id_fournisseur):
        result = self.db.query(
            "SELECT * FROM fournisseurs WHERE id_fournisseur = %s",
            (id_fournisseur,)
        )
        return result[0] if result else None

    def create(self, data):
        return self.db.execute(
            """INSERT INTO fournisseurs (raison_sociale, contact, telephone, email, adresse)
               VALUES (%s, %s, %s, %s, %s)""",
            (data['raison_sociale'], data['contact'], data['telephone'],
             data['email'], data['adresse'])
        )

    def update(self, id_fournisseur, data):
        return self.db.execute(
            """UPDATE fournisseurs SET raison_sociale=%s, contact=%s,
               telephone=%s, email=%s, adresse=%s WHERE id_fournisseur=%s""",
            (data['raison_sociale'], data['contact'], data['telephone'],
             data['email'], data['adresse'], id_fournisseur)
        )

    def delete(self, id_fournisseur):
        return self.db.execute(
            "DELETE FROM fournisseurs WHERE id_fournisseur = %s",
            (id_fournisseur,)
        )
