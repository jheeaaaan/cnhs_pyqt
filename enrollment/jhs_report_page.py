# enrollment/jhs_report_page.py
import csv
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QFrame, QScrollArea, QSizePolicy,
    QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont
from core.errors import show_error
from core.models import Learner, Section

try:
    from enrollment.jhs_sections_page import JHSEditModal
except ImportError:
    JHSEditModal = None

try:
    from enrollment.jhs_pending_page import JHSPendingPage
except ImportError:
    JHSPendingPage = None


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
# Horizontal bar chart
# ---------------------------------------------------------------------------
class HBarChart(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.data = data or []
        self.setMinimumHeight(max(60, len(self.data) * 44))

    def set_data(self, data):
        self.data = data
        self.setMinimumHeight(max(60, len(data) * 44))
        self.update()

    def paintEvent(self, event):
        if not self.data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        max_val    = max((v for _, v, _ in self.data), default=1) or 1
        bar_area_x = 140
        bar_area_w = self.width() - bar_area_x - 70
        bar_h      = 22
        row_h      = 40
        y          = 8

        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)

        for label, value, color in self.data:
            painter.setPen(QColor('#374151'))
            painter.drawText(
                0, y, bar_area_x - 8, bar_h,
                Qt.AlignRight | Qt.AlignVCenter, str(label)
            )
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor('#e2e8f0'))
            painter.drawRoundedRect(bar_area_x, y, bar_area_w, bar_h, 4, 4)

            filled_w = int(bar_area_w * value / max_val)
            if filled_w > 0:
                painter.setBrush(QColor(color))
                painter.drawRoundedRect(bar_area_x, y, filled_w, bar_h, 4, 4)

            painter.setPen(QColor('#0f172a'))
            pct = f'{value} ({int(value / max_val * 100)}%)' if max_val else f'{value}'
            painter.drawText(
                bar_area_x + filled_w + 6, y, 70, bar_h,
                Qt.AlignLeft | Qt.AlignVCenter, pct
            )
            y += row_h

        painter.end()


# ---------------------------------------------------------------------------
# Stat Card
# ---------------------------------------------------------------------------
class StatCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, label, value, accent_color, clickable=False):
        super().__init__()
        self._clickable = clickable
        self.setFixedSize(180, 90)
        if clickable:
            self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f'''
            StatCard {{
                background:white; border-radius:8px;
                border-top: 4px solid {accent_color};
                border: 1px solid #e2e8f0;
            }}
        ''')
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(14, 10, 14, 10)

        self.val_lbl = QLabel(str(value))
        self.val_lbl.setObjectName('val')
        self.val_lbl.setStyleSheet(
            f'font-size:26px; font-weight:bold; color:{accent_color};'
        )
        self.pct_lbl = QLabel('')
        self.pct_lbl.setStyleSheet('font-size:10px; color:#9ca3af;')
        key_lbl = QLabel(label)
        key_lbl.setStyleSheet('font-size:11px; color:#6b7280;')

        vbox.addWidget(self.val_lbl)
        vbox.addWidget(self.pct_lbl)
        vbox.addWidget(key_lbl)

    def set_value(self, value, pct_text=''):
        self.val_lbl.setText(str(value))
        self.pct_lbl.setText(pct_text)

    def mousePressEvent(self, event):
        if self._clickable:
            self.clicked.emit()


def _make_chart_card(title: str):
    card = QFrame()
    card.setStyleSheet(
        'QFrame { background:white; border-radius:8px; border:1px solid #e2e8f0; }'
    )
    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 12, 16, 12)
    ttl = QLabel(title)
    ttl.setStyleSheet('font-size:13px; font-weight:bold; color:#0c4a6e;')
    layout.addWidget(ttl)
    chart = HBarChart()
    chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    layout.addWidget(chart)
    return card, chart


