from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QLabel, QDateEdit,
    QSplitter, QGroupBox, QSpinBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt, QDate
from models.commande import Commande
from models.fournisseur import Fournisseur
from models.ligne_commande import LigneCommande
from config.database import Database


class CommandesPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.commande_model    = Commande()
        self.fournisseur_model = Fournisseur()
        self.ligne_model       = LigneCommande()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Barre actions
        bar = QHBoxLayout()
        btn_nouveau = QPushButton("+ Nouvelle commande")
        btn_nouveau.setFixedHeight(34)
        btn_nouveau.setCursor(Qt.PointingHandCursor)
        btn_nouveau.setStyleSheet("""
            QPushButton { background: #1a5276; color: white; border-radius: 5px; padding: 0 16px; font-size: 13px; border: none; }
            QPushButton:hover { background: #154360; }
        """)
        btn_nouveau.clicked.connect(self._nouvelle_commande)
        bar.addWidget(btn_nouveau)
        bar.addStretch()
        layout.addLayout(bar)

        # Splitter : liste commandes + détail lignes
        splitter = QSplitter(Qt.Vertical)

        # Tableau commandes
        self.table_commandes = QTableWidget()
        self.table_commandes.setColumnCount(7)
        self.table_commandes.setHorizontalHeaderLabels([
            "N° Commande", "Fournisseur", "Date", "Livraison prévue", "Statut", "Passée par", "Actions"
        ])
        self.table_commandes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_commandes.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.table_commandes.setColumnWidth(6, 160)
        self.table_commandes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_commandes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_commandes.setAlternatingRowColors(True)
        self.table_commandes.verticalHeader().setVisible(False)
        self.table_commandes.clicked.connect(self._afficher_lignes)
        self.table_commandes.setStyleSheet(self._table_style())
        splitter.addWidget(self.table_commandes)

        # Tableau lignes de commande
        group_lignes = QGroupBox("Lignes de commande")
        group_lignes.setStyleSheet("QGroupBox { font-weight: bold; color: #1a5276; border: 1px solid #dee2e6; border-radius: 6px; margin-top: 8px; padding-top: 8px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; }")
        lignes_layout = QVBoxLayout(group_lignes)

        lignes_bar = QHBoxLayout()
        self.btn_ajouter_ligne = QPushButton("+ Ajouter une ligne")
        self.btn_ajouter_ligne.setFixedHeight(30)
        self.btn_ajouter_ligne.setEnabled(False)
        self.btn_ajouter_ligne.setCursor(Qt.PointingHandCursor)
        self.btn_ajouter_ligne.setStyleSheet("""
            QPushButton { background: #117a65; color: white; border-radius: 4px; padding: 0 12px; font-size: 12px; border: none; }
            QPushButton:hover { background: #0e6655; }
            QPushButton:disabled { background: #adb5bd; }
        """)
        self.btn_ajouter_ligne.clicked.connect(self._ajouter_ligne)
        lignes_bar.addWidget(self.btn_ajouter_ligne)
        lignes_bar.addStretch()
        lignes_layout.addLayout(lignes_bar)

        self.table_lignes = QTableWidget()
        self.table_lignes.setColumnCount(5)
        self.table_lignes.setHorizontalHeaderLabels(["Référence", "Produit", "Quantité", "Prix unitaire", "Actions"])
        self.table_lignes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_lignes.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table_lignes.setColumnWidth(4, 80)
        self.table_lignes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_lignes.setAlternatingRowColors(True)
        self.table_lignes.verticalHeader().setVisible(False)
        self.table_lignes.setStyleSheet(self._table_style())
        lignes_layout.addWidget(self.table_lignes)

        splitter.addWidget(group_lignes)
        splitter.setSizes([400, 220])
        layout.addWidget(splitter)

        self.commande_selectionnee_id = None

    def refresh(self):
        commandes = self.commande_model.get_all()
        self.table_commandes.setRowCount(len(commandes))
        self._commandes_data = commandes

        statut_labels = {'en_cours':'En cours','validee':'Validée','livree':'Livrée','annulee':'Annulée'}

        for row, c in enumerate(commandes):
            self.table_commandes.setItem(row, 0, QTableWidgetItem(c['numero_commande']))
            self.table_commandes.setItem(row, 1, QTableWidgetItem(c['fournisseur'] or ''))
            self.table_commandes.setItem(row, 2, QTableWidgetItem(str(c['date_commande'])))
            self.table_commandes.setItem(row, 3, QTableWidgetItem(str(c['date_livraison_prevue'] or '—')))

            statut_item = QTableWidgetItem(statut_labels.get(c['statut'], c['statut']))
            statut_item.setTextAlignment(Qt.AlignCenter)
            self.table_commandes.setItem(row, 4, statut_item)
            self.table_commandes.setItem(row, 5, QTableWidgetItem(
                f"{c['utilisateur_prenom']} {c['utilisateur_nom']}"
            ))

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)

            btn_statut = QPushButton("⚙ Statut")
            btn_statut.setFixedHeight(26)
            btn_statut.setStyleSheet("QPushButton { background: #d6eaf8; border-radius: 4px; border: none; font-size: 11px; padding: 0 6px; } QPushButton:hover { background: #aed6f1; }")
            btn_statut.clicked.connect(lambda _, cid=c['id_commande']: self._changer_statut(cid))

            btn_del = QPushButton("🗑")
            btn_del.setFixedSize(26, 26)
            btn_del.setStyleSheet("QPushButton { background: #f8d7da; border-radius: 4px; border: none; } QPushButton:hover { background: #f5c2c7; }")
            btn_del.clicked.connect(lambda _, cid=c['id_commande']: self._supprimer(cid))

            actions_layout.addWidget(btn_statut)
            actions_layout.addWidget(btn_del)
            self.table_commandes.setCellWidget(row, 6, actions_widget)

        self.table_lignes.setRowCount(0)
        self.btn_ajouter_ligne.setEnabled(False)
        self.commande_selectionnee_id = None

    def _afficher_lignes(self, index):
        row = index.row()
        commande = self._commandes_data[row]
        self.commande_selectionnee_id = commande['id_commande']
        self.btn_ajouter_ligne.setEnabled(True)

        lignes = self.ligne_model.get_by_commande(self.commande_selectionnee_id)
        self.table_lignes.setRowCount(len(lignes))
        for r, l in enumerate(lignes):
            self.table_lignes.setItem(r, 0, QTableWidgetItem(l['reference'] or ''))
            self.table_lignes.setItem(r, 1, QTableWidgetItem(l['produit'] or ''))
            self.table_lignes.setItem(r, 2, QTableWidgetItem(str(l['quantite_commandee'])))
            self.table_lignes.setItem(r, 3, QTableWidgetItem(f"{l['prix_unitaire']:.2f} €"))

            btn_del = QPushButton("🗑")
            btn_del.setFixedSize(26, 26)
            btn_del.setStyleSheet("QPushButton { background: #f8d7da; border-radius: 4px; border: none; } QPushButton:hover { background: #f5c2c7; }")
            btn_del.clicked.connect(lambda _, lid=l['id_ligne']: self._supprimer_ligne(lid))
            self.table_lignes.setCellWidget(r, 4, btn_del)

    def _nouvelle_commande(self):
        fournisseurs = self.fournisseur_model.get_all()
        if not fournisseurs:
            QMessageBox.warning(self, "Attention", "Aucun fournisseur disponible. Veuillez d'abord créer un fournisseur.")
            return
        dialog = CommandeDialog(self, fournisseurs, self.commande_model.get_last_numero())
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            data['id_utilisateur'] = self.user['id_utilisateur']
            self.commande_model.create(data)
            self.refresh()

    def _changer_statut(self, id_commande):
        dialog = StatutDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.commande_model.update_statut(id_commande, dialog.get_statut())
            self.refresh()

    def _supprimer(self, id_commande):
        rep = QMessageBox.question(self, "Confirmation", "Supprimer cette commande et ses lignes ?",
                                   QMessageBox.Yes | QMessageBox.No)
        if rep == QMessageBox.Yes:
            self.commande_model.delete(id_commande)
            self.refresh()

    def _ajouter_ligne(self):
        db = Database.get_instance()
        produits = db.query("SELECT id_produit, reference, designation FROM produits ORDER BY designation")
        dialog = LigneDialog(self, produits)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            data['id_commande'] = self.commande_selectionnee_id
            self.ligne_model.create(data)
            # Rafraîchir les lignes
            row = self.table_commandes.currentRow()
            self._afficher_lignes(self.table_commandes.currentIndex())

    def _supprimer_ligne(self, id_ligne):
        rep = QMessageBox.question(self, "Confirmation", "Supprimer cette ligne ?",
                                   QMessageBox.Yes | QMessageBox.No)
        if rep == QMessageBox.Yes:
            self.ligne_model.delete(id_ligne)
            self._afficher_lignes(self.table_commandes.currentIndex())

    def _table_style(self):
        return """
            QTableWidget { background: white; border: 1px solid #dee2e6; border-radius: 6px; gridline-color: #dee2e6; }
            QHeaderView::section { background: #1a5276; color: white; font-weight: bold; padding: 6px; border: none; border-right: 1px solid #2e86c1; }
            QTableWidget::item { color: #212529; background: white; }
            QTableWidget::item:alternate { background: #f8f9fa; color: #212529; }
            QTableWidget::item:selected { background: #d6eaf8; color: #1a5276; }
        """


