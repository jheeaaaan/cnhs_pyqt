# enrollment/jhs_sections_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView,
    QFrame, QScrollArea, QGridLayout, QSizePolicy,
    QStackedWidget, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import date
from core.errors import show_error
from core.models import Section, Learner

TEXT    = '#052e16'
MUTED   = '#4b7a5a'
BG      = '#eff6ff'
CARD    = '#ffffff'
BORDER  = '#bfdbfe'
PRIMARY = '#0369a1'
PRIMARY_DARK = '#0c4a6e'
RED     = '#dc2626'
YELLOW  = '#d97706'


def make_status_badge(status: str) -> QLabel:
    badge = QLabel(status)
    badge.setAlignment(Qt.AlignCenter)
    badge.setFixedHeight(24)
    colors = {
        'Enrolled':    'background:#1d4ed8; color:#fff;',
        'Pending':     'background:#d97706; color:#fff;',
        'Dropped':     'background:#dc2626; color:#fff;',
        'Transferred': 'background:#6b7280; color:#fff;',
    }
    style = colors.get(status, 'background:#6b7280; color:#fff;')
    badge.setStyleSheet(
        f'{style} border-radius:4px; padding:0 8px; font-size:11px; font-weight:bold;'
    )
    return badge


# ---------------------------------------------------------------------------
# Section Card
# ---------------------------------------------------------------------------
class SectionCard(QFrame):
    clicked = pyqtSignal(object)
    delete_requested = pyqtSignal(object)

    ACCENT_COLORS = [
        '#0369a1', '#0891b2', '#0284c7', '#0c4a6e',
        '#1d4ed8', '#2563eb', '#075985', '#0e7490',
    ]

    def __init__(self, section, enrolled, pending, total, color_index=0):
        super().__init__()
        self.section = section
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(188)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f'''
            SectionCard {{
                background: {CARD};
                border-radius: 8px;
                border: 1.5px solid {BORDER};
            }}
            SectionCard:hover {{
                border: 1.5px solid {PRIMARY};
            }}
        ''')
        accent_color = self.ACCENT_COLORS[color_index % len(self.ACCENT_COLORS)]

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        accent = QFrame()
        accent.setFixedHeight(6)
        accent.setStyleSheet(f'background:{accent_color}; border-radius:8px 8px 0 0;')
        outer.addWidget(accent)

        content = QVBoxLayout()
        content.setContentsMargins(18, 12, 18, 12)
        content.setSpacing(6)

        name_lbl = QLabel(section.name)
        name_lbl.setStyleSheet(f'font-size:20px; font-weight:800; color:{TEXT}; background:transparent;')
        name_lbl.setWordWrap(True)
        content.addWidget(name_lbl)
        level_lbl = QLabel('Junior High School')
        level_lbl.setStyleSheet(f'font-size:12px; color:{MUTED}; background:transparent;')
        content.addWidget(level_lbl)

        stats_row = QHBoxLayout()
        for label, val, color in [
            ('Enrolled', enrolled, PRIMARY),
            ('Pending',  pending,  YELLOW if pending else MUTED),
            ('Total',    total,    '#374151'),
        ]:
            col = QVBoxLayout()
            col.setSpacing(0)
            v = QLabel(str(val))
            v.setStyleSheet(f'font-size:22px; font-weight:800; color:{color};')
            v.setAlignment(Qt.AlignCenter)
            k = QLabel(label)
            k.setStyleSheet(f'font-size:10px; font-weight:700; color:{MUTED};')
            k.setAlignment(Qt.AlignCenter)
            k.setWordWrap(True)
            col.addWidget(v)
            col.addWidget(k)
            stats_row.addLayout(col)
        content.addLayout(stats_row)

        open_lbl = QLabel('Open →')
        open_lbl.setStyleSheet(f'font-size:13px; color:{PRIMARY}; font-weight:700;')
        open_lbl.setAlignment(Qt.AlignRight)
        content.addWidget(open_lbl)

        del_btn = QPushButton('Delete Section')
        del_btn.setStyleSheet(
            f'QPushButton {{ padding:6px 12px; background:#fef2f2; border:1px solid #fecaca;'
            f'color:{RED}; border-radius:6px; font-size:12px; font-weight:700; }}'
            f'QPushButton:hover {{ background:{RED}; color:#fff; border-color:{RED}; }}'
        )
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self.section))
        content.addWidget(del_btn, 0, Qt.AlignRight)

        outer.addLayout(content)

    def mousePressEvent(self, event):
        self.clicked.emit(self.section)


