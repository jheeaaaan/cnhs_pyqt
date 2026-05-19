from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QScrollArea, QGridLayout,
    QComboBox, QSizePolicy,
)
from PyQt5.QtCore import Qt
from core.errors import show_error
from core.models import Section, Learner

TEXT    = '#052e16'
MUTED   = '#4b7a5a'
BG      = '#f0fdf4'
CARD    = '#ffffff'
BORDER  = '#d1fae5'
PRIMARY = '#16a34a'
RED     = '#dc2626'
TVL     = '#0f766e'
YELLOW  = '#d97706'


class SHSSectionsPage(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self.add_open = False
        self._refresh_error_shown = False
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')

        container = QWidget()
        container.setStyleSheet('background: #f0fdf4;')
        scroll.setWidget(container)

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

        self.form = QVBoxLayout(container)
        self.form.setContentsMargins(32, 28, 32, 32)
        self.form.setSpacing(0)

        self.form.addWidget(self.make_header())
        self.form.addWidget(self.make_add_frame())
        self.form.addSpacing(4)
        self.form.addWidget(self.make_info_banner())
        self.form.addSpacing(20)

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet('background: transparent;')
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(16)
        self.form.addWidget(self.grid_widget)

        self.empty_state = self.make_empty_state()
        self.form.addWidget(self.empty_state)
        self.form.addStretch()

    def make_header(self):
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

        bc = QLabel(f'Enrollment  /  Grade {self.grade}  /  Sections')
        bc.setStyleSheet(f'font-size: 12px; color: {MUTED}; background: transparent;')
        pt = QLabel(f'Grade {self.grade} — Sections')
        pt.setStyleSheet(f'font-size: 24px; font-weight: 800; color: {TEXT}; background: transparent;')
        ps = QLabel('Click a section card to view and manage its enrolled learners.')
        ps.setStyleSheet(f'font-size: 14px; color: {MUTED}; background: transparent;')
        lv.addWidget(bc)
        lv.addWidget(pt)
        lv.addWidget(ps)
        row.addWidget(left, 1)

        self.add_btn = QPushButton('+ Add Section')
        self.add_btn.setMinimumHeight(38)
        self.add_btn.setMinimumWidth(130)
        self.add_btn.setStyleSheet(self.btn_style(False))
        self.add_btn.clicked.connect(self.toggle_add_form)
        row.addWidget(self.add_btn, 0, Qt.AlignVCenter)
        return hdr

    def make_add_frame(self):
        self.add_frame = QFrame()
        self.add_frame.setStyleSheet(
            f'QFrame {{ background: {CARD}; border: 2px solid rgba(22,163,74,0.18);'
            f'border-radius: 8px; margin-bottom: 4px; }}'
        )
        row = QHBoxLayout(self.add_frame)
        row.setContentsMargins(20, 14, 20, 14)
        row.setSpacing(12)

        row.addWidget(QLabel('Section Name:'))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('e.g. NARRA, MOLAVE, YAKAL')
        self.name_input.setMinimumHeight(36)
        self.name_input.setMinimumWidth(200)
        self.name_input.setStyleSheet(
            f'QLineEdit {{ background: {BG}; border: 1.5px solid {PRIMARY}; border-radius: 8px;'
            f'padding: 8px 14px; font-size: 13px; color: {TEXT}; }}'
            f'QLineEdit:focus {{ background: #fff; }}'
        )
        self.name_input.returnPressed.connect(self.do_add)
        row.addWidget(self.name_input)

        row.addWidget(QLabel('Track:'))

        self.track_combo = QComboBox()
        self.track_combo.addItems(['Academic', 'TechPro/TVL'])
        self.track_combo.setMinimumHeight(36)
        self.track_combo.setMinimumWidth(140)
        row.addWidget(self.track_combo)

        save_btn = QPushButton('Add Section')
        save_btn.setMinimumHeight(36)
        save_btn.setMinimumWidth(110)
        save_btn.setStyleSheet(
            f'QPushButton {{ background: {PRIMARY}; color: #fff; border: none; border-radius: 8px;'
            f'font-size: 13px; font-weight: 700; padding: 8px 18px; }}'
            f'QPushButton:hover {{ background: #15803d; }}'
        )
        save_btn.clicked.connect(self.do_add)
        row.addWidget(save_btn)
        row.addStretch()

        self.add_frame.hide()
        return self.add_frame

    def make_info_banner(self):
        info = QFrame()
        info.setStyleSheet('QFrame { background: rgba(22,163,74,0.07); border: none; border-radius: 8px; }')
        row = QHBoxLayout(info)
        row.setContentsMargins(16, 10, 16, 10)
        lbl = QLabel(
            'ℹ️  Sections sync with the BMI module. '
            'Click a card to open a section and use <b>View / Edit</b> on any learner.'
        )
        lbl.setStyleSheet(f'font-size: 12.5px; color: {PRIMARY}; background: transparent;')
        lbl.setWordWrap(True)
        row.addWidget(lbl)
        return info

    def make_empty_state(self):
        empty = QFrame()
        empty.setStyleSheet('QFrame { background: transparent; border: none; }')
        ev = QVBoxLayout(empty)
        ev.setContentsMargins(56, 56, 56, 56)
        ev.setAlignment(Qt.AlignCenter)

        icon = QLabel('🗂️')
        icon.setStyleSheet('font-size: 36px; background: transparent;')
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel('No Sections Yet')
        title.setStyleSheet(f'font-size: 16px; font-weight: 700; color: {TEXT}; background: transparent;')
        title.setAlignment(Qt.AlignCenter)

        sub = QLabel(f'Click \"+ Add Section\" above to create your first section for Grade {self.grade}.')
        sub.setStyleSheet(f'font-size: 13px; color: {MUTED}; background: transparent;')
        sub.setAlignment(Qt.AlignCenter)

        ev.addWidget(icon)
        ev.addWidget(title)
        ev.addWidget(sub)
        return empty

    def btn_style(self, cancel):
        color = RED if cancel else PRIMARY
        return (
            f'QPushButton {{ border: 1.5px solid {color}; border-radius: 10px;'
            f'background: transparent; color: {color}; font-size: 13px; font-weight: 700; padding: 8px 20px; }}'
            f'QPushButton:hover {{ background: {color}; color: #fff; }}'
        )

    def toggle_add_form(self):
        self.add_open = not self.add_open
        if self.add_open:
            self.add_frame.show()
            self.name_input.setFocus()
            self.add_btn.setText('✕ Cancel')
            self.add_btn.setStyleSheet(self.btn_style(True))
        else:
            self.add_frame.hide()
            self.name_input.clear()
            self.add_btn.setText('+ Add Section')
            self.add_btn.setStyleSheet(self.btn_style(False))

    def do_add(self):
        name = self.name_input.text().strip().upper()
        track = self.track_combo.currentText()
        if not name:
            QMessageBox.warning(self, 'Required', 'Section name is required.')
            return
        try:
            Section.create(name, self.grade, 'SHS', track)
            self.name_input.clear()
            if self.add_open:
                self.toggle_add_form()
            self.refresh()
        except Exception as e:
            show_error(self, 'Unable to Create Section', e)

    def delete_section(self, section_id, section_name):
        if QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete section "{section_name}"?\n\nLearners in it will become Pending.',
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            Section.delete(section_id)
            self.refresh()

    def open_detail(self, section_id, section_name):
        mw = self.window()
        if hasattr(mw, 'open_section_detail'):
            mw.open_section_detail('SHS', self.grade, section_id, section_name)

    def refresh(self):
        try:
            sections = Section.get_all(grade=self.grade, level='SHS')
        except Exception as e:
            if not self._refresh_error_shown:
                self._refresh_error_shown = True
                show_error(self, 'Unable to Load Sections', e)
            sections = []

        try:
            learners_all = Learner.get_all(grade=self.grade, level='SHS')
        except Exception as e:
            if sections and not self._refresh_error_shown:
                self._refresh_error_shown = True
                show_error(self, 'Unable to Load Learner Counts', e)
            learners_all = []

        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)

        if not sections:
            self.grid_widget.hide()
            self.empty_state.show()
        else:
            self.empty_state.hide()
            self.grid_widget.show()
            for i, s in enumerate(sections):
                learners = [l for l in learners_all if l.section_id == s.id]
                enrolled = sum(1 for l in learners if l.status == 'Enrolled')
                pending  = sum(1 for l in learners if l.status == 'Pending')
                total    = len(learners)
                self.grid.addWidget(self.make_card(s, total, enrolled, pending), i // 3, i % 3)

    def make_card(self, section, total, enrolled, pending):
        is_tvl = section.track in ('TechPro/TVL', 'TVL')
        tc = TVL if is_tvl else PRIMARY
        W = '#ffffff'

        frame = QFrame()
        frame.setObjectName('sectionCard')
        frame.setStyleSheet(
            f'QFrame#sectionCard {{ background: #ffffff; border: 1.5px solid {BORDER}; border-radius: 8px; }}'
        )
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        fv = QVBoxLayout(frame)
        fv.setContentsMargins(0, 0, 0, 0)
        fv.setSpacing(0)

        # head
        head = QWidget()
        head.setStyleSheet(f'background: {W};')
        hh = QHBoxLayout(head)
        hh.setContentsMargins(20, 18, 20, 14)
        hh.setSpacing(0)

        name_col = QWidget()
        name_col.setStyleSheet(f'background: {W};')
        nc = QVBoxLayout(name_col)
        nc.setContentsMargins(0, 0, 0, 0)
        nc.setSpacing(2)

        name_lbl = QLabel(section.name)
        name_lbl.setStyleSheet(f'font-size: 22px; font-weight: 800; color: {TEXT}; background: {W};')
        track_lbl = QLabel('TechPro/TVL Track' if is_tvl else 'Academic Track')
        track_lbl.setStyleSheet(f'font-size: 12px; color: {MUTED}; font-weight: 500; background: {W};')
        nc.addWidget(name_lbl)
        nc.addWidget(track_lbl)
        hh.addWidget(name_col, 1)

        rgba = '15,118,110' if is_tvl else '22,163,74'
        rec_lbl = QLabel(f'{total} record{"s" if total != 1 else ""}')
        rec_lbl.setStyleSheet(
            f'font-size: 11px; font-weight: 700; color: {tc};'
            f'background: rgba({rgba}, 0.1); border-radius: 20px; padding: 3px 10px;'
        )
        rec_lbl.setAlignment(Qt.AlignRight | Qt.AlignTop)
        hh.addWidget(rec_lbl, 0, Qt.AlignTop)
        fv.addWidget(head)

        div1 = QFrame()
        div1.setFixedHeight(1)
        div1.setStyleSheet(f'background: {BORDER}; border: none;')
        fv.addWidget(div1)

        # stats
        stats_w = QWidget()
        stats_w.setStyleSheet(f'background: {W};')
        sg = QHBoxLayout(stats_w)
        sg.setContentsMargins(0, 0, 0, 0)
        sg.setSpacing(0)

        def stat_cell(label, value, color, right_border=False):
            cell = QWidget()
            cell.setStyleSheet(f'background: {W};')
            cv = QVBoxLayout(cell)
            cv.setContentsMargins(20, 14, 20, 14)
            cv.setSpacing(4)
            lbl = QLabel(label)
            lbl.setStyleSheet(f'font-size: 9.5px; font-weight: 700; letter-spacing: 0.8px; color: {MUTED}; background: {W};')
            num = QLabel(str(value))
            num.setStyleSheet(f'font-size: 26px; font-weight: 800; color: {color}; background: {W};')
            cv.addWidget(lbl)
            cv.addWidget(num)
            if right_border:
                wrap = QWidget()
                wrap.setStyleSheet(f'background: {W};')
                wh = QHBoxLayout(wrap)
                wh.setContentsMargins(0, 0, 0, 0)
                wh.setSpacing(0)
                wh.addWidget(cell, 1)
                sep = QFrame()
                sep.setFixedWidth(1)
                sep.setStyleSheet(f'background: {BORDER}; border: none;')
                wh.addWidget(sep)
                return wrap
            return cell

        sg.addWidget(stat_cell('ENROLLED', enrolled, PRIMARY, right_border=True), 1)
        sg.addWidget(stat_cell('PENDING', pending, YELLOW if pending > 0 else MUTED), 1)
        fv.addWidget(stats_w)

        div2 = QFrame()
        div2.setFixedHeight(1)
        div2.setStyleSheet(f'background: {BORDER}; border: none;')
        fv.addWidget(div2)

        # footer
        foot = QWidget()
        foot.setStyleSheet(f'background: {W}; border-radius: 0 0 8px 8px;')
        fh = QHBoxLayout(foot)
        fh.setContentsMargins(16, 12, 16, 12)
        fh.setSpacing(8)

        open_btn = QPushButton('Open')
        open_btn.setStyleSheet(
            f'QPushButton {{ color: {PRIMARY}; font-size: 13px; font-weight: 700;'
            f'background: transparent; border: none; padding: 0; }}'
            f'QPushButton:hover {{ text-decoration: underline; }}'
        )
        open_btn.clicked.connect(lambda _, sid=section.id, sn=section.name: self.open_detail(sid, sn))
        fh.addWidget(open_btn)
        fh.addStretch()

        del_btn = QPushButton('Delete Section')
        del_btn.setStyleSheet(
            f'QPushButton {{ padding: 6px 14px; background: #fef2f2; border: 1px solid #fecaca;'
            f'color: {RED}; border-radius: 8px; font-size: 12px; font-weight: 700; }}'
            f'QPushButton:hover {{ background: {RED}; color: #fff; border-color: {RED}; }}'
        )
        del_btn.clicked.connect(lambda _, sid=section.id, sn=section.name: self.delete_section(sid, sn))
        fh.addWidget(del_btn)
        fv.addWidget(foot)

        return frame
