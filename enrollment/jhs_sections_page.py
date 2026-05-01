# enrollment/jhs_sections_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView
)
from core.models import Section

class JHSSectionsPage(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel(f'Grade {self.grade} — JHS Sections')
        title.setStyleSheet('font-size:18px; font-weight:bold;')
        layout.addWidget(title)

        add_row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Section name (e.g. SAMPAGUITA)')
        add_btn = QPushButton('+ Add Section')
        add_btn.clicked.connect(self._add_section)
        add_row.addWidget(QLabel('Name:'))
        add_row.addWidget(self.name_input)
        add_row.addWidget(add_btn)
        layout.addLayout(add_row)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(['Name', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

    def _add_section(self):
        name = self.name_input.text().strip().upper()
        if not name:
            QMessageBox.warning(self, 'Error', 'Section name is required.')
            return
        try:
            Section.create(name, self.grade, 'JHS')
            self.name_input.clear()
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def _delete_section(self, section_id):
        confirm = QMessageBox.question(self, 'Confirm', 'Delete this section?')
        if confirm == QMessageBox.Yes:
            Section.delete(section_id)
            self.refresh()

    def refresh(self):
        sections = Section.get_all(grade=self.grade, level='JHS')
        self.table.setRowCount(0)
        for s in sections:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(s.name))
            del_btn = QPushButton('Delete')
            del_btn.setStyleSheet('background:#dc2626;')
            del_btn.clicked.connect(lambda _, sid=s.id: self._delete_section(sid))
            self.table.setCellWidget(r, 1, del_btn)