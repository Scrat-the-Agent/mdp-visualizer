from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QComboBox, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import settings
from .automaticrl import AutomaticRL
from .iamrlagent import IAmRLAgent

from scene.gamescreen import GameScreen
from WTF import World




class MainWindow(QMainWindow):
    def _init_ui(self):
        # mode switcher
        self._combo_box = QComboBox()
        self._combo_box.addItems(["I Am RL Agent", "Automatic RL, Please"])

        # game screen
        self._game_screen = GameScreen(self._world)

        # widget for each mode
        self._iAmRLAgent = IAmRLAgent(self._world)
        self._automaticRL = AutomaticRL(self._world, self._game_screen)

        # mode widget
        self._mode_widget = QStackedWidget()
        self._mode_widget.addWidget(self._iAmRLAgent)
        self._mode_widget.addWidget(self._automaticRL)

        # left widget
        self._left_layout = QVBoxLayout()
        self._left_layout.addWidget(self._combo_box)
        self._left_layout.addWidget(self._mode_widget)
        self._left_widget = QWidget()
        self._left_widget.setLayout(self._left_layout)

        # central widget
        self._central_layout = QHBoxLayout()
        self._central_layout.addWidget(self._left_widget)
        self._central_layout.addWidget(self._game_screen)

        self._central_widget = QWidget()
        self._central_widget.setLayout(self._central_layout)
        self.setCentralWidget(self._central_widget)

    def __init__(self):
        super().__init__()
        self._world = World(settings.ROWS, settings.COLS)
        self._init_ui()
        self._combo_box.currentIndexChanged.connect(self._mode_change)

    def _mode_change(self, mode):
        if mode == 0:
            self._automaticRL.setEnabled(False)
            self._iAmRLAgent.setEnabled(True)
            self._mode_widget.setCurrentWidget(self._iAmRLAgent)
        else:
            self._automaticRL.setEnabled(True)
            self._iAmRLAgent.setEnabled(False)
            self._mode_widget.setCurrentWidget(self._automaticRL)
