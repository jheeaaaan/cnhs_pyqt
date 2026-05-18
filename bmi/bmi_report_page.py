# bmi/bmi_report_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox,
    QPushButton, QHeaderView, QFrame, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from core.models import BMIRecord, Learner, Section
from bmi.bmi_entry_page import BMIEditModal


def _stat_card(label, value, color):
    card = QFrame()
    card.setMinimumSize(150, 94)
    card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    card.setStyleSheet(
        'QFrame { background:#ffffff; border:0; border-radius:10px; }'
    )
    layout = QVBoxLayout(card)
    layout.setContentsMargins(14, 10, 14, 10)
    layout.setSpacing(4)
    title = QLabel(label)
    title.setWordWrap(True)
    title.setStyleSheet('font-size:11px; font-weight:700; color:#4b7a5a;')
    num = QLabel(str(value))
    num.setStyleSheet(f'font-size:26px; font-weight:800; color:{color};')
    layout.addWidget(title)
    layout.addWidget(num)
    return card

class BMIReportPage(QWidget):
    # STEP 1: Add 'grade' to the parameters (match it with BMIEntryPage)
    def __init__(self, level='JHS', grade=7): 
        super().__init__()
        self.level = level
        self.grade = grade # Save the grade to use it later
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Update title to show the grade level
        title = QLabel(f'{self.level} Grade {self.grade} BMI Report')
        title.setStyleSheet('font-size:22px; font-weight:bold; color:#052e16;')
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
        self._load_sections()
        apply_btn = QPushButton('Apply Filter')
        apply_btn.clicked.connect(self.refresh)
        filter_bar.addWidget(apply_btn)
        filter_bar.addStretch()
        layout.addLayout(filter_bar)

        self.stats_grid = QGridLayout()
        self.stats_grid.setHorizontalSpacing(14)
        self.stats_grid.setVerticalSpacing(14)
        layout.addLayout(self.stats_grid)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            'Name', 'Section', 'Height (cm)',
            'Weight (kg)', 'BMI', 'Status', 'Action'
        ])
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(0, QHeaderView.Stretch)
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)
        hdr.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(6, 110)
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.SolidLine)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(42)
        self.table.setMinimumHeight(380)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet(
            'QTableWidget { background:#ffffff; border:1px solid #bbf7d0;'
            'gridline-color:#bbf7d0; outline:0; }'
            'QHeaderView::section { background:#f0fdf4; border:1px solid #bbf7d0;'
            'padding:8px; font-weight:700; color:#14532d; }'
            'QTableWidget::item { padding:6px; }'
            'QTableWidget::item:selected { background:#dcfce7; color:#052e16; }'
        )
        layout.addWidget(self.table)

    def refresh(self):
        bmi_status = self.status_filter.currentText()
        bmi_status = None if bmi_status == 'All' else bmi_status
        section_id = self.section_filter.currentData()

        records = BMIRecord.get_all(
            level=self.level,
            grade=self.grade,
            section_id=section_id
        )
        bmi_map = {r.learner_id: r for r in records}
        learners = self._load_learners(section_id)

        rows = []
        for learner in learners:
            record = bmi_map.get(learner.id)
            if bmi_status and (not record or record.bmi_status != bmi_status):
                continue
            rows.append((learner, record))

        self.table.setRowCount(0)
        for learner, rec in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(learner.full_name))
            self.table.setItem(r, 1, QTableWidgetItem(learner.section_name))
            if rec:
                self.table.setItem(r, 2, QTableWidgetItem(str(rec.height)))
                self.table.setItem(r, 3, QTableWidgetItem(str(rec.weight)))
                self.table.setItem(r, 4, QTableWidgetItem(str(rec.bmi)))
                self.table.setItem(r, 5, QTableWidgetItem(rec.bmi_status))
            else:
                self.table.setItem(r, 2, QTableWidgetItem('-'))
                self.table.setItem(r, 3, QTableWidgetItem('-'))
                self.table.setItem(r, 4, QTableWidgetItem('-'))
                self.table.setItem(r, 5, QTableWidgetItem('Not measured'))
            edit_btn = QPushButton('Edit')
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet(
                'QPushButton { background:#16a34a; color:#ffffff; border:0;'
                'border-radius:6px; padding:5px 12px; font-weight:700; }'
                'QPushButton:hover { background:#15803d; }'
            )
            edit_btn.clicked.connect(
                lambda _, learner_id=learner.id: self._open_bmi_editor(learner_id)
            )
            self.table.setCellWidget(r, 6, edit_btn)
            self.table.setRowHeight(r, 42)

        measured = [r for r in bmi_map.values()]
        normal = sum(1 for r in measured if r.bmi_status == 'Normal')
        thin   = sum(1 for r in measured if r.bmi_status in ['Thin', 'Severely Thin'])
        over   = sum(1 for r in measured if r.bmi_status in ['Overweight', 'Obese I', 'Obese II'])
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for idx, card in enumerate([
            _stat_card('Total Learners', len(learners), '#16a34a' if self.level == 'SHS' else '#0369a1'),
            _stat_card('Normal', normal, '#16a34a'),
            _stat_card('Thin / Severely Thin', thin, '#d97706'),
            _stat_card('Overweight / Obese', over, '#dc2626'),
        ]):
            self.stats_grid.addWidget(card, idx // 2, idx % 2)
            self.stats_grid.setColumnStretch(idx % 2, 1)

    def _load_sections(self):
        current_id = self.section_filter.currentData()
        self.section_filter.blockSignals(True)
        self.section_filter.clear()
        self.section_filter.addItem('All Sections', None)
        for s in Section.get_all(level=self.level, grade=self.grade):
            self.section_filter.addItem(s.name, s.id)
        if current_id is not None:
            idx = self.section_filter.findData(current_id)
            if idx >= 0:
                self.section_filter.setCurrentIndex(idx)
        self.section_filter.blockSignals(False)

    def _load_learners(self, section_id=None):
        if section_id:
            return Learner.get_all(section_id=section_id)

        learners_by_id = {}
        for section in Section.get_all(level=self.level, grade=self.grade):
            for learner in Learner.get_all(section_id=section.id):
                learners_by_id[learner.id] = learner

        for learner in Learner.get_all(level=self.level, grade=self.grade):
            learners_by_id[learner.id] = learner

        return sorted(learners_by_id.values(), key=lambda l: l.full_name.lower())

    def _open_bmi_editor(self, learner_id):
        learner = Learner.get_by_id(learner_id)
        if not learner:
            return

        records = BMIRecord.get_all(level=self.level, grade=self.grade)
        existing = {r.learner_id: r for r in records}.get(learner_id)
        modal = BMIEditModal(learner, existing, parent=self)
        if modal.exec_() and modal.was_saved():
            self.refresh()
