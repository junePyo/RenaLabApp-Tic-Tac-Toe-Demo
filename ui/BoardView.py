from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5 import uic
from pylsl import StreamInfo, IRREGULAR_RATE, StreamOutlet

PLAYER_MARK = 'O'
COMPUTER_MARK = 'X'

class BoardView(QWidget):
    def __init__(self, parent):
        super().__init__()
        # load ui file
        self.ui = uic.loadUi("ui/BoardView.ui", self)
        self.parent = parent

        # init LSL fields
        info = StreamInfo('TicTacToeEvents', 'Events', 1, IRREGULAR_RATE, 'float32', 'someuuid1234')
        self.outlet = StreamOutlet(info)

        # UI elements
        self.transition_timer = QTimer()
        self.transition_timer.setInterval(2000)
        self.transition_timer.setSingleShot(True)
        # transition initiated by the push button always goes from computer board view -> player board view
        self.transition_timer.timeout.connect(self.to_player_board_view)

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
            # order matters! button1 should be matched with the first frequency, and so on.
            frequency: button for frequency, button in zip(self.blink_frequencies.values(), self.buttons)
        }
        self.button_to_flash_timers = {
            # order matters! button1 should be matched with button1_flash_timer, and so on.
            button: timer for button, timer in zip(self.buttons, self.flash_timers)
        }

        self.unclicked_buttons = self.buttons.copy()
        self.unclicked_buttons_timers = self.flash_timers.copy()
        self.player_clicked_buttons = []
        self.computer_clicked_buttons = []

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
        if a.text() == COMPUTER_MARK:
            self.parent.finish_game('computer')
        else:
            self.parent.finish_game('player')

    def process_clicked(self, observed_frequency):
        """ To be called from MainWindow when response is received from RenaLabApp """
        most_likely_frequency = self.identify_closest_button_to_classification_result(observed_frequency)
        clicked_button = self.blink_frequencies_to_buttons[most_likely_frequency]
        clicked_button.setEnabled(False)
        # clicked = (row, column)
        # clicked_button = self.button_positions(clicked)
        # clicked_button.setText("X")
        self.player_clicked_buttons.append(clicked_button)
        self.unclicked_buttons.remove(clicked_button)
        self.unclicked_buttons_timers.remove(self.button_to_flash_timers[clicked_button])
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
        self.is_player_turn = False
        self.PlacePieceBtn.setEnabled(True)

        # display marks for the clicked grids
        for button in self.player_clicked_buttons:
            button.setText(PLAYER_MARK)
        for button in self.computer_clicked_buttons:
            button.setText(COMPUTER_MARK)

        # flashing should be disabled

        # computer makes a move
        chosen_button = self.unclicked_buttons[0]
        chosen_button.setText(COMPUTER_MARK)
        chosen_button.setEnabled(False)
        # clicked = (row, column)
        # clicked_button = self.button_positions(clicked)
        # clicked_button.setText("X")
        self.computer_clicked_buttons.append(chosen_button)
        self.unclicked_buttons.remove(chosen_button)
        self.unclicked_buttons_timers.remove(self.button_to_flash_timers[chosen_button])
        # clicked_button.setEnabled = False
        self.check_win()

        self.PlacePieceBtn.setText(
            'Press when you are ready to make your next move.\nThe board will start flashing in 2 seconds!')

    def to_player_board_view(self):
        self.is_player_turn = True
        # hide marks for the clicked grids
        # clicked grids should be grayed out
        # for button in self.player_clicked_buttons:
        #     button.setText('')
        # for button in self.computer_clicked_buttons:
        #     button.setText('')

        # turn on flashing
        # flashing should be enabled, but only for the buttons that have not yet been clicked
        self.start_flashing()
        self.send_lsl(flash=True)

        # hand back the flow control back to the main window
        # timeout connect main window callback function
        QTimer.singleShot(4000, self.complete_player_board_view)

    def complete_player_board_view(self):
        self.stop_flashing()
        # send LSL termination signal to RenaLabApp
        self.send_lsl(flash=False)
        # clean up flashing stylesheets
        [button.setStyleSheet('background-color: none;') for button in self.buttons]

        # receive response back from RenaLabApp
        response = self.receive_lsl()
        if response:
            self.process_clicked(response)

        # self.computer_turn_prompt.show()
        self.PlacePieceBtn.setText('Computer is making its next move...\n You will see the updated board soon.')
        QTimer.singleShot(2000, self.to_computer_board_view)

    def place_piece_btn_pressed(self):
        self.transition_timer.start()
        self.PlacePieceBtn.setEnabled(False)

    def start_flashing(self):
        [timer.start() for timer in self.unclicked_buttons_timers]
        print('Flash started')

    def stop_flashing(self):
        [timer.stop() for timer in self.unclicked_buttons_timers]
        print('Flash stopped')

    def toggle_flashing(self):
        if self.is_flashing:
            [timer.stop() for timer in self.unclicked_buttons_timers]
            print('Flash stopped')
        else:
            [timer.start() for timer in self.unclicked_buttons_timers]
            print('Flash started')

        self.is_flashing = not self.is_flashing

    def send_lsl(self, flash=True):
        # sending the event markers
        # send number 1 when the flash starts
        # send number 2 when the flash ends
        if flash:
            self.outlet.push_sample([1])
        else:
            self.outlet.push_sample([2])

    def receive_lsl(self):
        # receive classification result
        # listen for certain amount of time after sending number 2 event marker
        # inlet.poll_sample
        # after receivng anything, make sure to clear the buffer -- poll_sample function will automatically clear the buffeer
        # poll, if there is no data, wait 3 more seconds (use the timeout parameter in the poll_sample function)
        # handle exception if something is wrong with the classifier
        pass
