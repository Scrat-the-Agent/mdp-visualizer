from random import shuffle

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap

import settings
from .button import Button

class RewardLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(225, 150)
        self.setPixmap(QPixmap("./images/frame"))
        self.setScaledContents(True)
        
        self.nut = QLabel(parent=self)
        self.nut.setPixmap(QPixmap("./images/nut"))
        self.nut.setScaledContents(True)

        self.reward = QLabel(parent=self)
        self.reward.setText("0.0")
        self.reward.setAlignment(Qt.AlignCenter)
        self.reward.setFont(settings.REWARD_FONT)

        self.value = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_value)

    def resizeEvent(self, e):
        self.nut.setGeometry(self.height() / 4, self.height() / 4, self.height() / 2, self.height() / 2)
        self.reward.setGeometry(self.height() / 2, 0, self.width() - self.height() / 2, self.height())

    def set_value(self, new_value):
        self._target_value = new_value
        self._timer.start(10)  # TODO: settings!

    # TODO: this is a copypaste from scene/cell.py :(
    def _update_value(self):
        diff = abs(self._target_value - self.value)
        step = max(0.1, diff / 20)

        if diff < step:
            self.value = self._target_value
            self._timer.stop()
        elif self._target_value > self.value:
            self.value += step
        else:
            self.value -= step

        # this is new part...
        self.reward.setText(f"{self.value:.1f}")


class IAmRLAgent(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal()

    def _init_ui(self):
        # Reset layout
        self._reset_layout = QHBoxLayout()
        self._reset_button = Button("./images/reset")
        self._full_reset_button = Button("./images/newgame")
        self._reset_layout.addWidget(self._reset_button)
        self._reset_layout.addWidget(self._full_reset_button)

        # Text label
        self._actions_label = QLabel()
        self._actions_label.setFont(settings.DESCRIPTION_FONT)
        self._actions_label.setAlignment(Qt.AlignCenter)
        self._actions_label.setText("Select your next action.\n\nPress T to rotate field view.")

        # Actions layout
        self._actions_layout = QGridLayout()
        self._action_buttons = []
        for i in range(self._logic.n_actions):
            self._action_buttons.append(Button("./images/symbol" + str(i)))
            self._actions_layout.addWidget(self._action_buttons[i], i // 3, i % 3)

        # Reward label
        self._reward_label = RewardLabel()
        
        # Unite everything in vertical layout!
        self._command_layout = QVBoxLayout()
        self._command_layout.addLayout(self._reset_layout)
        self._command_layout.addWidget(self._actions_label)
        self._command_layout.setStretchFactor(self._actions_label, 0)
        self._command_layout.addLayout(self._actions_layout)
        self._command_layout.addWidget(self._reward_label)
        self._command_layout.setAlignment(self._reward_label, Qt.AlignHCenter)
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

        _, reward, done, _ = self._logic.step(action)
        self._reward_label.set_value(reward)

        # TODO: Restart needed
        if done:
            print(f"Game finished! Full reward: {self._logic.full_reward}. Restart needed!")

        self.made_step_signal.emit()

    def _reset(self):
        self._logic.reset()
        self.made_step_signal.emit()

    def _full_reset(self):  # if random param, resample random values
        self._logic.full_reset()
        self.made_step_signal.emit()
