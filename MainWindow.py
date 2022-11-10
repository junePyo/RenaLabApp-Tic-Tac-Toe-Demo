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

    def finish_game(self, winner):
        if winner == 'computer':
            self.computer_turn_prompt.textEdit.setPlainText("Game Over! Computer Wins!")
        else:
            self.computer_turn_prompt.textEdit.setPlainText("Game Over! Player Wins!!")

        self.computer_turn_prompt.show()
        # self.player_boardview.hide()