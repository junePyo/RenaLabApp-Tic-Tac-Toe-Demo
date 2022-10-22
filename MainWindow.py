from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5 import uic
import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        # display timer
        self.display_timer = QTimer()

        # load presentation screens
        self.player_boardview = PlayerBoardView(self)
        self.computer_boardview = ComputerBoardView(self)
        self.player_turn_prompt = PlayerTurnPrompt(self)
        self.computer_turn_prompt = ComputerTurnPrompt(self)

    def switch_views(self):
        pass

    def send_lsl(self):
        pass

    def receive_lsl(self):
        pass
