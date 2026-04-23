from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
import os


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("LogiDesk — Promex")
        self.setMinimumSize(900, 600)
        self.resize(1280, 720)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #1a5276;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo dans sidebar
        logo_frame = QFrame()
        logo_frame.setStyleSheet("background-color: #154360; padding: 16px 0px;")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(16, 16, 16, 16)
        logo_layout.setSpacing(4)

        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("LogiDesk")
            logo_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        app_name = QLabel("LogiDesk")
        app_name.setAlignment(Qt.AlignCenter)
        app_name.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        logo_layout.addWidget(app_name)

        company = QLabel("Promex")
        company.setAlignment(Qt.AlignCenter)
        company.setStyleSheet("color: #85c1e9; font-size: 12px; padding: 0 8px;")
        logo_layout.addWidget(company)

        sidebar_layout.addWidget(logo_frame)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #2e86c1;")
        sidebar_layout.addWidget(sep)

        # Boutons navigation
        nav_items = [
            ("🏠  Tableau de bord", "dashboard"),
            ("📋  Commandes",       "commandes"),
            ("🏭  Fournisseurs",    "fournisseurs"),
        ]
        if self.user['role'] == 'admin':
            nav_items.append(("👥  Utilisateurs", "utilisateurs"))

        self.nav_buttons = {}
        self.stack = QStackedWidget()

        for label, key in nav_items:
            btn = QPushButton(label)
            btn.setFixedHeight(46)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setStyleSheet(self._nav_btn_style())
            btn.clicked.connect(lambda checked, k=key: self._navigate(k))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn

        sidebar_layout.addStretch()

        # Infos utilisateur en bas de sidebar
        user_frame = QFrame()
        user_frame.setStyleSheet("background-color: #154360; padding: 10px;")
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(12, 10, 12, 10)
        user_layout.setSpacing(2)

        nom_complet = QLabel(f"{self.user['prenom']} {self.user['nom']}")
        nom_complet.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        user_layout.addWidget(nom_complet)

        role_label = QLabel(self.user['role'].capitalize())
        role_label.setStyleSheet("color: #85c1e9; font-size: 12px; padding: 0 8px;")
        user_layout.addWidget(role_label)

        btn_deconnexion = QPushButton("Déconnexion")
        btn_deconnexion.setFixedHeight(32)
        btn_deconnexion.setCursor(Qt.PointingHandCursor)
        btn_deconnexion.setStyleSheet("""
            QPushButton {
                background-color: #0e2f44;
                color: #aed6f1;
                border: 1px solid #2e86c1;
                border-radius: 4px;
                font-size: 12px; padding: 0 8px;
                margin-top: 6px;
            }
            QPushButton:hover { background: #1a5276; color: white; }
        """)
        btn_deconnexion.clicked.connect(self._deconnecter)
        user_layout.addWidget(btn_deconnexion)
        sidebar_layout.addWidget(user_frame)

        # ── Zone contenu ──
        content_area = QFrame()
        content_area.setStyleSheet("background-color: #f0f4f8;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Barre titre contenu
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(52)
        self.title_bar.setStyleSheet("""
            background: white;
            border-bottom: 1px solid #dee2e6;
        """)
        title_bar_layout = QHBoxLayout(self.title_bar)
        title_bar_layout.setContentsMargins(24, 0, 24, 0)
        self.title_label = QLabel("Tableau de bord")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1a5276;")
        title_bar_layout.addWidget(self.title_label)
        content_layout.addWidget(self.title_bar)

        # Pages (StackedWidget)
        self._init_pages()
        content_layout.addWidget(self.stack)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)

        # Activer dashboard par défaut
        self._navigate("dashboard")

    def _init_pages(self):
        from views.dashboard_page import DashboardPage
        from views.commandes_page import CommandesPage
        from views.fournisseurs_page import FournisseursPage
        from views.utilisateurs_page import UtilisateursPage

        self.pages = {
            "dashboard":    DashboardPage(self.user),
            "commandes":    CommandesPage(self.user),
            "fournisseurs": FournisseursPage(self.user),
            "utilisateurs": UtilisateursPage(self.user),
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

    def _navigate(self, key):
        titles = {
            "dashboard":    "Tableau de bord",
            "commandes":    "Commandes fournisseurs",
            "fournisseurs": "Fournisseurs",
            "utilisateurs": "Utilisateurs",
        }
        # Décocher tous les boutons
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == key)

        self.title_label.setText(titles.get(key, ""))
        self.stack.setCurrentWidget(self.pages[key])

        # Rafraîchir la page
        if hasattr(self.pages[key], 'refresh'):
            self.pages[key].refresh()

    def _deconnecter(self):
        from views.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def _nav_btn_style(self):
        return """
            QPushButton {
                background-color: #0e2f44;
                color: #aed6f1;
                text-align: left;
                padding-left: 20px;
                font-size: 13px;
                border: none;
                border-left: 3px solid transparent;
            }
            QPushButton:hover {
                background-color: #154360;
                color: white;
            }
            QPushButton:checked {
                background-color: #154360;
                color: white;
                border-left: 3px solid #5dade2;
            }
        """
