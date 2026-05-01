# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from core.styles import STYLESHEET
from windows.login_window import LoginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('CNHS System')
    app.setStyle('Fusion')

    # ── Load custom fonts from the fonts/ folder ──────────────────
    fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
    font_files = [
        "DMMono-Italic.ttf",
        "DMMono-Regular.ttf",
        "PlusJakartaSans-Bold.ttf",
        "PlusJakartaSans-Italic-VariableFont_wght.ttf",
        "PlusJakartaSans-SemiBold.ttf",
        "PlusJakartaSans-VariableFont_wght.ttf",
    ]
    for font_file in font_files:
        path = os.path.join(fonts_dir, font_file)
        if os.path.exists(path):
            QFontDatabase.addApplicationFont(path)

    # ── Set Plus Jakarta Sans as the default app font ─────────────
    app.setFont(QFont("Plus Jakarta Sans", 13))

    app.setStyleSheet(STYLESHEET)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())