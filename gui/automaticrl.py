"""
Automatic RL module
======================

This module contains widget for the automatic RL mode.
"""

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont

import settings
from utils import value_update

from scene.gamescreen import GameScreen
from logic.q_learning import QLearning
from logic.gameLogic import GameLogic, GameParams
from logic.actions_objects_list import Modes

from .button import Button

__all__ = ('AutomaticRL',)


class QLabelsVisualization(QWidget):
    """
    This widget is designed to show Q-values of the state
    corresponding to cell over which cursor hovers.
    """

    def __init__(self, q_learning: QLearning):
        """
        Constructs widget with four arrows.
        Takes Q-learning object as input to take
        Q-values from it.

        Args:
            q_learning(QLearning): object that implements Q-learning algorithm
        """
        super().__init__()

        self._q_learning = q_learning
        self._layout = QGridLayout()

        self._q_labels = [QLabel() for _ in range(4)]
        self._arrows = [QLabel() for _ in range(4)]

        pics = [settings.RIGHT_ARROW_BUTTON_IMAGE,
                settings.LEFT_ARROW_BUTTON_IMAGE,
                settings.DOWN_ARROW_BUTTON_IMAGE,
                settings.UP_ARROW_BUTTON_IMAGE]
        font = QFont("Impact", weight=QFont.Bold)
        font.setPixelSize(24)

        for _q_label, pos in zip(self._q_labels, [(2, 4), (2, 0), (4, 2), (0, 2)]):
            self._layout.addWidget(_q_label, *pos)
            _q_label.setAlignment(Qt.AlignCenter)
            _q_label.setFont(font)
            _q_label.setFixedSize(QSize(50, 30))
        for _arrow, pos, pic in zip(self._arrows, [(2, 3), (2, 1), (3, 2), (1, 2)], pics):
            self._layout.addWidget(_arrow, *pos)
            _arrow.setAlignment(Qt.AlignCenter)
            _arrow.setPixmap(QPixmap(pic).scaled(50, 50, Qt.KeepAspectRatio))
            _arrow.setScaledContents(False)

        self._displayed_coords = None
        self._timer = QTimer()
        self._timer.setInterval(settings.VALUE_UPDATE_TIME)
        self._timer.timeout.connect(self._update)

        self.setLayout(self._layout)
        self.setFixedSize(settings.Q_VISUALIZATION_NAILS)

    def cell_entered(self):
        """Updates Q-values on the arrows"""
        cell = self.sender()
        self._displayed_coords = cell.x, cell.y
        
        qvalues = self._q_learning.get_q_values(self._displayed_coords)
        self._qvalues = [qvalues[2], qvalues[0], qvalues[3], qvalues[1]]
        
        for i in range(4):
            self._q_labels[i].setText(f"{self._qvalues[i]:.2f}")

    def cell_left(self):
        """Removes text from arrows if cursor hovers over nothing"""
        for i in range(4):
            self._q_labels[i].setText("")

    def _update(self):
        all_done = True
        for i in range(4):
            self._qvalues[i], done = value_update(self._qvalues[i], self._target_qvalues[i])
            all_done = all_done and done
            self._q_labels[i].setText(f"{self._qvalues[i]:.2f}")

        if all_done:
            self._timer.stop()

    def values_updates(self, x : int, y : int):
        """
        Notifies widget that cell with coordinates x, y has updated Q-values
        
        Args:
            x - int
            y - int
        """
        if (x, y) == self._displayed_coords:
            qvalues = self._q_learning.get_q_values(self._displayed_coords)
            self._target_qvalues = [qvalues[2], qvalues[0], qvalues[3], qvalues[1]]

            self._timer.start()


