# enrollment/shs_enrollment_form.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QComboBox, QCheckBox, QDateEdit,
    QPushButton, QFrame, QMessageBox, QButtonGroup, QRadioButton,
    QSizePolicy,
)
from PyQt5.QtCore import QDate, Qt
from core.errors import friendly_error_message
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
        f'QFrame#fc{{background:{G["card"]};border:1px solid {G["border"]};border-radius:16px;'
        f'box-shadow:0 2px 16px rgba(5,46,22,0.08);}}'
    )
    vbox = QVBoxLayout(frame)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(0)
    head = QWidget()
    head.setMinimumHeight(52)
    head.setStyleSheet(
        f'background:{color};border-top-left-radius:15px;border-top-right-radius:15px;'
    )
    hl = QHBoxLayout(head)
    hl.setContentsMargins(24, 0, 24, 0)
    il = QLabel(icon)
    il.setStyleSheet(f'color:{G["accent"]};font-size:16px;background:transparent;')
    tl = QLabel(title)
    tl.setStyleSheet('color:#fff;font-size:13px;font-weight:700;background:transparent;')
    tl.setWordWrap(True)
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


def _grid(cols):
    w = QWidget()
    w.setStyleSheet('background:transparent;')
    g = QGridLayout(w)
    g.setContentsMargins(0, 0, 0, 0)
    g.setHorizontalSpacing(16)
    g.setVerticalSpacing(10)
    return w, g


def _section_label(text):
    """Small all-caps divider label like in prototype."""
    l = QLabel(text)
    l.setStyleSheet(
        f'font-size:11px;font-weight:700;color:{G["muted"]};text-transform:uppercase;'
        f'letter-spacing:0.8px;background:transparent;margin-bottom:4px;'
    )
    return l