# ---------------------------------------------------------------------------
# Sections Grid View
# ---------------------------------------------------------------------------
class OldSectionsGridView(QWidget):
    section_opened = pyqtSignal(object)

    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        header_row = QHBoxLayout()
        title = QLabel(f'Grade {self.grade} — JHS Sections')
        title.setStyleSheet('font-size:18px; font-weight:bold; color:#0c4a6e;')
        header_row.addWidget(title)
        header_row.addStretch()
        layout.addLayout(header_row)

        add_row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Section name (e.g. SAMPAGUITA)')
        self.name_input.setFixedWidth(240)
        add_btn = QPushButton('+ Add Section')
        add_btn.setStyleSheet(
            'background:#0369a1; color:white; border-radius:6px;'
            'padding:6px 14px; font-weight:bold;'
        )
        add_btn.clicked.connect(self._add_section)
        add_row.addWidget(QLabel('Name:'))
        add_row.addWidget(self.name_input)
        add_row.addWidget(add_btn)
        add_row.addStretch()
        layout.addLayout(add_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        scroll.setWidget(self.grid_container)
        layout.addWidget(scroll)

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
            show_error(self, 'Unable to Create Section', e)

    def _delete_section(self, section):
        confirm = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete section "{section.name}"?\n\nLearners in it will become Pending.',
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            Section.delete(section.id)
            self.refresh()

    def refresh(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sections = Section.get_all(grade=self.grade, level='JHS')
        learners_all = Learner.get_all(grade=self.grade, level='JHS')

        col_count = 3
        for idx, s in enumerate(sections):
            s_learners = [l for l in learners_all if l.section_id == s.id]
            enrolled = sum(1 for l in s_learners if l.status == 'Enrolled')
            pending  = sum(1 for l in s_learners if l.status == 'Pending')
            total    = len(s_learners)

            card = SectionCard(s, enrolled, pending, total, color_index=idx)
            card.clicked.connect(self.section_opened.emit)
            card.delete_requested.connect(self._delete_section)
            row, col = divmod(idx, col_count)
            self.grid_layout.addWidget(card, row, col)


class SectionsGridView(QWidget):
    section_opened = pyqtSignal(object)

    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self.add_open = False
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
        root.addWidget(scroll)

        container = QWidget()
        container.setStyleSheet(f'background: {BG};')
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 28, 32, 32)
        layout.setSpacing(0)

        layout.addWidget(self._make_header())
        layout.addWidget(self._make_add_frame())
        layout.addSpacing(4)
        layout.addWidget(self._make_info_banner())
        layout.addSpacing(20)

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet('background: transparent;')
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.grid_container)

        self.empty_state = self._make_empty_state()
        layout.addWidget(self.empty_state)
        layout.addStretch()

    def _make_header(self):
        header = QWidget()
        header.setStyleSheet('background: transparent;')
        row = QHBoxLayout(header)
        row.setContentsMargins(0, 0, 0, 20)
        row.setSpacing(16)

        left = QWidget()
        left.setStyleSheet('background: transparent;')
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)

        breadcrumb = QLabel(f'Enrollment  /  JHS  /  Grade {self.grade}  /  Sections')
        breadcrumb.setStyleSheet(f'font-size: 12px; color: {MUTED}; background: transparent;')
        title = QLabel(f'Grade {self.grade} - JHS Sections')
        title.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {TEXT}; background: transparent;')
        subtitle = QLabel('Click a section card to view and manage its enrolled learners.')
        subtitle.setStyleSheet(f'font-size: 14px; color: {MUTED}; background: transparent;')
        left_layout.addWidget(breadcrumb)
        left_layout.addWidget(title)
        left_layout.addWidget(subtitle)
        row.addWidget(left, 1)

        self.add_btn = QPushButton('+ Add Section')
        self.add_btn.setMinimumHeight(38)
        self.add_btn.setMinimumWidth(130)
        self.add_btn.setStyleSheet(self._btn_style(False))
        self.add_btn.clicked.connect(self._toggle_add_form)
        row.addWidget(self.add_btn, 0, Qt.AlignVCenter)
        return header

    def _make_add_frame(self):
        self.add_frame = QFrame()
        self.add_frame.setStyleSheet(
            f'QFrame {{ background: {CARD}; border: 2px solid rgba(3,105,161,0.18);'
            f'border-radius: 8px; margin-bottom: 4px; }}'
        )
        row = QHBoxLayout(self.add_frame)
        row.setContentsMargins(20, 14, 20, 14)
        row.setSpacing(12)

        label = QLabel('Section Name:')
        label.setStyleSheet(f'color: {TEXT}; background: transparent; font-size: 13px;')
        row.addWidget(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('e.g. SAMPAGUITA, NARRA, MOLAVE')
        self.name_input.setMinimumHeight(36)
        self.name_input.setMinimumWidth(260)
        self.name_input.setStyleSheet(
            f'QLineEdit {{ background: {BG}; border: 1.5px solid {PRIMARY}; border-radius: 8px;'
            f'padding: 8px 14px; font-size: 13px; color: {TEXT}; }}'
            f'QLineEdit:focus {{ background: #fff; }}'
        )
        self.name_input.returnPressed.connect(self._add_section)
        row.addWidget(self.name_input)

        save_btn = QPushButton('Add Section')
        save_btn.setMinimumHeight(36)
        save_btn.setMinimumWidth(110)
        save_btn.setStyleSheet(
            f'QPushButton {{ background: {PRIMARY}; color: #fff; border: none; border-radius: 8px;'
            f'font-size: 13px; font-weight: 700; padding: 8px 18px; }}'
            f'QPushButton:hover {{ background: {PRIMARY_DARK}; }}'
        )
        save_btn.clicked.connect(self._add_section)
        row.addWidget(save_btn)
        row.addStretch()

        self.add_frame.hide()
        return self.add_frame

    def _make_info_banner(self):
        info = QFrame()
        info.setStyleSheet('QFrame { background: rgba(3,105,161,0.08); border: none; border-radius: 8px; }')
        row = QHBoxLayout(info)
        row.setContentsMargins(16, 10, 16, 10)
        label = QLabel(
            'Sections sync with the BMI module. '
            'Click a card to open a section and use Edit on any learner.'
        )
        label.setStyleSheet(f'font-size: 12.5px; color: {PRIMARY}; background: transparent;')
        label.setWordWrap(True)
        row.addWidget(label)
        return info

    def _make_empty_state(self):
        empty = QFrame()
        empty.setStyleSheet('QFrame { background: rgba(255,255,255,0.72); border: none; border-radius: 8px; }')
        layout = QVBoxLayout(empty)
        layout.setContentsMargins(56, 64, 56, 64)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel('No Sections Yet')
        title.setStyleSheet(f'font-size: 18px; font-weight: 800; color: {TEXT}; background: transparent;')
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(f'Click "+ Add Section" above to create the first section for Grade {self.grade}.')
        subtitle.setStyleSheet(
            f'font-size: 15px; color: #052e16; background: transparent; '
            f'font-weight: 700; line-height: 1.5;'
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setMaximumWidth(520)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return empty

    def _btn_style(self, cancel):
        color = RED if cancel else PRIMARY
        return (
            f'QPushButton {{ border: 1.5px solid {color}; border-radius: 10px;'
            f'background: transparent; color: {color}; font-size: 13px; font-weight: 700; padding: 8px 20px; }}'
            f'QPushButton:hover {{ background: {color}; color: #fff; }}'
        )

    def _toggle_add_form(self):
        self.add_open = not self.add_open
        if self.add_open:
            self.add_frame.show()
            self.name_input.setFocus()
            self.add_btn.setText('Cancel')
            self.add_btn.setStyleSheet(self._btn_style(True))
        else:
            self.add_frame.hide()
            self.name_input.clear()
            self.add_btn.setText('+ Add Section')
            self.add_btn.setStyleSheet(self._btn_style(False))

    def _add_section(self):
        name = self.name_input.text().strip().upper()
        if not name:
            QMessageBox.warning(self, 'Required', 'Section name is required.')
            return
        try:
            Section.create(name, self.grade, 'JHS')
            self.name_input.clear()
            if self.add_open:
                self._toggle_add_form()
            self.refresh()
        except Exception as e:
            show_error(self, 'Unable to Create Section', e)

    def _delete_section(self, section):
        confirm = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete section "{section.name}"?\n\nLearners in it will become Pending.',
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            Section.delete(section.id)
            self.refresh()

    def refresh(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sections = Section.get_all(grade=self.grade, level='JHS')
        learners_all = Learner.get_all(grade=self.grade, level='JHS')

        if not sections:
            self.grid_container.hide()
            self.empty_state.show()
            return

        self.empty_state.hide()
        self.grid_container.show()

        col_count = 3
        for idx, s in enumerate(sections):
            s_learners = [l for l in learners_all if l.section_id == s.id]
            enrolled = sum(1 for l in s_learners if l.status == 'Enrolled')
            pending = sum(1 for l in s_learners if l.status == 'Pending')
            total = len(s_learners)

            card = SectionCard(s, enrolled, pending, total, color_index=idx)
            card.clicked.connect(self.section_opened.emit)
            card.delete_requested.connect(self._delete_section)
            row, col = divmod(idx, col_count)
            self.grid_layout.addWidget(card, row, col)


# ---------------------------------------------------------------------------
# Section Detail View
# ---------------------------------------------------------------------------
class SectionDetailView(QWidget):
    back_requested = pyqtSignal()
    edit_requested = pyqtSignal(object)

    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self.section = None
        self._all_learners = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(14)

        top_row = QHBoxLayout()
        back_btn = QPushButton('← Back to Sections')
        back_btn.setStyleSheet(
            'background:transparent; color:#0369a1; font-weight:bold; border:none;'
        )
        back_btn.clicked.connect(self.back_requested.emit)
        top_row.addWidget(back_btn)
        top_row.addStretch()
        layout.addLayout(top_row)

        self.breadcrumb = QLabel()
        self.breadcrumb.setStyleSheet('font-size:12px; color:#6b7280;')
        layout.addWidget(self.breadcrumb)

        self.section_title = QLabel()
        self.section_title.setStyleSheet('font-size:18px; font-weight:bold; color:#0c4a6e;')
        layout.addWidget(self.section_title)

        stat_row = QHBoxLayout()
        self.stat_total    = self._make_stat_card('Total Learners', '0', '#0369a1')
        self.stat_enrolled = self._make_stat_card('Enrolled',       '0', '#1d4ed8')
        self.stat_pending  = self._make_stat_card('Pending',        '0', '#d97706')
        for card in [self.stat_total, self.stat_enrolled, self.stat_pending]:
            stat_row.addWidget(card)
        stat_row.addStretch()
        layout.addLayout(stat_row)

        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by name or LRN…')
        self.search_input.setFixedWidth(280)
        self.search_input.textChanged.connect(self._filter_table)
        search_row.addWidget(self.search_input)
        search_row.addStretch()
        layout.addLayout(search_row)

        show_tve = self.grade in (8, 9, 10)
        col_count = 7 if show_tve else 6
        self.table = QTableWidget(0, col_count)
        if show_tve:
            self.table.setHorizontalHeaderLabels(
                ['#', 'LRN', "Learner's Name", 'Sex', 'TVE Major', 'Status', 'Action']
            )
        else:
            self.table.setHorizontalHeaderLabels(
                ['#', 'LRN', "Learner's Name", 'Sex', 'Status', 'Action']
            )
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)
        if show_tve:
            hdr.setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(42)
        self.table.setMinimumHeight(360)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def _make_stat_card(self, label, value, accent_color):
        card = QFrame()
        card.setMinimumSize(150, 92)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setStyleSheet(f'''
            QFrame {{
                background:white; border-radius:8px;
                border-top: 4px solid {accent_color};
                border: 1px solid #e2e8f0;
            }}
        ''')
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(12, 8, 12, 8)
        val_lbl = QLabel(value)
        val_lbl.setObjectName('val')
        val_lbl.setStyleSheet(f'font-size:22px; font-weight:bold; color:{accent_color};')
        key_lbl = QLabel(label)
        key_lbl.setStyleSheet('font-size:11px; color:#6b7280;')
        key_lbl.setWordWrap(True)
        vbox.addWidget(val_lbl)
        vbox.addWidget(key_lbl)
        return card

    def _update_stat_card(self, card, value):
        card.findChild(QLabel, 'val').setText(str(value))

    def load_section(self, section, grade):
        self.section = section
        self.grade = grade
        self.section_title.setText(section.name)
        self.breadcrumb.setText(
            f'Enrollment / JHS / Grade {grade} / Sections / {section.name}'
        )
        self.refresh()

    def refresh(self):
        if not self.section:
            return
        self._all_learners = Learner.get_all(
            grade=self.grade, level='JHS', section_id=self.section.id
        )
        self._populate_table(self._all_learners)

    def _filter_table(self, text):
        q = text.strip().lower()
        filtered = (
            [l for l in self._all_learners
             if q in l.full_name.lower() or q in l.lrn.lower()]
            if q else self._all_learners
        )
        self._populate_table(filtered)

    def _populate_table(self, learners):
        self.table.setRowCount(0)
        enrolled = pending = 0
        show_tve = self.grade in (8, 9, 10)

        for idx, l in enumerate(learners):
            r = self.table.rowCount()
            self.table.insertRow(r)

            num_item = QTableWidgetItem(str(idx + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(r, 0, num_item)
            self.table.setItem(r, 1, QTableWidgetItem(l.lrn))
            self.table.setItem(r, 2, QTableWidgetItem(l.full_name))
            self.table.setItem(r, 3, QTableWidgetItem(l.sex or ''))

            col = 4
            if show_tve:
                self.table.setItem(r, col, QTableWidgetItem(getattr(l, 'tve_major', '') or ''))
                col += 1

            badge_container = QWidget()
            bl = QHBoxLayout(badge_container)
            bl.setContentsMargins(4, 2, 4, 2)
            bl.addWidget(make_status_badge(l.status))
            self.table.setCellWidget(r, col, badge_container)
            col += 1

            edit_btn = QPushButton('Edit')
            edit_btn.setStyleSheet(
                'background:#0369a1; color:white; border-radius:4px;'
                'padding:4px 12px; font-size:11px;'
            )
            edit_btn.clicked.connect(lambda _, learner=l: self.edit_requested.emit(learner))
            self.table.setCellWidget(r, col, edit_btn)

            if l.status == 'Enrolled':
                enrolled += 1
            elif l.status == 'Pending':
                pending += 1

        self._update_stat_card(self.stat_total,    len(learners))
        self._update_stat_card(self.stat_enrolled, enrolled)
        self._update_stat_card(self.stat_pending,  pending)


# ---------------------------------------------------------------------------
# JHS Edit Modal
# ---------------------------------------------------------------------------
class JHSEditModal(QDialog):
    saved = pyqtSignal()

    def __init__(self, learner, grade, parent=None):
        super().__init__(parent)
        self.learner = learner
        self.grade = grade
        self.setWindowTitle('Edit JHS Learner')
        self.setMinimumSize(860, 700)
        self.setModal(True)
        self._selected_section_id = getattr(learner, 'section_id', None)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet('background:#0c4a6e;')
        header.setFixedHeight(80)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(24, 0, 24, 0)

        name_col = QVBoxLayout()
        self.header_name = QLabel(self.learner.full_name)
        self.header_name.setStyleSheet('color:white; font-size:18px; font-weight:bold;')
        self.header_lrn = QLabel(f'LRN: {self.learner.lrn}')
        self.header_lrn.setStyleSheet('color:#bae6fd; font-size:12px;')
        name_col.addWidget(self.header_name)
        name_col.addWidget(self.header_lrn)
        h_layout.addLayout(name_col)
        h_layout.addStretch()

        badge_colors = {'Enrolled': '#1d4ed8', 'Pending': '#d97706', 'Dropped': '#dc2626'}
        bc = badge_colors.get(self.learner.status, '#6b7280')
        self.status_badge = QLabel(self.learner.status)
        self.status_badge.setStyleSheet(
            f'background:{bc}; color:white; border-radius:6px;'
            'padding:4px 14px; font-weight:bold; font-size:13px;'
        )
        h_layout.addWidget(self.status_badge)
        root.addWidget(header)

        # Scrollable body
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        body_widget = QWidget()
        body = QVBoxLayout(body_widget)
        body.setContentsMargins(24, 20, 24, 20)
        body.setSpacing(16)

        # Section assignment
        body.addWidget(self._section_label('Section Assignment'))
        sections = Section.get_all(grade=self.grade, level='JHS')
        self.section_pills = {}
        pill_row = QHBoxLayout()
        pill_row.setSpacing(8)
        for s in sections:
            pill = QPushButton(s.name)
            pill.setCheckable(True)
            pill.setChecked(s.id == self._selected_section_id)
            pill.setStyleSheet(self._pill_style(pill.isChecked()))
            pill.clicked.connect(lambda _, sid=s.id, p=pill: self._on_pill(sid, p))
            self.section_pills[s.id] = pill
            pill_row.addWidget(pill)
        pill_row.addStretch()
        body.addLayout(pill_row)

        # Status buttons
        body.addWidget(self._section_label('Change Status'))
        status_row = QHBoxLayout()
        status_row.setSpacing(8)
        for st, color in [('Enrolled', '#1d4ed8'), ('Pending', '#d97706'), ('Dropped', '#dc2626')]:
            btn = QPushButton(st)
            active = (self.learner.status == st)
            btn.setStyleSheet(
                f'background:{color}; color:white; border-radius:6px;'
                f'padding:6px 18px; font-weight:bold;'
                + ('border: 3px solid white;' if active else 'opacity:0.7;')
            )
            btn.clicked.connect(lambda _, s=st: self._set_status(s))
            status_row.addWidget(btn)
        status_row.addStretch()
        body.addLayout(status_row)

        # Learner Info
        body.addWidget(self._section_label('Learner Information'))
        self.fields = {}
        info_grid = QGridLayout()
        info_grid.setSpacing(10)
        fields_info = [
            (0, 0, 'Last Name',   'last_name'),
            (0, 1, 'First Name',  'first_name'),
            (1, 0, 'Middle Name', 'middle_name'),
            (1, 1, 'LRN',         'lrn'),
            (2, 0, 'Birthdate',   'birthdate'),
            (2, 1, 'Sex',         'sex'),
            (3, 0, 'Age',         'age'),
            (3, 1, 'Mother Tongue', 'mother_tongue'),
        ]
        for row, col, label, attr in fields_info:
            info_grid.addWidget(QLabel(label), row, col * 2)
            le = QLineEdit(str(getattr(self.learner, attr, '') or ''))
            info_grid.addWidget(le, row, col * 2 + 1)
            self.fields[attr] = le
        body.addLayout(info_grid)

        # Address
        body.addWidget(self._section_label('Address'))
        addr_grid = QGridLayout()
        addr_grid.setSpacing(10)
        for row, col, label, attr in [
            (0, 0, 'House No.', 'house_no'),
            (0, 1, 'Street', 'street'),
            (1, 0, 'Barangay', 'barangay'),
            (1, 1, 'Municipality', 'municipality'),
            (2, 0, 'Province', 'province'),
            (2, 1, 'ZIP Code', 'zip_code'),
        ]:
            addr_grid.addWidget(QLabel(label), row, col * 2)
            le = QLineEdit(str(getattr(self.learner, attr, '') or ''))
            addr_grid.addWidget(le, row, col * 2 + 1)
            self.fields[attr] = le
        body.addLayout(addr_grid)

        # Parent / Guardian
        body.addWidget(self._section_label('Parent / Guardian'))
        pg_grid = QGridLayout()
        pg_grid.setSpacing(10)
        for row, col, label, attr in [
            (0, 0, "Father's Last Name", 'father_last_name'),
            (0, 1, "Father's First Name", 'father_first_name'),
            (1, 0, "Father's Contact", 'father_contact'),
            (1, 1, "Mother's Last Name", 'mother_last_name'),
            (2, 0, "Mother's First Name", 'mother_first_name'),
            (2, 1, "Mother's Contact", 'mother_contact'),
            (3, 0, "Guardian's Last Name", 'guardian_last_name'),
            (3, 1, "Guardian's First Name", 'guardian_first_name'),
            (4, 0, 'Guardian Contact', 'guardian_contact'),
        ]:
            pg_grid.addWidget(QLabel(label), row, col * 2)
            le = QLineEdit(str(getattr(self.learner, attr, '') or ''))
            pg_grid.addWidget(le, row, col * 2 + 1)
            self.fields[attr] = le
        body.addLayout(pg_grid)

        # Previous School
        body.addWidget(self._section_label('Previous School'))
        ps_grid = QGridLayout()
        ps_grid.setSpacing(10)
        for row, col, label, attr in [
            (0, 0, 'Last Grade Completed', 'last_grade_completed'),
            (0, 1, 'School Year', 'last_sy_completed'),
            (1, 0, 'School Attended', 'last_school_attended'),
        ]:
            ps_grid.addWidget(QLabel(label), row, col * 2)
            le = QLineEdit(str(getattr(self.learner, attr, '') or ''))
            ps_grid.addWidget(le, row, col * 2 + 1)
            self.fields[attr] = le
        body.addLayout(ps_grid)

        # TVE Major (Grades 8-10)
        if self.grade in (8, 9, 10):
            body.addWidget(self._section_label('TVE Major'))
            tve_grid = QGridLayout()
            tve_grid.setSpacing(10)
            tve_grid.addWidget(QLabel('TVE Major'), 0, 0)
            le = QLineEdit(str(getattr(self.learner, 'tve_major', '') or ''))
            tve_grid.addWidget(le, 0, 1)
            self.fields['tve_major'] = le
            body.addLayout(tve_grid)

        body.addStretch()
        scroll.setWidget(body_widget)
        root.addWidget(scroll)

        # Footer
        footer = QFrame()
        footer.setStyleSheet('background:#f8fafc; border-top:1px solid #e2e8f0;')
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(24, 12, 24, 12)
        f_layout.addStretch()

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setStyleSheet(
            'background:white; color:#374151; border:1px solid #d1d5db;'
            'border-radius:6px; padding:8px 20px;'
        )
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton('Save Changes')
        save_btn.setStyleSheet(
            'background:#0369a1; color:white; border-radius:6px;'
            'padding:8px 20px; font-weight:bold;'
        )
        save_btn.clicked.connect(self._save)

        f_layout.addWidget(cancel_btn)
        f_layout.addWidget(save_btn)
        root.addWidget(footer)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            'font-size:13px; font-weight:bold; color:#0c4a6e;'
            'border-bottom:2px solid #bae6fd; padding-bottom:4px;'
        )
        return lbl

    def _pill_style(self, active):
        if active:
            return ('background:#0369a1; color:white; border-radius:16px;'
                    'padding:6px 16px; font-weight:bold; border:none;')
        return ('background:#e0f2fe; color:#0369a1; border-radius:16px;'
                'padding:6px 16px; border:none;')

    def _on_pill(self, section_id, pill):
        if self._selected_section_id == section_id:
            self._selected_section_id = None
        else:
            self._selected_section_id = section_id
        for sid, p in self.section_pills.items():
            p.setChecked(sid == self._selected_section_id)
            p.setStyleSheet(self._pill_style(p.isChecked()))

    def _set_status(self, status):
        self.learner.status = status
        badge_colors = {'Enrolled': '#1d4ed8', 'Pending': '#d97706', 'Dropped': '#dc2626'}
        bc = badge_colors.get(status, '#6b7280')
        self.status_badge.setText(status)
        self.status_badge.setStyleSheet(
            f'background:{bc}; color:white; border-radius:6px;'
            'padding:4px 14px; font-weight:bold; font-size:13px;'
        )

    def _save(self):
        status = self.learner.status
        if self._selected_section_id and status == 'Pending':
            status = 'Enrolled'
        elif not self._selected_section_id and status == 'Enrolled':
            status = 'Pending'
        try:
            birthdate_text = self.fields['birthdate'].text().strip()
            birthdate_value = (
                date.fromisoformat(birthdate_text)
                if birthdate_text else self.learner.birthdate
            )
            Learner.update(
                self.learner.id,
                last_name=self.fields['last_name'].text().strip(),
                first_name=self.fields['first_name'].text().strip(),
                middle_name=self.fields['middle_name'].text().strip(),
                lrn=self.fields['lrn'].text().strip(),
                birthdate=birthdate_value,
                sex=self.fields['sex'].text().strip(),
                age=int(self.fields['age'].text().strip() or 0),
                mother_tongue=self.fields['mother_tongue'].text().strip(),
                house_no=self.fields['house_no'].text().strip(),
                street=self.fields['street'].text().strip(),
                barangay=self.fields['barangay'].text().strip(),
                municipality=self.fields['municipality'].text().strip(),
                province=self.fields['province'].text().strip(),
                zip_code=self.fields['zip_code'].text().strip(),
                father_last_name=self.fields['father_last_name'].text().strip(),
                father_first_name=self.fields['father_first_name'].text().strip(),
                father_contact=self.fields['father_contact'].text().strip(),
                mother_last_name=self.fields['mother_last_name'].text().strip(),
                mother_first_name=self.fields['mother_first_name'].text().strip(),
                mother_contact=self.fields['mother_contact'].text().strip(),
                guardian_last_name=self.fields['guardian_last_name'].text().strip(),
                guardian_first_name=self.fields['guardian_first_name'].text().strip(),
                guardian_contact=self.fields['guardian_contact'].text().strip(),
                last_grade_completed=self.fields['last_grade_completed'].text().strip(),
                last_sy_completed=self.fields['last_sy_completed'].text().strip(),
                last_school_attended=self.fields['last_school_attended'].text().strip(),
                section_id=self._selected_section_id,
                status=status,
                tve_major=self.fields.get('tve_major').text().strip()
                if 'tve_major' in self.fields else self.learner.tve_major,
            )
            self.saved.emit()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, 'Invalid Age', 'Age must be a valid number.')
        except Exception as e:
            show_error(self, 'Unable to Save Learner', e)


# ---------------------------------------------------------------------------
# Main JHS Sections Page
# ---------------------------------------------------------------------------
class JHSSectionsPage(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.grid_view   = SectionsGridView(self.grade)
        self.detail_view = SectionDetailView(self.grade)

        self.grid_view.section_opened.connect(self._open_section)
        self.detail_view.back_requested.connect(self._back_to_grid)
        self.detail_view.edit_requested.connect(self._open_edit_modal)

        self.stack.addWidget(self.grid_view)
        self.stack.addWidget(self.detail_view)
        layout.addWidget(self.stack)

    def _open_section(self, section):
        self.detail_view.load_section(section, self.grade)
        self.stack.setCurrentWidget(self.detail_view)

    def _back_to_grid(self):
        self.grid_view.refresh()
        self.stack.setCurrentWidget(self.grid_view)

    def _open_edit_modal(self, learner):
        modal = JHSEditModal(learner, self.grade, self)
        modal.saved.connect(self.detail_view.refresh)
        modal.exec_()

    def refresh(self):
        self.grid_view.refresh()
