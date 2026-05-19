from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView,
    QScrollArea, QFrame, QLineEdit, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from core.models import Learner

# Color shortcuts
TEXT    = '#052e16'
MUTED   = '#4b7a5a'
BG      = '#f0fdf4'
CARD    = '#ffffff'
BORDER  = '#d1fae5'
PRIMARY = '#16a34a'
RED     = '#dc2626'
TVL     = '#0f766e'
YELLOW  = '#d97706'


class SHSPendingPage(QWidget):
    def __init__(self, grade, parent=None):
        super().__init__(parent, Qt.Window)
        self.grade = grade
        self.pending = []
        self.search_text = ''
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        self.setStyleSheet(f'background: {BG};')
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self.make_topbar())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea { border: none; background: #f0fdf4; }')

        content = QWidget()
        content.setStyleSheet(f'background: {BG};')
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(0)

        # breadcrumb
        bc = QLabel(
            f'Enrollment / Grade {self.grade} / '
            f'<span style="color: {PRIMARY}; font-weight: 600;">Pending</span>'
        )
        bc.setStyleSheet(f'font-size: 12px; color: {MUTED}; background: transparent;')
        layout.addWidget(bc)
        layout.addSpacing(16)

        h1 = QLabel('PENDING LEARNERS')
        h1.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {TEXT}; background: transparent;')
        layout.addWidget(h1)

        self.subtitle = QLabel(f'Grade {self.grade} · 0 learners awaiting completion')
        self.subtitle.setStyleSheet(f'font-size: 13px; color: {MUTED}; background: transparent;')
        layout.addWidget(self.subtitle)
        layout.addSpacing(20)

        layout.addWidget(self.make_stat_cards())
        layout.addWidget(self.make_table_card())

        scroll.setWidget(content)
        outer.addWidget(scroll)

    def make_topbar(self):
        bar = QFrame()
        bar.setFixedHeight(56)
        bar.setStyleSheet(f'QFrame {{ background: {CARD}; border-bottom: 1px solid {BORDER}; border-radius: 0; }}')

        row = QHBoxLayout(bar)
        row.setContentsMargins(28, 0, 20, 0)
        row.setSpacing(12)

        title = QLabel(f'Grade {self.grade} – Pending Learners')
        title.setStyleSheet(f'font-size: 15px; font-weight: 800; color: {TEXT}; background: transparent;')
        row.addWidget(title)

        badge = QLabel('PENDING')
        badge.setStyleSheet(
            f'font-size: 11px; font-weight: 700; color: {RED}; background: #fee2e2;'
            f'border-radius: 6px; padding: 3px 10px;'
        )
        row.addWidget(badge)
        row.addStretch()

        back = QPushButton('← Back to Report')
        back.setCursor(Qt.PointingHandCursor)
        back.setStyleSheet(
            f'QPushButton {{ border: 1.5px solid {BORDER}; border-radius: 8px; '
            f'font-size: 12px; font-weight: 600; color: {TEXT}; background: {BG}; padding: 6px 16px; }}'
            f'QPushButton:hover {{ background: #dcfce7; }}'
        )
        back.clicked.connect(self.close)
        row.addWidget(back)
        return bar

    def make_stat_cards(self):
        stats_row = QWidget()
        stats_row.setStyleSheet('background: transparent;')
        row = QHBoxLayout(stats_row)
        row.setContentsMargins(0, 0, 0, 24)
        row.setSpacing(16)

        self.stat_nums = {}
        for key, label, color in [
            ('total',  'Total Pending', RED),
            ('female', 'Female',        '#059669'),
            ('male',   'Male',          '#0891b2'),
        ]:
            card = QFrame()
            card.setStyleSheet(f'QFrame {{ background: {CARD}; border: none; border-radius: 14px; }}')
            cv = QVBoxLayout(card)
            cv.setContentsMargins(24, 20, 24, 20)
            cv.setSpacing(8)

            bar = QFrame()
            bar.setFixedHeight(3)
            bar.setStyleSheet(f'background: {color}; border: none; border-radius: 3px;')
            cv.addWidget(bar)

            lbl = QLabel(label.upper())
            lbl.setStyleSheet(f'font-size: 10px; font-weight: 700; color: {MUTED}; letter-spacing: 0.8px; background: transparent;')
            num = QLabel('0')
            num.setStyleSheet(f'font-size: 34px; font-weight: 800; color: {color}; background: transparent;')
            cv.addWidget(lbl)
            cv.addWidget(num)
            self.stat_nums[key] = num
            row.addWidget(card, 1)

        return stats_row

    def make_table_card(self):
        card = QFrame()
        card.setStyleSheet(f'QFrame {{ background: {CARD}; border: none; border-radius: 16px; }}')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # header with search
        hdr = QFrame()
        hdr.setFixedHeight(52)
        hdr.setStyleSheet(
            'QFrame { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,'
            'stop:0 #7f1d1d, stop:1 #991b1b); border: none; border-radius: 0px; }'
        )
        hdr_row = QHBoxLayout(hdr)
        hdr_row.setContentsMargins(24, 0, 20, 0)
        hdr_row.setSpacing(10)

        ico = QLabel('⏳')
        ico.setStyleSheet('font-size: 15px; background: transparent;')
        hdr_row.addWidget(ico)

        self.hdr_title = QLabel(f'PENDING LEARNERS  ·  GRADE {self.grade}')
        self.hdr_title.setStyleSheet('font-size: 13px; font-weight: 700; color: #ffffff; background: transparent;')
        hdr_row.addWidget(self.hdr_title)
        hdr_row.addStretch()

        search_wrap = QFrame()
        search_wrap.setStyleSheet('QFrame { background: rgba(255,255,255,0.12); border: none; border-radius: 50px; }')
        sw = QHBoxLayout(search_wrap)
        sw.setContentsMargins(10, 0, 10, 0)
        sw.setSpacing(4)
        sw.addWidget(QLabel('🔍'))

        self.search = QLineEdit()
        self.search.setPlaceholderText('🔍  Search by name or LRN...')
        self.search.setStyleSheet(
            'QLineEdit { border: none; background: transparent; font-size: 12px;'
            'color: #ffffff; padding: 7px 0; min-width: 200px; }'
        )
        self.search.textChanged.connect(self.on_search)
        sw.addWidget(self.search)
        hdr_row.addWidget(search_wrap)
        layout.addWidget(hdr)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f'background: {BORDER}; border: none;')
        layout.addWidget(sep)

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            '#', 'LRN', "Learner's Name", 'Sex', 'Track', 'Electives', 'Semester', '4Ps', 'Action'
        ])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        hh.setSectionResizeMode(5, QHeaderView.Stretch)
        hh.setSectionResizeMode(8, QHeaderView.Fixed)
        self.table.setColumnWidth(8, 200)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.setStyleSheet(
            f'QTableWidget {{ background: {CARD}; border: none; font-size: 12px; }}'
            f'QTableWidget::item {{ padding: 10px 14px; border-bottom: 1px solid {BORDER}; }}'
            f'QTableWidget::item:selected {{ background: rgba(220,38,38,0.06); color: {TEXT}; }}'
            f'QHeaderView::section {{ background: {BG}; padding: 11px 14px; font-size: 10.5px;'
            f'font-weight: 700; color: {MUTED}; letter-spacing: 0.8px;'
            f'border: none; border-bottom: 1px solid {BORDER}; }}'
        )
        self.table.doubleClicked.connect(self.open_edit_by_click)
        layout.addWidget(self.table)

        self.footer = QLabel('')
        self.footer.setContentsMargins(24, 8, 24, 8)
        self.footer.setStyleSheet(
            f'font-size: 12px; color: {MUTED}; background: {BG};'
            f'border-top: 1px solid {BORDER};'
        )
        layout.addWidget(self.footer)
        return card

    def refresh(self):
        all_lrn = Learner.get_all(grade=self.grade, level='SHS')
        self.pending = [l for l in all_lrn if l.status == 'Pending']

        total   = len(self.pending)
        females = sum(1 for l in self.pending if l.sex == 'F')
        males   = sum(1 for l in self.pending if l.sex == 'M')

        self.subtitle.setText(f'Grade {self.grade} · {total} learner{"s" if total != 1 else ""} awaiting completion')
        self.stat_nums['total'].setText(str(total))
        self.stat_nums['female'].setText(str(females))
        self.stat_nums['male'].setText(str(males))
        self.fill_table()

    def get_filtered(self):
        q = self.search_text.lower()
        if not q:
            return self.pending
        return [l for l in self.pending if q in l.full_name.lower() or q in l.lrn]

    def fill_table(self):
        rows = self.get_filtered()
        self.table.setRowCount(len(rows))

        for r, learner in enumerate(rows):
            num = QTableWidgetItem(str(r + 1))
            num.setTextAlignment(Qt.AlignCenter)
            num.setForeground(QColor(MUTED))
            self.table.setItem(r, 0, num)

            lrn_item = QTableWidgetItem(learner.lrn)
            lrn_item.setForeground(QColor(PRIMARY))
            lrn_item.setFont(QFont('Consolas', 10))
            self.table.setItem(r, 1, lrn_item)

            name_item = QTableWidgetItem(learner.full_name)
            name_item.setData(Qt.UserRole, learner.id)
            name_item.setForeground(QColor(TEXT))
            f = QFont()
            f.setWeight(QFont.DemiBold)
            name_item.setFont(f)
            self.table.setItem(r, 2, name_item)

            self.table.setItem(r, 3, QTableWidgetItem('Male' if learner.sex == 'M' else 'Female'))

            track_item = QTableWidgetItem(learner.track or '—')
            track_item.setForeground(QColor(PRIMARY if learner.track == 'Academic' else TVL))
            self.table.setItem(r, 4, track_item)

            elv = ', '.join(learner.electives_list) if learner.electives else '—'
            elv_item = QTableWidgetItem(elv)
            elv_item.setForeground(QColor(MUTED))
            self.table.setItem(r, 5, elv_item)

            self.table.setItem(r, 6, QTableWidgetItem(learner.semester or '—'))
            self.table.setItem(r, 7, QTableWidgetItem('Yes' if learner.is_four_ps else 'No'))

            edit_btn = QPushButton('✏  Edit')
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet(
                'QPushButton { background: #fef2f2; color: #dc2626; border: 1.5px solid #fecaca;'
                'border-radius: 8px; font-size: 12px; font-weight: 700; padding: 6px 20px; }'
                'QPushButton:hover { background: #dc2626; color: #ffffff; }'
            )
            lid = learner.id
            edit_btn.clicked.connect(lambda _, i=lid: self.open_edit(i))

            wrap = QWidget()
            wrap.setStyleSheet('background: transparent;')
            wh = QHBoxLayout(wrap)
            wh.setContentsMargins(8, 4, 8, 4)
            wh.addWidget(edit_btn)
            self.table.setCellWidget(r, 8, wrap)

        total = len(self.pending)
        shown = len(rows)
        self.footer.setText(f'Showing {shown} of {total} pending learner{"s" if total != 1 else ""}')

    def on_search(self, text):
        self.search_text = text
        self.fill_table()

    def open_edit(self, lid):
        from enrollment.shs_learner_edit import SHSLearnerEditDialog
        dlg = SHSLearnerEditDialog(lid, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            self.refresh()

    def open_edit_by_click(self, index):
        item = self.table.item(index.row(), 2)
        if item:
            lid = item.data(Qt.UserRole)
            if lid:
                self.open_edit(lid)
