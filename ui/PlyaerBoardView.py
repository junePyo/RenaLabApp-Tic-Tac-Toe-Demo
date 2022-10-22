from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5 import uic


class PlayerBoardView(QWidget):
    def __init__(self, parent):
        super().__init__()

        # load ui file
        self.ui = uic.loadUi("ui/PlayerBoardView.ui", self)

        self.parent = parent

        # button to row/column mapping
        self.button_positions = {
            self.button1.objectName: (0, 0),
            self.button2.objectName: (1, 0),
            self.button3.objectName: (2, 0),
            self.button4.objectName: (0, 1),
            self.button5.objectName: (1, 1),
            self.button6.objectName: (2, 1),
            self.button7.objectName: (0, 2),
            self.button8.objectName: (1, 2),
            self.button9.objectName: (2, 2),
        }

        # flag to enable flashing
        # TODO: define the frequency intervals for different timers
        self.flash = True
        self.button1_flash_timer = QTimer(self, interval=31)
        self.button2_flash_timer = QTimer(self, interval=31)
        self.button3_flash_timer = QTimer(self, interval=31)
        self.button4_flash_timer = QTimer(self, interval=31)
        self.button5_flash_timer = QTimer(self, interval=31)
        self.button6_flash_timer = QTimer(self, interval=31)
        self.button7_flash_timer = QTimer(self, interval=31)
        self.button8_flash_timer = QTimer(self, interval=31)
        self.button9_flash_timer = QTimer(self, interval=31)

        # utility collections
        self.flash_timers = [
            self.button1_flash_timer,
            self.button2_flash_timer,
            self.button3_flash_timer,
            self.button4_flash_timer,
            self.button5_flash_timer,
            self.button6_flash_timer,
            self.button7_flash_timer,
            self.button8_flash_timer,
            self.button9_flash_timer,
        ]
        self.buttons = [
            self.button1, self.button2, self.button3, self.button4, self.button5,
            self.button6, self.button7, self.button8, self.button9
        ]

    def check_win(self):
        # Across
        if self.button1.text() != "" and self.button1.text() == self.button4.text() and self.button1.text() == self.button7.text():
            self.win(self.button1, self.button4, self.button7)

        if self.button2.text() != "" and self.button2.text() == self.button5.text() and self.button2.text() == self.button8.text():
            self.win(self.button2, self.button5, self.button8)

        if self.button3.text() != "" and self.button3.text() == self.button6.text() and self.button3.text() == self.button9.text():
            self.win(self.button3, self.button6, self.button9)

        # Down
        if self.button1.text() != "" and self.button1.text() == self.button2.text() and self.button1.text() == self.button3.text():
            self.win(self.button1, self.button2, self.button3)

        if self.button4.text() != "" and self.button4.text() == self.button5.text() and self.button4.text() == self.button6.text():
            self.win(self.button4, self.button5, self.button6)

        if self.button7.text() != "" and self.button7.text() == self.button8.text() and self.button7.text() == self.button9.text():
            self.win(self.button7, self.button8, self.button9)

        # Diagonal
        if self.button1.text() != "" and self.button1.text() == self.button5.text() and self.button1.text() == self.button9.text():
            self.win(self.button1, self.button5, self.button9)

        if self.button3.text() != "" and self.button3.text() == self.button5.text() and self.button3.text() == self.button7.text():
            self.win(self.button3, self.button5, self.button7)

    def win(self, a, b, c):
        self.label.setText("Game Over!")

    def clicked(self, row, column):
        """ To be called from MainWindow when response is received from RenaLabApp """
        clicked = (row, column)
        clicked_button = self.button_positions(clicked)
        clicked_button.setText("X")
        clicked_button.setEnabled = False
        self.check_win()

    def initialize_flash_timers(self):
        for timer in self.flash_timers:
            timer.timeout.connect(self.flashing)
        for timer in self.flash_timers:
            timer.start()

    def flashing(self):
        if self.flash:
            self.setStyleSheet('background-color: none;')
        else:
            self.setStyleSheet('background-color: medium orchid;')

        self.flash = not self.flash
