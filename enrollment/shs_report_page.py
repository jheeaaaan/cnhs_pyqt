# enrollment/shs_report_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView,
    QScrollArea, QFrame, QSizePolicy, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from core.models import Learner, Section

# ── Colour tokens (mirrors prototype G object exactly) ──────────────────────
G = {
    'text':          '#052e16',
    'muted':         '#4b7a5a',
    'bg':            '#f0fdf4',
    'card':          '#ffffff',
    'border':        '#d1fae5',
    'primary':       '#16a34a',
    'accent':        '#fbbf24',
    'red':           '#dc2626',
    'sectionHeader': '#14532d',
    'yellow':        '#d97706',
    'tvl':           '#0f766e',
}

ACADEMIC_ELECTIVES = [
    'Humanities and Social Sciences',
    'Science, Technology, Engineering and Mathematics',
    'General Academic Strand',
    'Accountancy, Business and Management',
    'Creative Writing / Literary Arts',
    'Sports',
]
TVL_ELECTIVES = [
    'Home Economics',
    'Agri-Fishery Arts',
    'Industrial Arts',
    'Information and Communications Technology (ICT)',
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def _label(text, size=13, weight=400, color=None, bg='transparent', wrap=False):
    l = QLabel(text)
    l.setStyleSheet(
        f'font-size:{size}px;font-weight:{weight};'
        f'color:{color or G["text"]};background:{bg};'
    )
    if wrap:
        l.setWordWrap(True)
    return l


def _make_stat_card(label_text, value, sub_text, color):
    """Matches prototype stat cards: coloured top stripe, big number, sub text."""
    card = QFrame()
    card.setObjectName('statCard')
    card.setMinimumSize(150, 112)
    card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    card.setStyleSheet(
        'QFrame#statCard{background:#ffffff;border:1px solid #d1fae5;border-radius:14px;}'
    )
    outer = QVBoxLayout(card)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    stripe = QFrame()
    stripe.setFixedHeight(3)
    stripe.setStyleSheet(f'background:{color};border:none;border-radius:14px 14px 0 0;')
    outer.addWidget(stripe)

    inner = QVBoxLayout()
    inner.setContentsMargins(20, 14, 20, 16)
    inner.setSpacing(2)

    lbl = QLabel(label_text.upper())
    lbl.setStyleSheet(
        f'font-size:10px;font-weight:700;color:{G["muted"]};'
        f'letter-spacing:0.8px;background:transparent;'
    )
    lbl.setWordWrap(True)
    inner.addWidget(lbl)

    num = QLabel(str(value))
    num.setStyleSheet(
        f'font-size:30px;font-weight:800;color:{color};background:transparent;'
    )
    inner.addWidget(num)

    sub = QLabel(sub_text)
    sub.setStyleSheet(f'font-size:11px;color:{G["muted"]};background:transparent;')
    sub.setWordWrap(True)
    inner.addWidget(sub)

    outer.addLayout(inner)
    return card


def _make_section_header_widget(icon, title, gradient_css, btn_text=None, btn_callback=None):
    hdr = QFrame()
    hdr.setMinimumHeight(60)
    hdr.setStyleSheet(
        f'QFrame{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,{gradient_css});'
        f'border:none;border-radius:0px;}}'
    )
    row = QHBoxLayout(hdr)
    row.setContentsMargins(24, 0, 20, 0)
    row.setSpacing(10)

    ico = QLabel(icon)
    ico.setStyleSheet('font-size:15px;background:transparent;')
    row.addWidget(ico)

    t = QLabel(title)
    t.setStyleSheet('font-size:13px;font-weight:700;color:#ffffff;background:transparent;')
    t.setWordWrap(True)
    row.addWidget(t)
    row.addStretch()

    if btn_text and btn_callback:
        btn = QPushButton(btn_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            'QPushButton{padding:6px 14px;border-radius:8px;font-size:12px;font-weight:700;'
            'border:1.5px solid rgba(255,255,255,0.3);background:rgba(255,255,255,0.1);color:#ffffff;}'
            'QPushButton:hover{background:rgba(255,255,255,0.22);}'
        )
        btn.clicked.connect(btn_callback)
        row.addWidget(btn)

    return hdr


class _ElectiveBarRow(QWidget):
    """Full-name stacked elective bar row — matches prototype ElectiveBarRow."""

    def __init__(self, label, count, total, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background:transparent;')
        pct = round((count / max(total, 1)) * 100)
        self._fill_pct = max(pct, 3) if count > 0 else 0
        self._color = color

        v = QVBoxLayout(self)
        v.setContentsMargins(0, 8, 0, 0)
        v.setSpacing(7)

        name_lbl = QLabel(label)
        name_lbl.setStyleSheet(
            f'font-size:12px;font-weight:700;color:{G["text"]};background:transparent;'
        )
        name_lbl.setWordWrap(True)
        v.addWidget(name_lbl)

        bar_row = QHBoxLayout()
        bar_row.setContentsMargins(0, 0, 0, 0)
        bar_row.setSpacing(10)

        self._bar_bg = QFrame()
        self._bar_bg.setFixedHeight(16)
        self._bar_bg.setStyleSheet(
            f'QFrame{{background:{G["bg"]};border-radius:5px;border:1px solid {G["border"]};}}'
        )
        self._bar_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._bar_fill = QFrame(self._bar_bg)
        self._bar_fill.setFixedHeight(16)
        self._bar_fill.setStyleSheet(f'QFrame{{background:{color};border-radius:5px;border:none;}}')
        self._bar_bg.resizeEvent = self._resize_fill

        bar_row.addWidget(self._bar_bg)

        pct_lbl = QLabel(f'{pct}%')
        pct_lbl.setStyleSheet(
            f'font-size:11px;font-weight:700;color:{color};background:transparent;'
        )
        pct_lbl.setFixedWidth(38)
        pct_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        bar_row.addWidget(pct_lbl)
        v.addLayout(bar_row)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f'background:{G["border"]};border:none;')
        v.addWidget(sep)

    def _resize_fill(self, event):
        self._bar_fill.setFixedWidth(max(0, int(self._bar_bg.width() * self._fill_pct / 100)))


class _BarRow(QWidget):
    """Horizontal bar row for track breakdown."""

    def __init__(self, label, count, total, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background:transparent;')
        pct = round((count / max(total, 1)) * 100)
        self._fill_pct = max(pct, 3) if count > 0 else 0

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)

        lbl = QLabel(label)
        lbl.setStyleSheet(f'font-size:11px;font-weight:600;color:{G["text"]};background:transparent;')
        lbl.setFixedWidth(100)
        row.addWidget(lbl)

        self._bar_bg = QFrame()
        self._bar_bg.setFixedHeight(18)
        self._bar_bg.setStyleSheet(f'QFrame{{background:{G["bg"]};border-radius:5px;border:none;}}')
        self._bar_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._bar_fill = QFrame(self._bar_bg)
        self._bar_fill.setFixedHeight(18)
        self._bar_fill.setStyleSheet(f'QFrame{{background:{color};border-radius:5px;border:none;}}')
        self._bar_bg.resizeEvent = self._resize_fill

        row.addWidget(self._bar_bg)

        pct_lbl = QLabel(f'{pct}%')
        pct_lbl.setStyleSheet(f'font-size:10px;color:{G["muted"]};background:transparent;')
        pct_lbl.setFixedWidth(28)
        pct_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row.addWidget(pct_lbl)

    def _resize_fill(self, event):
        self._bar_fill.setFixedWidth(max(0, int(self._bar_bg.width() * self._fill_pct / 100)))


class _ElectiveFilterBar(QWidget):
    """Pill-style elective filter bar."""

    def __init__(self, electives, learners, color, on_change, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background:{G["bg"]};border:none;')
        self._electives = electives
        self._learners = learners
        self._color = color
        self._on_change = on_change
        self._active = 'ALL'
        self._buttons = {}

        v = QVBoxLayout(self)
        v.setContentsMargins(24, 12, 24, 12)
        v.setSpacing(8)

        hdr = QLabel('FILTER BY ELECTIVE:')
        hdr.setStyleSheet(
            f'font-size:10.5px;font-weight:700;color:{G["muted"]};'
            f'letter-spacing:0.8px;background:transparent;'
        )
        v.addWidget(hdr)

        pills = QHBoxLayout()
        pills.setContentsMargins(0, 0, 0, 0)
        pills.setSpacing(6)

        all_btn = self._pill('ALL', f'All ({len(learners)})')
        pills.addWidget(all_btn)

        for e in electives:
            cnt = sum(1 for l in learners if e in (l.electives or ''))
            short = (e[:12] + '…') if len(e) > 14 else e
            pills.addWidget(self._pill(e, f'{short} ({cnt})'))

        pills.addStretch()
        v.addLayout(pills)

        self._active_lbl = QLabel('')
        self._active_lbl.setStyleSheet(f'font-size:11px;color:{G["muted"]};background:transparent;')
        self._active_lbl.hide()
        v.addWidget(self._active_lbl)

    def _pill(self, key, text):
        active = key == self._active
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(active)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip(key)
        self._style(btn, active)
        btn.clicked.connect(lambda _, k=key: self._select(k))
        self._buttons[key] = btn
        return btn

    def _style(self, btn, active):
        if active:
            btn.setStyleSheet(
                f'QPushButton{{padding:5px 14px;border-radius:20px;font-size:12px;font-weight:600;'
                f'border:1.5px solid {self._color};background:{self._color};color:#fff;}}'
            )
        else:
            btn.setStyleSheet(
                f'QPushButton{{padding:5px 14px;border-radius:20px;font-size:12px;font-weight:600;'
                f'border:1.5px solid {G["border"]};background:{G["card"]};color:{G["muted"]};}}'
                f'QPushButton:hover{{border-color:{self._color};color:{self._color};}}'
            )

    def _select(self, key):
        self._active = key
        for k, b in self._buttons.items():
            self._style(b, k == key)
            b.setChecked(k == key)
        if key != 'ALL':
            self._active_lbl.setText(f'Showing: {key}')
            self._active_lbl.show()
        else:
            self._active_lbl.hide()
        self._on_change(key)


class _TrackSection(QWidget):
    STATUS_COLORS = {
        'Enrolled':    ('#15803d', 'rgba(22,163,74,0.10)'),
        'Pending':     ('#b45309', 'rgba(251,191,36,0.15)'),
        'Dropped':     ('#dc2626', 'rgba(239,68,68,0.10)'),
        'Transferred': ('#6d28d9', 'rgba(109,40,217,0.10)'),
    }

    def __init__(self, track, grade, color, gradient_css, icon, parent=None):
        super().__init__(parent)
        self.track = track
        self.grade = grade
        self.color = color
        self._all_learners = []
        self._search = ''
        self._active_elective = 'ALL'
        self._electives = ACADEMIC_ELECTIVES if track == 'Academic' else TVL_ELECTIVES

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # card wrapper
        self._card = QFrame()
        self._card.setObjectName('trackCard')
        self._card.setStyleSheet(
            f'QFrame#trackCard{{background:{G["card"]};border:1.5px solid {color}28;'
            f'border-radius:16px;}}'
        )
        card_v = QVBoxLayout(self._card)
        card_v.setContentsMargins(0, 0, 0, 0)
        card_v.setSpacing(0)

        # header (with Export CSV button + subtitle label)
        self._hdr_frame = _make_section_header_widget(
            icon, f'{track} Track', gradient_css,
            btn_text='Export CSV', btn_callback=self._export_csv,
        )
        # inject subtitle into header
        self._sub_lbl = QLabel(f'Grade {grade}')
        self._sub_lbl.setStyleSheet(
            'font-size:11px;color:rgba(255,255,255,0.65);background:transparent;'
        )
        self._sub_lbl.setWordWrap(True)
        self._hdr_frame.layout().insertWidget(2, self._sub_lbl)
        card_v.addWidget(self._hdr_frame)

        # filter bar placeholder
        self._filter_holder = QVBoxLayout()
        self._filter_holder.setContentsMargins(0, 0, 0, 0)
        self._filter_holder.setSpacing(0)
        card_v.addLayout(self._filter_holder)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f'background:{G["border"]};border:none;')
        card_v.addWidget(sep)

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ['LRN', "Learner's Name", 'Sex', 'Electives', 'Section', 'Sem', '4Ps', 'Status']
        )
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setDefaultSectionSize(44)
        self.table.setMinimumHeight(320)
        self.table.setShowGrid(False)
        self.table.verticalHeader().hide()
        self.table.setStyleSheet(
            f'QTableWidget{{background:{G["card"]};border:none;font-size:12px;}}'
            f'QTableWidget::item{{padding:10px 14px;border-bottom:1px solid {G["border"]};}}'
            f'QTableWidget::item:selected{{background:rgba(22,163,74,0.08);color:{G["text"]};}}'
            f'QHeaderView::section{{background:{G["bg"]};padding:11px 14px;font-size:10.5px;'
            f'font-weight:700;color:{G["muted"]};text-transform:uppercase;letter-spacing:0.8px;'
            f'border:none;border-bottom:1px solid {G["border"]};}}'
        )
        self.table.doubleClicked.connect(self._open_edit)
        card_v.addWidget(self.table)

        # footer
        self._footer = QLabel('')
        self._footer.setContentsMargins(24, 8, 24, 8)
        self._footer.setStyleSheet(
            f'font-size:12px;color:{G["muted"]};background:{G["bg"]};'
            f'border-top:1px solid {G["border"]};'
        )
        card_v.addWidget(self._footer)

        outer.addWidget(self._card)

    def refresh(self, all_learners, search=''):
        self._all_learners = [
            l for l in all_learners
            if l.track == self.track or
               (self.track == 'TechPro/TVL' and l.track in ('TVL', 'TechPro/TVL'))
        ]
        self._search = search
        self._active_elective = 'ALL'

        n = len(self._all_learners)
        self._sub_lbl.setText(f'Grade {self.grade} · {n} learner{"s" if n!=1 else ""} enrolled')

        # rebuild filter bar
        while self._filter_holder.count():
            item = self._filter_holder.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._filter_bar = _ElectiveFilterBar(
            self._electives, self._all_learners, self.color,
            on_change=self._on_elective_change,
        )
        self._filter_holder.addWidget(self._filter_bar)

        self._fill_table()

    def _on_elective_change(self, key):
        self._active_elective = key
        self._fill_table()

    def set_search(self, text):
        self._search = text
        self._fill_table()

    def _filtered(self):
        data = self._all_learners
        if self._active_elective != 'ALL':
            data = [l for l in data if self._active_elective in (l.electives or '')]
        if self._search:
            q = self._search.lower()
            data = [l for l in data if q in l.full_name.lower() or q in l.lrn]
        return data

    def _fill_table(self):
        rows = self._filtered()
        self.table.setRowCount(len(rows))
        for r, l in enumerate(rows):
            # LRN
            item = QTableWidgetItem(l.lrn)
            item.setForeground(QColor(G['muted']))
            item.setFont(QFont('Consolas', 10))
            self.table.setItem(r, 0, item)
            # Name
            item = QTableWidgetItem(l.full_name)
            item.setData(Qt.UserRole, l.id)
            item.setForeground(QColor(G['text']))
            f = QFont(); f.setWeight(QFont.DemiBold); item.setFont(f)
            self.table.setItem(r, 1, item)
            # Sex
            self.table.setItem(r, 2, QTableWidgetItem('Male' if l.sex == 'M' else 'Female'))
            # Electives
            elv = ', '.join(l.electives_list) if l.electives else '—'
            e_item = QTableWidgetItem(elv)
            e_item.setForeground(QColor(self.color))
            self.table.setItem(r, 3, e_item)
            # Section
            self.table.setItem(r, 4, QTableWidgetItem(l.section_name or '—'))
            # Sem
            self.table.setItem(r, 5, QTableWidgetItem(l.semester or '—'))
            # 4Ps
            self.table.setItem(r, 6, QTableWidgetItem('Yes' if l.is_four_ps else 'No'))
            # Status
            st = l.status or 'Pending'
            fg, bg = self.STATUS_COLORS.get(st, (G['muted'], G['bg']))
            s_item = QTableWidgetItem(f'  {st}  ')
            s_item.setForeground(QColor(fg))
            s_item.setBackground(QColor(bg))
            f2 = QFont(); f2.setWeight(QFont.Bold); s_item.setFont(f2)
            self.table.setItem(r, 7, s_item)

        n_track = len(self._all_learners)
        n_shown = len(rows)
        txt = f'Showing {n_shown} of {n_track} {self.track} learner{"s" if n_track!=1 else ""}'
        if self._active_elective != 'ALL':
            txt += f' · Elective: {self._active_elective}'
        self._footer.setText(txt)

    def _export_csv(self):
        import csv
        from PyQt5.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, 'Export CSV',
            f'grade{self.grade}-{self.track.replace("/","")}-enrollment.csv',
            'CSV Files (*.csv)',
        )
        if not path:
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['LRN', 'Name', 'Sex', 'Track', 'Electives', 'Section', 'Semester', '4Ps', 'Status'])
            for l in self._all_learners:
                w.writerow([l.lrn, l.full_name, l.sex, l.track, l.electives,
                             l.section_name, l.semester, 'Yes' if l.is_four_ps else 'No', l.status])

    def _open_edit(self, index):
        item = self.table.item(index.row(), 1)
        if not item:
            return
        lid = item.data(Qt.UserRole)
        if not lid:
            return
        from enrollment.shs_learner_edit import SHSLearnerEditDialog
        dlg = SHSLearnerEditDialog(lid, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            all_lrn = Learner.get_all(grade=self.grade, level='SHS')
            self.refresh(all_lrn, self._search)


# ── Main report page ──────────────────────────────────────────────────────────

class SHSReportPage(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea{border:none;background:#f0fdf4;}')

        content = QWidget()
        content.setStyleSheet('background:#f0fdf4;')
        lay = QVBoxLayout(content)
        lay.setContentsMargins(30, 28, 30, 30)
        lay.setSpacing(24)

        # ── Breadcrumb ────────────────────────────────────────────────────────
        bc = QLabel(
            f'Enrollment '
            f'<span style="color:{G["primary"]};font-weight:600;">'
            f'/ Reports / Grade {self.grade}</span>'
        )
        bc.setStyleSheet(f'font-size:12px;color:{G["muted"]};background:transparent;')
        lay.addWidget(bc)

        # ── Title row ─────────────────────────────────────────────────────────
        title_row = QHBoxLayout()
        title_row.setSpacing(16)

        left = QVBoxLayout()
        left.setSpacing(4)
        h1 = QLabel(f'Grade {self.grade} Enrollment Report')
        h1.setStyleSheet(f'font-size:24px;font-weight:800;color:{G["text"]};background:transparent;')
        left.addWidget(h1)
        sub = QLabel('Track & Elective-based overview — S.Y. 2025–2026')
        sub.setStyleSheet(f'font-size:14px;color:{G["muted"]};background:transparent;')
        left.addWidget(sub)
        title_row.addLayout(left)
        title_row.addStretch()

        lay.addLayout(title_row)

        # ── Stat cards (5 across) ─────────────────────────────────────────────
        self._stats_row = QHBoxLayout()
        self._stats_row.setSpacing(16)
        lay.addLayout(self._stats_row)

        # ── Enrollment by Track chart ─────────────────────────────────────────
        track_card = QFrame()
        track_card.setObjectName('tchart')
        track_card.setStyleSheet(
            f'QFrame#tchart{{background:{G["card"]};border:1px solid {G["border"]};'
            f'border-radius:16px;}}'
        )
        tc_v = QVBoxLayout(track_card)
        tc_v.setContentsMargins(0, 0, 0, 0)
        tc_v.setSpacing(0)
        tc_v.addWidget(_make_section_header_widget(
            '🏫', 'ENROLLMENT BY TRACK',
            'stop:0 #14532d, stop:1 #166534',
        ))
        self._track_bars = QVBoxLayout()
        self._track_bars.setContentsMargins(20, 16, 20, 16)
        self._track_bars.setSpacing(14)
        tc_v.addLayout(self._track_bars)
        lay.addWidget(track_card)

        # ── Elective charts row (Academic | TVL) ──────────────────────────────
        elv_row = QHBoxLayout()
        elv_row.setSpacing(20)

        acad_card = QFrame()
        acad_card.setObjectName('acadElv')
        acad_card.setStyleSheet(
            'QFrame#acadElv{background:#ffffff;border:1.5px solid rgba(22,163,74,0.2);border-radius:16px;}'
        )
        av = QVBoxLayout(acad_card)
        av.setContentsMargins(0, 0, 0, 0)
        av.setSpacing(0)
        av.addWidget(_make_section_header_widget(
            '📚', 'ACADEMIC TRACK — ENROLLMENT BY ELECTIVES',
            'stop:0 #14532d, stop:1 #166534',
        ))
        self._acad_elv = QVBoxLayout()
        self._acad_elv.setContentsMargins(20, 4, 20, 12)
        self._acad_elv.setSpacing(0)
        av.addLayout(self._acad_elv)
        elv_row.addWidget(acad_card, 1)

        tvl_card = QFrame()
        tvl_card.setObjectName('tvlElv')
        tvl_card.setStyleSheet(
            'QFrame#tvlElv{background:#ffffff;border:1.5px solid rgba(15,118,110,0.2);border-radius:16px;}'
        )
        tv = QVBoxLayout(tvl_card)
        tv.setContentsMargins(0, 0, 0, 0)
        tv.setSpacing(0)
        tv.addWidget(_make_section_header_widget(
            '🔧', 'TVL TRACK — ENROLLMENT BY ELECTIVES',
            'stop:0 #134e4a, stop:1 #0f766e',
        ))
        self._tvl_elv = QVBoxLayout()
        self._tvl_elv.setContentsMargins(20, 4, 20, 12)
        self._tvl_elv.setSpacing(0)
        tv.addLayout(self._tvl_elv)
        elv_row.addWidget(tvl_card, 1)

        lay.addLayout(elv_row)

        # ── Track sections ────────────────────────────────────────────────────
        self._acad_sec = _TrackSection(
            'Academic', self.grade, G['primary'],
            'stop:0 #14532d, stop:1 #166534', '📚',
        )
        lay.addWidget(self._acad_sec)

        self._tvl_sec = _TrackSection(
            'TechPro/TVL', self.grade, G['tvl'],
            'stop:0 #134e4a, stop:1 #0f766e', '🔧',
        )
        lay.addWidget(self._tvl_sec)

        scroll.setWidget(content)
        outer.addWidget(scroll)

    def refresh(self):
        all_lrn = Learner.get_all(grade=self.grade, level='SHS')
        total   = len(all_lrn)
        females = sum(1 for l in all_lrn if l.sex == 'F')
        males   = sum(1 for l in all_lrn if l.sex == 'M')
        pending = sum(1 for l in all_lrn if l.status == 'Pending')

        # stat cards
        while self._stats_row.count():
            item = self._stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        def pct(n): return f'{round(n/max(total,1)*100)}% of total'

        for label, val, sub, color in [
            ('Total Enrolled', total,   'As of April 2026',   G['primary']),
            ('Pending',        pending, 'Awaiting completion', G['red']),
            ('Female',         females, pct(females),          '#059669'),
            ('Male',           males,   pct(males),            '#0891b2'),
        ]:
            card = _make_stat_card(label, val, sub, color)
            if label == 'Pending':
                card.setCursor(Qt.PointingHandCursor)
                card.setToolTip('Click to view pending learners')
                card.mousePressEvent = lambda _e: self._open_pending_page()
            self._stats_row.addWidget(card)

        # track bars
        while self._track_bars.count():
            item = self._track_bars.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        acad = [l for l in all_lrn if l.track == 'Academic']
        tvl  = [l for l in all_lrn if l.track in ('TechPro/TVL', 'TVL')]

        self._track_bars.addWidget(_BarRow('Academic', len(acad), total, G['primary']))
        self._track_bars.addWidget(_BarRow('TechPro / TVL', len(tvl), total, G['tvl']))

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f'background:{G["border"]};border:none;')
        self._track_bars.addWidget(sep)

        legend_w = QWidget()
        legend_w.setStyleSheet('background:transparent;')
        leg = QHBoxLayout(legend_w)
        leg.setContentsMargins(0, 0, 0, 0)
        leg.setSpacing(18)
        for ltxt, lcnt, lcol in [('Academic', len(acad), G['primary']), ('TechPro/TVL', len(tvl), G['tvl'])]:
            dot = QFrame()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f'background:{lcol};border-radius:3px;border:none;')
            leg.addWidget(dot)
            lbl = QLabel(f'{ltxt}: <b>{lcnt}</b>')
            lbl.setStyleSheet(f'font-size:12px;color:{G["text"]};background:transparent;')
            leg.addWidget(lbl)
        leg.addStretch()
        self._track_bars.addWidget(legend_w)

        # elective charts
        self._rebuild_elv(self._acad_elv, acad, ACADEMIC_ELECTIVES, G['primary'])
        self._rebuild_elv(self._tvl_elv,  tvl,  TVL_ELECTIVES,      G['tvl'])

        # track sections
        self._acad_sec.refresh(all_lrn, '')
        self._tvl_sec.refresh(all_lrn, '')

    def _rebuild_elv(self, layout, learners, electives, color):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        counts = sorted(
            [(e, sum(1 for l in learners if e in (l.electives or ''))) for e in electives],
            key=lambda x: -x[1]
        )
        counts = [(e, c) for e, c in counts if c > 0]
        max_val = counts[0][1] if counts else 1

        if not counts:
            nd = QLabel('No elective data.')
            nd.setStyleSheet(f'font-size:13px;color:{G["muted"]};background:transparent;padding:16px 0;')
            layout.addWidget(nd)
            return

        for elec, count in counts:
            layout.addWidget(_ElectiveBarRow(elec, count, max_val, color))

    def _open_pending_page(self):
        from enrollment.shs_pending_page import SHSPendingPage
        page = SHSPendingPage(self.grade, parent=self)
        page.setWindowTitle(f'Grade {self.grade} – Pending Learners')
        page.setWindowModality(Qt.ApplicationModal)
        page.resize(1100, 700)
        page.show()
