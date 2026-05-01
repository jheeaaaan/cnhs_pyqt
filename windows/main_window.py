from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QScrollArea,
)
from PyQt5.QtCore import Qt
import core.auth as auth

PAGE_INFO = {
    'dashboard':        ('Welcome Back! 👋',                   None,             False, False),
    'jhs7enroll':       ('Grade 7 – JHS Enrollment Form',      'JHS ENROLLMENT', False, True),
    'jhs7sections':     ('Grade 7 – JHS Section Management',   'JHS ENROLLMENT', False, True),
    'jhs7report':       ('Grade 7 – JHS Enrollment Report',    'JHS REPORTS',    False, True),
    'jhs8enroll':       ('Grade 8 – JHS Enrollment Form',      'JHS ENROLLMENT', False, True),
    'jhs8sections':     ('Grade 8 – JHS Section Management',   'JHS ENROLLMENT', False, True),
    'jhs8report':       ('Grade 8 – JHS Enrollment Report',    'JHS REPORTS',    False, True),
    'jhs9enroll':       ('Grade 9 – JHS Enrollment Form',      'JHS ENROLLMENT', False, True),
    'jhs9sections':     ('Grade 9 – JHS Section Management',   'JHS ENROLLMENT', False, True),
    'jhs9report':       ('Grade 9 – JHS Enrollment Report',    'JHS REPORTS',    False, True),
    'jhs10enroll':      ('Grade 10 – JHS Enrollment Form',     'JHS ENROLLMENT', False, True),
    'jhs10sections':    ('Grade 10 – JHS Section Management',  'JHS ENROLLMENT', False, True),
    'jhs10report':      ('Grade 10 – JHS Enrollment Report',   'JHS REPORTS',    False, True),
    'bmi_jhs7':         ('Grade 7 – JHS Body Mass Index',      'JHS BMI',        True,  True),
    'bmi_jhs7_report':  ('Grade 7 – JHS BMI Report',           'JHS BMI',        True,  True),
    'bmi_jhs8':         ('Grade 8 – JHS Body Mass Index',      'JHS BMI',        True,  True),
    'bmi_jhs8_report':  ('Grade 8 – JHS BMI Report',           'JHS BMI',        True,  True),
    'bmi_jhs9':         ('Grade 9 – JHS Body Mass Index',      'JHS BMI',        True,  True),
    'bmi_jhs9_report':  ('Grade 9 – JHS BMI Report',           'JHS BMI',        True,  True),
    'bmi_jhs10':        ('Grade 10 – JHS Body Mass Index',     'JHS BMI',        True,  True),
    'bmi_jhs10_report': ('Grade 10 – JHS BMI Report',          'JHS BMI',        True,  True),
    'shs11enroll':      ('Grade 11 – Enrollment Form',         'ENROLLMENT',     False, False),
    'shs11sections':    ('Grade 11 – Section Management',      'ENROLLMENT',     False, False),
    'shs11report':      ('Grade 11 – Enrollment Report',       'REPORTS',        False, False),
    'shs12enroll':      ('Grade 12 – Enrollment Form',         'ENROLLMENT',     False, False),
    'shs12sections':    ('Grade 12 – Section Management',      'ENROLLMENT',     False, False),
    'shs12report':      ('Grade 12 – Enrollment Report',       'REPORTS',        False, False),
    'bmi_shs11':        ('Grade 11 – Body Mass Index',         'BODY MASS INDEX',True,  False),
    'bmi_shs11_report': ('Grade 11 – BMI Report',              'BMI REPORTS',    True,  False),
    'bmi_shs12':        ('Grade 12 – Body Mass Index',         'BODY MASS INDEX',True,  False),
    'bmi_shs12_report': ('Grade 12 – BMI Report',              'BMI REPORTS',    True,  False),
    'change_password':  ('Change Password',                    'SETTINGS',       False, False),
}


