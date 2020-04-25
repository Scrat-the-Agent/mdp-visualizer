from random import shuffle

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont

import settings
from utils import value_update
from logic.gameLogic import GameLogic, GameParams
from logic.actions_objects_list import Modes
from .button import Button


class RewardLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(225, 150)
        self.setPixmap(QPixmap(settings.REWARD_FRAME_IMAGE))
        self.setScaledContents(True)
        
        self.nut = QLabel(parent=self)
        self.nut.setPixmap(QPixmap(settings.REWARD_ICON_IMAGE))
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
        self._timer.start(settings.VALUE_UPDATE_TIME)

    def _update_value(self):
        self.value, stop_timer = value_update(self.value, self._target_value)
        if stop_timer:
            self._timer.stop()

        self.reward.setText(f"{self.value:.1f}")


class IAmRLAgent(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal()

    def _init_ui(self):
        # Text label
        self._description_label = QLabel()
        self._description_label.setFont(QFont("Pacifico", 14, QFont.Normal))
        self._description_label.setAlignment(Qt.AlignCenter)
        self._description_label.setText("Select one of 6 possible actions.\n\n Learn how to get as much \nreward per episode as possible!\n")
        self._description_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

        # Actions layout
        self._actions_widget = QWidget()
        self._actions_layout = QGridLayout()
        self._action_buttons = []
        for i in range(self._logic.n_actions):
            self._action_buttons.append(Button("./images/symbol" + str(i)))
            self._actions_layout.addWidget(self._action_buttons[i], i // 3, i % 3)
        self._actions_widget.setLayout(self._actions_layout)
        self._actions_widget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
        
        # Reward label
        self._reward_label = RewardLabel()
        
        # Unite everything in vertical layout!
        self._command_layout = QVBoxLayout()
        self._command_layout.addWidget(self._description_label)
        self._command_layout.addWidget(self._actions_widget)#, 20)
        self._command_layout.addWidget(self._reward_label)
        self._command_layout.setAlignment(self._reward_label, Qt.AlignHCenter)
        self.setLayout(self._command_layout)

    def __init__(self, game_screen):
        super().__init__()       

        # I Am RL Agent game logic and parameters
        self._game_screen = game_screen
        self._params = GameParams(Modes.IAMRLAGENT,
                                  game_height=settings.GAME_HEIGHT, game_width=settings.GAME_WIDTH,
                                  hippo_random=True, hippo_move_prob=0.3,
                                  watermelon_random=True, watermelon_move_prob=0.1,
                                  lava_random=5, lava_is_terminal=True)
        self._logic = GameLogic(self._params)

        # Shuffle actions meaning   
        self._actions_correspondence = list(range(self._logic.n_actions))
        shuffle(self._actions_correspondence)

        # Initializing UI
        self._init_ui()

        # Connecting player buttons
        for button in self._action_buttons:
            button.clicked.connect(self._action_chosen)

        self.require_reset = False
        self.made_step_signal.connect(game_screen.update_screen)

    def enter_mode(self):
        self._game_screen.change_logic(self._logic)

    def exit_mode(self):
        pass

    def _action_chosen(self):
        if not self.require_reset:
            clicked_button = self.sender()
            action = -1
            for i, button in enumerate(self._action_buttons):
                if clicked_button is button:
                    action = self._actions_correspondence[i]
                    break

            _, _, done, _ = self._logic.step(action)
            self._reward_label.set_value(self._logic.full_reward)

            if done:
                self.require_reset = True
                
                #TODO: splash screen required
                print(f"Game finished! Full reward: {self._logic.full_reward}. Restart needed!")

            self.made_step_signal.emit()

    def reset(self):
        self._logic.reset()
        self.require_reset = False
        self.made_step_signal.emit()

    def full_reset(self):
        self._logic.full_reset()
        self.require_reset = False
        self.made_step_signal.emit()
