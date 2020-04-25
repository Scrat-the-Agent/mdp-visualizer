from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont

import settings
from logic.q_learning import QLearning
from logic.gameLogic import GameLogic, GameParams
from logic.actions_objects_list import Modes
from .button import Button


class QLabelsVisualization(QWidget):
    def __init__(self, q_learning):
        super().__init__()

        self._q_learning = q_learning
        self._layout = QGridLayout()

        self._q_labels = [QLabel() for i in range(4)]
        self._arrows = [QLabel() for i in range(4)]
        
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

        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    def cell_entered(self):
        cell = self.sender()
        x, y = cell.x, cell.y
        qvalues = self._q_learning.get_q_values((x, y))
        qvalues = [qvalues[2], qvalues[0], qvalues[3], qvalues[1]]

        for i in range(4):
            self._q_labels[i].setText(f"{qvalues[i]:.2f}")

    def cell_left(self):
        for i in range(4):
            self._q_labels[i].setText("")


class AutomaticRL(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal()

    def _init_ui(self):
        self._command_layout = QVBoxLayout()

        # Text label
        self._description_label = QLabel()
        self._description_label.setFont(QFont("Pacifico", 14, QFont.Normal))
        self._description_label.setAlignment(Qt.AlignCenter)
        self._description_label.setText("Press play to launch\nQ-learning algorithm!\n\nHover over cells to watch\nQ-values for them.\n")
        self._description_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
        self._command_layout.addWidget(self._description_label)
        
        # q-values visualization
        self._qlabels = QLabelsVisualization(self._q_learning)
        self._command_layout.addWidget(self._qlabels)

        # rl buttons
        self._buttons = QWidget()
        self._buttons_layout = QHBoxLayout()
        self._play_button = Button(settings.PLAY_BUTTON_IMAGE)
        self._next_step_button = Button(settings.STEP_BUTTON_IMAGE)
        self._buttons_layout.addWidget(self._play_button)
        self._buttons_layout.addWidget(self._next_step_button)
        self._buttons.setLayout(self._buttons_layout)
        self._command_layout.addWidget(self._buttons)

        self.setLayout(self._command_layout)

    def __init__(self, game_screen):
        super().__init__()
        
        self._game_screen = game_screen
        self._params = GameParams(Modes.AUTOMATICRL,
                                  game_height=settings.GAME_HEIGHT, game_width=settings.GAME_WIDTH,
                                  lava_random=2, lava_reward=-10., lava_is_terminal=True,
                                  green_random=5, green_is_terminal=True)

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
        self._game_screen.change_logic(self._logic)
        self.init_cells()

    def exit_mode(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            return

    def init_cells(self):
        # connecting mouse hover from cells to our q-values visualization
        for cell in self._game_screen.cells:
            cell.enter_signal.connect(self._qlabels.cell_entered)
            cell.leave_signal.connect(self._qlabels.cell_left)

        # initialize values
        # TODO: should not it happen in redrawing?
        for i in range(self._logic.game_size[0]):
            for j in range(self._logic.game_size[1]):
                self._game_screen.set_cell_value(i, j, 0.)

        for pos in self._logic.terminal_cells:
            reward = self._logic.game_board.cell_reward(pos)
            self._game_screen.set_cell_value(pos[0], pos[1], reward)

    def _next_step_click(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.updatePic(settings.PLAY_BUTTON_IMAGE)

        self._next_step()

    def _next_step(self):
        print(self._logic.done)
        if self._logic.done:
            self._q_learning.reset()
            print(self._logic.scrat_position, self._logic.done)
        else:
            old_x, old_y = self._logic.scrat_position
            reward, done, info = self._q_learning.step()

            x, y = self._logic.scrat_position
            print(old_x, old_y, x, y, self._q_learning.get_q_values((old_x, old_y)), reward, done)

            new_value = max(self._q_learning.get_q_values((old_x, old_y)))
            self._game_screen.set_cell_value(old_x, old_y, new_value)

        self.made_step_signal.emit()

    def _reset(self):
        self._q_learning.reset()
        self.made_step_signal.emit()

    def full_reset(self):
        self._logic.full_reset()
        self._q_learning.reset_q()
        self.init_cells()
        self.made_step_signal.emit()

    def _play(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.updatePic(settings.PLAY_BUTTON_IMAGE)
            return

        self._playing = True
        self._timer.start(settings.Q_LEARNING_PLAY_SPEED)
        self._play_button.updatePic(settings.STOP_BUTTON_IMAGE)
