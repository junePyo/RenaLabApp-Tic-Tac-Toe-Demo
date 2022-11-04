from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5 import uic

class BoardView(QWidget):
    def __init__(self, parent):
        super().__init__()
        # load ui file
        self.ui = uic.loadUi("ui/BoardView.ui", self)

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
        self.buttons = [
            self.button1, self.button2, self.button3, self.button4, self.button5,
            self.button6, self.button7, self.button8, self.button9
        ]

        # blink frequencies
        self.blink_frequencies = {
            "frequency1": 4,
            "frequency2": 6.6,
            "frequency3": 7.5,
            "frequency4": 8.57,
            "frequency5": 10,
            "frequency6": 12,
            "frequency7": 15,
            "frequency8": 20,
            "frequency9": 25
        }

        # flag to denote whose turn it is
        self.is_player_turn = True

        # flag to enable flashing
        self.is_flashing = False
        self.is_flashed_on = [True] * 9

        self.button1_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency1"])
        self.button2_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency2"])
        self.button3_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency3"])
        self.button4_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency4"])
        self.button5_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency5"])
        self.button6_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency6"])
        self.button7_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency7"])
        self.button8_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency8"])
        self.button9_flash_timer = QTimer(self, interval=self.blink_frequencies["frequency9"])

        self.button1_flash_timer.timeout.connect(lambda: self.flashing(0))
        self.button2_flash_timer.timeout.connect(lambda: self.flashing(1))
        self.button3_flash_timer.timeout.connect(lambda: self.flashing(2))
        self.button4_flash_timer.timeout.connect(lambda: self.flashing(3))
        self.button5_flash_timer.timeout.connect(lambda: self.flashing(4))
        self.button6_flash_timer.timeout.connect(lambda: self.flashing(5))
        self.button7_flash_timer.timeout.connect(lambda: self.flashing(6))
        self.button8_flash_timer.timeout.connect(lambda: self.flashing(7))
        self.button9_flash_timer.timeout.connect(lambda: self.flashing(8))
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


        self.blink_frequencies_to_buttons = {
            frequency: button for frequency, button in zip(self.blink_frequencies.values(), self.buttons)
        }
        self.clicked_buttons = []

        self.PlacePieceBtn.clicked.connect(self.place_piece_btn_pressed)

    def check_win(self):
        # Across
        if (self.button1.text() != ""
                and self.button1.text() == self.button4.text()
                and self.button1.text() == self.button7.text()):
            self.win(self.button1, self.button4, self.button7)

        if (self.button2.text() != ""
                and self.button2.text() == self.button5.text()
                and self.button2.text() == self.button8.text()):
            self.win(self.button2, self.button5, self.button8)

        if (self.button3.text() != ""
                and self.button3.text() == self.button6.text()
                and self.button3.text() == self.button9.text()):
            self.win(self.button3, self.button6, self.button9)

        # Down
        if (self.button1.text() != ""
                and self.button1.text() == self.button2.text()
                and self.button1.text() == self.button3.text()):
            self.win(self.button1, self.button2, self.button3)

        if (self.button4.text() != ""
                and self.button4.text() == self.button5.text()
                and self.button4.text() == self.button6.text()):
            self.win(self.button4, self.button5, self.button6)

        if (self.button7.text() != ""
                and self.button7.text() == self.button8.text()
                and self.button7.text() == self.button9.text()):
            self.win(self.button7, self.button8, self.button9)

        # Diagonal
        if (self.button1.text() != ""
                and self.button1.text() == self.button5.text()
                and self.button1.text() == self.button9.text()):
            self.win(self.button1, self.button5, self.button9)

        if (self.button3.text() != ""
                and self.button3.text() == self.button5.text()
                and self.button3.text() == self.button7.text()):
            self.win(self.button3, self.button5, self.button7)

    def win(self, a, b, c):
        self.label.setText("Game Over!")

    def clicked(self, observed_frequency):
        """ To be called from MainWindow when response is received from RenaLabApp """
        most_likely_frequency = self.identify_closest_button_to_classification_result(observed_frequency)
        clicked_button = self.blink_frequencies_to_buttons[most_likely_frequency]
        # clicked = (row, column)
        # clicked_button = self.button_positions(clicked)
        # clicked_button.setText("X")
        self.clicked_buttons.append(clicked_button)
        # clicked_button.setEnabled = False
        self.check_win()

    def identify_closest_button_to_classification_result(self, observed_frequency):
        most_likely_frequency = min(self.blink_frequencies.values(), key=lambda x: abs(x - observed_frequency))
        return most_likely_frequency

    def initialize_flash_timers(self):
        # only make the buttons that have not been clicked to flash
        for timer in self.flash_timers:
            timer.timeout.connect(self.flashing)
        for timer in self.flash_timers:
            timer.start()

    @pyqtSlot(int)
    def flashing(self, i):
        if self.is_flashed_on[i]:
            self.buttons[i].setStyleSheet('background-color: none;')
        else:
            self.buttons[i].setStyleSheet('background-color: orange;')

        self.is_flashed_on[i] = not self.is_flashed_on[i]

    def to_computer_board_view(self):
        # is_player_turn = False
        # flashing should be disabled
        # for all buttons that have been clicked, set text to either O or X
        pass
    def to_player_board_view(self):
        # is_player_turn = True
        # flashing should be enabled, but only for the buttons that have not yet been clicked
        # clicked grids should be grayed out
        # for the buttons that are flashing, no text should be set
        pass

    def place_piece_btn_pressed(self):
        if self.is_flashing:
            [timer.stop() for timer in self.flash_timers]
            print('Flash stopped')
        else:
            [timer.start() for timer in self.flash_timers]
            print('Flash started')

        self.is_flashing = not self.is_flashing
