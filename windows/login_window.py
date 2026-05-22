# windows/login_window.py  — matches Figma LoginPage.tsx
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import core.auth as auth


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cansojong NHS — Enrollment & BMI System')
        self.setObjectName('login_bg')
        self._build_ui()
        self.resize(640, 922)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(0)
        root.setAlignment(Qt.AlignCenter)

        logo = QLabel('🎓')
        logo.setAlignment(Qt.AlignCenter)
        logo.setFixedSize(80, 80)
        logo.setObjectName('login_logo')

        logo_shadow = QGraphicsDropShadowEffect()
        logo_shadow.setBlurRadius(32)
        logo_shadow.setOffset(0, 8)
        logo_shadow.setColor(QColor(251, 191, 36, 100))
        logo.setGraphicsEffect(logo_shadow)

        logo_wrap = QWidget()
        logo_wrap.setStyleSheet('background: transparent;')
        from PyQt5.QtWidgets import QVBoxLayout as VBL
        lw = VBL(logo_wrap)
        lw.setAlignment(Qt.AlignCenter)
        lw.setContentsMargins(0, 0, 0, 0)
        lw.addWidget(logo, 0, Qt.AlignCenter)

        school_name = QLabel('Cansojong National High School')
        school_name.setObjectName('login_school_name')
        school_name.setAlignment(Qt.AlignCenter)

        school_sub = QLabel('Enrollment & BMI Management System')
        school_sub.setObjectName('login_school_sub')
        school_sub.setAlignment(Qt.AlignCenter)

        badge = QLabel('🔐 Admin Portal · SY 2026 – 2027')
        badge.setObjectName('login_badge')
        badge.setAlignment(Qt.AlignCenter)

        root.addWidget(logo_wrap)
        root.addSpacing(12)
        root.addWidget(school_name)
        root.addSpacing(4)
        root.addWidget(school_sub)
        root.addSpacing(8)
        root.addWidget(badge, 0, Qt.AlignCenter)
        root.addSpacing(20)

        card = QFrame()
        card.setObjectName('login_card')
        card.setMaximumWidth(520)

        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(60)
        card_shadow.setOffset(0, 20)
        card_shadow.setColor(QColor(0, 0, 0, 64))
        card.setGraphicsEffect(card_shadow)

        card_layout = VBL(card)
        card_layout.setContentsMargins(32, 28, 32, 28)
        card_layout.setSpacing(6)

        card_title = QLabel('Admin Sign In')
        card_title.setObjectName('login_card_title')

        card_sub = QLabel('Enter your credentials to access the portal')
        card_sub.setObjectName('login_card_sub')

        card_layout.addWidget(card_title)
        card_layout.addWidget(card_sub)
        card_layout.addSpacing(18)

        lbl_user = QLabel('USERNAME')
        lbl_user.setObjectName('field_label')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        self.username_input.setMinimumHeight(50)

        lbl_pass = QLabel('PASSWORD')
        lbl_pass.setObjectName('field_label')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setMinimumHeight(50)
        self.password_input.returnPressed.connect(self._do_login)

        self.error_label = QLabel('')
        self.error_label.setObjectName('login_error')
        self.error_label.setAlignment(Qt.AlignLeft)
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        hint = QLabel('💡 Demo:  <b>admin</b> / <b>admin123</b>')
        hint.setObjectName('login_hint')
        hint.setTextFormat(Qt.RichText)

        login_btn = QPushButton('🔓  Sign In to Portal')
        login_btn.setMinimumHeight(52)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self._do_login)

        card_layout.addWidget(lbl_user)
        card_layout.addWidget(self.username_input)
        card_layout.addSpacing(10)
        card_layout.addWidget(lbl_pass)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(8)
        card_layout.addWidget(self.error_label)
        card_layout.addWidget(hint)
        card_layout.addSpacing(12)
        card_layout.addWidget(login_btn)

        root.addWidget(card)
        root.addSpacing(14)

        footer = QLabel('Cansojong NHS · DepEd Region VII · Cebu Province')
        footer.setObjectName('login_footer')
        footer.setAlignment(Qt.AlignCenter)
        root.addWidget(footer)

    def _do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self._show_error('⚠️  Please enter your username and password.')
            return

        ok, result = auth.login(username, password)
        if ok:
            from windows.main_window import MainWindow
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            self._show_error(f'⚠️  {result}')
            self.password_input.clear()

    def _show_error(self, msg):
        self.error_label.setText(msg)
        self.error_label.show()
