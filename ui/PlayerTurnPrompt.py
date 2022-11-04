from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class PlayerTurnPrompt(QWidget):
    def __init__(self, parent):
        super().__init__()

        # load ui file
        self.ui = uic.loadUi("ui/PlayerTurnPrompt.ui", self)
        self.parent = parent