# noinspection PyArgumentEqualDefault,PyCompatibility
class AutomaticRL(QWidget):
    """
    This class represents a widget for the Q-learning mode.
    It consists of play/step buttons, labels for visualization of
    Q-values for hovered cell. It uses instance of `logic.gameLogic.GameLogic`
    as an environment for RL agent.
    """

    made_step_signal = pyqtSignal()
    user_interacted = pyqtSignal()

    def _init_ui(self):
        self._command_layout = QVBoxLayout()

        # Text label
        self._description_label = QLabel()
        self._description_label.setFont(QFont("Pacifico", 14, QFont.Normal))
        self._description_label.setAlignment(Qt.AlignCenter)
        self._description_label.setText(settings.Q_LEARNING_DESCRIPTION)
        self._description_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
        self._description_label.setFixedSize(settings.AUTO_RL_DESCRIPTION_NAILS)
        self._command_layout.addWidget(self._description_label, 0, Qt.AlignHCenter)

        # q-values visualization
        self._qlabels = QLabelsVisualization(self._q_learning)
        self._command_layout.addWidget(self._qlabels, 0, Qt.AlignHCenter)

        # rl buttons
        self._buttons = QWidget()
        self._buttons_layout = QHBoxLayout()
        self._play_button = Button(settings.PLAY_BUTTON_IMAGE)
        self._next_step_button = Button(settings.STEP_BUTTON_IMAGE)
        self._buttons_layout.addWidget(self._play_button)
        self._buttons_layout.addWidget(self._next_step_button)
        self._buttons.setLayout(self._buttons_layout)
        self._buttons.setFixedWidth(settings.BUTTONS_NAILS_WIDTH)
        self._command_layout.addWidget(self._buttons, 0, Qt.AlignHCenter)

        self.setLayout(self._command_layout)

    def __init__(self, game_screen : GameScreen):
        """
        Constructs an AutomaticRL widget.

        AutomaticRL widget needs `game_screen` to update
        information in cells about Q-values.
        
        Args:
            game_screen - GameScreen instance.
        """
        super().__init__()

        self._game_screen = game_screen
        self._params = GameParams(Modes.AUTOMATICRL,
                                  game_height=settings.GAME_HEIGHT, game_width=settings.GAME_WIDTH,
                                  lava_random=settings.AUTOMATIC_LAVA_RANDOM, lava_reward=settings.LAVA_REWARD,
                                  lava_is_terminal=True,
                                  green_random=settings.GREEN_RANDOM, green_reward=settings.GREEN_REWARD,
                                  green_is_terminal=True)

        self._logic = GameLogic(self._params)
        self._q_learning = QLearning(self._logic)

        self._playing = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._next_step)

        self._init_ui()

        # connecting player buttons
        self._play_button.clicked.connect(self._play)
        self._next_step_button.clicked.connect(self._next_step_click)

        self.made_step_signal.connect(game_screen.update_screen)

    def enter_mode(self):
        """Replaces game screen logic with RL environment and resets cells."""
        self._game_screen.change_logic(self._logic)
        self.init_cells()

    def exit_mode(self):
        """Stops playing. Used when current mode is being changed."""
        if self._playing:
            self._playing = False
            self._timer.stop()
            return

    def init_cells(self):
        """
        Reinitializes self if cells have changed.

        Internally does two things:
            1. Connects signals to new cells;
            2. Resets values for each cell.

        #TODO: if graphic scene will be switched without scene reinitialization
        (see issue #44), this function will not be required.
        """

        # connecting mouse hover from cells to our q-values visualization
        for cell in self._game_screen.cells:
            cell.enter_signal.connect(self._qlabels.cell_entered)
            cell.leave_signal.connect(self._qlabels.cell_left)

        # initialize values
        for i in range(self._logic.game_size[0]):
            for j in range(self._logic.game_size[1]):
                self._game_screen.set_cell_value(i, j, 0.)

        for pos in self._logic.terminal_cells:
            reward = self._logic.game_board.cell_reward(pos)
            self._game_screen.set_cell_value(pos[0], pos[1], reward)

    def _next_step_click(self):
        self.user_interacted.emit()
        self._stop_playing()
        self._next_step()

    def _next_step(self):
        if self._logic.done:
            self._q_learning.reset()
        else:
            old_x, old_y = self._logic.scrat_position
            reward, done, info = self._q_learning.step()
            new_value = max(self._q_learning.get_q_values((old_x, old_y)))
            
            # updating value on the cell in gamefield
            self._game_screen.set_cell_value(old_x, old_y, new_value)
            
            # updating q-visualization
            self._qlabels.values_updates(old_x, old_y)

        self.made_step_signal.emit()

    def _stop_playing(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.updatePic(settings.PLAY_BUTTON_IMAGE)

    def reset(self):
        """Reset game state and send signal that state changed"""
        self._stop_playing()
        self._q_learning.reset()
        self.made_step_signal.emit()

    def full_reset(self):
        """Reinitialize logic randomly"""
        self._stop_playing()
        self._logic.full_reset()
        self._q_learning.reset_q()
        self.init_cells()
        self.made_step_signal.emit()

    def _play(self):
        self.user_interacted.emit()
        
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.updatePic(settings.PLAY_BUTTON_IMAGE)
            return

        self._playing = True
        self._timer.start(settings.Q_LEARNING_PLAY_SPEED)
        self._play_button.updatePic(settings.STOP_BUTTON_IMAGE)
