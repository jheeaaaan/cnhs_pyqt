# windows/change_password.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
import core.auth as auth

class ChangePasswordPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel('Change Password')
        title.setStyleSheet('font-size:18px; font-weight:bold;')
        layout.addWidget(title)

        form = QFormLayout()
        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.Password)
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.confirm_pass = QLineEdit()
        self.confirm_pass.setEchoMode(QLineEdit.Password)
        form.addRow('Current Password:', self.old_pass)
        form.addRow('New Password:', self.new_pass)
        form.addRow('Confirm New Password:', self.confirm_pass)
        layout.addLayout(form)

        btn = QPushButton('Update Password')
        btn.setFixedHeight(38)
        btn.clicked.connect(self._update)
        layout.addWidget(btn)
        layout.addStretch()

    def _update(self):
        if self.new_pass.text() != self.confirm_pass.text():
            QMessageBox.warning(self, 'Error', 'New passwords do not match.')
            return
        user = auth.get_current_user()
        if not user:
            QMessageBox.warning(self, 'Error', 'No user logged in.')
            return
        ok, msg = auth.change_password(
            user.id,
            self.old_pass.text(),
            self.new_pass.text()
        )
        if ok:
            QMessageBox.information(self, 'Success', msg)
            self.old_pass.clear()
            self.new_pass.clear()
            self.confirm_pass.clear()
        else:
            QMessageBox.warning(self, 'Error', msg)