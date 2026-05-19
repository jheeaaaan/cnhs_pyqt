# bmi/bmi_entry_page.py
# Mio's task — SHS BMI (Grades 11 & 12)
# All features from the prototype are implemented here.

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QScrollArea, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy,
    QDialog, QDialogButtonBox,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont
from core.errors import show_error
from core.models import Learner, BMIRecord, Section


# ── BMI classification colors (shared) ──────────────────────────
BMI_COLORS = {
    'Normal':         '#16a34a',
    'Thin':           '#ea580c',
    'Moderately Thin':'#dc2626',
    'Severely Thin':  '#dc2626',
    'Overweight':     '#d97706',
    'Obese I':        '#dc2626',
    'Obese II':       '#991b1b',
}
BMI_BG = {
    'Normal':         '#f0fdf4',
    'Thin':           '#fff7ed',
    'Moderately Thin':'#fef2f2',
    'Severely Thin':  '#fef2f2',
    'Overweight':     '#fffbeb',
    'Obese I':        '#fef2f2',
    'Obese II':       '#fef2f2',
}


def _color_palette(level):
    """Return a color dict depending on JHS (blue) or SHS (green)."""
    if level == 'JHS':
        return {
            'text':    '#0c1a2e',
            'muted':   '#4a6fa5',
            'bg':      '#f0f9ff',
            'card':    '#ffffff',
            'border':  '#bae6fd',
            'primary': '#0369a1',
            'header':  '#0c4a6e',
            'accent':  '#38bdf8',
            'tvl':     '#0e7490',
            'yellow':  '#d97706',
            'red':     '#dc2626',
        }
    else:  # SHS
        return {
            'text':    '#052e16',
            'muted':   '#4b7a5a',
            'bg':      '#f0fdf4',
            'card':    '#ffffff',
            'border':  '#d1fae5',
            'primary': '#16a34a',
            'header':  '#0c4a6e',
            'accent':  '#16a34a',
            'tvl':     '#0f766e',
            'yellow':  '#d97706',
            'red':     '#dc2626',
        }


# ── Toast notification ───────────────────────────────────────────
class ToastNotification(QFrame):
    """Floating toast shown in the bottom-right corner for 3.5 seconds."""

    def __init__(self, parent, message='✅ BMI record updated.'):
        super().__init__(parent)
        self.setObjectName('toast')
        self.setStyleSheet(
            'QFrame#toast {'
            '  background: #1e293b;'
            '  border-radius: 10px;'
            '  padding: 0px;'
            '}'
        )
        self.setFixedHeight(48)
        self.setMinimumWidth(260)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        lbl = QLabel(message)
        lbl.setStyleSheet('color: #f8fafc; font-size: 13px; font-weight: 600; background: transparent;')
        layout.addWidget(lbl)

        self._reposition()
        self.show()
        self.raise_()

        QTimer.singleShot(3500, self.deleteLater)

    def _reposition(self):
        if self.parent():
            pw = self.parent().width()
            ph = self.parent().height()
            self.adjustSize()
            self.move(pw - self.width() - 24, ph - self.height() - 24)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition()


