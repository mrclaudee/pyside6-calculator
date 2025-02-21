from PySide6 import QtCore
from PySide6.QtGui import QShortcut, QKeyEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QSizePolicy

BUTTONS = {"C": (1, 0, 1, 1),
           "/": (1, 3, 1, 1),
           "7": (2, 0, 1, 1),
           "8": (2, 1, 1, 1),
           "9": (2, 2, 1, 1),
           "x": (2, 3, 1, 1),
           "4": (3, 0, 1, 1),
           "5": (3, 1, 1, 1),
           "6": (3, 2, 1, 1),
           "-": (3, 3, 1, 1),
           "1": (4, 0, 1, 1),
           "2": (4, 1, 1, 1),
           "3": (4, 2, 1, 1),
           "+": (4, 3, 1, 1),
           "0": (5, 0, 1, 2),
           ".": (5, 2, 1, 1),
           "=": (5, 3, 1, 1)
           }
OPERATIONS = ['+', '-', '/', 'x']

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice")

        self.setStyleSheet("""
            background-color: rgb(20,20,20);
            color: rgb(220, 220, 220);
            font-size: 18px;
        """)

        self.buttons = {}

        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.le_result = QLineEdit("0")
        self.le_result.setMinimumHeight(50)
        self.le_result.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.le_result.setEnabled(False)
        self.le_result.setStyleSheet("""
            border: none;
            border-bottom: 2px solid rgb(30, 30, 30);
            padding: 0 8px;
            font-size: 24px;
            font-weight: bold;
        """)

        self.main_layout.addWidget(self.le_result, 0, 0, 1, 4)

        for button_text, button_position in BUTTONS.items():
            button = QPushButton(button_text)
            button.setMinimumSize(48, 48)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setStyleSheet(f"""
                QPushButton {{
                        border: none;
                        font-weight: bold;
                        background-color: {'#1e1e2d' if button_text in OPERATIONS else 'none'}
                    }}
                QPushButton:pressed {{background-color: #f31d58;}}  
                
            """)
            if button_text not in ["C", "="]:
                button.clicked.connect(self.number_or_operation_pressed)
            self.main_layout.addWidget(button, *button_position)
            self.buttons[button_text] = button

        self.buttons['C'].clicked.connect(self.clear_result)
        self.buttons['='].clicked.connect(self.compute_result)
        self.buttons['='].setStyleSheet("background-color: #f31d58;")

        self.connect_keyboard_shorcut()

    @property
    def result(self):
        return self.le_result.text()

    def compute_result(self):
        try:
            result = eval(self.result.replace('x', '*'))
        except SyntaxError:
            return

        self.le_result.setText(str(result))

    def clear_result(self):
        self.le_result.setText("0")

    def number_or_operation_pressed(self):
        if self.sender().text() in OPERATIONS:
            if self.result[-1] in OPERATIONS or self.result == "0":
                return

        if self.result == "0":
            self.le_result.clear()
        self.le_result.setText(self.result + self.sender().text())

    def remove_last_character(self):
        if len(self.result) > 1:
            self.le_result.setText(self.result[:-1])
        else:
            self.le_result.setText("0")

    def connect_keyboard_shorcut(self):
        for button_text, button in self.buttons.items():
            # La méthode emit permet de simuler un click sur le bouton
            # Du coup, on va aller chercher directement le signal relié à cet élément
            QShortcut(QKeySequence(button_text), self, button.clicked.emit)

        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Return), self, self.compute_result)
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Backspace), self, self.remove_last_character)


app = QApplication()
win = Calculator()
win.show()
app.exec()