# ---------------------------------------------------------------------------
# JHS Report Page
# ---------------------------------------------------------------------------
class JHSReportPage(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._active_section_id = None
        self._all_learners = []
        self._current_learners = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel(f'Grade {self.grade} — JHS Enrollment Report')
        title.setStyleSheet('font-size:20px; font-weight:bold; color:#0c4a6e;')
        layout.addWidget(title)

        # Stat Cards
        stat_row = QHBoxLayout()
        self.card_total    = StatCard('Total Learners',     '0', '#0369a1')
        self.card_enrolled = StatCard('Enrolled',           '0', '#1d4ed8')
        self.card_pending  = StatCard('Pending',            '0', '#d97706', clickable=True)
        self.card_dropped  = StatCard('Dropped',            '0', '#dc2626')
        self.card_4ps      = StatCard('4Ps Beneficiaries',  '0', '#059669')
        for c in [self.card_total, self.card_enrolled, self.card_pending,
                  self.card_dropped, self.card_4ps]:
            stat_row.addWidget(c)
        stat_row.addStretch()
        self.card_pending.clicked.connect(self._open_pending_page)
        layout.addLayout(stat_row)

        # Section pills
        self.pills_row = QHBoxLayout()
        self.pills_row.setSpacing(8)
        layout.addLayout(self.pills_row)

        # Charts row
        charts_row = QHBoxLayout()
        charts_row.setSpacing(16)

        self.chart_enrollment_card, self.chart_enrollment = _make_chart_card('Enrollment by Section')
        charts_row.addWidget(self.chart_enrollment_card, 2)

        self.chart_sex_card, self.chart_sex = _make_chart_card('Sex Distribution')
        charts_row.addWidget(self.chart_sex_card, 1)

        if self.grade in (8, 9, 10):
            self.chart_tve_card, self.chart_tve = _make_chart_card('TVE Major Breakdown')
            charts_row.addWidget(self.chart_tve_card, 1)
        else:
            self.chart_tve_card = None
            self.chart_tve = None

        layout.addLayout(charts_row)

        # Table header
        table_header = QHBoxLayout()
        tbl_title = QLabel('Learner List')
        tbl_title.setStyleSheet('font-size:14px; font-weight:bold; color:#0c4a6e;')
        table_header.addWidget(tbl_title)
        table_header.addStretch()

        export_btn = QPushButton('⬇ Export CSV')
        export_btn.setStyleSheet(
            'background:#0369a1; color:white; border-radius:6px;'
            'padding:6px 14px; font-weight:bold;'
        )
        export_btn.clicked.connect(self._export_csv)
        table_header.addWidget(export_btn)
        layout.addLayout(table_header)

        # Learner table
        show_tve = self.grade in (8, 9, 10)
        col_count = 7 if show_tve else 6
        self.table = QTableWidget(0, col_count)
        if show_tve:
            self.table.setHorizontalHeaderLabels(
                ['LRN', 'Name', 'Sex', 'TVE Major', 'Status', 'Edit', '#']
            )
        else:
            self.table.setHorizontalHeaderLabels(
                ['LRN', 'Name', 'Sex', 'Status', 'Edit', '#']
            )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        scroll.setWidget(container)
        root.addWidget(scroll)

    # -----------------------------------------------------------------------
    def _rebuild_pills(self):
        while self.pills_row.count():
            item = self.pills_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sections = Section.get_all(grade=self.grade, level='JHS')

        all_pill = QPushButton('ALL')
        all_pill.setStyleSheet(self._pill_style(self._active_section_id is None))
        all_pill.clicked.connect(lambda: self._filter_by_section(None))
        self.pills_row.addWidget(all_pill)

        for s in sections:
            pill = QPushButton(s.name)
            pill.setStyleSheet(self._pill_style(self._active_section_id == s.id))
            pill.clicked.connect(lambda _, sid=s.id: self._filter_by_section(sid))
            self.pills_row.addWidget(pill)

        self.pills_row.addStretch()

    def _pill_style(self, active):
        if active:
            return ('background:#0369a1; color:white; border-radius:14px;'
                    'padding:5px 16px; font-weight:bold; border:none;')
        return ('background:#e0f2fe; color:#0369a1; border-radius:14px;'
                'padding:5px 16px; border:none;')

    def _filter_by_section(self, section_id):
        self._active_section_id = section_id
        self._rebuild_pills()
        self._update_views()

    # -----------------------------------------------------------------------
    def refresh(self):
        self._all_learners = Learner.get_all(grade=self.grade, level='JHS')
        self._rebuild_pills()
        self._update_views()

    def _update_views(self):
        if self._active_section_id is not None:
            learners = [l for l in self._all_learners
                        if l.section_id == self._active_section_id]
        else:
            learners = self._all_learners

        total    = len(learners)
        enrolled = sum(1 for l in learners if l.status == 'Enrolled')
        pending  = sum(1 for l in learners if l.status == 'Pending')
        dropped  = sum(1 for l in learners if l.status == 'Dropped')
        four_ps  = sum(1 for l in learners if getattr(l, 'is_four_ps', False))

        def pct(n):
            return f'{int(n / total * 100)}% of total' if total else '0%'

        self.card_total.set_value(total)
        self.card_enrolled.set_value(enrolled, pct(enrolled))
        self.card_pending.set_value(pending,   pct(pending))
        self.card_dropped.set_value(dropped,   pct(dropped))
        self.card_4ps.set_value(four_ps,       pct(four_ps))

        # Enrollment by section chart
        sections = Section.get_all(grade=self.grade, level='JHS')
        section_map = {s.id: s.name for s in sections}
        COLORS = ['#0369a1', '#0891b2', '#0284c7', '#0c4a6e',
                  '#1d4ed8', '#4f46e5', '#7c3aed']
        sec_counts = {}
        for l in learners:
            sec_counts[l.section_id] = sec_counts.get(l.section_id, 0) + 1
        enroll_data = [
            (section_map.get(sid, 'Unassigned'), cnt, COLORS[i % len(COLORS)])
            for i, (sid, cnt) in enumerate(
                sorted(sec_counts.items(), key=lambda x: -x[1])
            )
        ]
        self.chart_enrollment.set_data(enroll_data)

        # Sex distribution
        male   = sum(1 for l in learners if (l.sex or '').upper() in ('M', 'MALE'))
        female = sum(1 for l in learners if (l.sex or '').upper() in ('F', 'FEMALE'))
        self.chart_sex.set_data([
            ('Male',   male,   '#0369a1'),
            ('Female', female, '#db2777'),
        ])

        # TVE Major (Grades 8-10)
        if self.chart_tve is not None:
            tve_counts = {}
            for l in learners:
                tve = getattr(l, 'tve_major', '') or 'N/A'
                tve_counts[tve] = tve_counts.get(tve, 0) + 1
            tve_colors = ['#059669', '#0891b2', '#7c3aed', '#d97706', '#dc2626']
            tve_data = [
                (major, cnt, tve_colors[i % len(tve_colors)])
                for i, (major, cnt) in enumerate(
                    sorted(tve_counts.items(), key=lambda x: -x[1])
                )
            ]
            self.chart_tve.set_data(tve_data)

        self._populate_table(learners)

    def _populate_table(self, learners):
        self.table.setRowCount(0)
        self._current_learners = learners
        show_tve = self.grade in (8, 9, 10)

        for learner in learners:
            r = self.table.rowCount()
            self.table.insertRow(r)

            self.table.setItem(r, 0, QTableWidgetItem(learner.lrn))
            self.table.setItem(r, 1, QTableWidgetItem(learner.full_name))
            self.table.setItem(r, 2, QTableWidgetItem(learner.sex or ''))

            col = 3
            if show_tve:
                self.table.setItem(
                    r, col, QTableWidgetItem(getattr(learner, 'tve_major', '') or '')
                )
                col += 1

            badge_container = QWidget()
            bl = QHBoxLayout(badge_container)
            bl.setContentsMargins(4, 2, 4, 2)
            bl.addWidget(make_status_badge(learner.status))
            self.table.setCellWidget(r, col, badge_container)
            col += 1

            if JHSEditModal:
                edit_btn = QPushButton('Edit')
                edit_btn.setStyleSheet(
                    'background:#0369a1; color:white; border-radius:4px;'
                    'padding:4px 10px; font-size:11px;'
                )
                edit_btn.clicked.connect(
                    lambda _, l=learner: self._open_edit(l)
                )
                self.table.setCellWidget(r, col, edit_btn)
                col += 1

            num_item = QTableWidgetItem(str(r + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(r, col, num_item)

    def _open_edit(self, learner):
        if JHSEditModal is None:
            QMessageBox.warning(self, 'Unavailable', 'Edit modal not available.')
            return
        modal = JHSEditModal(learner, self.grade, self)
        modal.saved.connect(self.refresh)
        modal.exec_()

    def _open_pending_page(self):
        if JHSPendingPage is None:
            QMessageBox.warning(self, 'Unavailable', 'Pending page not available.')
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(f'Grade {self.grade} — Pending Learners')
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.resize(1100, 700)
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(0, 0, 0, 0)
        page = JHSPendingPage(self.grade)
        page.enrolled.connect(self.refresh)
        layout.addWidget(page)
        dlg.exec_()

    def _export_csv(self):
        learners = self._current_learners
        if not learners:
            QMessageBox.information(self, 'Export', 'No data to export.')
            return
        path, _ = QFileDialog.getSaveFileName(
            self, 'Save CSV',
            f'JHS_Grade{self.grade}_Enrollment.csv',
            'CSV Files (*.csv)'
        )
        if not path:
            return
        show_tve = self.grade in (8, 9, 10)
        headers = ['LRN', 'Name', 'Sex']
        if show_tve:
            headers.append('TVE Major')
        headers += ['Status', 'Section']
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for l in learners:
                    row = [l.lrn, l.full_name, l.sex or '']
                    if show_tve:
                        row.append(getattr(l, 'tve_major', '') or '')
                    row += [l.status, getattr(l, 'section_name', '') or '']
                    writer.writerow(row)
            QMessageBox.information(self, 'Export', f'Saved to:\n{path}')
        except Exception as e:
            show_error(self, 'Unable to Export File', e)
