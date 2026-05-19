# enrollment/jhs_pending_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from core.errors import friendly_error_message
from core.models import Learner, Section

try:
    from enrollment.jhs_sections_page import JHSEditModal
except ImportError:
    JHSEditModal = None


class JHSPendingPage(QWidget):
    enrolled = pyqtSignal()

    def __init__(self, grade, parent=None):
        super().__init__(parent)
        self.grade = grade
        self._all_learners = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet('background:#0c4a6e;')
        header.setFixedHeight(64)
        h_row = QHBoxLayout(header)
        h_row.setContentsMargins(24, 0, 24, 0)

        title = QLabel(f'Grade {self.grade} — Pending Learners')
        title.setStyleSheet('color:white; font-size:17px; font-weight:bold;')
        h_row.addWidget(title)
        h_row.addStretch()

        self.count_lbl = QLabel()
        self.count_lbl.setStyleSheet(
            'background:#0369a1; color:white; border-radius:10px;'
            'padding:4px 14px; font-weight:bold;'
        )
        h_row.addWidget(self.count_lbl)
        layout.addWidget(header)

        # Body
        body = QWidget()
        body.setStyleSheet('background:#f0f9ff;')
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(24, 20, 24, 20)
        body_layout.setSpacing(14)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('🔍  Search by name or LRN...')
        self.search_input.setFixedWidth(300)
        self.search_input.setStyleSheet(
            'border:1px solid #bae6fd; border-radius:6px;'
            'padding:6px 10px; background:white;'
        )
        self.search_input.textChanged.connect(self._filter)
        filter_row.addWidget(self.search_input)

        filter_row.addWidget(QLabel('Assign to Section:'))
        self.section_combo = QComboBox()
        self.section_combo.setFixedWidth(220)
        filter_row.addWidget(self.section_combo)

        assign_btn = QPushButton('Assign & Enroll Selected')
        assign_btn.setStyleSheet(
            'background:#0369a1; color:white; border-radius:6px;'
            'padding:7px 16px; font-weight:bold;'
        )
        assign_btn.clicked.connect(self._assign_selected)
        filter_row.addWidget(assign_btn)
        filter_row.addStretch()
        body_layout.addLayout(filter_row)

        hint = QLabel(
            'Select learners below, choose a section, then click "Assign & Enroll Selected".'
        )
        hint.setStyleSheet('color:#0369a1; font-size:11px;')
        body_layout.addWidget(hint)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ['', 'LRN', "Learner's Name", 'Sex', 'Grade', 'Current Section', 'Edit']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 36)
        self.table.setColumnWidth(6, 96)
        self.table.verticalHeader().setDefaultSectionSize(52)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            'QTableWidget { background:white; border-radius:8px; border:1px solid #bae6fd; }'
            'QTableWidget::item { border:none; padding:8px 10px; }'
            'QTableWidget::item:selected { background:#e0f2fe; color:#0f172a; border:none; }'
            'QHeaderView::section { background:#0c4a6e; color:white;'
            '  font-weight:bold; padding:6px; }'
            'QPushButton { outline:none; }'
        )
        body_layout.addWidget(self.table)

        bottom_row = QHBoxLayout()
        sel_all = QPushButton('Select All')
        sel_all.setStyleSheet(
            'background:#e0f2fe; color:#0369a1; border-radius:6px; padding:5px 12px;'
        )
        sel_all.clicked.connect(self._select_all)
        desel_all = QPushButton('Deselect All')
        desel_all.setStyleSheet(
            'background:#f1f5f9; color:#374151; border-radius:6px; padding:5px 12px;'
        )
        desel_all.clicked.connect(self._deselect_all)
        bottom_row.addWidget(sel_all)
        bottom_row.addWidget(desel_all)
        bottom_row.addStretch()
        body_layout.addLayout(bottom_row)

        layout.addWidget(body)

    def refresh(self):
        self._all_learners = Learner.get_all(
            grade=self.grade, level='JHS', status='Pending'
        )
        self._rebuild_section_combo()
        self._populate_table(self._all_learners)

    def _rebuild_section_combo(self):
        self.section_combo.clear()
        self.section_combo.addItem('— Select section —', None)
        for s in Section.get_all(grade=self.grade, level='JHS'):
            self.section_combo.addItem(s.name, s.id)

    def _filter(self, text):
        q = text.strip().lower()
        filtered = (
            [l for l in self._all_learners
             if q in l.full_name.lower() or q in l.lrn.lower()]
            if q else self._all_learners
        )
        self._populate_table(filtered)

    def _populate_table(self, learners):
        self.table.setRowCount(0)
        self.count_lbl.setText(f'{len(learners)} Pending')

        for l in learners:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setRowHeight(r, 52)

            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            chk_item.setCheckState(Qt.Unchecked)
            chk_item.setData(Qt.UserRole, l)
            self.table.setItem(r, 0, chk_item)

            self.table.setItem(r, 1, QTableWidgetItem(l.lrn))
            self.table.setItem(r, 2, QTableWidgetItem(l.full_name))
            self.table.setItem(r, 3, QTableWidgetItem(l.sex or ''))
            self.table.setItem(r, 4, QTableWidgetItem(str(l.grade)))
            self.table.setItem(r, 5, QTableWidgetItem(
                getattr(l, 'section_name', '') or 'Unassigned'
            ))

            edit_btn = QPushButton('Edit')
            edit_btn.setFixedHeight(30)
            edit_btn.setStyleSheet(
                'background:#0369a1; color:white; border-radius:5px;'
                'padding:4px 12px; font-size:11px; font-weight:700; border:none;'
            )
            edit_btn.clicked.connect(lambda _, learner=l: self._open_edit(learner))
            self.table.setCellWidget(r, 6, edit_btn)

    def _open_edit(self, learner):
        if JHSEditModal is None:
            QMessageBox.warning(self, 'Unavailable', 'Edit modal not available.')
            return
        modal = JHSEditModal(learner, self.grade, self)
        modal.saved.connect(self.enrolled.emit)
        modal.saved.connect(self.refresh)
        modal.exec_()

    def _select_all(self):
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item:
                item.setCheckState(Qt.Checked)

    def _deselect_all(self):
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item:
                item.setCheckState(Qt.Unchecked)

    def _assign_selected(self):
        section_id = self.section_combo.currentData()
        if not section_id:
            QMessageBox.warning(self, 'No Section', 'Please select a section first.')
            return

        selected = []
        for r in range(self.table.rowCount()):
            chk_item = self.table.item(r, 0)
            if chk_item and chk_item.checkState() == Qt.Checked:
                selected.append(chk_item.data(Qt.UserRole))

        if not selected:
            QMessageBox.warning(self, 'No Selection', 'Please select at least one learner.')
            return

        errors = []
        for l in selected:
            try:
                Learner.update(l.id, section_id=section_id, status='Enrolled')
            except Exception as e:
                errors.append(f'{l.full_name}: {friendly_error_message(e)}')

        if errors:
            QMessageBox.critical(self, 'Errors', '\n'.join(errors))
        else:
            QMessageBox.information(
                self, 'Done',
                f'{len(selected)} learner(s) enrolled successfully.'
            )

        self.enrolled.emit()
        self.refresh()