# ── BMI Edit Modal ───────────────────────────────────────────────
class BMIEditModal(QDialog):
    """
    Modal popup for entering/editing height and weight for a learner.
    Matches the prototype: dark header, read-only info row, BMI result card,
    Cancel and Save/Update buttons.
    """

    def __init__(self, learner: Learner, existing_record: BMIRecord = None,
                 G: dict = None, parent=None):
        super().__init__(parent)
        self.learner = learner
        self.existing = existing_record
        self.G = G or _color_palette('SHS')
        self._saved = False

        self.setWindowTitle(f'BMI Entry — {learner.full_name}')
        self.setMinimumWidth(520)
        self.setModal(True)
        self.setStyleSheet(
            f'QDialog {{ background: {self.G["card"]}; }}'
            'QLineEdit { border:none; }'
            'QLineEdit:focus { border:none; outline:none; }'
            'QFrame { border:none; }'
            'QPushButton { outline:none; }'
        )

        self._build_ui()
        if existing_record:
            self.height_input.setText(str(existing_record.height))
            self.weight_input.setText(str(existing_record.weight))
            self._calc_bmi()

    def _build_ui(self):
        G = self.G
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Dark header
        header = QWidget()
        header.setStyleSheet(f'background: {G["header"]}; border-radius: 0px;')
        header.setFixedHeight(80)
        hh = QHBoxLayout(header)
        hh.setContentsMargins(24, 16, 24, 16)
        hh.setSpacing(12)

        left_col = QWidget()
        left_col.setStyleSheet('background: transparent;')
        lv = QVBoxLayout(left_col)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(2)
        name_lbl = QLabel(self.learner.full_name)
        name_lbl.setStyleSheet('color: #ffffff; font-size: 16px; font-weight: 800; background: transparent;')
        lrn_lbl = QLabel(f'LRN: {self.learner.lrn}')
        lrn_lbl.setStyleSheet('color: rgba(255,255,255,0.65); font-size: 12px; background: transparent;')
        lv.addWidget(name_lbl)
        lv.addWidget(lrn_lbl)
        hh.addWidget(left_col, 1)

        action_badge = QLabel('Update BMI' if self.existing else 'Add BMI')
        action_badge.setStyleSheet(
            f'color: {G["primary"]}; background: rgba(255,255,255,0.12);'
            f'border: 1px solid rgba(255,255,255,0.2); border-radius: 20px;'
            f'font-size: 11px; font-weight: 700; padding: 4px 12px;'
        )
        hh.addWidget(action_badge, 0, Qt.AlignVCenter)
        root.addWidget(header)

        # Body
        body = QWidget()
        body.setStyleSheet(f'background: {G["card"]};')
        bv = QVBoxLayout(body)
        bv.setContentsMargins(24, 20, 24, 20)
        bv.setSpacing(16)

        # Read-only info row: Section, Sex, Grade
        info_row = QHBoxLayout()
        info_row.setSpacing(12)
        for label, value in [
            ('SECTION', self.learner.section_name or '—'),
            ('SEX',     'Male' if self.learner.sex == 'M' else 'Female'),
            ('GRADE',   str(self.learner.grade)),
        ]:
            cell = QFrame()
            cell.setStyleSheet(
                f'QFrame {{ background: {G["bg"]}; border: none;'
                f'border-radius: 8px; }}'
            )
            cv = QVBoxLayout(cell)
            cv.setContentsMargins(12, 8, 12, 8)
            cv.setSpacing(2)
            l = QLabel(label)
            l.setStyleSheet(f'font-size: 9px; font-weight: 700; letter-spacing: 0.8px; color: {G["muted"]};')
            v = QLabel(value)
            v.setStyleSheet(f'font-size: 14px; font-weight: 700; color: {G["text"]};')
            cv.addWidget(l)
            cv.addWidget(v)
            info_row.addWidget(cell)
        bv.addLayout(info_row)

        # Divider
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet('background: transparent; border: none;')
        bv.addWidget(div)

        # Height / Weight / BMI inputs
        inputs_row = QHBoxLayout()
        inputs_row.setSpacing(12)

        # Height
        h_col = QVBoxLayout()
        h_label = QLabel('Height (cm)')
        h_label.setStyleSheet(f'font-size: 12px; font-weight: 600; color: {G["text"]};')
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText('e.g. 155')
        self.height_input.setMinimumHeight(40)
        self.height_input.setStyleSheet(
            f'QLineEdit {{ border: none; border-radius: 8px;'
            f'padding: 6px 12px; font-size: 14px; background: #fff; }}'
            f'QLineEdit:focus {{ border: none; background: #fff; }}'
        )
        self.height_input.textChanged.connect(self._calc_bmi)
        h_col.addWidget(h_label)
        h_col.addWidget(self.height_input)
        inputs_row.addLayout(h_col)

        # Weight
        w_col = QVBoxLayout()
        w_label = QLabel('Weight (kg)')
        w_label.setStyleSheet(f'font-size: 12px; font-weight: 600; color: {G["text"]};')
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText('e.g. 52')
        self.weight_input.setMinimumHeight(40)
        self.weight_input.setStyleSheet(
            f'QLineEdit {{ border: none; border-radius: 8px;'
            f'padding: 6px 12px; font-size: 14px; background: #fff; }}'
            f'QLineEdit:focus {{ border: none; background: #fff; }}'
        )
        self.weight_input.textChanged.connect(self._calc_bmi)
        w_col.addWidget(w_label)
        w_col.addWidget(self.weight_input)
        inputs_row.addLayout(w_col)

        # BMI (read-only)
        b_col = QVBoxLayout()
        b_label = QLabel('BMI')
        b_label.setStyleSheet(f'font-size: 12px; font-weight: 600; color: {G["text"]};')
        self.bmi_display = QLineEdit('—')
        self.bmi_display.setReadOnly(True)
        self.bmi_display.setMinimumHeight(40)
        self.bmi_display.setStyleSheet(
            f'QLineEdit {{ border: none; border-radius: 8px;'
            f'padding: 6px 12px; font-size: 14px; background: {G["bg"]}; color: {G["muted"]}; }}'
        )
        b_col.addWidget(b_label)
        b_col.addWidget(self.bmi_display)
        inputs_row.addLayout(b_col)

        bv.addLayout(inputs_row)

        # BMI result card
        self.result_card = QFrame()
        self.result_card.setFixedHeight(72)
        self.result_card.setStyleSheet(
            f'QFrame {{ background: {G["bg"]}; border: none;'
            f'border-radius: 10px; }}'
        )
        rh = QHBoxLayout(self.result_card)
        rh.setContentsMargins(18, 0, 18, 0)
        self.result_bmi_lbl = QLabel('BMI: —')
        self.result_bmi_lbl.setStyleSheet(
            f'font-size: 22px; font-weight: 800; color: {G["muted"]};'
        )
        self.result_status_lbl = QLabel('Enter height and weight')
        self.result_status_lbl.setStyleSheet(
            f'font-size: 14px; font-weight: 600; color: {G["muted"]};'
        )
        rh.addWidget(self.result_bmi_lbl)
        rh.addSpacing(16)
        rh.addWidget(self.result_status_lbl)
        rh.addStretch()
        bv.addWidget(self.result_card)

        root.addWidget(body)

        # Footer buttons
        footer = QWidget()
        footer.setStyleSheet(
            f'background: {G["bg"]}; border-top: none;'
        )
        fh = QHBoxLayout(footer)
        fh.setContentsMargins(24, 14, 24, 14)
        fh.setSpacing(10)
        fh.addStretch()

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setMinimumHeight(38)
        cancel_btn.setMinimumWidth(90)
        cancel_btn.setStyleSheet(
            f'QPushButton {{ border: none; border-radius: 8px;'
            f'background: #fff; color: {G["text"]}; font-size: 13px; font-weight: 600; padding: 0 18px; }}'
            f'QPushButton:hover {{ background: {G["bg"]}; }}'
        )
        cancel_btn.clicked.connect(self.reject)
        fh.addWidget(cancel_btn)

        label = 'Update BMI' if self.existing else 'Save BMI'
        self.save_btn = QPushButton(label)
        self.save_btn.setMinimumHeight(38)
        self.save_btn.setMinimumWidth(110)
        self.save_btn.setStyleSheet(
            f'QPushButton {{ background: {G["primary"]}; color: #fff; border: none;'
            f'border-radius: 8px; font-size: 13px; font-weight: 700; padding: 0 18px; }}'
            f'QPushButton:hover {{ background: {G["header"]}; }}'
            f'QPushButton:disabled {{ background: {G["border"]}; color: {G["muted"]}; }}'
        )
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self._save)
        fh.addWidget(self.save_btn)

        root.addWidget(footer)

    def _calc_bmi(self):
        G = self.G
        try:
            h = float(self.height_input.text())
            w = float(self.weight_input.text())
            if h <= 0 or w <= 0:
                raise ValueError
            bmi, status = BMIRecord.calc_bmi(h, w)
            color = BMI_COLORS.get(status, G['muted'])
            bg    = BMI_BG.get(status, G['bg'])

            self.bmi_display.setText(str(bmi))
            self.result_bmi_lbl.setText(f'BMI: {bmi}')
            self.result_bmi_lbl.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {color};')
            self.result_status_lbl.setText(status)
            self.result_status_lbl.setStyleSheet(f'font-size: 14px; font-weight: 700; color: {color};')
            self.result_card.setStyleSheet(
                f'QFrame {{ background: {bg}; border: none; border-radius: 10px; }}'
            )
            self.save_btn.setEnabled(True)
        except (ValueError, ZeroDivisionError):
            self.bmi_display.setText('—')
            self.result_bmi_lbl.setText('BMI: —')
            self.result_bmi_lbl.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {G["muted"]};')
            self.result_status_lbl.setText('Enter height and weight')
            self.result_status_lbl.setStyleSheet(f'font-size: 14px; font-weight: 600; color: {G["muted"]};')
            self.result_card.setStyleSheet(
                f'QFrame {{ background: {G["bg"]}; border: none; border-radius: 10px; }}'
            )
            self.save_btn.setEnabled(False)

    def _save(self):
        try:
            h = float(self.height_input.text())
            w = float(self.weight_input.text())
            BMIRecord.save(self.learner.id, h, w)
            self._saved = True
            self.accept()
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid numbers.')
        except Exception as e:
            show_error(self, 'Unable to Save BMI Record', e)

    def was_saved(self):
        return self._saved


