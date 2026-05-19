from PyQt5.QtWidgets import QMessageBox


BUTTON_STYLE = """
QMessageBox { background: #ffffff; }
QMessageBox QLabel { color: #052e16; background: transparent; font-size: 13px; }
QPushButton {
    min-width: 96px;
    min-height: 36px;
    padding: 7px 18px;
    border: 1.5px solid #0369a1;
    border-radius: 8px;
    background-color: #0369a1;
    color: #ffffff;
    font-size: 13px;
    font-weight: 800;
}
QPushButton:hover {
    background-color: #0c4a6e;
    border-color: #0c4a6e;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #075985;
    border-color: #075985;
    color: #ffffff;
}
"""


def style_message_box(box):
    box.setStyleSheet(BUTTON_STYLE)
    for button in box.buttons():
        button.setStyleSheet(BUTTON_STYLE)
    return box


def _show(icon, parent, title, text, buttons=QMessageBox.Ok, default_button=QMessageBox.NoButton):
    box = QMessageBox(parent)
    box.setIcon(icon)
    box.setWindowTitle(title)
    box.setText(text)
    box.setStandardButtons(buttons)
    if default_button != QMessageBox.NoButton:
        box.setDefaultButton(default_button)
    style_message_box(box)
    return box.exec_()


def information(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton):
    return _show(QMessageBox.Information, parent, title, text, buttons, defaultButton)


def warning(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton):
    return _show(QMessageBox.Warning, parent, title, text, buttons, defaultButton)


def critical(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton):
    return _show(QMessageBox.Critical, parent, title, text, buttons, defaultButton)


def question(parent, title, text, buttons=QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.NoButton):
    return _show(QMessageBox.Question, parent, title, text, buttons, defaultButton)


def install_message_box_styles():
    QMessageBox.information = staticmethod(information)
    QMessageBox.warning = staticmethod(warning)
    QMessageBox.critical = staticmethod(critical)
    QMessageBox.question = staticmethod(question)
