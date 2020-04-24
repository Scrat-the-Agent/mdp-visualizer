from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap, QFont

import settings
from logic.q_learning import QLearning
from .button import Button


class QLabelsVisualization(QWidget):
    def __init__(self, q_learning):
        super().__init__()

        self._q_learning = q_learning
        self._layout = QGridLayout()

        self._q_labels = [QLabel() for i in range(4)]
        self._arrows = [QLabel() for i in range(4)]

        font = QFont("Impact")
        font.setPixelSize(24)
        
        pics = [settings.RIGHT_ARROW_BUTTON_IMAGE,
                settings.LEFT_ARROW_BUTTON_IMAGE,
                settings.DOWN_ARROW_BUTTON_IMAGE,
                settings.UP_ARROW_BUTTON_IMAGE]
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

        # rl buttons
        self._buttons = QWidget()
        self._play_button = Button(settings.PLAY_BUTTON_IMAGE)
        self._next_step_button = Button(settings.STEP_BUTTON_IMAGE)
        self._reset_button = Button(settings.RESET_BUTTON_IMAGE)
        self._full_reset_button = Button(settings.FULL_RESET_BUTTON_IMAGE)

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._play_button)
        self._buttons_layout.addWidget(self._next_step_button)
        self._buttons_layout.addWidget(self._reset_button)
        self._buttons_layout.addWidget(self._full_reset_button)
        self._buttons.setLayout(self._buttons_layout)
        self._command_layout.addWidget(self._buttons)

        # q-values visualization
        self._qlabels = QLabelsVisualization(self._q_learning)
        self._command_layout.addWidget(self._qlabels)

        self.setLayout(self._command_layout)

    def __init__(self, logic, gamescreen, parent=None):
        super().__init__(parent)
        self._logic = logic
        self._q_learning = QLearning(self._logic)
        self._gamescreen = gamescreen

        self._playing = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._next_step)

        self._init_ui()

        # connecting player buttons
        self._play_button.clicked.connect(self._play)
        self._next_step_button.clicked.connect(self._next_step_click)
        self._reset_button.clicked.connect(self._reset)
        self._full_reset_button.clicked.connect(self._full_reset)

        self.made_step_signal.connect(gamescreen.update_screen)

    def exit_mode(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.setText("Play")
            return

    def init_cells(self):
        # connecting mouse hover from cells to our q-values visualization
        for cell in self._gamescreen.cells:
            cell.enter_signal.connect(self._qlabels.cell_entered)
            cell.leave_signal.connect(self._qlabels.cell_left)

        for pos in self._logic.terminal_cells:
            reward = self._logic.game_board.cell_reward(pos)
            self._gamescreen.set_cell_value(pos[0], pos[1], reward)

    def _next_step_click(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.updatePic(settings.PLAY_BUTTON_IMAGE)

        self._next_step()

    def _next_step(self):
        old_x, old_y = self._logic.scrat_position
        reward, done, info = self._q_learning.step()

        new_value = max(self._q_learning.get_q_values((old_x, old_y)))
        self._gamescreen.set_cell_value(old_x, old_y, new_value)

        self.made_step_signal.emit()

        if done:
            self._q_learning.reset()

    def _reset(self):
        self._q_learning.reset()
        self.made_step_signal.emit()

    def _full_reset(self):
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
