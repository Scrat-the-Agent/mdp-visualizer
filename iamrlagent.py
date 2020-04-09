from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout


class IAmRLAgent(QWidget):
    clicked_mode = pyqtSignal()

    def _init_ui(self):
        self._reward_label = QLabel()
        self._reward_label.setText("Your last reward: 5")

        self._actions_label = QLabel()
        self._actions_label.setText("Choose your next action")

        self._actions_layout = QGridLayout()
        self._actions_layout.setColumnStretch(0, 10)
        self._actions_layout.setColumnStretch(1, 10)
        self._actions_layout.setColumnStretch(2, 10)
        self._actions_layout.setRowStretch(0, 10)
        self._actions_layout.setRowStretch(1, 10)

        self._action_1 = QPushButton()
        self._action_2 = QPushButton()
        self._action_3 = QPushButton()
        self._action_4 = QPushButton()
        self._action_5 = QPushButton()
        self._action_6 = QPushButton()

        self._actions_layout.addWidget(self._action_1, 0, 0)
        self._actions_layout.addWidget(self._action_2, 0, 1)
        self._actions_layout.addWidget(self._action_3, 0, 2)
        # self._actions_layout.addWidget(self._actions_label, 1, 1)
        self._actions_layout.addWidget(self._action_4, 1, 0)
        self._actions_layout.addWidget(self._action_5, 1, 1)
        self._actions_layout.addWidget(self._action_6, 1, 2)

        self._command_layout = QVBoxLayout()
        self._command_layout.addWidget(self._actions_label)
        self._command_layout.addLayout(self._actions_layout)
        self._command_layout.addWidget(self._reward_label)

        self.setLayout(self._command_layout)

    def __init__(self, world, parent=None):
        super().__init__(parent)
        self._world = world
        self._init_ui()