# ── Learner table for section detail view ───────────────────────
class SectionDetailWidget(QWidget):
    """
    Detail view shown after clicking a section card.
    Shows stat cards + searchable learner table with BMI data.
    """

    def __init__(self, section: Section, grade, level, G, parent_page):
        super().__init__()
        self.section = section
        self.grade = grade
        self.level = level
        self.G = G
        self.parent_page = parent_page
        self._all_rows = []   # list of (learner, bmi_record_or_None)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        G = self.G
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 32)
        root.setSpacing(0)

        # Breadcrumb
        bc = QLabel(
            f'Body Mass Index  /  {self.level}  /  Grade {self.grade}  /  '
            f'<a href="#" style="color:{G["primary"]};font-weight:600;text-decoration:none;">Sections</a>'
            f'  /  {self.section.name}'
        )
        bc.setStyleSheet(f'font-size: 12px; color: {G["muted"]}; background: transparent; margin-bottom: 6px;')
        bc.setOpenExternalLinks(False)
        bc.linkActivated.connect(lambda _: self.parent_page.show_grid())
        root.addWidget(bc)

        # Title row
        title_row = QWidget()
        title_row.setStyleSheet('background: transparent;')
        tr = QHBoxLayout(title_row)
        tr.setContentsMargins(0, 8, 0, 20)
        tr.setSpacing(12)

        left = QWidget()
        left.setStyleSheet('background: transparent;')
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(4)

        title = QLabel(self.section.name)
        title.setStyleSheet(f'font-size: 26px; font-weight: 800; color: {G["text"]}; background: transparent;')
        sub = QLabel(f'SF8 — Enter BMI measurements for enrolled learners in this section.')
        sub.setStyleSheet(f'font-size: 13px; color: {G["muted"]}; background: transparent;')
        lv.addWidget(title)
        lv.addWidget(sub)
        tr.addWidget(left, 1)

        back_btn = QPushButton('← Back to Sections')
        back_btn.setMinimumHeight(36)
        back_btn.setStyleSheet(
            f'QPushButton {{ border: 1.5px solid {G["border"]}; border-radius: 8px;'
            f'background: transparent; color: {G["primary"]}; font-size: 13px; font-weight: 600;'
            f'padding: 0 16px; }}'
            f'QPushButton:hover {{ background: {G["primary"]}; color: #fff; }}'
        )
        back_btn.clicked.connect(lambda: self.parent_page.show_grid())
        tr.addWidget(back_btn, 0, Qt.AlignVCenter)
        root.addWidget(title_row)

        # Stat cards
        self.stat_cards_widget = QWidget()
        self.stat_cards_widget.setStyleSheet('background: transparent;')
        self.stat_row = QHBoxLayout(self.stat_cards_widget)
        self.stat_row.setContentsMargins(0, 0, 0, 20)
        self.stat_row.setSpacing(14)
        root.addWidget(self.stat_cards_widget)

        # Table card
        table_card = QFrame()
        table_card.setStyleSheet('QFrame { background: #fff; border: none; border-radius: 12px; }')
        tv = QVBoxLayout(table_card)
        tv.setContentsMargins(0, 0, 0, 0)
        tv.setSpacing(0)

        # Table header bar (search)
        thead = QWidget()
        thead.setStyleSheet(f'background: #fff; border-radius: 14px 14px 0 0;')
        th = QHBoxLayout(thead)
        th.setContentsMargins(16, 14, 16, 14)
        th.setSpacing(10)

        th.addWidget(QLabel('Learners'))

        th.addStretch()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Search by name or LRN...')
        self.search_box.setMinimumWidth(240)
        self.search_box.setMinimumHeight(34)
        self.search_box.setStyleSheet(
            f'QLineEdit {{ border: 1px solid {G["border"]}; border-radius: 8px;'
            f'padding: 4px 10px; font-size: 13px; background: {G["bg"]}; }}'
            f'QLineEdit:focus {{ border-color: {G["primary"]}; }}'
        )
        self.search_box.textChanged.connect(self._filter_table)
        th.addWidget(self.search_box)
        tv.addWidget(thead)

        # Table
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            '#', 'LRN', "Learner's Name", 'Sex',
            'Height (cm)', 'Weight (kg)', 'BMI', 'Classification', 'Action'
        ])
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)
        hdr.setSectionResizeMode(7, QHeaderView.Stretch)
        for col in [0, 3, 4, 5, 6]:
            hdr.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(8, QHeaderView.Fixed)
        hdr.setSectionResizeMode(1, QHeaderView.Interactive)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(7, 150)
        self.table.setColumnWidth(8, 158)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            'QTableWidget { border: none; background: #fff; font-size: 13px; }'
            f'QHeaderView::section {{ background: {G["bg"]}; color: {G["muted"]};'
            f'font-size: 11px; font-weight: 700;'
            f'padding: 9px 10px; border: none; }}'
            'QTableWidget::item { padding: 10px 12px; border: none; }'
        )
        tv.addWidget(self.table)

        # Footer count
        self.footer_lbl = QLabel('0 learners  |  0 measured')
        self.footer_lbl.setStyleSheet(
            f'font-size: 12px; color: {G["muted"]}; padding: 10px 16px;'
            f'background: {G["bg"]}; border-radius: 0 0 12px 12px;'
        )
        tv.addWidget(self.footer_lbl)

        root.addWidget(table_card)

    def _make_stat_card(self, label, value, color, is_alert=False):
        G = self.G
        frame = QFrame()
        frame.setObjectName('bmiDetailStatCard')
        frame.setMinimumSize(170, 104)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frame.setStyleSheet(
            f'QFrame#bmiDetailStatCard {{ background: #fff; border: none;'
            f'border-radius: 12px; }}'
        )
        fv = QVBoxLayout(frame)
        fv.setContentsMargins(16, 12, 16, 12)
        fv.setSpacing(4)

        accent = QFrame()
        accent.setFixedHeight(3)
        accent.setStyleSheet(f'background: {color}; border: none; border-radius: 2px;')

        lbl = QLabel(label.upper())
        lbl.setStyleSheet(
            f'font-size: 9.5px; font-weight: 700; color: {G["muted"]};'
            f'background: transparent; border: none;'
        )
        lbl.setWordWrap(True)
        num = QLabel(str(value))
        num.setStyleSheet(
            f'font-size: 28px; font-weight: 800; color: {color};'
            f'background: transparent; border: none;'
        )
        fv.addWidget(accent)
        fv.addWidget(lbl)
        fv.addWidget(num)
        return frame

    def _update_stat_cards(self, total, measured, normal, alerts):
        G = self.G
        # Clear old cards
        for i in reversed(range(self.stat_row.count())):
            item = self.stat_row.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        alert_color = G['red'] if alerts > 0 else G['muted']
        cards = [
            ('Total Learners', total,   G['primary']),
            ('Measured',       measured, '#16a34a'),
            ('BMI Status',     normal,   G['primary']),
            ('Alerts',         alerts,   alert_color),
        ]
        for label, val, color in cards:
            self.stat_row.addWidget(self._make_stat_card(label, val, color))
        self.stat_row.addStretch()

    def refresh(self):
        learners = Learner.get_all(section_id=self.section.id)
        all_records = BMIRecord.get_all(level=self.level, section_id=self.section.id)
        bmi_map = {r.learner_id: r for r in all_records}

        self._all_rows = [(l, bmi_map.get(l.id)) for l in learners]

        total    = len(learners)
        measured = sum(1 for _, r in self._all_rows if r is not None)
        normal   = sum(1 for _, r in self._all_rows if r and r.bmi_status == 'Normal')
        alerts   = sum(1 for _, r in self._all_rows
                       if r and r.bmi_status in ('Severely Thin', 'Obese I', 'Obese II'))

        self._update_stat_cards(total, measured, normal, alerts)
        self._populate_table(self._all_rows)
        self.footer_lbl.setText(f'{total} learner{"s" if total != 1 else ""}  |  {measured} measured')

    def _populate_table(self, rows):
        G = self.G
        self.table.clearSpans()
        self.table.setRowCount(0)
        for idx, (learner, record) in enumerate(rows):
            r = self.table.rowCount()
            self.table.insertRow(r)

            # Alternating row color
            row_bg = '#ffffff' if idx % 2 == 0 else G['bg']

            def cell(text, align=Qt.AlignLeft, italic=False, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(align | Qt.AlignVCenter)
                if italic:
                    f = QFont()
                    f.setItalic(True)
                    item.setFont(f)
                if color:
                    item.setForeground(QColor(color))
                item.setBackground(QColor(row_bg))
                return item

            self.table.setItem(r, 0, cell(str(idx + 1), Qt.AlignCenter))
            self.table.setItem(r, 1, cell(learner.lrn))
            self.table.setItem(r, 2, cell(learner.full_name))
            self.table.setItem(r, 3, cell('M' if learner.sex == 'M' else 'F', Qt.AlignCenter))

            if record:
                self.table.setItem(r, 4, cell(str(record.height), Qt.AlignCenter))
                self.table.setItem(r, 5, cell(str(record.weight), Qt.AlignCenter))
                bmi_color = BMI_COLORS.get(record.bmi_status, G['text'])
                self.table.setItem(r, 6, cell(str(record.bmi), Qt.AlignCenter, color=bmi_color))

                # Classification badge cell
                class_item = QTableWidgetItem(record.bmi_status)
                class_item.setBackground(QColor(row_bg))
                class_item.setForeground(QColor(BMI_COLORS.get(record.bmi_status, G['text'])))
                class_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                f2 = QFont()
                f2.setBold(True)
                class_item.setFont(f2)
                self.table.setItem(r, 7, class_item)
            else:
                for col in [4, 5, 6]:
                    dash = cell('—', Qt.AlignCenter, color=G['muted'])
                    dash.setBackground(QColor(row_bg))
                    self.table.setItem(r, col, dash)
                nm = cell('Not measured', Qt.AlignCenter, italic=True, color=G['muted'])
                nm.setBackground(QColor(row_bg))
                self.table.setItem(r, 7, nm)

            # View / Edit button
            btn_w = QWidget()
            btn_w.setStyleSheet(f'background: {row_bg};')
            btn_h = QHBoxLayout(btn_w)
            btn_h.setContentsMargins(8, 6, 8, 6)
            btn_h.setSpacing(0)
            edit_btn = QPushButton('View / Edit')
            edit_btn.setMinimumWidth(130)
            edit_btn.setFixedHeight(34)
            edit_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            edit_btn.setStyleSheet(
                f'QPushButton {{ background: transparent; border: 1px solid {G["primary"]};'
                f'border-radius: 6px; color: {G["primary"]}; font-size: 12px; font-weight: 600;'
                f'padding: 0 10px; }}'
                f'QPushButton:hover {{ background: {G["primary"]}; color: #fff; }}'
            )
            edit_btn.clicked.connect(
                lambda _, lid=learner.id: self._open_modal(lid)
            )
            btn_h.addWidget(edit_btn, 0, Qt.AlignCenter)
            self.table.setCellWidget(r, 8, btn_w)
            self.table.setRowHeight(r, 58)

    def _filter_table(self):
        q = self.search_box.text().strip().lower()
        if not q:
            self._populate_table(self._all_rows)
            total = len(self._all_rows)
            measured = sum(1 for _, r in self._all_rows if r is not None)
            self.footer_lbl.setText(f'{total} learner{"s" if total != 1 else ""}  |  {measured} measured')
            return
        filtered = [
            (l, r) for l, r in self._all_rows
            if q in l.full_name.lower() or q in l.lrn.lower()
        ]
        self._populate_table(filtered)
        if not filtered:
            self._show_no_result_row()
            self.footer_lbl.setText('No Result Found')
        else:
            measured = sum(1 for _, r in filtered if r is not None)
            self.footer_lbl.setText(f'{len(filtered)} result{"s" if len(filtered) != 1 else ""}  |  {measured} measured')

    def _show_no_result_row(self):
        self.table.setRowCount(1)
        self.table.setSpan(0, 0, 1, self.table.columnCount())
        item = QTableWidgetItem('No Result Found')
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor(self.G['muted']))
        self.table.setItem(0, 0, item)
        self.table.setRowHeight(0, 56)

    def _open_modal(self, learner_id):
        learner = Learner.get_by_id(learner_id)
        if not learner:
            return
        all_records = BMIRecord.get_all(level=self.level, section_id=self.section.id)
        bmi_map = {r.learner_id: r for r in all_records}
        existing = bmi_map.get(learner_id)

        modal = BMIEditModal(learner, existing, self.G, parent=self)
        if modal.exec_() == QDialog.Accepted and modal.was_saved():
            self.refresh()
            # Show toast on the main window or this widget's top-level
            top = self.window()
            ToastNotification(top, '✅ BMI record updated.')


