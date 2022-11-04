from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5 import uic

from ui.BoardView import BoardView
from ui.PlayerTurnPrompt import  PlayerTurnPrompt
from ui.ComputerTurnPrompt import ComputerTurnPrompt

import sys

class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.setWindowTitle('Rena Tic Tac Toe')
        self.app = app
        self.ui = uic.loadUi("MainWindow.ui", self)

        # display timer
        self.display_timer = QTimer()

        # load presentation screens
        self.player_boardview = BoardView(self)
        self.player_turn_prompt = PlayerTurnPrompt(self)
        self.computer_turn_prompt = ComputerTurnPrompt(self)

        # connect start button to an appropriate callback function
        self.startButton.clicked.connect(self.start_button_pressed)

    def start_button_pressed(self):
        # timer that runs for certain amount of time
        self.player_boardview.show()

    def switch_views(self):
        pass

    def send_lsl(self):
        # sending the event markers
        # send number 1 when the flash starts
        # send number 2 when the flash ends
        pass

    def receive_lsl(self):
        # receive classification result
        # listen for certain amount of time after sending number 2 event marker
        # inlet.poll_sample
        # after receivng anything, make sure to clear the buffer -- poll_sample function will automatically clear the buffeer
        # poll, if there is no data, wait 3 more seconds (use the timeout parameter in the poll_sample function)
        # handle exception if something is wrong with the classifier
        pass
