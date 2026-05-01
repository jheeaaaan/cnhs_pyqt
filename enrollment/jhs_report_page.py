# enrollment/jhs_report_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox,
    QPushButton, QHeaderView
)
from PyQt5.QtCore import Qt
from core.models import Learner, Section

class JHSReportPage(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(f'Grade {self.grade} — JHS Learners')
        title.setStyleSheet('font-size:18px; font-weight:bold;')
        layout.addWidget(title)

        filter_bar = QHBoxLayout()
        filter_bar.addWidget(QLabel('Status:'))
        self.status_filter = QComboBox()
        self.status_filter.addItems(['All', 'Enrolled', 'Pending', 'Dropped', 'Transferred'])
        filter_bar.addWidget(self.status_filter)
        filter_bar.addWidget(QLabel('Section:'))
        self.section_filter = QComboBox()
        filter_bar.addWidget(self.section_filter)
        apply_btn = QPushButton('Apply Filter')
        apply_btn.clicked.connect(self.refresh)
        filter_bar.addWidget(apply_btn)
        filter_bar.addStretch()
        layout.addLayout(filter_bar)

        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            'LRN', 'Name', 'Sex', 'Grade', 'Section', 'Status'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

    def refresh(self):
        status = self.status_filter.currentText()
        status = None if status == 'All' else status
        section_id = self.section_filter.currentData()

        learners = Learner.get_all(
            grade=self.grade, level='JHS',
            status=status, section_id=section_id
        )

        self.section_filter.blockSignals(True)
        self.section_filter.clear()
        self.section_filter.addItem('All Sections', None)
        for s in Section.get_all(grade=self.grade, level='JHS'):
            self.section_filter.addItem(s.name, s.id)
        self.section_filter.blockSignals(False)

        self.table.setRowCount(0)
        for l in learners:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(l.lrn))
            self.table.setItem(r, 1, QTableWidgetItem(l.full_name))
            self.table.setItem(r, 2, QTableWidgetItem(l.sex))
            self.table.setItem(r, 3, QTableWidgetItem(str(l.grade)))
            self.table.setItem(r, 4, QTableWidgetItem(l.section_name))
            self.table.setItem(r, 5, QTableWidgetItem(l.status))

        enrolled = sum(1 for l in learners if l.status == 'Enrolled')
        pending  = sum(1 for l in learners if l.status == 'Pending')
        self.stats_label.setText(
            f'Total: {len(learners)}  |  Enrolled: {enrolled}  |  Pending: {pending}'
        )