# ── Main entry page: sections grid + detail switcher ────────────
class BMIEntryPage(QWidget):
    """
    Main BMI entry page for a grade level.
    Opens to a sections grid. Clicking a card switches to SectionDetailWidget.
    Wired identically in main_window.py for both JHS and SHS.
    """

    def __init__(self, level='SHS', grade=11):
        super().__init__()
        self.level = level
        self.grade = grade
        self.G = _color_palette(level)
        self.add_open = False
        self._stack_widget = None
        self._detail_widget = None
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        G = self.G
        # Outer layout — holds scroll area (grid) or detail view
        self._root = QVBoxLayout(self)
        self._root.setContentsMargins(0, 0, 0, 0)
        self._root.setSpacing(0)

        # ── Grid view (scroll area) ──────────────────────────────
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')

        self._grid_container = QWidget()
        self._grid_container.setStyleSheet(f'background: {G["bg"]};')
        self._scroll.setWidget(self._grid_container)

        self._form = QVBoxLayout(self._grid_container)
        self._form.setContentsMargins(32, 28, 32, 32)
        self._form.setSpacing(0)

        self._form.addWidget(self._make_header())
        self._form.addWidget(self._make_add_frame())
        self._form.addSpacing(4)
        self._form.addWidget(self._make_info_banner())
        self._form.addSpacing(20)

        self._grid_widget = QWidget()
        self._grid_widget.setStyleSheet('background: transparent;')
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(20)
        self._form.addWidget(self._grid_widget)

        self._empty_state = self._make_empty_state()
        self._form.addWidget(self._empty_state)
        self._form.addStretch()

        self._root.addWidget(self._scroll)

    def _make_header(self):
        G = self.G
        hdr = QWidget()
        hdr.setStyleSheet('background: transparent;')
        row = QHBoxLayout(hdr)
        row.setContentsMargins(0, 0, 0, 20)
        row.setSpacing(16)

        left = QWidget()
        left.setStyleSheet('background: transparent;')
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(4)

        bc = QLabel(f'Body Mass Index  /  {self.level}  /  Grade {self.grade}  /  Sections')
        bc.setStyleSheet(f'font-size: 12px; color: {G["muted"]}; background: transparent;')
        pt = QLabel(f'Grade {self.grade} — Body Mass Index')
        pt.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {G["text"]}; background: transparent;')
        ps = QLabel('Select a section to view and enter BMI measurements.')
        ps.setStyleSheet(f'font-size: 14px; color: {G["muted"]}; background: transparent;')
        lv.addWidget(bc)
        lv.addWidget(pt)
        lv.addWidget(ps)
        row.addWidget(left, 1)

        self._add_btn = QPushButton('+ Add Section')
        self._add_btn.setMinimumHeight(38)
        self._add_btn.setMinimumWidth(130)
        self._add_btn.setStyleSheet(self._btn_style(False))
        self._add_btn.clicked.connect(self._toggle_add_form)
        row.addWidget(self._add_btn, 0, Qt.AlignVCenter)
        return hdr

    def _make_add_frame(self):
        G = self.G
        self._add_frame = QFrame()
        self._add_frame.setStyleSheet(
            f'QFrame {{ background: {G["card"]}; border: 2px solid rgba(22,163,74,0.18);'
            f'border-radius: 12px; margin-bottom: 4px; }}'
        )
        row = QHBoxLayout(self._add_frame)
        row.setContentsMargins(20, 14, 20, 14)
        row.setSpacing(10)

        row.addWidget(QLabel('Section name:'))
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText('e.g. ACAD-A')
        self._name_input.setMinimumHeight(34)
        self._name_input.setStyleSheet(
            f'QLineEdit {{ border: 1px solid {G["border"]}; border-radius: 8px;'
            f'padding: 4px 10px; }}'
            f'QLineEdit:focus {{ border-color: {G["primary"]}; }}'
        )
        row.addWidget(self._name_input, 1)

        save_btn = QPushButton('Save')
        save_btn.setMinimumHeight(34)
        save_btn.setMinimumWidth(72)
        save_btn.setStyleSheet(
            f'QPushButton {{ background: {G["primary"]}; color: #fff; border: none;'
            f'border-radius: 8px; font-size: 13px; font-weight: 700; padding: 0 16px; }}'
            f'QPushButton:hover {{ background: {G["header"]}; }}'
        )
        save_btn.clicked.connect(self._do_add)
        row.addWidget(save_btn)

        self._add_frame.hide()
        return self._add_frame

    def _make_info_banner(self):
        G = self.G
        banner = QFrame()
        banner.setStyleSheet(
            'QFrame { background: rgba(3,105,161,0.07); border: none; border-radius: 10px; }'
        )
        bh = QHBoxLayout(banner)
        bh.setContentsMargins(16, 10, 16, 10)
        icon = QLabel('ℹ')
        icon.setStyleSheet(f'font-size: 15px; color: {G["primary"]}; background: transparent;')
        txt = QLabel(
            f'Sections sync from the Enrollment module. '
            f'BMI is calculated as: <b>weight (kg) ÷ height² (m)</b>'
        )
        txt.setStyleSheet(f'font-size: 12px; color: {G["muted"]}; background: transparent;')
        txt.setTextFormat(Qt.RichText)
        bh.addWidget(icon)
        bh.addWidget(txt)
        bh.addStretch()
        return banner

    def _make_empty_state(self):
        G = self.G
        empty = QWidget()
        empty.setStyleSheet('background: transparent;')
        ev = QVBoxLayout(empty)
        ev.setAlignment(Qt.AlignCenter)
        ev.setSpacing(8)
        icon = QLabel('⚖')
        icon.setStyleSheet('font-size: 36px; background: transparent;')
        icon.setAlignment(Qt.AlignCenter)
        title = QLabel('No sections yet')
        title.setStyleSheet(f'font-size: 16px; font-weight: 700; color: {G["text"]}; background: transparent;')
        title.setAlignment(Qt.AlignCenter)
        sub = QLabel('Click "+ Add Section" above to create one.')
        sub.setStyleSheet(f'font-size: 13px; color: {G["muted"]}; background: transparent;')
        sub.setAlignment(Qt.AlignCenter)
        ev.addWidget(icon)
        ev.addWidget(title)
        ev.addWidget(sub)
        empty.hide()
        return empty

    def _btn_style(self, cancel):
        G = self.G
        color = G['red'] if cancel else G['primary']
        return (
            f'QPushButton {{ border: 1.5px solid {color}; border-radius: 10px;'
            f'background: transparent; color: {color}; font-size: 13px; font-weight: 700; padding: 8px 20px; }}'
            f'QPushButton:hover {{ background: {color}; color: #fff; }}'
        )

    def _toggle_add_form(self):
        self.add_open = not self.add_open
        if self.add_open:
            self._add_frame.show()
            self._name_input.setFocus()
            self._add_btn.setText('✕ Cancel')
            self._add_btn.setStyleSheet(self._btn_style(True))
        else:
            self._add_frame.hide()
            self._name_input.clear()
            self._add_btn.setText('+ Add Section')
            self._add_btn.setStyleSheet(self._btn_style(False))

    def _do_add(self):
        name = self._name_input.text().strip().upper()
        if not name:
            QMessageBox.warning(self, 'Required', 'Section name is required.')
            return
        # Determine track from name prefix for SHS
        track = ''
        if self.level == 'SHS':
            track = 'TechPro/TVL' if 'TVL' in name else 'Academic'
        try:
            Section.create(name, self.grade, self.level, track)
            self._name_input.clear()
            if self.add_open:
                self._toggle_add_form()
            self.refresh()
        except Exception as e:
            show_error(self, 'Unable to Create Section', e)

    def show_grid(self):
        """Switch back to the sections grid view."""
        if self._detail_widget:
            self._root.removeWidget(self._detail_widget)
            self._detail_widget.setParent(None)
            self._detail_widget.deleteLater()
            self._detail_widget = None
        self._scroll.show()

    def _open_detail(self, section: Section):
        """Switch to the detail view for a section."""
        self._scroll.hide()
        self._detail_widget = SectionDetailWidget(
            section, self.grade, self.level, self.G, self
        )
        self._root.addWidget(self._detail_widget)

    def refresh(self):
        sections = Section.get_all(grade=self.grade, level=self.level)

        # Clear grid
        for i in reversed(range(self._grid.count())):
            w = self._grid.itemAt(i).widget()
            if w:
                w.setParent(None)

        if not sections:
            self._grid_widget.hide()
            self._empty_state.show()
        else:
            self._empty_state.hide()
            self._grid_widget.show()

            # Build BMI summary per section
            all_records = BMIRecord.get_all(grade=self.grade, level=self.level)
            bmi_map = {r.learner_id: r for r in all_records}

            col_count = 2 if self.level == 'SHS' else 3
            for i, s in enumerate(sections):
                learners = Learner.get_all(section_id=s.id)
                measured = sum(1 for l in learners if l.id in bmi_map)
                normal   = sum(1 for l in learners if bmi_map.get(l.id) and
                               bmi_map[l.id].bmi_status == 'Normal')
                alerts   = sum(1 for l in learners if bmi_map.get(l.id) and
                               bmi_map[l.id].bmi_status in ('Severely Thin', 'Obese I', 'Obese II'))
                card = self._make_card(s, len(learners), measured, normal, alerts)
                self._grid.addWidget(card, i // col_count, i % col_count)

    def _make_card(self, section, total, measured, normal, alerts):
        G = self.G
        is_tvl = section.track in ('TechPro/TVL', 'TVL')
        tc = G['tvl'] if is_tvl else G['primary']
        W = '#ffffff'

        frame = QFrame()
        frame.setObjectName('bmiCard')
        frame.setStyleSheet(
            f'QFrame#bmiCard {{ background: {W}; border: none; border-radius: 14px; }}'
        )
        frame.setMinimumWidth(270)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        fv = QVBoxLayout(frame)
        fv.setContentsMargins(0, 0, 0, 0)
        fv.setSpacing(0)

        # Colored top accent bar
        accent = QFrame()
        accent.setFixedHeight(4)
        accent.setStyleSheet(f'background: {tc}; border-radius: 14px 14px 0 0; border: none;')
        fv.addWidget(accent)

        # Head
        head = QWidget()
        head.setStyleSheet(f'background: {W};')
        hh = QHBoxLayout(head)
        hh.setContentsMargins(20, 16, 20, 12)
        hh.setSpacing(0)

        name_col = QWidget()
        name_col.setStyleSheet(f'background: {W};')
        nc = QVBoxLayout(name_col)
        nc.setContentsMargins(0, 0, 0, 0)
        nc.setSpacing(2)
        name_lbl = QLabel(section.name)
        name_lbl.setStyleSheet(f'font-size: 20px; font-weight: 800; color: {G["text"]}; background: {W};')
        name_lbl.setWordWrap(True)
        track_lbl = QLabel('Grade ' + str(section.grade) + (' — TechPro/TVL' if is_tvl else ' — Academic'))
        track_lbl.setStyleSheet(f'font-size: 11px; color: {G["muted"]}; background: {W};')
        nc.addWidget(name_lbl)
        nc.addWidget(track_lbl)
        hh.addWidget(name_col, 1)

        rgba_str = '15,118,110' if is_tvl else ('3,105,161' if self.level == 'JHS' else '22,163,74')
        lrn_badge = QLabel(f'{total} learner{"s" if total != 1 else ""}')
        lrn_badge.setStyleSheet(
            f'font-size: 11px; font-weight: 700; color: {tc};'
            f'background: rgba({rgba_str},0.1); border-radius: 20px; padding: 3px 10px;'
        )
        lrn_badge.setAlignment(Qt.AlignRight | Qt.AlignTop)
        hh.addWidget(lrn_badge, 0, Qt.AlignTop)
        fv.addWidget(head)

        # Stats row
        stats_w = QWidget()
        stats_w.setStyleSheet(f'background: {W};')
        sg = QHBoxLayout(stats_w)
        sg.setContentsMargins(0, 0, 0, 0)
        sg.setSpacing(0)

        def stat_cell(label, value, color):
            cell = QWidget()
            cell.setStyleSheet(f'background: {W};')
            cv = QVBoxLayout(cell)
            cv.setContentsMargins(14, 12, 14, 12)
            cv.setSpacing(3)
            lbl = QLabel(label)
            lbl.setStyleSheet(
                f'font-size: 9px; font-weight: 700; color: {G["muted"]}; background: {W};'
            )
            lbl.setWordWrap(True)
            lbl.setAlignment(Qt.AlignCenter)
            num = QLabel(str(value))
            num.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {color}; background: {W};')
            num.setAlignment(Qt.AlignCenter)
            cv.addWidget(lbl)
            cv.addWidget(num)
            return cell

        alert_color = G['red'] if alerts > 0 else G['muted']
        sg.addWidget(stat_cell('MEASURED', measured, tc), 1)
        sg.addWidget(stat_cell('NORMAL',   normal,   '#16a34a'), 1)
        sg.addWidget(stat_cell('ALERTS',   alerts,   alert_color), 1)
        fv.addWidget(stats_w)

        # Footer
        foot = QWidget()
        foot.setStyleSheet(f'background: {W}; border-radius: 0 0 14px 14px;')
        fh = QHBoxLayout(foot)
        fh.setContentsMargins(16, 12, 16, 12)

        open_btn = QPushButton('Open →')
        open_btn.setStyleSheet(
            f'QPushButton {{ color: {tc}; font-size: 13px; font-weight: 700;'
            f'background: transparent; border: none; padding: 0; }}'
            f'QPushButton:hover {{ text-decoration: underline; }}'
        )
        open_btn.clicked.connect(lambda _, s=section: self._open_detail(s))
        fh.addWidget(open_btn)
        fh.addStretch()

        del_btn = QPushButton('Delete Section')
        del_btn.setStyleSheet(
            f'QPushButton {{ padding: 6px 12px; background: #fef2f2; border: 1px solid #fecaca;'
            f'color: {G["red"]}; border-radius: 8px; font-size: 12px; font-weight: 700; }}'
            f'QPushButton:hover {{ background: {G["red"]}; color: #fff; border-color: {G["red"]}; }}'
        )
        del_btn.clicked.connect(
            lambda _, sid=section.id, sn=section.name: self._delete_section(sid, sn)
        )
        fh.addWidget(del_btn)
        fv.addWidget(foot)

        return frame

    def _delete_section(self, section_id, section_name):
        confirm = QMessageBox(self)
        confirm.setWindowTitle('Confirm Delete')
        confirm.setText(f'Delete section "{section_name}"?')
        confirm.setInformativeText('All BMI records in it will be unlinked.')
        confirm.setIcon(QMessageBox.Warning)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        confirm.setStyleSheet(
            f'QMessageBox {{ background: #ffffff; }}'
            f'QMessageBox QLabel {{ color: {self.G["text"]}; background: transparent; }}'
            f'QPushButton {{ min-width: 84px; padding: 7px 14px; border-radius: 7px;'
            f'font-size: 12px; font-weight: 700; }}'
        )

        yes_btn = confirm.button(QMessageBox.Yes)
        no_btn = confirm.button(QMessageBox.No)
        if yes_btn:
            yes_btn.setText('Yes')
            yes_btn.setStyleSheet(
                f'QPushButton {{ background: {self.G["red"]}; color: #ffffff;'
                f'border: 1.5px solid {self.G["red"]}; min-width: 92px; padding: 7px 14px;'
                f'border-radius: 7px; font-size: 12px; font-weight: 700; }}'
                f'QPushButton:hover {{ background: #b91c1c; border-color: #b91c1c; }}'
            )
        if no_btn:
            no_btn.setText('No')
            no_btn.setStyleSheet(
                f'QPushButton {{ background: #0369a1; color: #ffffff;'
                f'border: 1.5px solid #0369a1; min-width: 92px; padding: 7px 14px;'
                f'border-radius: 7px; font-size: 12px; font-weight: 700; }}'
                f'QPushButton:hover {{ background: #0c4a6e; border-color: #0c4a6e; }}'
            )

        if confirm.exec_() == QMessageBox.Yes:
            Section.delete(section_id)
            self.refresh()
