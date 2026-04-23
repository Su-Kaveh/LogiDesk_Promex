import mysql.connector
from mysql.connector import Error


class Database:
    _instance = None

    def __init__(self):
        try:
            self.connexion = mysql.connector.connect(
                host='localhost',
                database='promex_db',
                user='root',
                password=''
            )
        except Error as e:
            raise Exception(f"Erreur de connexion à la base de données : {e}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None or not cls._instance.connexion.is_connected():
            cls._instance = Database()
        return cls._instance

    def get_connexion(self):
        return self.connexion

    def query(self, sql, params=None):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute(self, sql, params=None):
        cursor = self.connexion.cursor()
        cursor.execute(sql, params or ())
        self.connexion.commit()
        cursor.close()
        return True
