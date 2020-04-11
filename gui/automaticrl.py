from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont, QIcon, QPalette, QColor

from logic.q_learning import QLearning


class QLabelsVisualization(QWidget):
    def __init__(self, q_learning):
        super().__init__()

        self._q_learning = q_learning
        self._layout = QGridLayout()

        self._q_labels = [QLabel() for i in range(4)]
        self._arrows = [QLabel() for i in range(4)]

        font = QFont("Impact")
        font.setPixelSize(24)
        
        pics = ["./images/right", "./images/left", "./images/down", "./images/up"]  # TODO: constant?        
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

        for i in range(4):
            self._q_labels[i].setText(f"{qvalues[i]:.2f}")

    def cell_left(self):
        for i in range(4):
            self._q_labels[i].setText("")


class Button(QPushButton):
    def __init__(self, name):
        super().__init__()

        self.setMinimumHeight(50)
        self.setMinimumWidth(50)

        # transparent background
        self.setStyleSheet("QPushButton {border-style: outset; border-width: 0px; margin: 0px; padding: 0px;}")
        self.setAttribute(Qt.WA_TranslucentBackground)

        #picture change
        self.name = name
        self._pressed = False
        self.updatePic()

        self.pressed.connect(self._whenpressed)
        self.released.connect(self._whenreleased)

    def resizeEvent(self, e):
        self.setIconSize(self.size())

    def _whenpressed(self):
        self._pressed = True
        self.updatePic()

    def _whenreleased(self):
        self._pressed = False
        self.updatePic()

    def updatePic(self, name=None):
        self.name = name or self.name
        pixmap = QPixmap(self.name + ("pr" if self._pressed else ""))
        self.setIcon(QIcon(pixmap))


class AutomaticRL(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal()

    def _init_ui(self):
        self._command_layout = QVBoxLayout()

        # q-values visualization
        self._qlabels = QLabelsVisualization(self._q_learning)
        self._command_layout.addWidget(self._qlabels)

        # rl buttons
        self._buttons = QWidget()
        self._play_button = Button("./images/play")
        self._next_step_button = Button("./images/step")
        self._reset_button = Button("./images/repeat")

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._play_button)
        self._buttons_layout.addWidget(self._next_step_button)
        self._buttons_layout.addWidget(self._reset_button)
        self._buttons.setLayout(self._buttons_layout)
        self._command_layout.addWidget(self._buttons)

        # info labels
        self._reward_label = QLabel()
        self._reward_label.setText("Last reward: 10")
        self._command_layout.addWidget(self._reward_label)

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
        self._next_step_button.clicked.connect(self._next_step)
        self._reset_button.clicked.connect(self._reset)

        self.made_step_signal.connect(gamescreen.update_screen)

    def init_cells(self):
        # connecting mouse hover from cells to our q-values visualization
        for cell in self._gamescreen.cells:
            cell.enter_signal.connect(self._qlabels.cell_entered)
            cell.leave_signal.connect(self._qlabels.cell_left)

        for pos in self._logic.terminal_cells:
            reward = self._logic.game_board.cell_reward(pos)
            print(pos, reward)
            self._gamescreen.set_cell_value(pos[0], pos[1], reward)

    def _next_step(self):
        reward, done, info = self._q_learning.step()
        if not done:
            x, y = self._logic.scrat_position
            new_value = self._q_learning.get_value(self._q_learning.state)
            self._gamescreen.set_cell_value(x, y, new_value)

        self.made_step_signal.emit()

        action = info['actions'][-1]
        if done:
            self._reward_label.setText("Done!")
        else:
            self._reward_label.setText(f"Last reward: {reward}; Last action: {action}")

    def _reset(self):
        self._q_learning.reset()
        self.made_step_signal.emit()

    def _play(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.updatePic("./images/play")
            return

        self._playing = True
        self._timer.start(500)  # TODO: move to settings
        self._play_button.updatePic("./images/stop")
