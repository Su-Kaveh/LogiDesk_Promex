from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QTextEdit,
    QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt
from models.fournisseur import Fournisseur


class FournisseursPage(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.fournisseur_model = Fournisseur()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Barre actions
        bar = QHBoxLayout()
        btn_nouveau = QPushButton("+ Nouveau fournisseur")
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

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Raison sociale", "Contact", "Téléphone", "Email", "Adresse", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 120)
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
        fournisseurs = self.fournisseur_model.get_all()
        self.table.setRowCount(len(fournisseurs))
        for row, f in enumerate(fournisseurs):
            self.table.setItem(row, 0, QTableWidgetItem(f['raison_sociale']))
            self.table.setItem(row, 1, QTableWidgetItem(f['contact'] or ''))
            self.table.setItem(row, 2, QTableWidgetItem(f['telephone'] or ''))
            self.table.setItem(row, 3, QTableWidgetItem(f['email'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(f['adresse'] or ''))

            # Boutons actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)

            btn_edit = QPushButton("✏")
            btn_edit.setFixedSize(28, 28)
            btn_edit.setToolTip("Modifier")
            btn_edit.setStyleSheet("QPushButton { background: #d6eaf8; border-radius: 4px; border: none; } QPushButton:hover { background: #aed6f1; }")
            btn_edit.clicked.connect(lambda _, fid=f['id_fournisseur']: self._modifier(fid))

            btn_del = QPushButton("🗑")
            btn_del.setFixedSize(28, 28)
            btn_del.setToolTip("Supprimer")
            btn_del.setStyleSheet("QPushButton { background: #f8d7da; border-radius: 4px; border: none; } QPushButton:hover { background: #f5c2c7; }")
            btn_del.clicked.connect(lambda _, fid=f['id_fournisseur']: self._supprimer(fid))

            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_del)
            self.table.setCellWidget(row, 5, actions_widget)

    def _nouveau(self):
        dialog = FournisseurDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.fournisseur_model.create(dialog.get_data())
            self.refresh()

    def _modifier(self, id_fournisseur):
        fournisseur = self.fournisseur_model.get_by_id(id_fournisseur)
        dialog = FournisseurDialog(self, fournisseur)
        if dialog.exec() == QDialog.Accepted:
            self.fournisseur_model.update(id_fournisseur, dialog.get_data())
            self.refresh()

    def _supprimer(self, id_fournisseur):
        rep = QMessageBox.question(self, "Confirmation", "Supprimer ce fournisseur ?",
                                   QMessageBox.Yes | QMessageBox.No)
        if rep == QMessageBox.Yes:
            self.fournisseur_model.delete(id_fournisseur)
            self.refresh()


class FournisseurDialog(QDialog):
    def __init__(self, parent=None, fournisseur=None):
        super().__init__(parent)
        self.fournisseur = fournisseur
        self.setWindowTitle("Fournisseur")
        self.setFixedWidth(420)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        self.input_rs      = QLineEdit(self.fournisseur['raison_sociale'] if self.fournisseur else '')
        self.input_contact = QLineEdit(self.fournisseur['contact'] or '' if self.fournisseur else '')
        self.input_tel     = QLineEdit(self.fournisseur['telephone'] or '' if self.fournisseur else '')
        self.input_email   = QLineEdit(self.fournisseur['email'] or '' if self.fournisseur else '')
        self.input_adresse = QTextEdit(self.fournisseur['adresse'] or '' if self.fournisseur else '')
        self.input_adresse.setFixedHeight(60)

        style = "border: 1px solid #ced4da; border-radius: 4px; padding: 4px 8px; font-size: 13px;"
        for w in [self.input_rs, self.input_contact, self.input_tel, self.input_email]:
            w.setStyleSheet(style)
            w.setFixedHeight(32)

        form.addRow("Raison sociale *", self.input_rs)
        form.addRow("Contact",          self.input_contact)
        form.addRow("Téléphone",        self.input_tel)
        form.addRow("Email",            self.input_email)
        form.addRow("Adresse",          self.input_adresse)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._valider)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _valider(self):
        if not self.input_rs.text().strip():
            QMessageBox.warning(self, "Erreur", "La raison sociale est obligatoire.")
            return
        self.accept()

    def get_data(self):
        return {
            'raison_sociale': self.input_rs.text().strip(),
            'contact':        self.input_contact.text().strip(),
            'telephone':      self.input_tel.text().strip(),
            'email':          self.input_email.text().strip(),
            'adresse':        self.input_adresse.toPlainText().strip(),
        }
