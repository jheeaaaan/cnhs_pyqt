
STYLESHEET = """

/* GLOBAL */
QWidget {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #052e16;
    background-color: #f0fdf4;
}
QMainWindow { background-color: #f0fdf4; }

/* SIDEBAR */
QWidget#sidebar { background-color: #0f4c2a; }

QLabel#sidebar_school {
    color: #ffffff; font-size: 12px; font-weight: bold;
    padding: 0px; background: transparent;
}
QLabel#sidebar_sub {
    color: #fbbf24; font-size: 11px;
    padding: 0px; background: transparent;
}
QLabel#sidebar_section {
    color: rgba(255,255,255,0.35); font-size: 9px;
    font-weight: bold; letter-spacing: 1.2px;
    padding: 10px 16px 4px 16px; background: transparent;
}

QWidget#sidebar QPushButton {
    text-align: left; padding: 8px 18px;
    color: rgba(255,255,255,0.88); background: transparent;
    border: none; border-radius: 8px;
    font-size: 14px; margin: 1px 8px;
}
QWidget#sidebar QPushButton:hover {
    background: rgba(255,255,255,0.09); color: #ffffff;
}

QPushButton#nav_shs {
    text-align: left; padding: 8px 18px;
    color: rgba(255,255,255,0.88); background: transparent;
    border: none; border-radius: 8px;
    font-size: 14px; margin: 1px 8px;
}
QPushButton#nav_shs:hover {
    background: rgba(255,255,255,0.09); color: #ffffff;
}
QPushButton#nav_shs:checked {
    background: #16a34a; color: #ffffff; font-weight: bold;
    border-left: 4px solid #fbbf24; padding-left: 14px;
}
QPushButton#nav_shs:checked:hover { background: #15803d; }

QPushButton#nav_jhs {
    text-align: left; padding: 8px 18px;
    color: rgba(255,255,255,0.88); background: transparent;
    border: none; border-radius: 8px;
    font-size: 14px; margin: 1px 8px;
}
QPushButton#nav_jhs:hover {
    background: rgba(255,255,255,0.09); color: #ffffff;
}
QPushButton#nav_jhs:checked {
    background: #0369a1; color: #ffffff; font-weight: bold;
    border-left: 4px solid #7dd3fc; padding-left: 14px;
}
QPushButton#nav_jhs:checked:hover { background: #1d4ed8; }

QPushButton#nav_bmi {
    text-align: left; padding: 8px 18px;
    color: rgba(255,255,255,0.88); background: transparent;
    border: none; border-radius: 8px;
    font-size: 14px; margin: 1px 8px;
}
QPushButton#nav_bmi:hover {
    background: rgba(255,255,255,0.09); color: #ffffff;
}
QPushButton#nav_bmi:checked {
    background: #0f766e; color: #ffffff; font-weight: bold;
    border-left: 4px solid #5eead4; padding-left: 14px;
}
QPushButton#nav_bmi:checked:hover { background: #0d9488; }

QPushButton#btn_logout {
    color: #fca5a5; background: transparent; border: none;
    text-align: left; padding: 10px 20px; font-size: 12px;
}
QPushButton#btn_logout:hover {
    background: #dc2626; color: #ffffff; border-radius: 8px;
}

/* TOP BAR */
QWidget#topbar {
    background: #ffffff; border-bottom: 1px solid #d1fae5;
}
QLabel#topbar_title {
    font-size: 15px; font-weight: bold;
    color: #052e16; background: transparent;
}
QLabel#topbar_tag {
    font-size: 10px; font-weight: bold; padding: 3px 10px;
    border-radius: 20px; background: rgba(22,163,74,0.10); color: #16a34a;
}
QLabel#topbar_tag_bmi { background: rgba(15,118,110,0.10); color: #0f766e; }
QLabel#topbar_tag_jhs { background: rgba(3,105,161,0.10); color: #0369a1; }

/* CARDS */
QFrame#card, QFrame#stat_card, QFrame#form_card {
    background: #ffffff; border: 1px solid #d1fae5; border-radius: 16px;
}
QFrame#card_head {
    background: #14532d;
    border-top-left-radius: 14px; border-top-right-radius: 14px;
}
QLabel#card_head_title {
    color: #ffffff; font-size: 13px; font-weight: bold;
    padding: 13px 24px; background: transparent;
}

/* BUTTONS */
QPushButton {
    background: #16a34a; color: #ffffff; border: none;
    border-radius: 8px; padding: 9px 22px;
    font-size: 13px; font-weight: bold;
}
QPushButton:hover   { background: #15803d; }
QPushButton:pressed { background: #166534; }
QPushButton:disabled { background: #d1fae5; color: #a7c5b0; }

QPushButton#btn_secondary {
    background: #f0fdf4; color: #052e16;
    border: 1.5px solid #d1fae5; font-weight: bold;
}
QPushButton#btn_secondary:hover { background: #dcfce7; }

QPushButton#btn_danger {
    background: #fef2f2; color: #dc2626;
    border: 1px solid #fecaca; font-weight: bold;
}
QPushButton#btn_danger:hover { background: #dc2626; color: white; }

QPushButton#btn_teal  { background: #0f766e; }
QPushButton#btn_teal:hover  { background: #0d6461; }
QPushButton#btn_blue  { background: #0369a1; }
QPushButton#btn_blue:hover  { background: #025f8a; }
QPushButton#btn_small { padding: 5px 14px; font-size: 12px; border-radius: 6px; }

/* INPUTS */
QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit {
    background: #f0fdf4; border: 1.5px solid #d1fae5;
    border-radius: 8px; padding: 7px 12px;
    font-size: 13px; color: #052e16;
    selection-background-color: #dcfce7;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
    border-color: #16a34a; background: #ffffff;
}
QLineEdit::placeholder { color: #a7c5b0; }
QComboBox::drop-down { border: none; padding-right: 6px; }
QComboBox QAbstractItemView {
    background: #ffffff; border: 1px solid #d1fae5;
    selection-background-color: #dcfce7;
    selection-color: #052e16; border-radius: 8px;
}

/* TABLE */
QTableWidget {
    background: #ffffff; border: 1px solid #d1fae5;
    border-radius: 8px; gridline-color: #f0fdf4;
    alternate-background-color: #f9fefb;
    font-size: 13px; color: #052e16;
}
QTableWidget::item {
    padding: 11px 14px; border-bottom: 1px solid #f0fdf4;
}
QTableWidget::item:selected { background: #dcfce7; color: #052e16; }
QTableWidget::item:hover    { background: #f0fdf4; }
QHeaderView::section {
    background: #f0fdf4; color: #4b7a5a;
    padding: 10px 14px; border: none;
    border-bottom: 1px solid #d1fae5;
    font-size: 10.5px; font-weight: bold;
    text-transform: uppercase; letter-spacing: 0.8px;
}
QHeaderView::section:first { border-top-left-radius: 8px; }
QHeaderView::section:last  { border-top-right-radius: 8px; }

/* GROUP BOX */
QGroupBox {
    background: #ffffff; border: 1px solid #d1fae5;
    border-radius: 12px; margin-top: 14px; padding-top: 10px;
    font-weight: bold; font-size: 13px; color: #052e16;
}
QGroupBox::title {
    subcontrol-origin: margin; left: 12px; padding: 0 6px;
    background: #ffffff; color: #4b7a5a;
    font-size: 10.5px; font-weight: bold;
    text-transform: uppercase; letter-spacing: 0.8px;
}

/* LABELS */
QLabel { background: transparent; color: #052e16; }
QLabel#page_title  { font-size: 22px; font-weight: bold; color: #052e16; }
QLabel#page_sub    { font-size: 13px; color: #4b7a5a; }
QLabel#field_label {
    font-size: 10.5px; font-weight: bold; color: #4b7a5a;
    text-transform: uppercase; letter-spacing: 0.8px;
}
QLabel#stat_number { font-size: 32px; font-weight: bold; color: #16a34a; }
QLabel#stat_label  {
    font-size: 10px; font-weight: bold; color: #4b7a5a;
    text-transform: uppercase; letter-spacing: 0.8px;
}
QLabel#badge_enrolled {
    background: rgba(22,163,74,0.10); color: #16a34a;
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: bold;
}
QLabel#badge_pending {
    background: rgba(217,119,6,0.12); color: #b45309;
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: bold;
}
QLabel#badge_dropped {
    background: rgba(220,38,38,0.10); color: #dc2626;
    border-radius: 10px; padding: 3px 10px;
    font-size: 11px; font-weight: bold;
}

/* TABS */
QTabWidget::pane {
    border: 1px solid #d1fae5;
    border-radius: 0 10px 10px 10px; background: #ffffff;
}
QTabBar::tab {
    background: #f0fdf4; color: #4b7a5a;
    padding: 9px 22px; border: 1px solid #d1fae5;
    border-bottom: none; border-radius: 8px 8px 0 0;
    margin-right: 3px; font-size: 13px; font-weight: bold;
}
QTabBar::tab:selected { background: #ffffff; color: #16a34a; border-color: #d1fae5; }
QTabBar::tab:hover    { background: #dcfce7; color: #052e16; }

/* SCROLLBARS */
QScrollBar:vertical {
    width: 7px; background: #f0fdf4; border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #a7c5b0; border-radius: 4px; min-height: 28px;
}
QScrollBar::handle:vertical:hover { background: #4b7a5a; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    height: 7px; background: #f0fdf4; border-radius: 4px;
}
QScrollBar::handle:horizontal { background: #a7c5b0; border-radius: 4px; }
QScrollBar::handle:horizontal:hover { background: #4b7a5a; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* CHECKBOX */
QCheckBox { spacing: 7px; color: #052e16; font-size: 13px; }
QCheckBox::indicator {
    width: 15px; height: 15px;
    border: 1.5px solid #d1fae5; border-radius: 4px; background: #f0fdf4;
}
QCheckBox::indicator:checked  { background: #16a34a; border-color: #16a34a; image: none; }
QCheckBox::indicator:hover    { border-color: #16a34a; }

/* SCROLL AREA */
QScrollArea { border: none; background: transparent; }
QScrollArea > QWidget > QWidget { background: transparent; }

/* DIALOG & MESSAGE BOX */
QDialog    { background: #f0fdf4; }
QMessageBox { background: #ffffff; }
QMessageBox QLabel {
    color: #052e16;
    background: transparent;
}
QMessageBox QPushButton,
QMessageBox QDialogButtonBox QPushButton {
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
QMessageBox QPushButton:hover,
QMessageBox QDialogButtonBox QPushButton:hover {
    background-color: #0c4a6e;
    border-color: #0c4a6e;
    color: #ffffff;
}
QMessageBox QPushButton:pressed,
QMessageBox QDialogButtonBox QPushButton:pressed {
    background-color: #075985;
    border-color: #075985;
    color: #ffffff;
}
QMessageBox QPushButton:focus,
QMessageBox QDialogButtonBox QPushButton:focus {
    background-color: #0369a1;
    color: #ffffff;
    border: 2px solid #38bdf8;
}
QMessageBox QPushButton:default,
QMessageBox QDialogButtonBox QPushButton:default {
    background-color: #0369a1;
    color: #ffffff;
    border: 2px solid #38bdf8;
}

/* LOGIN */
QWidget#login_bg {
    background: qradialgradient(
        cx:0.6, cy:0.4, radius:1.0, fx:0.6, fy:0.4,
        stop:0 #166534, stop:0.4 #14532d, stop:1.0 #052e16
    );
}
QFrame#login_card { background: #ffffff; border: none; border-radius: 20px; }
QLabel#login_school_name {
    font-size: 22px; font-weight: bold; color: #ffffff;
    background: transparent; qproperty-alignment: AlignCenter;
}
QLabel#login_school_sub {
    font-size: 13px; color: rgba(255,255,255,0.65);
    background: transparent; qproperty-alignment: AlignCenter;
}
QLabel#login_badge {
    font-size: 12px; font-weight: bold; color: rgba(255,255,255,0.85);
    background: rgba(255,255,255,0.10); border: 1px solid rgba(255,255,255,0.18);
    border-radius: 20px; padding: 5px 16px;
}
QLabel#login_card_title { font-size: 20px; font-weight: bold; color: #052e16; background: transparent; }
QLabel#login_card_sub   { font-size: 13px; color: #4b7a5a; background: transparent; }
QFrame#login_card QLineEdit {
    background: #f0fdf4; border: 1.5px solid #d1fae5;
    border-radius: 10px; padding: 11px 14px;
    font-size: 14px; color: #052e16;
}
QFrame#login_card QLineEdit:focus { border-color: #16a34a; background: #ffffff; }
QFrame#login_card QPushButton {
    background: #16a34a; color: #ffffff; border-radius: 10px;
    font-size: 15px; font-weight: bold; padding: 13px;
}
QFrame#login_card QPushButton:hover { background: #15803d; }
QLabel#login_hint {
    background: #f0fdf4; border: 1.5px solid #d1fae5;
    border-radius: 10px; padding: 10px 14px;
    font-size: 13px; color: #4b7a5a;
}
QLabel#login_error {
    background: #fef2f2; border: 1.5px solid #fecaca;
    border-radius: 10px; padding: 10px 14px;
    font-size: 13px; color: #dc2626;
}
QLabel#login_footer {
    font-size: 11.5px; color: rgba(255,255,255,0.35);
    background: transparent; qproperty-alignment: AlignCenter;
}

/* RADIO BUTTON */
QRadioButton { spacing: 8px; color: #052e16; font-size: 13px; }
QRadioButton::indicator {
    width: 16px; height: 16px;
    border: 2px solid #a7c5b0; border-radius: 8px; background: #f0fdf4;
}
QRadioButton::indicator:hover   { border-color: #16a34a; }
QRadioButton::indicator:checked {
    border: 2px solid #16a34a;
    background: qradialgradient(
        cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
        stop:0 #16a34a, stop:0.45 #16a34a,
        stop:0.46 #ffffff, stop:1 #ffffff
    );
}
"""
