import csv
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QMessageBox, QLineEdit, QDialog,
    QComboBox, QDialogButtonBox, QFrame, QFileDialog,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from core.models import Learner, Section

TEXT    = '#052e16'
MUTED   = '#4b7a5a'
BG      = '#f0fdf4'
CARD    = '#ffffff'
BORDER  = '#d1fae5'
PRIMARY = '#16a34a'
TVL     = '#0f766e'
YELLOW  = '#d97706'
RED     = '#dc2626'
ACCENT  = '#fbbf24'

STATUS_COLORS = {
    'Enrolled':    '#15803d',
    'Pending':     '#b45309',
    'Dropped':     '#dc2626',
    'Transferred': '#7c3aed',
}


class TransferDialog(QDialog):
    def __init__(self, learner, grade, current_section_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Transfer — {learner.full_name}')
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl = QLabel(f'Move <b>{learner.full_name}</b> to another section:')
        lbl.setStyleSheet(f'font-size: 13px; color: {TEXT};')
        layout.addWidget(lbl)

        self.section_combo = QComboBox()
        self.section_combo.setMinimumHeight(36)
        for s in Section.get_all(grade=grade, level='SHS'):
            if s.id != current_section_id:
                self.section_combo.addItem(s.name, s.id)
        layout.addWidget(self.section_combo)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def chosen_section_id(self):
        return self.section_combo.currentData()

    def chosen_section_name(self):
        return self.section_combo.currentText()


class SHSSectionDetailPage(QWidget):
    def __init__(self, grade, section_id, section_name):
        super().__init__()
        self.grade = grade
        self.current_section_id = section_id
        self.section_name = section_name
        self.all_learners = []
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 32)
        layout.setSpacing(0)

        # breadcrumb
        bc = QLabel(
            f'Enrollment  /  Grade {self.grade}  /  '
            f'<a href="#" style="color: #16a34a; font-weight: 600; text-decoration: none;">Sections</a>'
            f'  /  {self.section_name}'
        )
        bc.setStyleSheet(f'font-size: 12px; color: {MUTED}; background: transparent; margin-bottom: 6px;')
        bc.setOpenExternalLinks(False)
        bc.linkActivated.connect(lambda _: self.go_back())
        layout.addWidget(bc)

        layout.addWidget(self.make_title_row())
        layout.addWidget(self.make_stat_cards())
        layout.addWidget(self.make_table_card())

    def make_title_row(self):
        top = QWidget()
        top.setStyleSheet('background: transparent;')
        th = QHBoxLayout(top)
        th.setContentsMargins(0, 0, 0, 20)
        th.setSpacing(12)

        left = QWidget()
        left.setStyleSheet('background: transparent;')
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(6)

        name_row = QWidget()
        name_row.setStyleSheet('background: transparent;')
        nr = QHBoxLayout(name_row)
        nr.setContentsMargins(0, 0, 0, 0)
        nr.setSpacing(12)

        self.title_lbl = QLabel(self.section_name)
        self.title_lbl.setStyleSheet(f'font-size: 28px; font-weight: 800; color: {TEXT}; background: transparent;')
        self.track_badge = QLabel('Academic Track')
        self.track_badge.setStyleSheet(
            f'font-size: 12px; font-weight: 700; color: {PRIMARY};'
            f'background: rgba(22,163,74,0.1); border: 1px solid rgba(22,163,74,0.2);'
            f'border-radius: 20px; padding: 4px 12px;'
        )
        nr.addWidget(self.title_lbl)
        nr.addWidget(self.track_badge)
        nr.addStretch()
        lv.addWidget(name_row)

        self.sub_lbl = QLabel(f'Grade {self.grade} · 0 learners')
        self.sub_lbl.setStyleSheet(f'font-size: 13px; color: {MUTED}; background: transparent;')
        lv.addWidget(self.sub_lbl)
        th.addWidget(left, 1)

        btn_row = QWidget()
        btn_row.setStyleSheet('background: transparent;')
        br = QHBoxLayout(btn_row)
        br.setContentsMargins(0, 0, 0, 0)
        br.setSpacing(10)

        rename_btn = QPushButton('✏ Rename')
        rename_btn.setMinimumHeight(36)
        rename_btn.setStyleSheet(
            'QPushButton { border: 1.5px solid #fde68a; border-radius: 8px;'
            'background: #fffbeb; color: #d97706; font-size: 12px; font-weight: 700; padding: 7px 16px; }'
            'QPushButton:hover { background: #d97706; color: #fff; border-color: #d97706; }'
        )
        rename_btn.clicked.connect(self.rename_section)
        br.addWidget(rename_btn)

        export_btn = QPushButton('⬇  Export CSV')
        export_btn.setMinimumHeight(36)
        export_btn.setStyleSheet(
            f'QPushButton {{ border: 1.5px solid {BORDER}; border-radius: 8px;'
            f'background: {CARD}; color: {TEXT}; font-size: 12px; font-weight: 700; padding: 7px 16px; }}'
            f'QPushButton:hover {{ background: #dcfce7; border-color: {PRIMARY}; }}'
        )
        export_btn.clicked.connect(self.export_csv)
        br.addWidget(export_btn)

        back_btn = QPushButton('← Back to Sections')
        back_btn.setMinimumHeight(36)
        back_btn.setStyleSheet(
            f'QPushButton {{ border: 1.5px solid {BORDER}; border-radius: 8px;'
            f'background: {CARD}; color: {TEXT}; font-size: 12px; font-weight: 700; padding: 7px 16px; }}'
            f'QPushButton:hover {{ background: #dcfce7; }}'
        )
        back_btn.clicked.connect(self.go_back)
        br.addWidget(back_btn)
        th.addWidget(btn_row, 0, Qt.AlignVCenter)
        return top

    def make_stat_cards(self):
        stats_row = QWidget()
        stats_row.setStyleSheet('background: transparent;')
        row = QHBoxLayout(stats_row)
        row.setContentsMargins(0, 0, 0, 24)
        row.setSpacing(16)

        self.stat_nums = {}
        for key, label, color in [
            ('total',    'Total Learners', PRIMARY),
            ('enrolled', 'Enrolled',       '#059669'),
            ('pending',  'Pending',        YELLOW),
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

        # dark green header
        card_head = QWidget()
        card_head.setFixedHeight(54)
        card_head.setStyleSheet(
            f'background: #14532d;'
            f'border-top-left-radius: 15px; border-top-right-radius: 15px; border: none;'
        )
        ch = QHBoxLayout(card_head)
        ch.setContentsMargins(24, 0, 18, 0)
        ch.setSpacing(12)

        ico = QLabel('🏅')
        ico.setStyleSheet(f'font-size: 15px; color: {ACCENT}; background: transparent; border: none;')
        self.head_title = QLabel(f'LEARNERS IN SECTION {self.section_name.upper()}')
        self.head_title.setStyleSheet('color: #fff; font-size: 13px; font-weight: 700; background: transparent; border: none;')
        ch.addWidget(ico)
        ch.addWidget(self.head_title)
        ch.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('🔍  Search by name or LRN...')
        self.search_input.setMinimumHeight(34)
        self.search_input.setMinimumWidth(220)
        self.search_input.setStyleSheet(
            'QLineEdit { background: rgba(255,255,255,0.1); border: 1.5px solid rgba(255,255,255,0.3);'
            'border-radius: 8px; padding: 6px 12px; font-size: 13px; color: #fff; }'
            'QLineEdit:focus { background: rgba(255,255,255,0.15); border-color: rgba(255,255,255,0.6); }'
        )
        self.search_input.textChanged.connect(self.apply_search)
        ch.addWidget(self.search_input)
        layout.addWidget(card_head)

        # table
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            '#', 'LRN', "Learner's Name", 'Sex', 'Track', 'Electives', 'Semester', '4Ps', 'Status', 'Action'
        ])
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.Stretch)
        hdr.setSectionResizeMode(0, QHeaderView.Fixed)
        hdr.setSectionResizeMode(9, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(9, 160)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(48)
        self.table.setAlternatingRowColors(True)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setStyleSheet(
            f'QTableWidget {{ background: {CARD}; border: none; outline: 0;'
            f'gridline-color: {BG}; font-size: 13px; color: {TEXT}; }}'
            f'QTableWidget::item {{ padding: 10px 14px; border-bottom: 1px solid {BG}; outline: 0; }}'
            f'QTableWidget::item:selected {{ background: #dcfce7; color: {TEXT}; border: none; outline: 0; }}'
            f'QTableWidget::item:alternate {{ background: #f9fefb; }}'
            f'QHeaderView::section {{ background: {BG}; color: {MUTED};'
            f'padding: 10px 14px; border: none; border-bottom: 1px solid {BORDER};'
            f'font-size: 10.5px; font-weight: 700; letter-spacing: 0.7px; }}'
        )
        layout.addWidget(self.table)

        # footer
        footer = QWidget()
        footer.setStyleSheet(
            f'background: {BG}; border: none;'
            f'border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;'
        )
        fh = QHBoxLayout(footer)
        fh.setContentsMargins(24, 10, 24, 10)

        self.footer_lbl = QLabel('0 learners')
        self.footer_lbl.setStyleSheet(f'font-size: 12px; color: {MUTED}; background: transparent; border: none;')
        fh.addWidget(self.footer_lbl)
        fh.addStretch()

        exp2 = QPushButton('⬇  Export This View')
        exp2.setStyleSheet(
            f'QPushButton {{ border: 1.5px solid {BORDER}; border-radius: 7px;'
            f'background: transparent; color: {MUTED}; font-size: 11px; font-weight: 700; padding: 4px 14px; }}'
            f'QPushButton:hover {{ border-color: {PRIMARY}; color: {PRIMARY}; }}'
        )
        exp2.clicked.connect(self.export_csv)
        fh.addWidget(exp2)
        layout.addWidget(footer)
        return card

    def go_back(self):
        mw = self.window()
        if hasattr(mw, 'go_back_to_sections'):
            mw.go_back_to_sections('SHS', self.grade)

    def rename_section(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('Rename Section')
        dlg.setMinimumWidth(360)
        dlg.setStyleSheet('QDialog { background: #ffffff; }')

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(14)

        lbl = QLabel(f'Rename <b>{self.section_name}</b> to:')
        lbl.setStyleSheet(f'font-size: 13px; color: {TEXT}; background: transparent;')
        layout.addWidget(lbl)

        inp = QLineEdit()
        inp.setText(self.section_name)
        inp.selectAll()
        inp.setMinimumHeight(38)
        inp.setStyleSheet(
            f'QLineEdit {{ background: {BG}; border: 1.5px solid {PRIMARY}; border-radius: 8px;'
            f'padding: 8px 14px; font-size: 13px; color: {TEXT}; }}'
            f'QLineEdit:focus {{ background: #ffffff; }}'
        )
        layout.addWidget(inp)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setStyleSheet(
            f'QPushButton {{ background: {BG}; color: {TEXT}; border: 1.5px solid {BORDER};'
            f'border-radius: 8px; font-size: 13px; font-weight: 700; padding: 6px 18px; }}'
            f'QPushButton:hover {{ background: {RED}; color: #fff; border-color: {RED}; }}'
        )
        cancel_btn.clicked.connect(dlg.reject)

        save_btn = QPushButton('Save')
        save_btn.setMinimumHeight(36)
        save_btn.setStyleSheet(
            f'QPushButton {{ background: {PRIMARY}; color: #fff; border: none;'
            f'border-radius: 8px; font-size: 13px; font-weight: 700; padding: 6px 18px; }}'
            f'QPushButton:hover {{ background: #15803d; }}'
        )
        save_btn.clicked.connect(dlg.accept)
        inp.returnPressed.connect(dlg.accept)

        btn_row.addStretch()
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

        if dlg.exec_() == QDialog.Accepted:
            new_name = inp.text().strip().upper()
            if not new_name:
                QMessageBox.warning(self, 'Required', 'Section name cannot be empty.')
                return
            if new_name == self.section_name:
                return
            try:
                Section.rename(self.current_section_id, new_name)
                self.section_name = new_name
                self.title_lbl.setText(new_name)
                self.head_title.setText(f'LEARNERS IN SECTION {new_name.upper()}')
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))

    def refresh(self):
        self.all_learners = Learner.get_all(
            grade=self.grade, level='SHS',
            section_id=self.current_section_id
        )
        total = len(self.all_learners)
        self.sub_lbl.setText(f'Grade {self.grade} · {total} learner{"s" if total != 1 else ""}')

        if self.all_learners:
            track = self.all_learners[0].track
            is_tvl = track in ('TechPro/TVL', 'TVL')
            tc = TVL if is_tvl else PRIMARY
            rgba = '15,118,110' if is_tvl else '22,163,74'
            self.track_badge.setText(f'{"TechPro/TVL" if is_tvl else "Academic"} Track')
            self.track_badge.setStyleSheet(
                f'font-size: 12px; font-weight: 700; color: {tc};'
                f'background: rgba({rgba}, 0.1); border: 1px solid rgba({rgba}, 0.2);'
                f'border-radius: 20px; padding: 4px 12px;'
            )

        self.apply_search(self.search_input.text())

    def apply_search(self, text):
        query = text.strip().lower()
        if query:
            filtered = [l for l in self.all_learners if query in l.full_name.lower() or query in l.lrn.lower()]
        else:
            filtered = self.all_learners

        enrolled = sum(1 for l in self.all_learners if l.status == 'Enrolled')
        pending  = sum(1 for l in self.all_learners if l.status == 'Pending')
        total    = len(self.all_learners)

        self.stat_nums['total'].setText(str(total))
        self.stat_nums['enrolled'].setText(str(enrolled))
        self.stat_nums['pending'].setText(str(pending))

        self.table.setRowCount(0)
        for idx, learner in enumerate(filtered):
            r = self.table.rowCount()
            self.table.insertRow(r)

            num = QTableWidgetItem(str(idx + 1))
            num.setTextAlignment(Qt.AlignCenter)
            num.setForeground(QColor(MUTED))
            self.table.setItem(r, 0, num)

            lrn_item = QTableWidgetItem(learner.lrn)
            lrn_item.setForeground(QColor(PRIMARY))
            f = lrn_item.font()
            f.setFamily('Courier New')
            lrn_item.setFont(f)
            self.table.setItem(r, 1, lrn_item)

            name_item = QTableWidgetItem(f'{learner.last_name}, {learner.first_name}')
            name_item.setData(Qt.UserRole, learner.id)
            f2 = name_item.font()
            f2.setBold(True)
            name_item.setFont(f2)
            self.table.setItem(r, 2, name_item)

            self.table.setItem(r, 3, QTableWidgetItem('Male' if learner.sex == 'M' else 'Female'))

            is_tvl = learner.track in ('TechPro/TVL', 'TVL')
            tc = TVL if is_tvl else PRIMARY
            track_item = QTableWidgetItem(learner.track or '—')
            track_item.setForeground(QColor(tc))
            self.table.setItem(r, 4, track_item)

            self.table.setItem(r, 5, QTableWidgetItem(learner.electives or '—'))
            self.table.setItem(r, 6, QTableWidgetItem(f'{learner.semester} Sem'))
            self.table.setItem(r, 7, QTableWidgetItem('Yes' if learner.is_four_ps else 'No'))

            status_item = QTableWidgetItem(learner.status)
            status_item.setForeground(QColor(STATUS_COLORS.get(learner.status, TEXT)))
            f3 = status_item.font()
            f3.setBold(True)
            status_item.setFont(f3)
            self.table.setItem(r, 8, status_item)

            act_w = QWidget()
            act_w.setStyleSheet('background: transparent; border: none;')
            ah = QHBoxLayout(act_w)
            ah.setContentsMargins(6, 4, 6, 4)
            ah.setSpacing(0)

            edit_btn = QPushButton('✏ View / Edit')
            edit_btn.setFixedHeight(30)
            edit_btn.setMinimumWidth(120)
            edit_btn.setStyleSheet(
                f'QPushButton {{ font-size: 11.5px; font-weight: 600; color: {TEXT};'
                f'background: {BG}; border: 1.5px solid {BORDER};'
                f'border-radius: 6px; padding: 0 10px; }}'
                f'QPushButton:hover {{ border-color: {PRIMARY}; color: {PRIMARY}; }}'
            )
            edit_btn.clicked.connect(lambda _, lobj=learner: self.open_edit(lobj))
            ah.addWidget(edit_btn)
            self.table.setCellWidget(r, 9, act_w)

        showing = len(filtered)
        if query:
            self.footer_lbl.setText(f'Showing {showing} of {total} learner{"s" if total != 1 else ""}')
        else:
            self.footer_lbl.setText(f'Showing {total} of {total} learner{"s" if total != 1 else ""}')

    def open_edit(self, learner):
        from enrollment.shs_learner_edit import SHSLearnerEditDialog
        dlg = SHSLearnerEditDialog(learner.id, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            self.refresh()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, 'Export CSV',
            f'section-{self.section_name}-learners.csv',
            'CSV Files (*.csv)'
        )
        if not path:
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['#', 'LRN', 'Name', 'Sex', 'Track', 'Electives', 'Semester', '4Ps', 'Status'])
                for idx, l in enumerate(self.all_learners, 1):
                    w.writerow([
                        idx, l.lrn,
                        f'{l.last_name}, {l.first_name}',
                        'Male' if l.sex == 'M' else 'Female',
                        l.track, l.electives or '',
                        f'{l.semester} Sem',
                        'Yes' if l.is_four_ps else 'No',
                        l.status,
                    ])
            QMessageBox.information(self, 'Exported', f'Saved to:\n{path}')
        except Exception as e:
            QMessageBox.critical(self, 'Export Error', str(e))
