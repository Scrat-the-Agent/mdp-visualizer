from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout

from random import shuffle


class IAmRLAgent(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal()

    def _init_ui(self):
        # Text label
        self._actions_label = QLabel()
        self._actions_label.setText("Choose your next action")

        # Actions layout
        self._actions_layout = QGridLayout()
        self._actions_layout.setColumnStretch(0, 10)
        self._actions_layout.setColumnStretch(1, 10)
        self._actions_layout.setColumnStretch(2, 10)
        self._actions_layout.setRowStretch(0, 10)
        self._actions_layout.setRowStretch(1, 10)

        self._action_buttons = []
        for i in range(self._logic.n_actions):
            self._action_buttons.append(QPushButton())
            self._actions_layout.addWidget(self._action_buttons[i], i // 3, i % 3)

        # Reset layout
        self._reset_layout = QHBoxLayout()
        self._reset_button = QPushButton("Restart")  # reset
        self._full_reset_button = QPushButton("Full Reset")
        self._reset_layout.addWidget(self._reset_button)
        self._reset_layout.addWidget(self._full_reset_button)

        # Reward label
        self._reward_label = QLabel()
        self._reward_label.setText("Your last reward: 5")

        self._command_layout = QVBoxLayout()
        self._command_layout.addWidget(self._actions_label)
        self._command_layout.addLayout(self._actions_layout)
        self._command_layout.addLayout(self._reset_layout)
        self._command_layout.addWidget(self._reward_label)

        self.setLayout(self._command_layout)

    def __init__(self, logic, gamescreen):
        super().__init__()
        self._logic = logic
        self._actions_correspondence = list(range(self._logic.n_actions))
        shuffle(self._actions_correspondence)

        self._init_ui()

        # connecting player buttons
        for button in self._action_buttons:
            button.clicked.connect(self._action_chosen)

        self._reset_button.clicked.connect(self._reset)
        self._full_reset_button.clicked.connect(self._full_reset)

        self.made_step_signal.connect(gamescreen.update_screen)

    def _action_chosen(self):
        clicked_button = self.sender()
        action = -1
        for i, button in enumerate(self._action_buttons):
            if clicked_button is button:
                action = self._actions_correspondence[i]
                break

        self._logic.step(action)
        self.made_step_signal.emit()

    def _reset(self):
        self._logic.reset()
        self.made_step_signal.emit()

    def _full_reset(self):  # if random param, resample random values
        self._logic.full_reset()
        self.made_step_signal.emit()
