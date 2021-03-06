"""
I Am RL Agent module
=================

This module contains IAmRLAgent mode widget.
"""

from random import shuffle

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont

from .. import settings
from ..utils import value_update
from ..logic.gameLogic import GameLogic, GameParams
from ..logic.actions_objects_list import Modes
from .button import Button


class RewardLabel(QLabel):
    """Implements a reward label for pretty showing of reward.

    Attributes:
        nut: A QLabel for a nut picture.
        reward: A QLabel for current reward text.
        value: Current reward value for animated update.
    """

    def __init__(self):
        """A constructor of reward label."""
        super().__init__()
        self.setFixedSize(settings.REWARD_LABEL_NAILS)
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
        """Internal Qt function to process resizing of widget"""
        super().resizeEvent(e)
        self.nut.setGeometry(self.height() / 4, self.height() / 4, self.height() / 2, self.height() / 2)
        self.reward.setGeometry(self.height() / 2, 0, self.width() - self.height() / 2, self.height())

    def set_value(self, new_value: float):
        """Sets a new target value.

        Args:
            new_value - new target value.
        """

        self._target_value = new_value
        self._timer.start(settings.VALUE_UPDATE_TIME)

    def _update_value(self):
        self.value, stop_timer = value_update(self.value, self._target_value)
        if stop_timer:
            self._timer.stop()

        self.reward.setText(f"{self.value:.1f}")


# noinspection PyArgumentEqualDefault
class IAmRLAgent(QWidget):
    """A widget for IAmRLAgent game mode.

    Attributes:
        require_reset: The game requires reset or not.
    """

    user_interacted = pyqtSignal()
    made_step_signal = pyqtSignal()

    def _init_ui(self):
        """Initializes user interface of the widget for IAmRLAgent mode."""

        # Text label
        self._description_label = QLabel()
        self._description_label.setFont(QFont("Pacifico", 14, QFont.Normal))
        self._description_label.setAlignment(Qt.AlignCenter)
        self._description_label.setText(settings.IAMRLAGENT_DESCRIPTION)
        self._description_label.setFixedSize(settings.IAMRLAGENT_DESCRIPTION_NAILS)

        # Actions layout
        self._actions_widget = QWidget()
        self._actions_layout = QGridLayout()
        self._action_buttons = []
        for i in range(self._logic.n_actions):
            path = settings.BUTTONS_PATHS[i]
            self._action_buttons.append(Button(path))
            self._actions_layout.addWidget(self._action_buttons[i], i // 3, i % 3)
        self._actions_widget.setLayout(self._actions_layout)
        self._actions_widget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

        # Reward label
        self._reward_label = RewardLabel()

        # Unite everything in vertical layout!
        self._command_layout = QVBoxLayout()
        self._command_layout.addWidget(self._description_label, 0, Qt.AlignHCenter)
        self._command_layout.addWidget(self._actions_widget)
        self._command_layout.addWidget(self._reward_label, 0, Qt.AlignHCenter)
        self.setLayout(self._command_layout)

    def __init__(self, game_screen):
        """Initializes IAmRLAgent widget and starts the game.

        Args:
            game_screen: GameScreen object with the graphics scene.
        """

        super().__init__()

        # I Am RL Agent game logic and parameters
        self._game_screen = game_screen
        self._params = GameParams(Modes.IAMRLAGENT,
                                  game_height=settings.GAME_HEIGHT, game_width=settings.GAME_WIDTH,
                                  hippo_random=True, hippo_move_prob=settings.HIPPO_MOVE_PROB,
                                  watermelon_random=True, watermelon_move_prob=settings.WATERMELON_MOVE_PROB,
                                  lava_random=settings.IAMRLAGENT_LAVA_RANDOM, lava_is_terminal=True,
                                  tick_penalty=settings.TICK_PENALTY)
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
        """Turns on IAmRlAgent mode."""

        self._game_screen.change_logic(self._logic)
        self._reward_label.set_value(self._logic.full_reward)

    def exit_mode(self):
        """Turns off IAmRlAgent mode."""

        self._game_screen.splash.disappear()

    def _action_chosen(self):
        """Sends the chosen action to the logic and updates the screen."""
        if not self.require_reset:
            self.user_interacted.emit()

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

                text = settings.EPISODE_END_MESSAGE1
                text += f"{self._logic.full_reward:.1f}"
                text += settings.EPISODE_END_MESSAGE2
                self._game_screen.splash.appear(text)

            self.made_step_signal.emit()

    def reset(self):
        """Resets the board to the initial state without resampling of random values."""

        self._logic.reset()
        self.require_reset = False
        self._reward_label.set_value(self._logic.full_reward)
        self.made_step_signal.emit()
        self._game_screen.splash.disappear()

    def full_reset(self):
        """Resets the board to the initial state with resampling of random values."""

        self._logic.full_reset()
        shuffle(self._actions_correspondence)
        self.require_reset = False
        self._reward_label.set_value(self._logic.full_reward)
        self.made_step_signal.emit()
        self._game_screen.splash.disappear()
