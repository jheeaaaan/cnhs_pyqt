# bmi/bmi_report_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox,
    QPushButton, QHeaderView
)
from core.models import BMIRecord, Section

class BMIReportPage(QWidget):
    def __init__(self, level='JHS'):
        super().__init__()
        self.level = level
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(f'{self.level} BMI Report')
        title.setStyleSheet('font-size:18px; font-weight:bold;')
        layout.addWidget(title)

        filter_bar = QHBoxLayout()
        filter_bar.addWidget(QLabel('BMI Status:'))
        self.status_filter = QComboBox()
        self.status_filter.addItems([
            'All', 'Severely Thin', 'Thin',
            'Normal', 'Overweight', 'Obese I', 'Obese II'
        ])
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
            'Name', 'Section', 'Height (cm)',
            'Weight (kg)', 'BMI', 'Status'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

    def refresh(self):
        bmi_status = self.status_filter.currentText()
        bmi_status = None if bmi_status == 'All' else bmi_status
        section_id = self.section_filter.currentData()

        records = BMIRecord.get_all(
            level=self.level,
            bmi_status=bmi_status,
            section_id=section_id
        )

        self.section_filter.blockSignals(True)
        self.section_filter.clear()
        self.section_filter.addItem('All Sections', None)
        for s in Section.get_all(level=self.level):
            self.section_filter.addItem(s.name, s.id)
        self.section_filter.blockSignals(False)

        self.table.setRowCount(0)
        for rec in records:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(rec.learner_name))
            self.table.setItem(r, 1, QTableWidgetItem(rec.section_name))
            self.table.setItem(r, 2, QTableWidgetItem(str(rec.height)))
            self.table.setItem(r, 3, QTableWidgetItem(str(rec.weight)))
            self.table.setItem(r, 4, QTableWidgetItem(str(rec.bmi)))
            self.table.setItem(r, 5, QTableWidgetItem(rec.bmi_status))

        normal = sum(1 for r in records if r.bmi_status == 'Normal')
        thin   = sum(1 for r in records if r.bmi_status in ['Thin', 'Severely Thin'])
        over   = sum(1 for r in records if r.bmi_status in ['Overweight', 'Obese I', 'Obese II'])
        self.stats_label.setText(
            f'Total: {len(records)}  |  Normal: {normal}  |  Thin/Severely Thin: {thin}  |  Overweight/Obese: {over}'
        )