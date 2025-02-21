from PySide6 import QtCore
from PySide6.QtGui import QShortcut, QKeyEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton

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


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice")

        self.buttons = {}

        self.main_layout = QGridLayout(self)
        self.le_result = QLineEdit("0")
        self.le_result.setEnabled(False)
        self.main_layout.addWidget(self.le_result, 0, 0, 1, 4)

        for button_text, button_position in BUTTONS.items():
            button = QPushButton(button_text)
            if button_text not in ["C", "="]:
                button.clicked.connect(self.number_or_operation_pressed)
            self.main_layout.addWidget(button, *button_position)
            self.buttons[button_text] = button

        self.buttons['C'].clicked.connect(self.clear_result)
        self.buttons['='].clicked.connect(self.compute_result)

        self.connect_keyboard_shorcut()

    def compute_result(self):
        try:
            result = eval(self.le_result.text().replace('x', '*'))
        except SyntaxError:
            return

        self.le_result.setText(str(result))

    def clear_result(self):
        self.le_result.setText("0")

    def number_or_operation_pressed(self):
        if self.le_result.text() == "0":
            self.le_result.clear()
        self.le_result.setText(self.le_result.text() + self.sender().text())

    def connect_keyboard_shorcut(self):
        for button_text, button in self.buttons.items():
            # La méthode emit permet de simuler un click sur le bouton
            # Du coup, on va aller chercher directement le signal relié à cet élément
            QShortcut(QKeySequence(button_text), self, button.clicked.emit)

        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Return), self, self.compute_result)


app = QApplication()
win = Calculator()
win.show()
app.exec()
