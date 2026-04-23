from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from models.commande import Commande
from models.fournisseur import Fournisseur


class DashboardPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.commande_model   = Commande()
        self.fournisseur_model = Fournisseur()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Cartes stats
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.card_commandes   = self._make_card("Commandes", "0", "#1a5276")
        self.card_fournisseurs = self._make_card("Fournisseurs", "0", "#117a65")
        self.card_en_cours    = self._make_card("En cours", "0", "#b7950b")
        self.card_livrees     = self._make_card("Livrées", "0", "#1e8449")

        cards_layout.addWidget(self.card_commandes[0])
        cards_layout.addWidget(self.card_fournisseurs[0])
        cards_layout.addWidget(self.card_en_cours[0])
        cards_layout.addWidget(self.card_livrees[0])
        layout.addLayout(cards_layout)

        # Tableau dernières commandes
        title = QLabel("Dernières commandes")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #1a5276;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["N° Commande", "Fournisseur", "Date", "Livraison prévue", "Statut"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget { background: white; border: 1px solid #dee2e6; border-radius: 6px; gridline-color: #dee2e6; }
            QHeaderView::section { background: #1a5276; color: white; font-weight: bold; padding: 6px; border: none; border-right: 1px solid #2e86c1; }
            QTableWidget::item { color: #212529; background: white; }
            QTableWidget::item:alternate { background: #f8f9fa; color: #212529; }
            QTableWidget::item:selected { background: #d6eaf8; color: #1a5276; }
        """)
        layout.addWidget(self.table)

    def _make_card(self, titre, valeur, couleur):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 8px;
                border-left: 4px solid {couleur};
                border-top: 1px solid #dee2e6;
                border-right: 1px solid #dee2e6;
                border-bottom: 1px solid #dee2e6;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(4)

        lbl_titre = QLabel(titre)
        lbl_titre.setStyleSheet("color: #6c757d; font-size: 12px;")

        lbl_valeur = QLabel(valeur)
        lbl_valeur.setStyleSheet(f"color: {couleur}; font-size: 28px; font-weight: bold;")

        card_layout.addWidget(lbl_titre)
        card_layout.addWidget(lbl_valeur)
        return card, lbl_valeur

    def refresh(self):
        commandes    = self.commande_model.get_all()
        fournisseurs = self.fournisseur_model.get_all()

        en_cours = [c for c in commandes if c['statut'] == 'en_cours']
        livrees  = [c for c in commandes if c['statut'] == 'livree']

        self.card_commandes[1].setText(str(len(commandes)))
        self.card_fournisseurs[1].setText(str(len(fournisseurs)))
        self.card_en_cours[1].setText(str(len(en_cours)))
        self.card_livrees[1].setText(str(len(livrees)))

        # Tableau 10 dernières
        dernieres = commandes[:10]
        self.table.setRowCount(len(dernieres))

        statut_labels = {
            'en_cours': 'En cours',
            'validee':  'Validée',
            'livree':   'Livrée',
            'annulee':  'Annulée',
        }
        statut_colors = {
            'en_cours': '#fff3cd',
            'validee':  '#d1e7dd',
            'livree':   '#d1e7dd',
            'annulee':  '#f8d7da',
        }

        for row, c in enumerate(dernieres):
            self.table.setItem(row, 0, QTableWidgetItem(c['numero_commande']))
            self.table.setItem(row, 1, QTableWidgetItem(c['fournisseur'] or ''))
            self.table.setItem(row, 2, QTableWidgetItem(str(c['date_commande'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(c['date_livraison_prevue'] or '—')))

            statut_item = QTableWidgetItem(statut_labels.get(c['statut'], c['statut']))
            statut_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, statut_item)
