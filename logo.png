from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from models.utilisateur import Utilisateur


class UtilisateursPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.utilisateur_model = Utilisateur()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        bar = QHBoxLayout()
        btn_nouveau = QPushButton("+ Nouvel utilisateur")
        btn_nouveau.setFixedHeight(34)
        btn_nouveau.setCursor(Qt.PointingHandCursor)
        btn_nouveau.setStyleSheet("""
            QPushButton { background: #1a5276; color: white; border-radius: 5px; padding: 0 16px; font-size: 13px; border: none; }
            QPushButton:hover { background: #154360; }
        """)
        btn_nouveau.clicked.connect(self._nouveau)
        bar.addWidget(btn_nouveau)
        bar.addStretch()
        layout.addLayout(bar)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nom", "Prénom", "Email", "Rôle", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.table.setColumnWidth(4, 100)
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

    def refresh(self):
        utilisateurs = self.utilisateur_model.get_all()
        self.table.setRowCount(len(utilisateurs))
        for row, u in enumerate(utilisateurs):
            self.table.setItem(row, 0, QTableWidgetItem(u['nom']))
            self.table.setItem(row, 1, QTableWidgetItem(u['prenom']))
            self.table.setItem(row, 2, QTableWidgetItem(u['email']))
            self.table.setItem(row, 3, QTableWidgetItem(u['role'].capitalize()))

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)

            btn_edit = QPushButton("✏")
            btn_edit.setFixedSize(28, 28)
            btn_edit.setStyleSheet("QPushButton { background: #d6eaf8; border-radius: 4px; border: none; } QPushButton:hover { background: #aed6f1; }")
            btn_edit.clicked.connect(lambda _, uid=u['id_utilisateur']: self._modifier(uid))

            actions_layout.addWidget(btn_edit)

            # Pas de suppression de son propre compte
            if u['id_utilisateur'] != self.user['id_utilisateur']:
                btn_del = QPushButton("🗑")
                btn_del.setFixedSize(28, 28)
                btn_del.setStyleSheet("QPushButton { background: #f8d7da; border-radius: 4px; border: none; } QPushButton:hover { background: #f5c2c7; }")
                btn_del.clicked.connect(lambda _, uid=u['id_utilisateur']: self._supprimer(uid))
                actions_layout.addWidget(btn_del)

            self.table.setCellWidget(row, 4, actions_widget)

    def _nouveau(self):
        dialog = UtilisateurDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.utilisateur_model.create(dialog.get_data())
            self.refresh()

    def _modifier(self, id_utilisateur):
        u = self.utilisateur_model.get_by_id(id_utilisateur)
        dialog = UtilisateurDialog(self, u)
        if dialog.exec() == QDialog.Accepted:
            self.utilisateur_model.update(id_utilisateur, dialog.get_data())
            self.refresh()

    def _supprimer(self, id_utilisateur):
        rep = QMessageBox.question(self, "Confirmation", "Supprimer cet utilisateur ?",
                                   QMessageBox.Yes | QMessageBox.No)
        if rep == QMessageBox.Yes:
            self.utilisateur_model.delete(id_utilisateur)
            self.refresh()


class UtilisateurDialog(QDialog):
    def __init__(self, parent=None, utilisateur=None):
        super().__init__(parent)
        self.utilisateur = utilisateur
        self.setWindowTitle("Utilisateur")
        self.setFixedWidth(380)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        style = "border: 1px solid #ced4da; border-radius: 4px; padding: 4px 8px; font-size: 13px;"

        self.input_nom    = QLineEdit(self.utilisateur['nom'] if self.utilisateur else '')
        self.input_prenom = QLineEdit(self.utilisateur['prenom'] if self.utilisateur else '')
        self.input_email  = QLineEdit(self.utilisateur['email'] if self.utilisateur else '')
        self.combo_role   = QComboBox()
        self.combo_role.addItems(['admin', 'commercial', 'acheteur'])

        if self.utilisateur:
            idx = self.combo_role.findText(self.utilisateur['role'])
            if idx >= 0:
                self.combo_role.setCurrentIndex(idx)

        for w in [self.input_nom, self.input_prenom, self.input_email]:
            w.setStyleSheet(style)
            w.setFixedHeight(32)

        form.addRow("Nom *",    self.input_nom)
        form.addRow("Prénom",   self.input_prenom)
        form.addRow("Email *",  self.input_email)
        form.addRow("Rôle",     self.combo_role)

        if not self.utilisateur:
            self.input_mdp = QLineEdit()
            self.input_mdp.setEchoMode(QLineEdit.Password)
            self.input_mdp.setStyleSheet(style)
            self.input_mdp.setFixedHeight(32)
            form.addRow("Mot de passe *", self.input_mdp)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._valider)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _valider(self):
        if not self.input_nom.text().strip() or not self.input_email.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom et l'email sont obligatoires.")
            return
        self.accept()

    def get_data(self):
        data = {
            'nom':    self.input_nom.text().strip(),
            'prenom': self.input_prenom.text().strip(),
            'email':  self.input_email.text().strip(),
            'role':   self.combo_role.currentText(),
        }
        if not self.utilisateur:
            data['mot_de_passe'] = self.input_mdp.text().strip()
        return data
