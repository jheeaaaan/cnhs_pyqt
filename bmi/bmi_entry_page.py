# bmi/bmi_entry_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QMessageBox, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from core.models import Learner, BMIRecord, Section

G = {
    'text': '#052e16', 'muted': '#4b7a5a', 'bg': '#f0fdf4',
    'card': '#ffffff', 'border': '#d1fae5', 'primary': '#16a34a',
    'tvl': '#0f766e', 'yellow': '#d97706', 'red': '#dc2626',
}
BMI_COLORS = {
    'Normal':        '#16a34a',
    'Thin':          '#ea580c',
    'Severely Thin': '#dc2626',
    'Overweight':    '#d97706',
    'Obese I':       '#dc2626',
    'Obese II':      '#dc2626',
}


class BMIEntryPage(QWidget):
    def __init__(self, level='JHS', grade=7):
        super().__init__()
        self.level = level
        self.grade = grade
        self._all_learners = []
        self._bmi_map = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        hdr = QLabel(f'Grade {self.grade} {self.level} — BMI Entry')
        hdr.setStyleSheet('font-size:18px;font-weight:bold;color:#052e16;')
        layout.addWidget(hdr)

        sub = QLabel('Enter height and weight for enrolled learners. BMI is calculated automatically.')
        sub.setStyleSheet(f'font-size:12px;color:{G["muted"]};')
        layout.addWidget(sub)

        # ✅ Fix 7: Section filter
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel('Filter by Section:'))
        self.section_filter = QComboBox()
        self.section_filter.setMinimumHeight(34)
        self.section_filter.currentIndexChanged.connect(self._on_section_filter)
        filter_row.addWidget(self.section_filter)
        filter_row.addStretch()
        layout.addLayout(filter_row)

        card = QFrame()
        card.setStyleSheet(
            f'QFrame{{background:{G["card"]};border:1px solid {G["border"]};border-radius:14px;}}'
        )
        card_v = QVBoxLayout(card)
        card_v.setContentsMargins(20, 18, 20, 18)
        card_v.setSpacing(14)
        card_v.addWidget(QLabel('Enter BMI Data'))

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(QLabel('Select Learner:'), 0, 0)
        self.learner_combo = QComboBox()
        self.learner_combo.setEditable(True)
        self.learner_combo.setMinimumHeight(36)
        self.learner_combo.currentIndexChanged.connect(self._on_learner_selected)
        grid.addWidget(self.learner_combo, 0, 1, 1, 3)

        grid.addWidget(QLabel('Height (cm):'), 1, 0)
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText('e.g. 155')
        self.height_input.setMinimumHeight(36)
        self.height_input.textChanged.connect(self._calc_bmi)
        grid.addWidget(self.height_input, 1, 1)

        grid.addWidget(QLabel('Weight (kg):'), 1, 2)
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText('e.g. 52')
        self.weight_input.setMinimumHeight(36)
        self.weight_input.textChanged.connect(self._calc_bmi)
        grid.addWidget(self.weight_input, 1, 3)

        self.bmi_frame = QFrame()
        self.bmi_frame.setStyleSheet(
            f'QFrame{{background:#f0fdf4;border:1.5px solid {G["border"]};border-radius:10px;}}'
        )
        bmi_h = QHBoxLayout(self.bmi_frame)
        bmi_h.setContentsMargins(14, 10, 14, 10)
        self.bmi_value_lbl = QLabel('BMI: —')
        self.bmi_value_lbl.setStyleSheet('font-size:18px;font-weight:800;color:#052e16;')
        self.bmi_status_lbl = QLabel('Status: —')
        self.bmi_status_lbl.setStyleSheet(f'font-size:14px;font-weight:700;color:{G["muted"]};')
        self.existing_lbl = QLabel('')
        self.existing_lbl.setStyleSheet(f'font-size:11px;color:{G["muted"]};')
        bmi_h.addWidget(self.bmi_value_lbl)
        bmi_h.addWidget(QLabel('  |  '))
        bmi_h.addWidget(self.bmi_status_lbl)
        bmi_h.addStretch()
        bmi_h.addWidget(self.existing_lbl)
        grid.addWidget(self.bmi_frame, 2, 0, 1, 4)

        save_btn = QPushButton('Save BMI Record')
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self._save)
        grid.addWidget(save_btn, 3, 0, 1, 4)

        card_v.addLayout(grid)
        layout.addWidget(card)
        layout.addStretch()

    def _on_section_filter(self):
        self._populate_learner_combo(self.section_filter.currentData())

    def _populate_learner_combo(self, section_id=None):
        self.learner_combo.blockSignals(True)
        self.learner_combo.clear()
        self.learner_combo.addItem('— Select a learner —', None)
        shown = [l for l in self._all_learners if section_id is None or l.section_id == section_id]
        for l in shown:
            sec = f' [{l.section_name}]' if l.section_name else ''
            self.learner_combo.addItem(f'{l.full_name}{sec}', l.id)
        self.learner_combo.blockSignals(False)

    def _on_learner_selected(self):
        learner_id = self.learner_combo.currentData()
        if learner_id and learner_id in self._bmi_map:
            rec = self._bmi_map[learner_id]
            self.height_input.setText(str(rec.height))
            self.weight_input.setText(str(rec.weight))
            self.existing_lbl.setText(f'Existing: BMI {rec.bmi} ({rec.bmi_status})')
        else:
            self.height_input.clear()
            self.weight_input.clear()
            self.existing_lbl.setText('')

    def _calc_bmi(self):
        try:
            h = float(self.height_input.text())
            w = float(self.weight_input.text())
            bmi, status = BMIRecord.calc_bmi(h, w)
            color = BMI_COLORS.get(status, G['muted'])
            self.bmi_value_lbl.setText(f'BMI: {bmi}')
            self.bmi_status_lbl.setText(status)
            self.bmi_status_lbl.setStyleSheet(f'font-size:14px;font-weight:700;color:{color};')
            self.bmi_frame.setStyleSheet(
                f'QFrame{{background:{color}11;border:1.5px solid {color}55;border-radius:10px;}}'
            )
        except ValueError:
            self.bmi_value_lbl.setText('BMI: —')
            self.bmi_status_lbl.setText('Status: —')
            self.bmi_status_lbl.setStyleSheet(f'font-size:14px;font-weight:700;color:{G["muted"]};')
            self.bmi_frame.setStyleSheet(
                f'QFrame{{background:#f0fdf4;border:1.5px solid {G["border"]};border-radius:10px;}}'
            )

    def _save(self):
        learner_id = self.learner_combo.currentData()
        if not learner_id:
            QMessageBox.warning(self, 'Warning', 'Please select a learner.')
            return
        try:
            h = float(self.height_input.text())
            w = float(self.weight_input.text())
            BMIRecord.save(learner_id, h, w)
            bmi, status = BMIRecord.calc_bmi(h, w)
            QMessageBox.information(self, 'Saved', f'BMI saved! {bmi} ({status})')
            self.height_input.clear()
            self.weight_input.clear()
            self.existing_lbl.setText('')
            self.refresh()
        except ValueError:
            QMessageBox.warning(self, 'Invalid', 'Enter valid numbers for height and weight.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def refresh(self):
        self.section_filter.blockSignals(True)
        self.section_filter.clear()
        self.section_filter.addItem('All Sections', None)
        for s in Section.get_all(grade=self.grade, level=self.level):
            self.section_filter.addItem(s.name, s.id)
        self.section_filter.blockSignals(False)

        self._all_learners = Learner.get_all(grade=self.grade, level=self.level, status='Enrolled')
        all_records = BMIRecord.get_all(grade=self.grade, level=self.level)
        self._bmi_map = {r.learner_id: r for r in all_records}

        self._populate_learner_combo(self.section_filter.currentData())