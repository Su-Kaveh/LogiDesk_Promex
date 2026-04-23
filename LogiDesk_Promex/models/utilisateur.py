from config.database import Database


class Utilisateur:
    def __init__(self):
        self.db = Database.get_instance()

    def authentifier(self, email, mot_de_passe):
        # VULNERABILITE CONNUE : mot de passe en clair (à corriger avec bcrypt)
        result = self.db.query(
            "SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s",
            (email, mot_de_passe)
        )
        return result[0] if result else None

    def get_all(self):
        return self.db.query(
            "SELECT * FROM utilisateurs ORDER BY nom, prenom"
        )

    def get_by_id(self, id_utilisateur):
        result = self.db.query(
            "SELECT * FROM utilisateurs WHERE id_utilisateur = %s",
            (id_utilisateur,)
        )
        return result[0] if result else None

    def create(self, data):
        return self.db.execute(
            "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s)",
            (data['nom'], data['prenom'], data['email'], data['mot_de_passe'], data['role'])
        )

    def update(self, id_utilisateur, data):
        return self.db.execute(
            "UPDATE utilisateurs SET nom=%s, prenom=%s, email=%s, role=%s WHERE id_utilisateur=%s",
            (data['nom'], data['prenom'], data['email'], data['role'], id_utilisateur)
        )

    def delete(self, id_utilisateur):
        return self.db.execute(
            "DELETE FROM utilisateurs WHERE id_utilisateur = %s",
            (id_utilisateur,)
        )

    def email_existe(self, email, exclude_id=None):
        if exclude_id:
            result = self.db.query(
                "SELECT id_utilisateur FROM utilisateurs WHERE email = %s AND id_utilisateur != %s",
                (email, exclude_id)
            )
        else:
            result = self.db.query(
                "SELECT id_utilisateur FROM utilisateurs WHERE email = %s",
                (email,)
            )
        return len(result) > 0
