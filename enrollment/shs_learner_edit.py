# enrollment/shs_learner_edit.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox,
    QFrame, QWidget, QCheckBox, QDateEdit, QButtonGroup,
    QRadioButton, QSizePolicy,
)
from PyQt5.QtCore import QDate, Qt
from core.errors import show_error
from core.models import Learner, Section

G = {
    'text': '#052e16', 'muted': '#4b7a5a', 'bg': '#f0fdf4',
    'card': '#ffffff', 'border': '#d1fae5', 'primary': '#16a34a',
    'accent': '#fbbf24', 'red': '#dc2626', 'section_head': '#14532d',
    'tvl': '#0f766e', 'yellow': '#d97706',
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
MODALITIES = ['Modular (Print)', 'Modular (Digital)', 'Online',
               'Educational Television', 'Radio-Based Instruction', 'Blended', 'Face to Face']
MOTHER_TONGUES = ['Cebuano', 'Filipino', 'Tagalog', 'Ilocano',
                  'Bisaya', 'Waray', 'Kapampangan', 'Pangasinense', 'Other']

INPUT_STYLE = (
    f'QLineEdit{{background:{G["bg"]};border:1.5px solid {G["border"]};border-radius:8px;'
    f'padding:9px 14px;font-size:13px;color:{G["text"]};min-height:36px;}}'
    f'QLineEdit:focus{{border-color:{G["primary"]};background:#ffffff;}}'
)
COMBO_STYLE = (
    f'QComboBox{{background:{G["bg"]};border:1.5px solid {G["border"]};border-radius:8px;'
    f'padding:7px 34px 7px 14px;font-size:13px;color:{G["text"]};min-height:36px;}}'
    f'QComboBox:focus{{border-color:{G["primary"]};background:#ffffff;}}'
    f'QComboBox::drop-down{{border:none;width:28px;}}'
    f'QComboBox::down-arrow{{image:none;width:0;}}'
    f'QComboBox QAbstractItemView{{background:#ffffff;border:1px solid {G["border"]};'
    f'selection-background-color:#dcfce7;selection-color:{G["text"]};border-radius:8px;}}'
)
DATE_STYLE = (
    f'QDateEdit{{background:{G["bg"]};border:1.5px solid {G["border"]};border-radius:8px;'
    f'padding:7px 14px;font-size:13px;color:{G["text"]};min-height:36px;}}'
    f'QDateEdit:focus{{border-color:{G["primary"]};background:#ffffff;}}'
)


def _lbl(text, required=False):
    l = QLabel(text + (' *' if required else ''))
    l.setStyleSheet(
        f'font-size:10.5px;font-weight:700;color:{G["muted"]};'
        'text-transform:uppercase;letter-spacing:0.8px;background:transparent;'
    )
    return l


def _inp(ph=''):
    e = QLineEdit()
    e.setPlaceholderText(ph)
    e.setMinimumHeight(36)
    e.setStyleSheet(INPUT_STYLE)
    return e


def _combo(items):
    c = QComboBox()
    c.addItems(items)
    c.setMinimumHeight(36)
    c.setStyleSheet(COMBO_STYLE)
    return c


def _divider():
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet(f'background:{G["border"]};max-height:1px;border:none;margin:4px 0;')
    return f


def _card(icon, title, head_color=None):
    color = head_color or G['section_head']
    frame = QFrame()
    frame.setObjectName('fc')
    frame.setStyleSheet(
        f'QFrame#fc{{background:{G["card"]};border:1px solid {G["border"]};border-radius:16px;}}'
    )
    vbox = QVBoxLayout(frame)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(0)
    head = QWidget()
    head.setFixedHeight(46)
    head.setStyleSheet(
        f'background:{color};border-top-left-radius:15px;border-top-right-radius:15px;'
    )
    hl = QHBoxLayout(head)
    hl.setContentsMargins(24, 0, 24, 0)
    il = QLabel(icon)
    il.setStyleSheet(f'color:{G["accent"]};font-size:16px;background:transparent;')
    tl = QLabel(title)
    tl.setStyleSheet('color:#fff;font-size:13px;font-weight:700;background:transparent;')
    hl.addWidget(il)
    hl.addSpacing(8)
    hl.addWidget(tl)
    hl.addStretch()
    vbox.addWidget(head)
    body = QWidget()
    body.setStyleSheet('background:transparent;')
    bl = QVBoxLayout(body)
    bl.setContentsMargins(24, 22, 24, 22)
    bl.setSpacing(14)
    vbox.addWidget(body)
    return frame, bl


def _radio_row(options, default=None):
    w = QWidget()
    w.setStyleSheet('background:transparent;')
    h = QHBoxLayout(w)
    h.setContentsMargins(0, 2, 0, 0)
    h.setSpacing(20)
    g = QButtonGroup(w)
    for opt in options:
        rb = QRadioButton(opt)
        rb.setStyleSheet(f'font-size:13px;color:{G["text"]};background:transparent;')
        if opt == default:
            rb.setChecked(True)
        g.addButton(rb)
        h.addWidget(rb)
    h.addStretch()
    return w, g


def _grid_w(cols):
    w = QWidget()
    w.setStyleSheet('background:transparent;')
    g = QGridLayout(w)
    g.setContentsMargins(0, 0, 0, 0)
    g.setHorizontalSpacing(16)
    g.setVerticalSpacing(10)
    return w, g


class SHSLearnerEditDialog(QDialog):
    def __init__(self, learner_id, parent=None):
        super().__init__(parent)
        self.learner_id = learner_id
        self.learner = Learner.get_by_id(learner_id)
        self.setWindowTitle(f'Edit — {self.learner.full_name}')
        self.setMinimumWidth(1100)
        self.setMinimumHeight(700)
        self.setStyleSheet(f'QDialog{{background:{G["bg"]};}}')
        self._sel_track = self.learner.track or ''
        self._sel_electives = [e.strip() for e in (self.learner.electives or '').split(',') if e.strip()]
        self._sel_section = self.learner.section_name or ''
        self._initial_status = self.learner.status or 'Pending'
        self._elective_btns = []
        self._section_btns = []
        self._build_ui()
        self._populate()

    def _rval(self, grp):
        b = grp.checkedButton()
        return b.text() if b else ''

    # ── Track pill style ──────────────────────────────────────────
    def _track_style(self, selected, color):
        if selected:
            return (
                f'QPushButton{{background:{color};color:#fff;border:2px solid {color};'
                f'border-radius:10px;font-size:13px;font-weight:700;padding:8px 22px;}}'
                f'QPushButton:hover{{opacity:0.9;}}'
            )
        return (
            f'QPushButton{{background:transparent;color:{color};border:2px solid {color};'
            f'border-radius:10px;font-size:13px;font-weight:700;padding:8px 22px;}}'
            f'QPushButton:hover{{background:{color};color:#fff;}}'
        )

    def _elv_style(self, selected, color):
        if selected:
            return (
                f'QPushButton{{background:{color};color:#fff;border:1.5px solid {color};'
                f'border-radius:8px;font-size:12px;font-weight:600;padding:6px 14px;}}'
            )
        return (
            f'QPushButton{{background:transparent;color:{color};border:1.5px solid {color};'
            f'border-radius:8px;font-size:12px;font-weight:600;padding:6px 14px;}}'
            f'QPushButton:hover{{background:{color};color:#fff;}}'
        )

    def _sec_pill_style(self, sel):
        if sel:
            return (
                f'QPushButton{{background:{G["primary"]};color:#fff;'
                f'border:2px solid {G["primary"]};border-radius:20px;'
                f'font-size:12px;font-weight:700;padding:5px 16px;}}'
            )
        return (
            f'QPushButton{{background:transparent;color:{G["primary"]};'
            f'border:2px solid {G["primary"]};border-radius:20px;'
            f'font-size:12px;font-weight:700;padding:5px 16px;}}'
            f'QPushButton:hover{{background:{G["primary"]};color:#fff;}}'
        )

    def _on_track(self, track_name, color):
        self._sel_track = track_name
        for tn, (btn, tc) in self._track_btns.items():
            btn.setStyleSheet(self._track_style(tn == track_name, tc))
        # rebuild electives
        electives = ACADEMIC_ELECTIVES if track_name == 'Academic' else TVL_ELECTIVES
        for i in reversed(range(self._elv_grid.count())):
            w = self._elv_grid.itemAt(i).widget()
            if w: w.setParent(None)
        self._elective_btns.clear()
        self._sel_electives = []
        for i, e in enumerate(electives):
            tc = G['primary'] if track_name == 'Academic' else G['tvl']
            btn = QPushButton(e)
            btn.setCheckable(True)
            btn.setStyleSheet(self._elv_style(False, tc))
            btn.clicked.connect(lambda _, ev=e, c=tc: self._toggle_elv(ev, c))
            self._elective_btns.append((btn, e, tc))
            self._elv_grid.addWidget(btn, i // 2, i % 2)
        self._elv_lbl.show()
        self._elv_container.show()

    def _toggle_elv(self, elective, color):
        if elective in self._sel_electives:
            self._sel_electives.remove(elective)
        else:
            self._sel_electives.append(elective)
        for btn, e, c in self._elective_btns:
            btn.setStyleSheet(self._elv_style(e in self._sel_electives, c))

    def _toggle_sec(self, name):
        self._sel_section = '' if self._sel_section == name else name
        for btn, sn in self._section_btns:
            btn.setStyleSheet(self._sec_pill_style(sn == self._sel_section))

    def _rebuild_sections(self):
        for i in reversed(range(self._sec_hbox.count())):
            w = self._sec_hbox.itemAt(i).widget()
            if w: w.setParent(None)
        self._section_btns.clear()
        sections = Section.get_all(grade=self.learner.grade, level='SHS')
        if not sections:
            lbl = QLabel(f'No sections available.')
            lbl.setStyleSheet(f'font-size:12px;color:{G["muted"]};background:transparent;')
            self._sec_hbox.addWidget(lbl)
        else:
            for sec in sections:
                btn = QPushButton(sec.name)
                btn.setCheckable(True)
                btn.setChecked(sec.name == self._sel_section)
                btn.setStyleSheet(self._sec_pill_style(sec.name == self._sel_section))
                btn.clicked.connect(lambda _, sn=sec.name: self._toggle_sec(sn))
                self._section_btns.append((btn, sec.name))
                self._sec_hbox.addWidget(btn)
            self._sec_hbox.addStretch()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Scroll area ───────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea{border:none;background:transparent;}')
        container = QWidget()
        container.setStyleSheet(f'background:{G["bg"]};')
        scroll.setWidget(container)
        outer.addWidget(scroll)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 28, 32, 20)
        layout.setSpacing(20)

        # ── Title ─────────────────────────────────────────────────
        title_lbl = QLabel(f'Editing: {self.learner.full_name}')
        title_lbl.setStyleSheet(
            f'font-size:22px;font-weight:800;color:{G["text"]};background:transparent;'
        )
        layout.addWidget(title_lbl)

        # ══ CARD 1 — Identification ═══════════════════════════════
        c1, b1 = _card('🪪', 'IDENTIFICATION')
        gw, g = _grid_w(3)
        g.addWidget(_lbl('PSA Birth Certificate No.'), 0, 0)
        self.psa = _inp('e.g. 2024-012345')
        g.addWidget(self.psa, 1, 0)
        g.addWidget(_lbl('Learner Reference No. (LRN)', required=True), 0, 1)
        self.lrn = _inp('Enter LRN')
        self.lrn.setStyleSheet(
            INPUT_STYLE +
            f'QLineEdit{{font-family:Courier New;font-weight:700;color:{G["primary"]};}}'
        )
        g.addWidget(self.lrn, 1, 1)
        g.addWidget(_lbl('Place of Birth', required=True), 0, 2)
        self.place_of_birth = _inp('e.g. Cebu City')
        g.addWidget(self.place_of_birth, 1, 2)
        b1.addWidget(gw)

        row2w = QWidget(); row2w.setStyleSheet('background:transparent;')
        row2h = QHBoxLayout(row2w); row2h.setContentsMargins(0,0,0,0); row2h.setSpacing(32)
        lrn_v = QVBoxLayout(); lrn_v.setSpacing(4)
        lrn_v.addWidget(_lbl('With LRN?', required=True))
        lrn_r, self._lrn_grp = _radio_row(['Yes', 'No'])
        lrn_v.addWidget(lrn_r)
        row2h.addLayout(lrn_v)
        balik_v = QVBoxLayout(); balik_v.setSpacing(4)
        balik_v.addWidget(_lbl('Returning Learner (Balik-Aral)?'))
        balik_r, self._balik_grp = _radio_row(['Yes', 'No'], default='No')
        balik_v.addWidget(balik_r)
        row2h.addLayout(balik_v)
        row2h.addStretch()
        b1.addWidget(row2w)
        layout.addWidget(c1)

        # ══ CARD 2 — Personal Info ════════════════════════════════
        c2, b2 = _card('👤', 'PERSONAL INFORMATION')
        gw1, g1 = _grid_w(4)
        g1.addWidget(_lbl('Last Name', required=True), 0, 0, 1, 2)
        self.last_name = _inp('SURNAME')
        g1.addWidget(self.last_name, 1, 0, 1, 2)
        g1.addWidget(_lbl('First Name', required=True), 0, 2)
        self.first_name = _inp('GIVEN NAME')
        g1.addWidget(self.first_name, 1, 2)
        g1.addWidget(_lbl('Middle Name'), 0, 3)
        self.middle_name = _inp('MIDDLE NAME')
        g1.addWidget(self.middle_name, 1, 3)
        b2.addWidget(gw1)

        gw2, g2 = _grid_w(4)
        g2.addWidget(_lbl('Birthdate', required=True), 0, 0)
        self.birthdate = QDateEdit(QDate.currentDate())
        self.birthdate.setCalendarPopup(True)
        self.birthdate.setMinimumHeight(36)
        self.birthdate.setStyleSheet(DATE_STYLE)
        g2.addWidget(self.birthdate, 1, 0)
        g2.addWidget(_lbl('Age', required=True), 0, 1)
        self.age = _inp('0')
        g2.addWidget(self.age, 1, 1)
        g2.addWidget(_lbl('Extension Name'), 0, 2)
        self.extension = _inp('e.g. Jr.')
        g2.addWidget(self.extension, 1, 2)
        g2.addWidget(_lbl('Mother Tongue'), 0, 3)
        self.mother_tongue = _combo(MOTHER_TONGUES)
        g2.addWidget(self.mother_tongue, 1, 3)
        b2.addWidget(gw2)
        b2.addWidget(_divider())

        flags_w = QWidget(); flags_w.setStyleSheet('background:transparent;')
        flags_h = QHBoxLayout(flags_w); flags_h.setContentsMargins(0,0,0,0); flags_h.setSpacing(32)
        sv = QVBoxLayout(); sv.setSpacing(4)
        sv.addWidget(_lbl('Sex', required=True))
        sex_r, self._sex_grp = _radio_row(['Male', 'Female'])
        sv.addWidget(sex_r)
        flags_h.addLayout(sv)
        ipv = QVBoxLayout(); ipv.setSpacing(4)
        ipv.addWidget(_lbl('Indigenous People (IP)?'))
        ip_r, self._ip_grp = _radio_row(['Yes', 'No'], default='No')
        ipv.addWidget(ip_r)
        flags_h.addLayout(ipv)
        fpsv = QVBoxLayout(); fpsv.setSpacing(4)
        fpsv.addWidget(_lbl('4Ps Beneficiary?'))
        fps_r, self._fps_grp = _radio_row(['Yes', 'No'], default='No')
        fpsv.addWidget(fps_r)
        flags_h.addLayout(fpsv)
        fps_id_v = QVBoxLayout(); fps_id_v.setSpacing(4)
        fps_id_v.addWidget(_lbl('4Ps Household ID No. (if yes)'))
        self.four_ps_id = _inp('Leave blank if N/A')
        fps_id_v.addWidget(self.four_ps_id)
        flags_h.addLayout(fps_id_v)
        flags_h.addStretch()
        b2.addWidget(flags_w)
        layout.addWidget(c2)

        # ══ CARD 3 — Address ══════════════════════════════════════
        c3, b3 = _card('🏠', 'ADDRESS')
        agw, ag = _grid_w(4)
        for lbl_t, fname, ph, span in [
            ('House No.', 'house_no', 'e.g. 123', 1),
            ('Street Name', 'street', 'Street Name', 2),
            ('Barangay', 'barangay', 'Barangay', 1),
        ]:
            col = {'house_no': 0, 'street': 1, 'barangay': 3}[fname]
            ag.addWidget(_lbl(lbl_t), 0, col, 1, span)
            w2 = _inp(ph)
            setattr(self, fname, w2)
            ag.addWidget(w2, 1, col, 1, span)
        b3.addWidget(agw)

        agw2, ag2 = _grid_w(3)
        for i, (lbl_t, fname, ph) in enumerate([
            ('Municipality / City', 'municipality', 'City'),
            ('Province', 'province', 'Province'),
            ('ZIP Code', 'zip_code', '0000'),
        ]):
            ag2.addWidget(_lbl(lbl_t), 0, i)
            w2 = _inp(ph)
            setattr(self, fname, w2)
            ag2.addWidget(w2, 1, i)
        b3.addWidget(agw2)
        layout.addWidget(c3)

        # ══ CARD 4 — Parents / Guardian ═══════════════════════════
        c4, b4 = _card('👨‍👩‍👧', 'PARENTS / GUARDIAN')
        for title_p, prefix in [
            ("Father's Name", 'father'),
            ("Mother's Maiden Name", 'mother'),
            ("Guardian (if different)", 'guardian'),
        ]:
            if prefix != 'father':
                b4.addWidget(_divider())
            b4.addWidget(_lbl(title_p))
            pgw, pg = _grid_w(4)
            pg.addWidget(_lbl('Last Name'), 0, 0)
            w_last = _inp('Surname')
            setattr(self, f'{prefix}_last_name', w_last)
            pg.addWidget(w_last, 1, 0)
            pg.addWidget(_lbl('First Name'), 0, 1, 1, 2)
            w_first = _inp('Given Name')
            setattr(self, f'{prefix}_first_name', w_first)
            pg.addWidget(w_first, 1, 1, 1, 2)
            pg.addWidget(_lbl('Contact Number'), 0, 3)
            w_contact = _inp('09XX-XXX-XXXX')
            setattr(self, f'{prefix}_contact', w_contact)
            pg.addWidget(w_contact, 1, 3)
            b4.addWidget(pgw)
        layout.addWidget(c4)

        # ══ CARD 5 — SHS Details ══════════════════════════════════
        c5, b5 = _card('🏫', f'SENIOR HIGH SCHOOL — GRADE {self.learner.grade} DETAILS')
        b5.addWidget(_lbl('Track', required=True))
        track_row = QWidget(); track_row.setStyleSheet('background:transparent;')
        tr_h = QHBoxLayout(track_row); tr_h.setContentsMargins(0,0,0,0); tr_h.setSpacing(12)
        self._track_btns = {}
        for tn, tc in [('Academic', G['primary']), ('TechPro/TVL', G['tvl'])]:
            btn = QPushButton(tn)
            btn.setCheckable(True)
            btn.setStyleSheet(self._track_style(False, tc))
            btn.clicked.connect(lambda _, t=tn, c=tc: self._on_track(t, c))
            self._track_btns[tn] = (btn, tc)
            tr_h.addWidget(btn)
        tr_h.addStretch()
        b5.addWidget(track_row)

        self._elv_lbl = _lbl('Electives — select all that apply', required=True)
        self._elv_lbl.hide()
        b5.addWidget(self._elv_lbl)
        self._elv_container = QWidget()
        self._elv_container.setStyleSheet('background:transparent;')
        self._elv_grid = QGridLayout(self._elv_container)
        self._elv_grid.setSpacing(8)
        self._elv_container.hide()
        b5.addWidget(self._elv_container)

        b5.addWidget(_divider())
        shr = QWidget(); shr.setStyleSheet('background:transparent;')
        sh = QHBoxLayout(shr); sh.setContentsMargins(0,0,0,0); sh.setSpacing(12)
        sh.addWidget(_lbl('Section Assignment'))
        sh.addStretch()
        b5.addWidget(shr)
        self._sec_container = QWidget(); self._sec_container.setStyleSheet('background:transparent;')
        self._sec_hbox = QHBoxLayout(self._sec_container)
        self._sec_hbox.setContentsMargins(0,0,0,0); self._sec_hbox.setSpacing(8)
        b5.addWidget(self._sec_container)

        b5.addWidget(_divider())
        sem_v = QVBoxLayout(); sem_v.setSpacing(4)
        sem_v.addWidget(_lbl('Semester', required=True))
        sem_r, self._sem_grp = _radio_row(['1st Sem', '2nd Sem'], default='1st Sem')
        sem_v.addWidget(sem_r)
        sem_w = QWidget(); sem_w.setStyleSheet('background:transparent;')
        sem_w.setLayout(sem_v)
        b5.addWidget(sem_w)
        layout.addWidget(c5)

        # ══ CARD 6 — Previous School ══════════════════════════════
        c6, b6 = _card('📚', 'PREVIOUS SCHOOL RECORD')
        pgw2, pg2 = _grid_w(3)
        pg2.addWidget(_lbl('Last Grade Level Completed'), 0, 0)
        self.last_grade = _inp('e.g. Grade 10')
        pg2.addWidget(self.last_grade, 1, 0)
        pg2.addWidget(_lbl('Last School Year Completed'), 0, 1)
        self.last_sy = _inp('e.g. 2023-2024')
        pg2.addWidget(self.last_sy, 1, 1)
        pg2.addWidget(_lbl('Last School Attended'), 0, 2)
        self.last_school = _inp('School Name')
        pg2.addWidget(self.last_school, 1, 2)
        b6.addWidget(pgw2)
        layout.addWidget(c6)

        # ══ CARD 7 — Modality ═════════════════════════════════════
        c7, b7 = _card('📡', 'LEARNING MODALITY')
        mod_w = QWidget(); mod_w.setStyleSheet('background:transparent;')
        mod_h = QHBoxLayout(mod_w); mod_h.setContentsMargins(0,0,0,0); mod_h.setSpacing(12)
        self._modality_checks = []
        for m in MODALITIES:
            cb = QCheckBox(m)
            cb.setStyleSheet(f'font-size:12px;color:{G["text"]};background:transparent;')
            self._modality_checks.append(cb)
            mod_h.addWidget(cb)
        mod_h.addStretch()
        b7.addWidget(mod_w)
        layout.addWidget(c7)

        # ══ CARD 8 — Certification ════════════════════════════════
        c8, b8 = _card('✍️', 'CERTIFICATION')
        cgw, cg = _grid_w(2)
        cg.addWidget(_lbl('Certified by (Parent/Guardian Name)'), 0, 0)
        self.certifier_name = _inp('Full Name of Parent/Guardian')
        cg.addWidget(self.certifier_name, 1, 0)
        cg.addWidget(_lbl('Date Signed'), 0, 1)
        self.date_signed = QDateEdit(QDate.currentDate())
        self.date_signed.setCalendarPopup(True)
        self.date_signed.setMinimumHeight(36)
        self.date_signed.setStyleSheet(DATE_STYLE)
        cg.addWidget(self.date_signed, 1, 1)
        b8.addWidget(cgw)
        layout.addWidget(c8)

        # ══ Status ════════════════════════════════════════════════
        c9, b9 = _card('📋', 'ENROLLMENT STATUS', head_color='#1d4ed8')
        sw, sg = _grid_w(2)
        sg.addWidget(_lbl('Status'), 0, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Pending', 'Enrolled', 'Dropped', 'Transferred'])
        self.status_combo.setMinimumHeight(36)
        self.status_combo.setStyleSheet(COMBO_STYLE)
        sg.addWidget(self.status_combo, 1, 0)
        b9.addWidget(sw)
        layout.addWidget(c9)

        # ══ Bottom buttons ════════════════════════════════════════
        btn_bar = QWidget(); btn_bar.setStyleSheet('background:transparent;')
        bh = QHBoxLayout(btn_bar); bh.setContentsMargins(0, 8, 0, 8); bh.setSpacing(12)

        del_btn = QPushButton('🗑  Delete Enrollee')
        del_btn.setMinimumHeight(40)
        del_btn.setStyleSheet(
            f'QPushButton{{background:#fef2f2;color:{G["red"]};border:1.5px solid #fecaca;'
            f'border-radius:10px;font-size:13px;font-weight:700;padding:8px 20px;}}'
            f'QPushButton:hover{{background:{G["red"]};color:#fff;border-color:{G["red"]};}}'
        )
        del_btn.clicked.connect(self._delete)
        bh.addWidget(del_btn)
        bh.addStretch()

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setStyleSheet(
            f'QPushButton{{background:transparent;color:{G["muted"]};border:1.5px solid {G["border"]};'
            f'border-radius:10px;font-size:13px;font-weight:700;padding:8px 20px;}}'
            f'QPushButton:hover{{background:{G["border"]};}}'
        )
        cancel_btn.clicked.connect(self.reject)
        bh.addWidget(cancel_btn)

        save_btn = QPushButton('💾  Save Changes')
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet(
            f'QPushButton{{background:{G["primary"]};color:#fff;border:none;'
            f'border-radius:10px;font-size:13px;font-weight:700;padding:8px 24px;}}'
            f'QPushButton:hover{{background:#15803d;}}'
        )
        save_btn.clicked.connect(self._save)
        bh.addWidget(save_btn)

        outer.addWidget(btn_bar)
        # add bottom bar padding inside outer
        outer.setContentsMargins(32, 0, 32, 16)

        self._rebuild_sections()

    def _populate(self):
        l = self.learner
        # Identification
        self.psa.setText(l.psa_birth_cert or '')
        self.lrn.setText(l.lrn or '')
        self.place_of_birth.setText(l.place_of_birth or '')
        self._set_radio(self._lrn_grp, 'Yes' if l.has_lrn else 'No')
        self._set_radio(self._balik_grp, 'Yes' if l.is_balik_aral else 'No')
        # Personal
        self.last_name.setText(l.last_name or '')
        self.first_name.setText(l.first_name or '')
        self.middle_name.setText(l.middle_name or '')
        if l.birthdate:
            self.birthdate.setDate(QDate(l.birthdate.year, l.birthdate.month, l.birthdate.day))
        self.age.setText(str(l.age) if l.age else '')
        self.extension.setText(l.extension_name or '')
        idx = self.mother_tongue.findText(l.mother_tongue or '')
        if idx >= 0: self.mother_tongue.setCurrentIndex(idx)
        self._set_radio(self._sex_grp, 'Male' if l.sex == 'M' else 'Female')
        self._set_radio(self._ip_grp, 'Yes' if l.is_ip else 'No')
        self._set_radio(self._fps_grp, 'Yes' if l.is_four_ps else 'No')
        self.four_ps_id.setText(l.four_ps_id or '')
        # Address
        self.house_no.setText(l.house_no or '')
        self.street.setText(l.street or '')
        self.barangay.setText(l.barangay or '')
        self.municipality.setText(l.municipality or '')
        self.province.setText(l.province or '')
        self.zip_code.setText(l.zip_code or '')
        # Parents
        self.father_last_name.setText(l.father_last_name or '')
        self.father_first_name.setText(l.father_first_name or '')
        self.father_contact.setText(l.father_contact or '')
        self.mother_last_name.setText(l.mother_last_name or '')
        self.mother_first_name.setText(l.mother_first_name or '')
        self.mother_contact.setText(l.mother_contact or '')
        self.guardian_last_name.setText(l.guardian_last_name or '')
        self.guardian_first_name.setText(l.guardian_first_name or '')
        self.guardian_contact.setText(l.guardian_contact or '')
        # SHS details — trigger track to build electives
        if l.track:
            tc = G['primary'] if l.track == 'Academic' else G['tvl']
            self._on_track(l.track, tc)
            # now restore elective selections
            self._sel_electives = [e.strip() for e in (l.electives or '').split(',') if e.strip()]
            for btn, e, c in self._elective_btns:
                btn.setStyleSheet(self._elv_style(e in self._sel_electives, c))
        # Semester
        sem_val = (l.semester or '1st') + ' Sem'
        self._set_radio(self._sem_grp, sem_val)
        # Previous school
        self.last_grade.setText(l.last_grade_completed or '')
        self.last_sy.setText(l.last_sy_completed or '')
        self.last_school.setText(l.last_school_attended or '')
        # Certification
        self.certifier_name.setText(l.certifier_name or '')
        # Status
        self.status_combo.setCurrentText(l.status or 'Pending')

    def _set_radio(self, grp, value):
        for btn in grp.buttons():
            if btn.text() == value:
                btn.setChecked(True)
                return

    def _save(self):
        if not self.last_name.text().strip():
            QMessageBox.warning(self, 'Required', 'Last name is required.'); return
        if not self.first_name.text().strip():
            QMessageBox.warning(self, 'Required', 'First name is required.'); return
        section_id = None
        for sec in Section.get_all(grade=self.learner.grade, level='SHS'):
            if sec.name == self._sel_section:
                section_id = sec.id
                break

        status = self.status_combo.currentText()

        try:
            Learner.update(
                self.learner_id,
                lrn=self.lrn.text().strip(),
                has_lrn=(self._rval(self._lrn_grp) == 'Yes'),
                psa_birth_cert=self.psa.text().strip(),
                is_balik_aral=(self._rval(self._balik_grp) == 'Yes'),
                last_name=self.last_name.text().strip(),
                first_name=self.first_name.text().strip(),
                middle_name=self.middle_name.text().strip(),
                extension_name=self.extension.text().strip(),
                birthdate=self.birthdate.date().toPyDate(),
                age=int(self.age.text() or 0),
                sex='M' if self._rval(self._sex_grp) == 'Male' else 'F',
                place_of_birth=self.place_of_birth.text().strip(),
                mother_tongue=self.mother_tongue.currentText(),
                is_ip=(self._rval(self._ip_grp) == 'Yes'),
                is_four_ps=(self._rval(self._fps_grp) == 'Yes'),
                four_ps_id=self.four_ps_id.text().strip(),
                house_no=self.house_no.text().strip(),
                street=self.street.text().strip(),
                barangay=self.barangay.text().strip(),
                municipality=self.municipality.text().strip(),
                province=self.province.text().strip(),
                zip_code=self.zip_code.text().strip(),
                father_last_name=self.father_last_name.text().strip(),
                father_first_name=self.father_first_name.text().strip(),
                father_contact=self.father_contact.text().strip(),
                mother_last_name=self.mother_last_name.text().strip(),
                mother_first_name=self.mother_first_name.text().strip(),
                mother_contact=self.mother_contact.text().strip(),
                guardian_last_name=self.guardian_last_name.text().strip(),
                guardian_first_name=self.guardian_first_name.text().strip(),
                guardian_contact=self.guardian_contact.text().strip(),
                status=status,
                manual_status_override=(
                    status != self._initial_status
                    or getattr(self.learner, 'manual_status_override', False)
                ),
                section_id=section_id,
                track=self._sel_track,
                electives=','.join(self._sel_electives),
                tve_major=self._sel_electives[0] if self._sel_track == 'TechPro/TVL' and self._sel_electives else '',
                semester=self._rval(self._sem_grp).replace(' Sem', ''),
                last_grade_completed=self.last_grade.text().strip(),
                last_sy_completed=self.last_sy.text().strip(),
                last_school_attended=self.last_school.text().strip(),
                certifier_name=self.certifier_name.text().strip(),
            )
            QMessageBox.information(self, 'Saved', f'{self.learner.full_name} updated successfully!')
            self.accept()
        except Exception as e:
            show_error(self, 'Unable to Save Changes', e)

    def _delete(self):
        msg = QMessageBox(self)
        msg.setWindowTitle('Delete Enrollee')
        msg.setText(f'Permanently delete {self.learner.full_name}?')
        msg.setInformativeText('This cannot be undone. All their records will be removed.')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox { background-color: #ffffff; }
            QMessageBox QLabel { color: #052e16; font-size: 13px; background: transparent; }
            QMessageBox QPushButton {
                min-width: 80px; min-height: 32px; font-size: 13px; font-weight: 700;
                border-radius: 8px; padding: 6px 18px;
                background: #0369a1; color: #ffffff; border: 1.5px solid #0369a1;
            }
            QMessageBox QPushButton:hover { background: #0c4a6e; color: #ffffff; border-color: #0c4a6e; }
        """)
        yes_btn = msg.button(QMessageBox.Yes)
        no_btn  = msg.button(QMessageBox.No)
        if yes_btn:
            yes_btn.setText('Yes')
            yes_btn.setStyleSheet(
                'min-width:80px; min-height:32px; font-size:13px; font-weight:700;'
                'border-radius:8px; padding:6px 18px;'
                'background:#dc2626; color:#ffffff; border:1.5px solid #dc2626;'
            )
        if no_btn:
            no_btn.setText('No')
            no_btn.setStyleSheet(
                'min-width:80px; min-height:32px; font-size:13px; font-weight:700;'
                'border-radius:8px; padding:6px 18px;'
                'background:#0369a1; color:#ffffff; border:1.5px solid #0369a1;'
            )
        if msg.exec_() == QMessageBox.Yes:
            try:
                from core.database import execute
                execute('DELETE FROM enrollment_learner WHERE id = %s', (self.learner_id,))
                self.accept()
            except Exception as e:
                show_error(self, 'Unable to Delete Learner', e)
