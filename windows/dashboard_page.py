# windows/dashboard_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from core.models import Learner, BMIRecord


class DashboardPage(QWidget):
    def __init__(self, navigate_fn=None):
        super().__init__()
        self._navigate = navigate_fn
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        greeting = QLabel('Welcome back! 👋')
        greeting.setObjectName('page_title')

        sub = QLabel('Cansojong National High School · School Year 2026–2027 · DepEd Region VII')
        sub.setObjectName('page_sub')

        layout.addWidget(greeting)
        layout.addWidget(sub)

        overview_lbl = QLabel('OVERVIEW')
        overview_lbl.setObjectName('stat_label')
        layout.addWidget(overview_lbl)

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(16)
        layout.addLayout(self.stats_grid)

        quick_lbl = QLabel('QUICK ACCESS')
        quick_lbl.setObjectName('stat_label')
        layout.addWidget(quick_lbl)

        self.shortcuts_layout = QGridLayout()
        self.shortcuts_layout.setSpacing(14)
        layout.addLayout(self.shortcuts_layout)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

        self.refresh()

    def refresh(self):
        self._refresh_stats()
        self._refresh_shortcuts()

    def _refresh_stats(self):
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            jhs_enrolled = Learner.count(level='JHS', status='Enrolled')
            shs_enrolled = Learner.count(level='SHS', status='Enrolled')
            bmi_jhs = len(BMIRecord.get_all(level='JHS'))
            bmi_shs = len(BMIRecord.get_all(level='SHS'))
        except Exception:
            jhs_enrolled = shs_enrolled = bmi_jhs = bmi_shs = 0

        cards = [
            ('JHS LEARNERS',      str(jhs_enrolled), '🏫', '#dbeafe', '#1d4ed8', 'Grades 7 to 10'),
            ('SHS LEARNERS',      str(shs_enrolled), '🎓', '#dcfce7', '#15803d', 'Grades 11 to 12'),
            ('BMI RECORDS — JHS', str(bmi_jhs),      '⚖️', '#ccfbf1', '#0f766e', 'Grades 7 to 10'),
            ('BMI RECORDS — SHS', str(bmi_shs),      '⚖️', '#fef9c3', '#a16207', 'Grades 11 to 12'),
        ]

        for i, (lbl, num, icon, bg, number_color, note) in enumerate(cards):
            card = self._make_stat_card(lbl, num, icon, bg, number_color, note)
            self.stats_grid.addWidget(card, 0, i)

    def _make_stat_card(self, label_text, number, icon, bg, number_color, note):
        card = QFrame()
        card.setObjectName('stat_card')
        card.setStyleSheet(
            f'QFrame#stat_card {{'
            f'  background: {bg};'
            f'  border: 1px solid rgba(0,0,0,0.07);'
            f'  border-radius: 16px;'
            f'}}'
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        lbl_text = QLabel(label_text)
        lbl_text.setObjectName('stat_label')
        lbl_text.setStyleSheet('background: transparent;')

        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(40, 40)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(
            'background: rgba(255,255,255,0.55); border-radius:10px; font-size:18px;'
        )

        top_row.addWidget(lbl_text)
        top_row.addStretch()
        top_row.addWidget(icon_lbl)

        num_lbl = QLabel(number)
        num_lbl.setObjectName('stat_number')
        num_lbl.setStyleSheet(
            f'font-size: 32px; font-weight: bold; color: {number_color}; background: transparent;'
        )

        note_lbl = QLabel(note)
        note_lbl.setObjectName('page_sub')
        note_lbl.setStyleSheet(
            f'font-size: 11.5px; color: {number_color}; background: transparent;'
        )

        layout.addLayout(top_row)
        layout.addSpacing(6)
        layout.addWidget(num_lbl)
        layout.addWidget(note_lbl)

        return card

    def _refresh_shortcuts(self):
        while self.shortcuts_layout.count():
            item = self.shortcuts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        shortcuts = [
            ('📝', '#dcfce7', 'Grade 11 Enrollment', 'SHS · Academic & TVL',    'shs11enroll'),
            ('📝', '#dcfce7', 'Grade 12 Enrollment', 'SHS · Academic & TVL',    'shs12enroll'),
            ('📋', '#dbeafe', 'Grade 7 Enrollment',  'JHS · Junior High School', 'jhs7enroll'),
            ('⚖️', '#ccfbf1', 'Grade 11 BMI Entry',  'Academic Track',           'bmi_shs11'),
            ('⚖️', '#ccfbf1', 'Grade 12 BMI Entry',  'TechPro / TVL Track',     'bmi_shs12'),
            ('⚙️', '#fef9c3', 'Change Password',      'Account Settings',         'change_password'),
        ]

        for i, (icon, bg, title, note, page_key) in enumerate(shortcuts):
            card = self._make_shortcut_card(icon, bg, title, note, page_key)
            self.shortcuts_layout.addWidget(card, i // 3, i % 3)

    def _make_shortcut_card(self, icon, bg, title, note, page_key):
        card = QFrame()
        card.setObjectName('card')

        if self._navigate:
            card.setCursor(QCursor(Qt.PointingHandCursor))

        card.setStyleSheet(
            'QFrame#card {'
            '  background: #ffffff;'
            '  border: 1px solid #d1fae5;'
            '  border-radius: 14px;'
            '  padding: 6px;'
            '}'
            'QFrame#card:hover {'
            '  background: #f0fdf4;'
            '  border-color: #16a34a;'
            '}'
        )

        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(44, 44)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(
            f'background:{bg}; border-radius:12px; font-size:20px;'
        )

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet('font-size:13px; font-weight:bold; color:#052e16;')
        note_lbl = QLabel(note)
        note_lbl.setStyleSheet('font-size:11px; color:#4b7a5a;')
        text_col.addWidget(title_lbl)
        text_col.addWidget(note_lbl)

        arrow_lbl = QLabel('→')
        arrow_lbl.setStyleSheet('font-size:16px; color:#16a34a; background:transparent;')

        layout.addWidget(icon_lbl)
        layout.addLayout(text_col)
        layout.addStretch()
        layout.addWidget(arrow_lbl)

        if self._navigate:
            _key = page_key
            _nav = self._navigate

            def mouse_press(event, k=_key):
                if event.button() == Qt.LeftButton:
                    _nav(k)

            card.mousePressEvent = mouse_press

        return card