class CollapsibleGroup(QWidget):
    def __init__(self, label, badge_text, active_color, parent=None):
        super().__init__(parent)
        self.setObjectName('sidebar')
        self._open = True

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 2)
        outer.setSpacing(0)

        self._header = QPushButton()
        self._header.setObjectName('sidebar_group_header')
        self._header.setCursor(Qt.PointingHandCursor)
        self._header.clicked.connect(self._toggle)

        inner = QHBoxLayout(self._header)
        inner.setContentsMargins(8, 8, 10, 8)
        inner.setSpacing(9)

        badge = QLabel(badge_text)
        badge.setFixedSize(22, 22)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            'background: rgba(255,255,255,0.18); border-radius: 6px;'
            'font-size: 9px; font-weight: 800; color: #fff;'
        )

        lbl = QLabel(label)
        lbl.setStyleSheet('color: #fff; font-size: 14.5px; font-weight: 700; background: transparent;')

        self._chevron = QLabel('▾')
        self._chevron.setStyleSheet('color: rgba(255,255,255,0.6); font-size: 10px; background: transparent;')

        inner.addWidget(badge)
        inner.addWidget(lbl)
        inner.addStretch()
        inner.addWidget(self._chevron)

        self._body = QWidget()
        self._body.setObjectName('sidebar')
        self._body_layout = QVBoxLayout(self._body)
        self._body_layout.setContentsMargins(0, 0, 0, 0)
        self._body_layout.setSpacing(0)

        outer.addWidget(self._header)
        outer.addWidget(self._body)

    def add_item(self, btn):
        self._body_layout.addWidget(btn)

    def _toggle(self):
        self._open = not self._open
        self._body.setVisible(self._open)
        self._chevron.setText('▾' if self._open else '▸')

    def set_has_active(self, has_active):
        if has_active and not self._open:
            self._header.setStyleSheet(
                'QPushButton { background: rgba(22,163,74,0.15); border-radius: 8px; border: none; }'
            )
        else:
            self._header.setStyleSheet(
                'QPushButton { background: transparent; border-radius: 8px; border: none; }'
                'QPushButton:hover { background: rgba(255,255,255,0.09); }'
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cansojong NHS — Enrollment & BMI System')
        self.setMinimumSize(1200, 750)
        self._pages = {}
        self._nav_btns = {}
        self._current_page = 'dashboard'
        self.setup_ui()
        self.show_page('dashboard')

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self.build_sidebar())

        right = QWidget()
        right.setStyleSheet('background: #f0fdf4;')
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self._topbar = self.build_topbar()
        right_layout.addWidget(self._topbar)

        self.stack = QStackedWidget()
        right_layout.addWidget(self.stack, stretch=1)
        root.addWidget(right, stretch=1)

    def build_topbar(self):
        bar = QWidget()
        bar.setObjectName('topbar')
        bar.setFixedHeight(58)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(10)

        self._topbar_title = QLabel('Welcome Back! 👋')
        self._topbar_title.setObjectName('topbar_title')

        self._topbar_tag = QLabel()
        self._topbar_tag.setObjectName('topbar_tag')
        self._topbar_tag.hide()

        layout.addWidget(self._topbar_title)
        layout.addWidget(self._topbar_tag)
        layout.addStretch()

        user = auth.get_current_user()
        user_chip = QLabel(f'👤  {user.username if user else "admin"}')
        user_chip.setStyleSheet('color: #4b7a5a; font-size: 12px; font-weight: 600; background: transparent;')
        layout.addWidget(user_chip)
        return bar

    def update_topbar(self, page_key):
        info = PAGE_INFO.get(page_key)
        if not info:
            if page_key.startswith('shs_sec_detail_'):
                parts = page_key.split('_')
                grade = parts[3]
                title = f'Grade {grade} – Section Detail'
                tag, is_bmi, is_jhs = 'ENROLLMENT', False, False
            else:
                title = page_key.replace('_', ' ').title()
                tag, is_bmi, is_jhs = None, False, False
        else:
            title, tag, is_bmi, is_jhs = info

        self._topbar_title.setText(title)

        if tag:
            self._topbar_tag.setText(tag)
            self._topbar_tag.show()
            if is_jhs and is_bmi:
                obj = 'topbar_tag_bmi'
            elif is_jhs:
                obj = 'topbar_tag_jhs'
            elif is_bmi:
                obj = 'topbar_tag_bmi'
            else:
                obj = 'topbar_tag'
            self._topbar_tag.setObjectName(obj)
            self._topbar_tag.setStyleSheet(self._topbar_tag.styleSheet())
        else:
            self._topbar_tag.hide()

    def build_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName('sidebar')
        sidebar.setFixedWidth(270)

        outer = QVBoxLayout(sidebar)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # header
        header = QWidget()
        header.setObjectName('sidebar')
        header.setMinimumHeight(72)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(14, 14, 14, 14)
        hl.setSpacing(10)

        logo = QLabel('🎓')
        logo.setAlignment(Qt.AlignCenter)
        logo.setFixedSize(40, 40)
        logo.setStyleSheet('background: #fbbf24; border-radius: 10px; font-size: 20px; padding: 4px;')

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        school = QLabel('Cansojong NHS')
        school.setObjectName('sidebar_school')
        school.setWordWrap(True)
        sub = QLabel('Enrollment & BMI')
        sub.setObjectName('sidebar_sub')
        sub.setWordWrap(True)
        text_col.addWidget(school)
        text_col.addWidget(sub)

        hl.addWidget(logo, 0, Qt.AlignVCenter)
        hl.addLayout(text_col, 1)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet('background: rgba(255,255,255,0.07);')
        div.setFixedHeight(1)

        outer.addWidget(header)
        outer.addWidget(div)

        # scrollable nav
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('background: transparent; border: none;')

        nav_body = QWidget()
        nav_body.setObjectName('sidebar')
        nav_layout = QVBoxLayout(nav_body)
        nav_layout.setContentsMargins(8, 8, 8, 12)
        nav_layout.setSpacing(2)

        nav_layout.addWidget(self.nav_btn('dashboard', '🏠  Dashboard'))
        nav_layout.addSpacing(4)

        nav_layout.addWidget(self.section_divider('Junior High School'))
        nav_layout.addWidget(self.section_label('JHS ENROLLMENT'))

        for g in [7, 8, 9, 10]:
            grp = CollapsibleGroup(f'Grade {g} Enrollment', f'G{g}', '#0369a1')
            grp.add_item(self.nav_btn(f'jhs{g}enroll',   f'  📝  G{g} Enrollment Form', navtype='jhs'))
            grp.add_item(self.nav_btn(f'jhs{g}sections', f'  ⊞  G{g} Sections',         navtype='jhs'))
            grp.add_item(self.nav_btn(f'jhs{g}report',   f'  📊  G{g} Report',           navtype='jhs'))
            grp._open = False
            grp._body.setVisible(False)
            grp._chevron.setText('▸')
            nav_layout.addWidget(grp)

        nav_layout.addSpacing(4)
        nav_layout.addWidget(self.section_label('JHS BODY MASS INDEX'))
        for g in [7, 8, 9, 10]:
            grp = CollapsibleGroup(f'Grade {g} BMI', f'G{g}', '#0891b2')
            grp.add_item(self.nav_btn(f'bmi_jhs{g}',        f'  ⚖  G{g} BMI Entry',  navtype='bmi'))
            grp.add_item(self.nav_btn(f'bmi_jhs{g}_report', f'  📊  G{g} BMI Report', navtype='bmi'))
            grp._open = False
            grp._body.setVisible(False)
            grp._chevron.setText('▸')
            nav_layout.addWidget(grp)

        nav_layout.addSpacing(4)
        nav_layout.addWidget(self.section_divider('Senior High School'))
        nav_layout.addWidget(self.section_label('SHS ENROLLMENT'))

        for g in [11, 12]:
            grp = CollapsibleGroup(f'Grade {g} Enrollment', f'G{g}', '#16a34a')
            grp.add_item(self.nav_btn(f'shs{g}enroll',   f'  📝  G{g} Enrollment Form'))
            grp.add_item(self.nav_btn(f'shs{g}sections', f'  ⊞  G{g} Sections'))
            grp.add_item(self.nav_btn(f'shs{g}report',   f'  📊  G{g} Report'))
            nav_layout.addWidget(grp)

        nav_layout.addSpacing(4)
        nav_layout.addWidget(self.section_label('SHS BODY MASS INDEX'))
        for g in [11, 12]:
            grp = CollapsibleGroup(f'Grade {g} BMI', f'G{g}', '#0f766e')
            grp.add_item(self.nav_btn(f'bmi_shs{g}',        f'  ⚖  G{g} BMI Entry',  navtype='bmi'))
            grp.add_item(self.nav_btn(f'bmi_shs{g}_report', f'  📊  G{g} BMI Report', navtype='bmi'))
            nav_layout.addWidget(grp)

        nav_layout.addStretch()

        scroll.setWidget(nav_body)
        outer.addWidget(scroll, stretch=1)

        # footer
        footer_div = QFrame()
        footer_div.setFrameShape(QFrame.HLine)
        footer_div.setStyleSheet('background: rgba(255,255,255,0.07);')
        footer_div.setFixedHeight(1)

        user = auth.get_current_user()
        user_lbl = QLabel(f'  {user.username if user else "admin"}  ·  Administrator')
        user_lbl.setStyleSheet(
            'color: rgba(255,255,255,0.35); font-size: 10.5px;'
            'padding: 8px 16px; background: transparent;'
        )

        logout_btn = QPushButton('🚪  Logout')
        logout_btn.setObjectName('btn_logout')
        logout_btn.clicked.connect(self.logout)

        outer.addWidget(footer_div)
        outer.addWidget(user_lbl)
        outer.addWidget(logout_btn)

        return sidebar

    # Style applied when a nav button is active (checked)
    _ACTIVE_STYLE = (
        'background: rgba(255,255,255,0.92);'
        'color: #052e16;'
        'font-size: 14px;'
        'font-weight: bold;'
        'border-left: 3px solid #fbbf24;'
        'padding-left: 15px;'
        'border-radius: 8px;'
    )
    # Style applied when a nav button is inactive
    _INACTIVE_STYLE = (
        'background: transparent;'
        'color: rgba(255,255,255,0.88);'
        'font-size: 14px;'
        'font-weight: normal;'
        'border-left: none;'
        'padding-left: 18px;'
        'border-radius: 8px;'
    )

    def nav_btn(self, key, label, navtype=None):
        btn = QPushButton(label)
        btn.setCheckable(True)
        nt = navtype or 'shs'
        btn.setObjectName(f'nav_{nt}')
        btn.setStyleSheet(self._INACTIVE_STYLE)
        btn.clicked.connect(lambda _, k=key: self.show_page(k))
        self._nav_btns[key] = btn
        return btn

    def section_divider(self, text):
        w = QWidget()
        w.setObjectName('sidebar')
        layout = QHBoxLayout(w)
        layout.setContentsMargins(8, 8, 8, 4)
        layout.setSpacing(8)

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet('background: rgba(255,255,255,0.10);')

        lbl = QLabel(text)
        lbl.setStyleSheet(
            'color: rgba(255,255,255,0.40); font-size: 9px; font-weight: 800;'
            'letter-spacing: 1.2px; background: transparent; white-space: nowrap;'
        )
        lbl.setAlignment(Qt.AlignCenter)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet('background: rgba(255,255,255,0.10);')

        layout.addWidget(line1)
        layout.addWidget(lbl)
        layout.addWidget(line2)
        return w

    def section_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName('sidebar_section')
        return lbl

    def open_section_detail(self, level, grade, section_id, section_name):
        from enrollment.shs_section_detail import SHSSectionDetailPage
        page_key = f'shs_sec_detail_{grade}_{section_id}'

        if page_key in self._pages:
            old = self._pages.pop(page_key)
            self.stack.removeWidget(old)
            old.deleteLater()

        page = SHSSectionDetailPage(grade, section_id, section_name)
        self._pages[page_key] = page
        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        self._current_page = page_key
        self.update_topbar(page_key)

        for btn in self._nav_btns.values():
            btn.setChecked(False)

    def go_back_to_sections(self, level, grade):
        key = f'shs{grade}sections'
        page = self.get_page(key)
        if page:
            page.refresh()
            self.stack.setCurrentWidget(page)
            self._current_page = key
            self.update_topbar(key)
            for k, btn in self._nav_btns.items():
                is_active = (k == key)
                btn.setChecked(is_active)
                btn.setStyleSheet(self._ACTIVE_STYLE if is_active else self._INACTIVE_STYLE)

    def get_page(self, name):
        if name not in self._pages:
            from windows.dashboard_page import DashboardPage
            from enrollment.shs_enrollment_form import SHSEnrollmentForm
            from enrollment.jhs_enrollment_form import JHSEnrollmentForm
            from enrollment.shs_sections_page import SHSSectionsPage
            from enrollment.jhs_sections_page import JHSSectionsPage
            from enrollment.shs_report_page import SHSReportPage
            from enrollment.jhs_report_page import JHSReportPage
            from bmi.bmi_entry_page import BMIEntryPage
            from bmi.bmi_report_page import BMIReportPage
            from windows.change_password import ChangePasswordPage

            page_map = {
                'dashboard':       lambda: DashboardPage(navigate_fn=self.show_page),
                'jhs7enroll':      lambda: JHSEnrollmentForm(grade=7),
                'jhs7sections':    lambda: JHSSectionsPage(grade=7),
                'jhs7report':      lambda: JHSReportPage(grade=7),
                'jhs8enroll':      lambda: JHSEnrollmentForm(grade=8),
                'jhs8sections':    lambda: JHSSectionsPage(grade=8),
                'jhs8report':      lambda: JHSReportPage(grade=8),
                'jhs9enroll':      lambda: JHSEnrollmentForm(grade=9),
                'jhs9sections':    lambda: JHSSectionsPage(grade=9),
                'jhs9report':      lambda: JHSReportPage(grade=9),
                'jhs10enroll':     lambda: JHSEnrollmentForm(grade=10),
                'jhs10sections':   lambda: JHSSectionsPage(grade=10),
                'jhs10report':     lambda: JHSReportPage(grade=10),
                'shs11enroll':     lambda: SHSEnrollmentForm(grade=11),
                'shs11sections':   lambda: SHSSectionsPage(grade=11),
                'shs11report':     lambda: SHSReportPage(grade=11),
                'shs12enroll':     lambda: SHSEnrollmentForm(grade=12),
                'shs12sections':   lambda: SHSSectionsPage(grade=12),
                'shs12report':     lambda: SHSReportPage(grade=12),
                'bmi_jhs7':        lambda: BMIEntryPage(level='JHS', grade=7),
                'bmi_jhs7_report': lambda: BMIReportPage(level='JHS', grade=7),
                'bmi_jhs8':        lambda: BMIEntryPage(level='JHS', grade=8),
                'bmi_jhs8_report': lambda: BMIReportPage(level='JHS', grade=8),
                'bmi_jhs9':        lambda: BMIEntryPage(level='JHS', grade=9),
                'bmi_jhs9_report': lambda: BMIReportPage(level='JHS', grade=9),
                'bmi_jhs10':       lambda: BMIEntryPage(level='JHS', grade=10),
                'bmi_jhs10_report':lambda: BMIReportPage(level='JHS', grade=10),
                'bmi_shs11':       lambda: BMIEntryPage(level='SHS', grade=11),
                'bmi_shs11_report':lambda: BMIReportPage(level='SHS', grade=11),
                'bmi_shs12':       lambda: BMIEntryPage(level='SHS', grade=12),
                'bmi_shs12_report':lambda: BMIReportPage(level='SHS', grade=12),
                'change_password': lambda: ChangePasswordPage(),
            }

            if name in page_map:
                widget = page_map[name]()
                self._pages[name] = widget
                self.stack.addWidget(widget)

        return self._pages.get(name)

    def show_page(self, name):
        page = self.get_page(name)
        if page:
            self.stack.setCurrentWidget(page)
            if hasattr(page, 'refresh'):
                page.refresh()

        self._current_page = name
        self.update_topbar(name)

        for k, btn in self._nav_btns.items():
            is_active = (k == name)
            btn.setChecked(is_active)
            btn.setStyleSheet(self._ACTIVE_STYLE if is_active else self._INACTIVE_STYLE)

    def logout(self):
        auth.logout()
        from windows.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()