class SHSEnrollmentForm(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._sel_track = ''
        self._sel_electives = []
        self._sel_section = ''
        self._elective_btns = []
        self._section_btns = []
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea{border:none;background:transparent;}')
        container = QWidget()
        container.setStyleSheet('background:#f0fdf4;')
        scroll.setWidget(container)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

        form = QVBoxLayout(container)
        form.setContentsMargins(32, 28, 32, 32)
        form.setSpacing(0)

        # ── Page Header ────────────────────────────────────────────
        hdr = QWidget()
        hdr.setStyleSheet('background:transparent;')
        hdr_row = QHBoxLayout(hdr)
        hdr_row.setContentsMargins(0, 0, 0, 20)
        hdr_row.setSpacing(16)

        left = QWidget()
        left.setStyleSheet('background:transparent;')
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(4)
        bc = QLabel(f'Enrollment  /  Grade {self.grade}  /  New Learner')
        bc.setStyleSheet(f'font-size:12px;color:{G["muted"]};background:transparent;')
        pt = QLabel(f'Grade {self.grade} Enrollment Form')
        pt.setStyleSheet(f'font-size:24px;font-weight:800;color:{G["text"]};background:transparent;')
        ps = QLabel('Enhanced Basic Education Enrollment Form (BEEF) — Senior High School')
        ps.setStyleSheet(f'font-size:14px;color:{G["muted"]};background:transparent;')
        lv.addWidget(bc)
        lv.addWidget(pt)
        lv.addWidget(ps)

        self._badge = QFrame()
        self._badge.setObjectName('badge')
        self._badge.setMinimumWidth(210)
        self._badge.setStyleSheet(
            f'QFrame#badge{{border:2px solid {G["yellow"]};border-radius:12px;'
            f'background:rgba(217,119,6,0.08);}}'
        )
        bv = QVBoxLayout(self._badge)
        bv.setContentsMargins(18, 12, 18, 12)
        bv.setSpacing(2)
        self._badge_sm = QLabel('ENROLLMENT STATUS')
        self._badge_sm.setStyleSheet(
            f'font-size:9px;font-weight:700;color:{G["muted"]};'
            'text-transform:uppercase;letter-spacing:0.8px;background:transparent;'
        )
        self._badge_sm.setAlignment(Qt.AlignHCenter)
        self._badge_main = QLabel('⏳ Pending')
        self._badge_main.setStyleSheet(
            f'font-size:14px;font-weight:800;color:{G["yellow"]};background:transparent;'
        )
        self._badge_main.setAlignment(Qt.AlignHCenter)
        self._badge_sub = QLabel('No section assigned')
        self._badge_sub.setStyleSheet(f'font-size:10px;color:{G["muted"]};background:transparent;')
        self._badge_sub.setAlignment(Qt.AlignHCenter)
        self._badge_sub.setWordWrap(True)
        bv.addWidget(self._badge_sm)
        bv.addWidget(self._badge_main)
        bv.addWidget(self._badge_sub)

        hdr_row.addWidget(left, 1)
        hdr_row.addWidget(self._badge, 0, Qt.AlignTop)
        form.addWidget(hdr)

        # ── LEARNER IDENTIFICATION ─────────────────────────────────
        c, b = _card('🪪', 'LEARNER IDENTIFICATION')
        gw, g = _grid(3)
        g.addWidget(_lbl('PSA Birth Certificate No.'), 0, 0)
        self.psa = _inp('e.g. 2024-012345')
        g.addWidget(self.psa, 1, 0)
        g.addWidget(_lbl('Learner Reference No. (LRN)', required=True), 0, 1)
        self.lrn = _inp('Enter LRN')
        self.lrn.setStyleSheet(
            f'QLineEdit{{font-family:monospace;color:{G["primary"]};font-weight:500;letter-spacing:1px;'
            f'background:{G["bg"]};border:1.5px solid {G["border"]};border-radius:8px;padding:9px 14px;min-height:36px;}}'
            f'QLineEdit:focus{{border-color:{G["primary"]};background:#ffffff;}}'
        )
        g.addWidget(self.lrn, 1, 1)
        g.addWidget(_lbl('Place of Birth', required=True), 0, 2)
        self.place_of_birth = _inp('e.g. Cebu City')
        g.addWidget(self.place_of_birth, 1, 2)
        b.addWidget(gw)
        b.addWidget(_divider())

        rgw, rg = _grid(2)
        lrn_w = QWidget()
        lrn_w.setStyleSheet('background:transparent;')
        lrn_v = QVBoxLayout(lrn_w)
        lrn_v.setContentsMargins(0, 0, 0, 0)
        lrn_v.setSpacing(6)
        lrn_v.addWidget(_lbl('With LRN?', required=True))
        lrn_r, self._lrn_grp = _radio_row(['Yes', 'No'], default='Yes' if self.grade == 12 else 'No')
        lrn_v.addWidget(lrn_r)
        rg.addWidget(lrn_w, 0, 0)
        balik_w = QWidget()
        balik_w.setStyleSheet('background:transparent;')
        balik_v = QVBoxLayout(balik_w)
        balik_v.setContentsMargins(0, 0, 0, 0)
        balik_v.setSpacing(6)
        balik_v.addWidget(_lbl('Returning Learner (Balik-Aral)?'))
        balik_r, self._balik_grp = _radio_row(['Yes', 'No'], default='No')
        balik_v.addWidget(balik_r)
        rg.addWidget(balik_w, 0, 1)
        b.addWidget(rgw)
        form.addWidget(c)
        form.addSpacing(20)

        # ── LEARNER INFORMATION ────────────────────────────────────
        c2, b2 = _card('👤', 'LEARNER INFORMATION')
        g1w, g1 = _grid(4)
        g1.setColumnStretch(0, 2); g1.setColumnStretch(1, 2)
        g1.setColumnStretch(2, 2); g1.setColumnStretch(3, 1)
        g1.addWidget(_lbl('Last Name', required=True), 0, 0, 1, 2)
        self.last_name = _inp('SURNAME')
        g1.addWidget(self.last_name, 1, 0, 1, 2)
        g1.addWidget(_lbl('First Name', required=True), 0, 2)
        self.first_name = _inp('GIVEN NAME')
        g1.addWidget(self.first_name, 1, 2)
        g1.addWidget(_lbl('Middle Name'), 0, 3)
        self.middle_name = _inp('MIDDLE NAME')
        g1.addWidget(self.middle_name, 1, 3)
        b2.addWidget(g1w)

        g2w, g2 = _grid(4)
        g2.addWidget(_lbl('Birthdate', required=True), 0, 0)
        self.birthdate = QDateEdit(QDate.currentDate())
        self.birthdate.setCalendarPopup(True)
        self.birthdate.setMinimumHeight(36)
        self.birthdate.setStyleSheet(DATE_STYLE)
        g2.addWidget(self.birthdate, 1, 0)
        g2.addWidget(_lbl('Age', required=True), 0, 1)
        self.age = _inp(str(16 if self.grade == 11 else 17))
        g2.addWidget(self.age, 1, 1)
        g2.addWidget(_lbl('Extension Name'), 0, 2)
        self.extension = _inp('e.g. Jr.')
        g2.addWidget(self.extension, 1, 2)
        g2.addWidget(_lbl('Mother Tongue'), 0, 3)
        self.mother_tongue = _combo(MOTHER_TONGUES)
        g2.addWidget(self.mother_tongue, 1, 3)
        b2.addWidget(g2w)
        b2.addWidget(_divider())

        sw = QWidget()
        sw.setStyleSheet('background:transparent;')
        sv = QVBoxLayout(sw)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.setSpacing(6)
        sv.addWidget(_lbl('Sex', required=True))
        sex_r, self._sex_grp = _radio_row(['Male', 'Female'])
        sv.addWidget(sex_r)
        b2.addWidget(sw)
        b2.addWidget(_divider())

        g3w, g3 = _grid(3)
        ip_w = QWidget()
        ip_w.setStyleSheet('background:transparent;')
        ipv = QVBoxLayout(ip_w)
        ipv.setContentsMargins(0, 0, 0, 0)
        ipv.setSpacing(6)
        ipv.addWidget(_lbl('Indigenous People (IP)?'))
        ip_r, self._ip_grp = _radio_row(['Yes', 'No'], default='No')
        ipv.addWidget(ip_r)
        g3.addWidget(ip_w, 0, 0)
        fps_w = QWidget()
        fps_w.setStyleSheet('background:transparent;')
        fpsv = QVBoxLayout(fps_w)
        fpsv.setContentsMargins(0, 0, 0, 0)
        fpsv.setSpacing(6)
        fpsv.addWidget(_lbl('4Ps Beneficiary?'))
        fps_r, self._fps_grp = _radio_row(['Yes', 'No'], default='No')
        fpsv.addWidget(fps_r)
        g3.addWidget(fps_w, 0, 1)
        fps_id_w = QWidget()
        fps_id_w.setStyleSheet('background:transparent;')
        fps_id_v = QVBoxLayout(fps_id_w)
        fps_id_v.setContentsMargins(0, 0, 0, 0)
        fps_id_v.setSpacing(6)
        fps_id_v.addWidget(_lbl('4Ps Household ID No. (if yes)'))
        self.four_ps_id = _inp('Leave blank if N/A')
        fps_id_v.addWidget(self.four_ps_id)
        g3.addWidget(fps_id_w, 0, 2)
        b2.addWidget(g3w)
        form.addWidget(c2)
        form.addSpacing(20)

        # ── ADDRESS ────────────────────────────────────────────────
        c3, b3 = _card('📍', 'ADDRESS INFORMATION')
        b3.addWidget(_section_label('Current Address'))
        agw, ag = _grid(5)
        address_fields = [
            ('House No.', 'house_no', 'e.g. 123', 1),
            ('Street Name', 'street', 'Street Name', 2),
            ('Barangay', 'barangay', 'Barangay', 2),
        ]
        for col in range(5):
            ag.setColumnStretch(col, 1)
        for i, (lbl_t, attr, ph, span) in enumerate(address_fields):
            col = sum(s for _, _, _, s in address_fields[:i])
            ag.addWidget(_lbl(lbl_t), 0, col, 1, span)
            w2 = _inp(ph)
            setattr(self, attr, w2)
            ag.addWidget(w2, 1, col, 1, span)
        b3.addWidget(agw)
        agw2, ag2 = _grid(4)
        for i, (lbl_t, attr, ph) in enumerate([
            ('Municipality / City', 'municipality', 'City'),
            ('Province', 'province', 'Province'),
            ('Country', 'country', 'Philippines'),
            ('ZIP Code', 'zip_code', '0000'),
        ]):
            ag2.addWidget(_lbl(lbl_t), 0, i)
            w2 = _inp(ph)
            if attr == 'country':
                w2.setText('Philippines')
            setattr(self, attr, w2)
            ag2.addWidget(w2, 1, i)
        b3.addWidget(agw2)
        form.addWidget(c3)
        form.addSpacing(20)

        # ── PARENTS / GUARDIAN ─────────────────────────────────────
        c4, b4 = _card('👨\u200d👩\u200d👧', "PARENT'S / GUARDIAN'S INFORMATION")
        for group_label, prefix in [
            ("Father's Name", 'father'),
            ("Mother's Maiden Name", 'mother'),
            ("Guardian (if different)", 'guardian'),
        ]:
            if prefix != 'father':
                b4.addWidget(_divider())
            b4.addWidget(_section_label(group_label))
            pgw, pg = _grid(4)
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
        form.addWidget(c4)
        form.addSpacing(20)

        # ── TRACK & ELECTIVES ──────────────────────────────────────
        c5, b5 = _card('🏫', f'SENIOR HIGH SCHOOL — GRADE {self.grade} DETAILS')
        b5.addWidget(_lbl('Track', required=True))
        track_row = QWidget()
        track_row.setStyleSheet('background:transparent;')
        tr = QHBoxLayout(track_row)
        tr.setContentsMargins(0, 4, 0, 4)
        tr.setSpacing(14)
        self._track_btns = {}
        for tn, ti, ts, tc in [
            ('Academic', '📚', 'General & Specialized', G['primary']),
            ('TechPro/TVL', '🔧', 'Technical-Vocational-Livelihood', G['tvl']),
        ]:
            btn = QPushButton(f'{ti}  {tn}\n{ts}')
            btn.setCheckable(True)
            btn.setMinimumHeight(96)
            btn.setMinimumWidth(220)
            btn.setStyleSheet(self._track_style(False, tc))
            btn.clicked.connect(lambda _, t=tn, c=tc: self._on_track(t, c))
            self._track_btns[tn] = (btn, tc)
            tr.addWidget(btn)
        tr.addStretch()
        b5.addWidget(track_row)
        b5.addWidget(_divider())

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

        # Section header row
        sec_hdr = QWidget()
        sec_hdr.setStyleSheet('background:transparent;')
        shr = QHBoxLayout(sec_hdr)
        shr.setContentsMargins(0, 0, 0, 8)
        shr.setSpacing(10)
        shr.addWidget(_lbl('Section Assignment'))
        self._pend_badge = QLabel('⏳ Pending if unassigned')
        self._pend_badge.setStyleSheet(
            f'font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;'
            f'background:rgba(217,119,6,0.12);color:{G["yellow"]};'
        )
        shr.addWidget(self._pend_badge)
        shr.addStretch()
        b5.addWidget(sec_hdr)

        self._sec_container = QWidget()
        self._sec_container.setStyleSheet('background:transparent;')
        self._sec_hbox = QHBoxLayout(self._sec_container)
        self._sec_hbox.setContentsMargins(0, 0, 0, 0)
        self._sec_hbox.setSpacing(8)
        self._no_sec_lbl = QLabel(
            f'No sections available for Grade {self.grade}. Add sections from the Sections page.'
        )
        self._no_sec_lbl.setStyleSheet(
            f'font-size:13px;color:{G["muted"]};padding:14px 16px;'
            f'border:1.5px dashed {G["border"]};border-radius:10px;background:transparent;'
        )
        self._sec_hbox.addWidget(self._no_sec_lbl)
        b5.addWidget(self._sec_container)
        b5.addWidget(_divider())

        sem_w = QWidget()
        sem_w.setStyleSheet('background:transparent;')
        sem_v = QVBoxLayout(sem_w)
        sem_v.setContentsMargins(0, 0, 0, 0)
        sem_v.setSpacing(6)
        sem_v.addWidget(_lbl('Semester', required=True))
        sem_r, self._sem_grp = _radio_row(['1st Sem', '2nd Sem'], default='1st Sem')
        sem_v.addWidget(sem_r)
        b5.addWidget(sem_w)
        b5.addWidget(_divider())

        prev_title = ('For Returning Learner / Transfer-In'
                      if self.grade == 11 else 'Grade 11 Completion (Required for G12)')
        b5.addWidget(_section_label(prev_title))
        pg2w, pg2 = _grid(3)
        pg2.addWidget(_lbl('Last Grade Level Completed'), 0, 0)
        self.last_grade = _inp('e.g. Grade 10')
        pg2.addWidget(self.last_grade, 1, 0)
        pg2.addWidget(_lbl('Last School Year Completed'), 0, 1)
        self.last_sy = _inp('e.g. 2023-2024')
        pg2.addWidget(self.last_sy, 1, 1)
        pg2.addWidget(_lbl('Last School Attended'), 0, 2)
        self.last_school = _inp('School Name')
        pg2.addWidget(self.last_school, 1, 2)
        b5.addWidget(pg2w)
        b5.addWidget(_divider())

        b5.addWidget(_lbl('Preferred Distance Learning Modality'))
        mod_w = QWidget()
        mod_w.setStyleSheet('background:transparent;')
        mod_flow = QGridLayout(mod_w)
        mod_flow.setContentsMargins(0, 4, 0, 0)
        mod_flow.setSpacing(10)
        self._modality_checks = []
        for idx, m in enumerate(MODALITIES):
            cb = QCheckBox(m)
            cb.setStyleSheet(f'font-size:13px;color:{G["text"]};background:transparent;')
            if m == 'Face to Face':
                cb.setChecked(True)
            self._modality_checks.append(cb)
            mod_flow.addWidget(cb, idx // 4, idx % 4)
        b5.addWidget(mod_w)
        form.addWidget(c5)
        form.addSpacing(20)

        # ── CERTIFICATION ──────────────────────────────────────────
        c6, b6 = _card('✍️', 'CERTIFICATION')
        note = QLabel(
            'I hereby certify that the above information given are true and correct to the best '
            'of my knowledge and I allow the Department of Education to use my child\'s details '
            'to create and/or update his/her profile in the Learner Information System. The '
            'information herein shall be treated as confidential in compliance with the Data '
            'Privacy Act of 2012.'
        )
        note.setWordWrap(True)
        note.setStyleSheet(f'font-size:12.5px;color:{G["muted"]};background:transparent;line-height:1.7;')
        b6.addWidget(note)
        cgw, cg = _grid(2)
        cg.addWidget(_lbl('Signature / Printed Name', required=True), 0, 0)
        self.certifier_name = _inp('Full Name of Parent/Guardian')
        cg.addWidget(self.certifier_name, 1, 0)
        cg.addWidget(_lbl('Date Signed', required=True), 0, 1)
        self.date_signed = QDateEdit(QDate.currentDate())
        self.date_signed.setCalendarPopup(True)
        self.date_signed.setMinimumHeight(36)
        self.date_signed.setStyleSheet(DATE_STYLE)
        cg.addWidget(self.date_signed, 1, 1)
        b6.addWidget(cgw)
        form.addWidget(c6)
        form.addSpacing(24)

        # ── Actions ────────────────────────────────────────────────
        # IMPORTANT: wrap in a QWidget so scroll area handles it properly
        act_widget = QWidget()
        act_widget.setStyleSheet('background:transparent;')
        act_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        act = QHBoxLayout(act_widget)
        act.setContentsMargins(0, 0, 0, 0)
        act.setSpacing(12)
        act.addStretch(1)

        clr = QPushButton('Clear Form')
        clr.setObjectName('btn_secondary')
        clr.setMinimumHeight(42)
        clr.setMinimumWidth(120)
        clr.setStyleSheet(
            f'QPushButton{{background:{G["bg"]};color:{G["text"]};border:1.5px solid {G["border"]};'
            f'border-radius:8px;padding:10px 24px;font-size:13.5px;font-weight:700;}}'
            f'QPushButton:hover{{background:#dcfce7;}}'
        )
        clr.clicked.connect(self._reset_form)

        sub = QPushButton('Submit Enrollment')
        sub.setMinimumHeight(42)
        sub.setMinimumWidth(180)
        sub.setStyleSheet(
            f'QPushButton{{background:{G["primary"]};color:#ffffff;border:none;'
            f'border-radius:8px;padding:10px 24px;font-size:13.5px;font-weight:700;}}'
            f'QPushButton:hover{{background:#15803d;}}'
            f'QPushButton:pressed{{background:#166534;}}'
        )
        sub.clicked.connect(self._save)

        act.addWidget(clr)
        act.addWidget(sub)
        form.addWidget(act_widget)
        form.addSpacing(8)

    # ── TRACK ──────────────────────────────────────────────────────
    def _track_style(self, selected, color):
        if selected:
            return (
                f'QPushButton{{border:2px solid {color};border-radius:12px;'
                f'background:{color}1A;color:#052e16;font-size:13px;font-weight:700;'
                f'padding:12px;text-align:center;}}'
            )
        return (
            f'QPushButton{{border:2px solid #d1fae5;border-radius:12px;'
            f'background:#f0fdf4;color:#052e16;font-size:13px;font-weight:500;'
            f'padding:12px;text-align:center;}}'
            f'QPushButton:hover{{border-color:{color};}}'
        )

    def _on_track(self, track_name, color):
        self._sel_track = track_name
        self._sel_electives = []
        for tn, (btn, tc) in self._track_btns.items():
            btn.setStyleSheet(self._track_style(tn == track_name, tc))
            btn.setChecked(tn == track_name)
        electives = ACADEMIC_ELECTIVES if track_name == 'Academic' else TVL_ELECTIVES
        cols = 3 if track_name == 'Academic' else 2
        for i in reversed(range(self._elv_grid.count())):
            w = self._elv_grid.itemAt(i).widget()
            if w:
                w.setParent(None)
        self._elective_btns.clear()
        for i, e in enumerate(electives):
            r, c = divmod(i, cols)
            btn = QPushButton(e)
            btn.setCheckable(True)
            btn.setMinimumHeight(52)
            btn.setStyleSheet(self._elv_style(False, color))
            btn.clicked.connect(lambda _, ev=e, col=color: self._toggle_elv(ev, col))
            self._elective_btns.append((btn, e, color))
            self._elv_grid.addWidget(btn, r, c)
        self._elv_lbl.show()
        self._elv_container.show()
        self._update_badge()

    def _elv_style(self, sel, color):
        if sel:
            return (
                f'QPushButton{{border:1.5px solid {color};border-radius:10px;'
                f'background:{color}1A;color:{color};font-size:12.5px;font-weight:700;'
                f'padding:8px 14px;text-align:left;}}'
            )
        return (
            f'QPushButton{{border:1.5px solid #d1fae5;border-radius:10px;'
            f'background:#f0fdf4;color:#052e16;font-size:12.5px;font-weight:500;'
            f'padding:8px 14px;text-align:left;}}'
            f'QPushButton:hover{{border-color:{color};}}'
        )

    def _toggle_elv(self, elective, color):
        if elective in self._sel_electives:
            self._sel_electives.remove(elective)
        else:
            self._sel_electives.append(elective)
        for btn, e, c in self._elective_btns:
            btn.setStyleSheet(self._elv_style(e in self._sel_electives, c))

    def _sec_pill_style(self, sel):
        if sel:
            return (
                f'QPushButton{{border:2px solid {G["primary"]};border-radius:10px;'
                f'background:{G["primary"]}1A;color:{G["primary"]};font-size:13px;'
                f'font-weight:700;padding:6px 18px;}}'
            )
        return (
            f'QPushButton{{border:2px solid #d1fae5;border-radius:10px;'
            f'background:#f0fdf4;color:#052e16;font-size:13px;'
            f'font-weight:500;padding:6px 18px;}}'
            f'QPushButton:hover{{border-color:{G["primary"]};}}'
        )

    def _rebuild_sections(self, sections):
        for i in reversed(range(self._sec_hbox.count())):
            w = self._sec_hbox.itemAt(i).widget()
            if w:
                w.setParent(None)
        self._section_btns.clear()
        if not sections:
            self._sec_hbox.addWidget(self._no_sec_lbl)
            self._no_sec_lbl.show()
        else:
            self._no_sec_lbl.hide()
            for sec in sections:
                btn = QPushButton(sec.name)
                btn.setCheckable(True)
                btn.setMinimumHeight(42)
                btn.setMinimumWidth(110)
                btn.setStyleSheet(self._sec_pill_style(False))
                btn.clicked.connect(lambda _, sn=sec.name: self._toggle_sec(sn))
                self._section_btns.append((btn, sec.name))
                self._sec_hbox.addWidget(btn)
            self._sec_hbox.addStretch()

    def _toggle_sec(self, name):
        self._sel_section = '' if self._sel_section == name else name
        for btn, sn in self._section_btns:
            btn.setStyleSheet(self._sec_pill_style(sn == self._sel_section))
            btn.setChecked(sn == self._sel_section)
        self._update_badge()

    def _update_badge(self):
        if self._sel_section:
            self._badge.setStyleSheet(
                f'QFrame#badge{{border:2px solid {G["primary"]};border-radius:12px;'
                f'background:rgba(22,163,74,0.08);}}'
            )
            self._badge_main.setStyleSheet(
                f'font-size:14px;font-weight:800;color:{G["primary"]};background:transparent;'
            )
            self._badge_main.setText('✓ Ready to Enroll')
            self._badge_sub.setText(f'Section: {self._sel_section}')
        else:
            self._badge.setStyleSheet(
                f'QFrame#badge{{border:2px solid {G["yellow"]};border-radius:12px;'
                f'background:rgba(217,119,6,0.08);}}'
            )
            self._badge_main.setStyleSheet(
                f'font-size:14px;font-weight:800;color:{G["yellow"]};background:transparent;'
            )
            self._badge_main.setText('⏳ Pending')
            self._badge_sub.setText('No section assigned')

    def _rval(self, grp):
        b = grp.checkedButton()
        return b.text() if b else ''

    def _save(self):
        if not self.lrn.text().strip():
            QMessageBox.warning(self, 'Required', 'LRN is required.'); return
        if not self.last_name.text().strip():
            QMessageBox.warning(self, 'Required', 'Last Name is required.'); return
        if not self.first_name.text().strip():
            QMessageBox.warning(self, 'Required', 'First Name is required.'); return
        if not self._rval(self._sex_grp):
            QMessageBox.warning(self, 'Required', 'Sex is required.'); return
        modality = ','.join(cb.text() for cb in self._modality_checks if cb.isChecked())
        status = 'Enrolled' if self._sel_section else 'Pending'
        section_id = None
        for sec in Section.get_all(grade=self.grade, level='SHS'):
            if sec.name == self._sel_section:
                section_id = sec.id
                break
        status = Learner.enrollment_status_for({
            'lrn': self.lrn.text().strip(),
            'last_name': self.last_name.text().strip(),
            'first_name': self.first_name.text().strip(),
            'birthdate': self.birthdate.date().toPyDate(),
            'sex': 'M' if self._rval(self._sex_grp) == 'Male' else 'F',
            'level': 'SHS',
            'section_id': section_id,
            'track': self._sel_track,
            'electives': ','.join(self._sel_electives),
            'tve_major': self._sel_electives[0] if self._sel_track == 'TechPro/TVL' and self._sel_electives else '',
            'status': status,
        })

        try:
            learner_id = Learner.create(
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
                level='SHS',
                grade=self.grade,
                section_id=section_id,
                track=self._sel_track,
                electives=','.join(self._sel_electives),
                tve_major=self._sel_electives[0] if self._sel_track == 'TechPro/TVL' and self._sel_electives else '',
                semester=self._rval(self._sem_grp).replace(' Sem', ''),
                status=status,
                school_year='2026-2027',
                modalities=modality,
                last_grade_completed=self.last_grade.text().strip(),
                last_sy_completed=self.last_sy.text().strip(),
                last_school_attended=self.last_school.text().strip(),
                certifier_name=self.certifier_name.text().strip(),
                date_signed=self.date_signed.date().toPyDate(),
            )
            saved = Learner.get_by_id(learner_id)
            saved_status = saved.status if saved else status
            msg = (f'Grade {self.grade} learner enrolled in {self._sel_section} successfully!'
                   if saved_status == 'Enrolled' else
                   '⏳ Learner saved as Pending — required enrollment details are incomplete.')
            QMessageBox.information(self, 'Success', msg)
            self._reset_form()
        except Exception as e:
            QMessageBox.critical(self, 'Unable to Save Learner', friendly_error_message(e))

    def _reset_form(self):
        for attr in ['lrn', 'psa', 'last_name', 'first_name', 'middle_name', 'extension',
                     'age', 'place_of_birth', 'four_ps_id', 'house_no', 'street',
                     'barangay', 'municipality', 'province', 'zip_code',
                     'father_last_name', 'father_first_name', 'father_contact',
                     'mother_last_name', 'mother_first_name', 'mother_contact',
                     'guardian_last_name', 'guardian_first_name', 'guardian_contact',
                     'last_grade', 'last_sy', 'last_school', 'certifier_name']:
            getattr(self, attr).clear()
        self._sel_track = ''
        self._sel_electives = []
        self._sel_section = ''
        for btn, _, _ in self._elective_btns:
            btn.setChecked(False)
        for btn, _ in self._section_btns:
            btn.setChecked(False)
        for tn, (btn, tc) in self._track_btns.items():
            btn.setStyleSheet(self._track_style(False, tc))
            btn.setChecked(False)
        self._update_badge()

    def refresh(self):
        sections = Section.get_all(grade=self.grade, level='SHS')
        self._rebuild_sections(sections)
