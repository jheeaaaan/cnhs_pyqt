# enrollment/jhs_enrollment_form.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QComboBox, QCheckBox, QDateEdit,
    QPushButton, QFrame, QMessageBox, QButtonGroup, QRadioButton,
)
from PyQt5.QtCore import QDate, Qt
from core.errors import show_error
from core.models import Learner, Section

G = {
    'text': '#052e16', 'muted': '#4b7a5a', 'bg': '#f0fdf4',
    'card': '#ffffff', 'border': '#d1fae5', 'primary': '#0369a1',
    'accent': '#38bdf8', 'red': '#dc2626', 'section_head': '#0c4a6e',
    'yellow': '#d97706',
}

TVE_MAJORS = [
    '', 
    'Computer Servicing System (CSS)', 
    'Dressmaking', 
    'Bread and Pastry Production (BPP)', 
    'Front Desk Office Services (FOS)', 
    'Food and Beverage Services (FBS)', 
    'Housekeeping', 
    'Technical Drafting', 
    'Carpentry', 
    'Electronic Installation Maintenance (EIM)', 
    'Electronic Products Assembly and Servicing (EPAS)', 
    'Beauty Care', 
    'Cookery'
]
MODALITIES = ['Modular (Print)', 'Modular (Digital)', 'Online',
               'Educational Television', 'Radio-Based Instruction', 'Blended', 'Face to Face']
MOTHER_TONGUES = ['Cebuano', 'Filipino', 'Tagalog', 'Ilocano',
                  'Bisaya', 'Waray', 'Kapampangan', 'Pangasinense', 'Other']


def _lbl(text, required=False):
    l = QLabel(text + (' *' if required else ''))
    l.setStyleSheet(f'font-size:10.5px;font-weight:700;color:{G["muted"]};'
                    'text-transform:uppercase;letter-spacing:0.8px;background:transparent;')
    return l


def _inp(ph=''):
    e = QLineEdit()
    e.setPlaceholderText(ph)
    e.setMinimumHeight(36)
    return e


def _divider():
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet(f'background:{G["border"]};max-height:1px;border:none;')
    return f


def _card(icon, title):
    frame = QFrame()
    frame.setObjectName('jfc')
    frame.setStyleSheet(
        f'QFrame#jfc{{background:{G["card"]};border:1px solid {G["border"]};border-radius:16px;}}'
    )
    vbox = QVBoxLayout(frame)
    vbox.setContentsMargins(0, 0, 0, 0)
    vbox.setSpacing(0)

    head = QWidget()
    head.setStyleSheet(f'background:{G["section_head"]};border-top-left-radius:15px;border-top-right-radius:15px;')
    hl = QHBoxLayout(head)
    hl.setContentsMargins(24, 13, 24, 13)
    il = QLabel(icon)
    il.setStyleSheet(f'color:{G["accent"]};font-size:16px;background:transparent;')
    tl = QLabel(title)
    tl.setStyleSheet('color:#fff;font-size:13px;font-weight:700;background:transparent;')
    hl.addWidget(il)
    hl.addWidget(tl)
    hl.addStretch()
    vbox.addWidget(head)

    body = QWidget()
    body.setStyleSheet('background:transparent;')
    bl = QVBoxLayout(body)
    bl.setContentsMargins(24, 24, 24, 24)
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
    g.setSpacing(16)
    for col in range(cols):
        g.setColumnStretch(col, 1)
    return w, g


