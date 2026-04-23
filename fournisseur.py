from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from models.utilisateur import Utilisateur
import os


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.utilisateur_model = Utilisateur()
        self.setWindowTitle("LogiDesk — Promex")
        self.setFixedSize(420, 520)
        self.setStyleSheet("QWidget { background-color: #f0f4f8; font-family: Arial; }")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(0)

        # Card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                border: 1px solid #dee2e6;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 28, 32, 28)
        card_layout.setSpacing(12)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("LogiDesk")
            logo_label.setFont(QFont("Arial", 20, QFont.Bold))
            logo_label.setStyleSheet("color: #1a5276;")
        logo_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(logo_label)

        # Sous-titre
        subtitle = QLabel("Gestion des commandes fournisseurs")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6c757d; font-size: 12px; margin-bottom: 4px; background: transparent; border: none;")
        card_layout.addWidget(subtitle)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #dee2e6; border: none; max-height: 1px;")
        card_layout.addWidget(sep)

        # Label erreur
        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("""
            color: #842029;
            background: #f8d7da;
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 12px;
            border: none;
        """)
        self.label_erreur.setAlignment(Qt.AlignCenter)
        self.label_erreur.setWordWrap(True)
        self.label_erreur.hide()
        card_layout.addWidget(self.label_erreur)

        # Email
        lbl_email = QLabel("Email")
        lbl_email.setStyleSheet("font-weight: bold; font-size: 13px; color: #212529; background: transparent; border: none;")
        card_layout.addWidget(lbl_email)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("prenom.nom@promex.fr")
        self.input_email.setFixedHeight(36)
        self.input_email.setStyleSheet(self._input_style())
        card_layout.addWidget(self.input_email)

        # Mot de passe
        lbl_mdp = QLabel("Mot de passe")
        lbl_mdp.setStyleSheet("font-weight: bold; font-size: 13px; color: #212529; background: transparent; border: none;")
        card_layout.addWidget(lbl_mdp)

        self.input_mdp = QLineEdit()
        self.input_mdp.setEchoMode(QLineEdit.Password)
        self.input_mdp.setPlaceholderText("••••••••")
        self.input_mdp.setFixedHeight(36)
        self.input_mdp.setStyleSheet(self._input_style())
        self.input_mdp.returnPressed.connect(self._se_connecter)
        card_layout.addWidget(self.input_mdp)

        # Bouton connexion
        btn = QPushButton("Se connecter")
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1a5276;
                color: white;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover { background-color: #154360; }
            QPushButton:pressed { background-color: #0e2f44; }
        """)
        btn.clicked.connect(self._se_connecter)
        card_layout.addWidget(btn)

        layout.addWidget(card)

        # Footer
        footer = QLabel("Promex © 2026 — BTS SIO SLAM")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #adb5bd; font-size: 11px; margin-top: 10px; background: transparent; border: none;")
        layout.addWidget(footer)

    def _input_style(self):
        return """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 4px 10px;
                font-size: 13px;
                background: white;
                color: #212529;
            }
            QLineEdit:focus {
                border: 1px solid #1a5276;
            }
        """

    def _se_connecter(self):
        email = self.input_email.text().strip()
        mdp   = self.input_mdp.text().strip()

        if not email or not mdp:
            self._afficher_erreur("Veuillez remplir tous les champs.")
            return

        user = self.utilisateur_model.authentifier(email, mdp)
        if user:
            self.label_erreur.hide()
            self._ouvrir_main(user)
        else:
            self._afficher_erreur("Email ou mot de passe incorrect.")
            self.input_mdp.clear()

    def _afficher_erreur(self, message):
        self.label_erreur.setText(message)
        self.label_erreur.show()

    def _ouvrir_main(self, user):
        from views.main_window import MainWindow
        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()