class CommandeDialog(QDialog):
    def __init__(self, parent, fournisseurs, numero_suggere):
        super().__init__(parent)
        self.fournisseurs = fournisseurs
        self.setWindowTitle("Nouvelle commande")
        self.setFixedWidth(420)
        self._build_ui(numero_suggere)

    def _build_ui(self, numero):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.input_numero = QLineEdit(numero)
        self.input_numero.setFixedHeight(32)

        self.combo_fournisseur = QComboBox()
        for f in self.fournisseurs:
            self.combo_fournisseur.addItem(f['raison_sociale'], f['id_fournisseur'])

        self.date_commande = QDateEdit(QDate.currentDate())
        self.date_commande.setCalendarPopup(True)
        self.date_commande.setFixedHeight(32)

        self.date_livraison = QDateEdit(QDate.currentDate().addDays(7))
        self.date_livraison.setCalendarPopup(True)
        self.date_livraison.setFixedHeight(32)

        self.combo_statut = QComboBox()
        self.combo_statut.addItems(['en_cours', 'validee', 'livree', 'annulee'])

        style = "border: 1px solid #ced4da; border-radius: 4px; padding: 4px 8px; font-size: 13px;"
        self.input_numero.setStyleSheet(style)

        form.addRow("N° Commande *",      self.input_numero)
        form.addRow("Fournisseur *",      self.combo_fournisseur)
        form.addRow("Date commande",      self.date_commande)
        form.addRow("Date livraison",     self.date_livraison)
        form.addRow("Statut",             self.combo_statut)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._valider)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _valider(self):
        if not self.input_numero.text().strip():
            QMessageBox.warning(self, "Erreur", "Le numéro de commande est obligatoire.")
            return
        self.accept()

    def get_data(self):
        return {
            'numero_commande':       self.input_numero.text().strip(),
            'id_fournisseur':        self.combo_fournisseur.currentData(),
            'date_commande':         self.date_commande.date().toString("yyyy-MM-dd"),
            'date_livraison_prevue': self.date_livraison.date().toString("yyyy-MM-dd"),
            'statut':                self.combo_statut.currentText(),
        }


class StatutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Changer le statut")
        self.setFixedSize(280, 130)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nouveau statut :"))
        self.combo = QComboBox()
        self.combo.addItems(['en_cours', 'validee', 'livree', 'annulee'])
        layout.addWidget(self.combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_statut(self):
        return self.combo.currentText()


class LigneDialog(QDialog):
    def __init__(self, parent, produits):
        super().__init__(parent)
        self.produits = produits
        self.setWindowTitle("Ajouter une ligne")
        self.setFixedWidth(380)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.combo_produit = QComboBox()
        for p in self.produits:
            self.combo_produit.addItem(f"{p['reference']} — {p['designation']}", p['id_produit'])

        self.spin_qte = QSpinBox()
        self.spin_qte.setMinimum(1)
        self.spin_qte.setValue(1)
        self.spin_qte.setFixedHeight(32)

        self.spin_prix = QDoubleSpinBox()
        self.spin_prix.setMinimum(0)
        self.spin_prix.setMaximum(999999)
        self.spin_prix.setDecimals(2)
        self.spin_prix.setValue(0.00)
        self.spin_prix.setFixedHeight(32)

        form.addRow("Produit *",         self.combo_produit)
        form.addRow("Quantité *",        self.spin_qte)
        form.addRow("Prix unitaire (€)", self.spin_prix)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            'id_produit':         self.combo_produit.currentData(),
            'quantite_commandee': self.spin_qte.value(),
            'prix_unitaire':      self.spin_prix.value(),
        }