class JHSEnrollmentForm(QWidget):
    def __init__(self, grade):
        super().__init__()
        self.grade = grade
        self._sel_section = ''
        self._section_btns = []
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        container = QWidget()
        scroll.setWidget(container)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

        form = QVBoxLayout(container)
        form.setContentsMargins(32, 28, 32, 32)
        form.setSpacing(0)

        # ── Page Header ───────────────────────────────────────────
        hdr = QWidget()
        hdr.setStyleSheet('background:transparent;')
        hdr_row = QHBoxLayout(hdr)
        hdr_row.setContentsMargins(0, 0, 0, 20)

        left = QWidget()
        left.setStyleSheet('background:transparent;')
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(4)
        bc = QLabel(f'JHS Enrollment  /  Grade {self.grade}  /  New Learner')
        bc.setStyleSheet(f'font-size:12px;color:{G["muted"]};background:transparent;')
        pt = QLabel(f'Grade {self.grade} JHS Enrollment Form')
        pt.setStyleSheet(f'font-size:24px;font-weight:800;color:{G["text"]};background:transparent;')
        ps = QLabel('Enhanced Basic Education Enrollment Form (BEEF) — Junior High School')
        ps.setStyleSheet(f'font-size:14px;color:{G["muted"]};background:transparent;')
        lv.addWidget(bc); lv.addWidget(pt); lv.addWidget(ps)

        self._badge = QFrame()
        self._badge.setObjectName('jbadge')
        self._badge.setStyleSheet(
            f'QFrame#jbadge{{border:2px solid {G["yellow"]};border-radius:12px;'
            f'background:rgba(217,119,6,0.08);}}'
        )
        bv = QVBoxLayout(self._badge)
        bv.setContentsMargins(18, 10, 18, 10)
        bv.setSpacing(2)
        self._badge_sm = QLabel('ENROLLMENT STATUS')
        self._badge_sm.setStyleSheet(
            f'font-size:9px;font-weight:700;color:{G["muted"]};'
            'text-transform:uppercase;letter-spacing:0.8px;background:transparent;'
        )
        self._badge_main = QLabel('⏳ Pending')
        self._badge_main.setStyleSheet(
            f'font-size:14px;font-weight:800;color:{G["yellow"]};background:transparent;'
        )
        self._badge_sub = QLabel('No section assigned')
        self._badge_sub.setStyleSheet(f'font-size:10px;color:{G["muted"]};background:transparent;')
        for w in [self._badge_sm, self._badge_main, self._badge_sub]:
            bv.addWidget(w, 0, Qt.AlignHCenter)

        hdr_row.addWidget(left, 1)
        hdr_row.addWidget(self._badge)
        form.addWidget(hdr)

        # ── LEARNER IDENTIFICATION ────────────────────────────────
        c, b = _card('🪪', 'LEARNER IDENTIFICATION')
        gw, g = _grid(3)
        g.addWidget(_lbl('PSA Birth Certificate No.'), 0, 0)
        self.psa = _inp('e.g. 2024-012345')
        g.addWidget(self.psa, 1, 0)
        g.addWidget(_lbl('Learner Reference No. (LRN)', required=True), 0, 1)
        self.lrn = _inp('Enter LRN')
        self.lrn.setStyleSheet(
            f'font-family:monospace;color:{G["primary"]};font-weight:500;letter-spacing:1px;'
            f'background:{G["bg"]};border:1.5px solid {G["border"]};border-radius:8px;padding:9px 14px;'
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
        lrn_r, self._lrn_grp = _radio_row(['Yes', 'No'], default='Yes')
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

        # ── LEARNER INFORMATION ───────────────────────────────────
        c2, b2 = _card('👤', 'LEARNER INFORMATION')
        g1w, g1 = _grid(4)
        g1.addWidget(_lbl('Last Name', required=True), 0, 0, 1, 2)
        self.last_name = _inp('SURNAME')
        g1.addWidget(self.last_name, 1, 0, 1, 2)
        g1.addWidget(_lbl('First Name', required=True), 0, 2)
        self.first_name = _inp('FIRST NAME')
        g1.addWidget(self.first_name, 1, 2)
        g1.addWidget(_lbl('Middle Name'), 0, 3)
        self.middle_name = _inp('MIDDLE NAME')
        g1.addWidget(self.middle_name, 1, 3)
        b2.addWidget(g1w)

        g2w, g2 = _grid(4)
        g2.addWidget(_lbl('Extension'), 0, 0)
        self.extension = _inp('e.g. Jr.')
        g2.addWidget(self.extension, 1, 0)
        g2.addWidget(_lbl('Birthdate', required=True), 0, 1)
        self.birthdate = QDateEdit(QDate.currentDate())
        self.birthdate.setCalendarPopup(True)
        self.birthdate.setMinimumHeight(36)
        g2.addWidget(self.birthdate, 1, 1)
        g2.addWidget(_lbl('Age', required=True), 0, 2)
        self.age = _inp(str(12 + self.grade - 7))
        g2.addWidget(self.age, 1, 2)
        g2.addWidget(_lbl('Mother Tongue'), 0, 3)
        self.mother_tongue = QComboBox()
        self.mother_tongue.addItems(MOTHER_TONGUES)
        self.mother_tongue.setMinimumHeight(36)
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

        g3.addWidget(_lbl('4Ps ID'), 0, 2)
        self.four_ps_id = _inp('Enter 4Ps ID')
        g3.addWidget(self.four_ps_id, 1, 2)
        b2.addWidget(g3w)
        form.addWidget(c2)
        form.addSpacing(20)

        # ── ADDRESS ───────────────────────────────────────────────
        c3, b3 = _card('🏠', 'ADDRESS')
        agw, ag = _grid(3)
        for i, (lbl_t, attr, ph) in enumerate([
            ('House No.', 'house_no', 'e.g. 123'),
            ('Street / Purok', 'street', 'e.g. Purok 4'),
            ('Barangay', 'barangay', 'e.g. Talisay'),
            ('Municipality / City', 'municipality', 'e.g. Talisay City'),
            ('Province', 'province', 'e.g. Cebu'),
            ('ZIP Code', 'zip_code', 'e.g. 6045'),
        ]):
            r, co = divmod(i, 3)
            ag.addWidget(_lbl(lbl_t), r * 2, co)
            w2 = _inp(ph)
            setattr(self, attr, w2)
            ag.addWidget(w2, r * 2 + 1, co)
        b3.addWidget(agw)
        form.addWidget(c3)
        form.addSpacing(20)

        # ── PARENTS / GUARDIAN ────────────────────────────────────
        c4, b4 = _card('👨\u200d👩\u200d👧', 'PARENTS / GUARDIAN')
        pgw, pg = _grid(3)
        for i, (lbl_t, attr, ph) in enumerate([
            ("Father's Last Name", 'father_last_name', ''),
            ("Father's First Name", 'father_first_name', ''),
            ("Father's Contact No.", 'father_contact', '+63'),
            ("Mother's Last Name", 'mother_last_name', ''),
            ("Mother's First Name", 'mother_first_name', ''),
            ("Mother's Contact No.", 'mother_contact', '+63'),
            ("Guardian's Last Name", 'guardian_last_name', ''),
            ("Guardian's First Name", 'guardian_first_name', ''),
            ("Guardian's Contact No.", 'guardian_contact', '+63'),
        ]):
            r, co = divmod(i, 3)
            pg.addWidget(_lbl(lbl_t), r * 2, co)
            w2 = _inp(ph)
            setattr(self, attr, w2)
            pg.addWidget(w2, r * 2 + 1, co)
        b4.addWidget(pgw)
        form.addWidget(c4)
        form.addSpacing(20)

        # ── ENROLLMENT DETAILS ────────────────────────────────────
        c5, b5 = _card('📋', 'ENROLLMENT DETAILS')

        if self.grade >= 8:
            tve_w = QWidget()
            tve_w.setStyleSheet('background:transparent;')
            tvev = QVBoxLayout(tve_w)
            tvev.setContentsMargins(0, 0, 0, 0)
            tvev.setSpacing(6)
            tvev.addWidget(_lbl('TLE / TVE Major'))
            self.tve_major = QComboBox()
            self.tve_major.addItems(TVE_MAJORS)
            self.tve_major.setMinimumHeight(36)
            tvev.addWidget(self.tve_major)
            b5.addWidget(tve_w)
            b5.addWidget(_divider())
        else:
            self.tve_major = None

        sec_hdr = QWidget()
        sec_hdr.setStyleSheet('background:transparent;')
        shr = QHBoxLayout(sec_hdr)
        shr.setContentsMargins(0, 0, 0, 8)
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

        b5.addWidget(_lbl('Preferred Distance Learning Modality'))
        mod_w = QWidget()
        mod_w.setStyleSheet('background:transparent;')
        mod_h = QHBoxLayout(mod_w)
        mod_h.setContentsMargins(0, 4, 0, 0)
        mod_h.setSpacing(14)
        self._modality_checks = []
        for m in MODALITIES:
            cb = QCheckBox(m)
            cb.setStyleSheet(f'font-size:13px;color:{G["text"]};')
            if m == 'Face to Face':
                cb.setChecked(True)
            self._modality_checks.append(cb)
            mod_h.addWidget(cb)
        mod_h.addStretch()
        b5.addWidget(mod_w)
        b5.addWidget(_divider())

        b5.addWidget(_lbl('Previous School'))
        pg2w, pg2 = _grid(3)
        pg2.addWidget(_lbl('Last Grade Level Completed'), 0, 0)
        self.last_grade = _inp(f'e.g. Grade {self.grade - 1}')
        pg2.addWidget(self.last_grade, 1, 0)
        pg2.addWidget(_lbl('Last School Year Completed'), 0, 1)
        self.last_sy = _inp('e.g. 2023-2024')
        pg2.addWidget(self.last_sy, 1, 1)
        pg2.addWidget(_lbl('Last School Attended'), 0, 2)
        self.last_school = _inp('School Name')
        pg2.addWidget(self.last_school, 1, 2)
        b5.addWidget(pg2w)
        form.addWidget(c5)
        form.addSpacing(20)

        # ── CERTIFICATION ─────────────────────────────────────────
        c6, b6 = _card('✍️', 'CERTIFICATION')
        note = QLabel(
            'I hereby certify that the above information given are true and correct to the best '
            'of my knowledge and I allow the Department of Education to use my child\'s details '
            'to create and/or update his/her profile in the Learner Information System.'
        )
        note.setWordWrap(True)
        note.setStyleSheet(f'font-size:12.5px;color:{G["muted"]};background:transparent;')
        b6.addWidget(note)
        cgw, cg = _grid(2)
        cg.addWidget(_lbl('Signature / Printed Name', required=True), 0, 0)
        self.certifier_name = _inp('Full Name of Parent/Guardian')
        cg.addWidget(self.certifier_name, 1, 0)
        cg.addWidget(_lbl('Date Signed', required=True), 0, 1)
        self.date_signed = QDateEdit(QDate.currentDate())
        self.date_signed.setCalendarPopup(True)
        self.date_signed.setMinimumHeight(36)
        cg.addWidget(self.date_signed, 1, 1)
        b6.addWidget(cgw)
        form.addWidget(c6)
        form.addSpacing(20)

        # ── Actions ───────────────────────────────────────────────
        from PyQt5.QtWidgets import QSizePolicy as _SP
        act_widget = QWidget()
        act_widget.setStyleSheet('background:transparent;')
        act_widget.setSizePolicy(_SP.Expanding, _SP.Fixed)
        act = QHBoxLayout(act_widget)
        act.setContentsMargins(0, 0, 0, 0)
        act.setSpacing(12)
        act.addStretch(1)
        clr = QPushButton('Clear Form')
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
            f'QPushButton{{background:{G["primary"]};color:#fff;border:none;border-radius:8px;'
            f'padding:10px 24px;font-size:13.5px;font-weight:700;}}'
            f'QPushButton:hover{{background:#0284c7;}}'
            f'QPushButton:pressed{{background:#0c4a6e;}}'
        )
        sub.clicked.connect(self._save)
        act.addWidget(clr)
        act.addWidget(sub)
        form.addWidget(act_widget)
        form.addSpacing(8)

    def _sec_pill_style(self, sel):
        color = G['primary']
        if sel:
            return (f'QPushButton{{border:2px solid {color};border-radius:10px;'
                    f'background:{color}1A;color:{color};font-size:13px;'
                    f'font-weight:700;padding:6px 18px;}}')
        return (f'QPushButton{{border:2px solid #d1fae5;border-radius:10px;'
                f'background:#f0fdf4;color:#052e16;font-size:13px;'
                f'font-weight:500;padding:6px 18px;}}'
                f'QPushButton:hover{{border-color:{color};}}')

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
                btn.setMinimumHeight(36)
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
                f'QFrame#jbadge{{border:2px solid {G["primary"]};border-radius:12px;'
                f'background:rgba(3,105,161,0.08);}}'
            )
            self._badge_main.setStyleSheet(
                f'font-size:14px;font-weight:800;color:{G["primary"]};background:transparent;'
            )
            self._badge_main.setText('✓ Ready to Enroll')
            self._badge_sub.setText(f'Section: {self._sel_section}')
        else:
            self._badge.setStyleSheet(
                f'QFrame#jbadge{{border:2px solid {G["yellow"]};border-radius:12px;'
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
        lrn = self.lrn.text().strip()
        last_name = self.last_name.text().strip()
        first_name = self.first_name.text().strip()
        if not lrn:
            QMessageBox.warning(self, 'Validation', 'LRN is required.')
            return
        if not last_name or not first_name:
            QMessageBox.warning(self, 'Validation', 'Last name and first name are required.')
            return
        if not self._rval(self._sex_grp):
            QMessageBox.warning(self, 'Validation', 'Please select sex.')
            return

        status = 'Enrolled' if self._sel_section else 'Pending'
        section_id = None
        for sec in Section.get_all(grade=self.grade, level='JHS'):
            if sec.name == self._sel_section:
                section_id = sec.id
                break
        try:
            learner_id = Learner.create(
                lrn=lrn,
                has_lrn=(self._rval(self._lrn_grp) == 'Yes'),
                psa_birth_cert=self.psa.text().strip(),
                is_balik_aral=(self._rval(self._balik_grp) == 'Yes'),
                last_name=last_name,
                first_name=first_name,
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
                level='JHS', grade=self.grade,
                section_id=section_id,
                tve_major=self.tve_major.currentText() if self.tve_major else '',
                status=status, school_year='2026-2027',
                last_grade_completed=self.last_grade.text().strip(),
                last_sy_completed=self.last_sy.text().strip(),
                last_school_attended=self.last_school.text().strip(),
                certifier_name=self.certifier_name.text().strip(),
                date_signed=self.date_signed.date().toPyDate(),
            )
            saved = Learner.get_by_id(learner_id)
            saved_status = saved.status if saved else status
            QMessageBox.information(self, 'Success',
                f'Grade {self.grade} JHS learner saved!\nStatus: {saved_status}')
            self._reset_form()
        except Exception as e:
            show_error(self, 'Unable to Save Learner', e)

    def _reset_form(self):
        for attr in ['lrn', 'psa', 'last_name', 'first_name', 'middle_name', 'extension',
                     'age', 'place_of_birth', 'four_ps_id', 'house_no', 'street',
                     'barangay', 'municipality', 'province', 'zip_code',
                     'father_last_name', 'father_first_name', 'father_contact',
                     'mother_last_name', 'mother_first_name', 'mother_contact',
                     'guardian_last_name', 'guardian_first_name', 'guardian_contact',
                     'last_grade', 'last_sy', 'last_school', 'certifier_name']:
            getattr(self, attr).clear()
        self._sel_section = ''
        for btn, _ in self._section_btns:
            btn.setChecked(False)
            btn.setStyleSheet(self._sec_pill_style(False))
        self._update_badge()

    def refresh(self):
        sections = Section.get_all(grade=self.grade, level='JHS')
        self._rebuild_sections(sections)
