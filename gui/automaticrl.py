from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont

from WTF import EnvGameInterface


class QLabelsVisualization(QWidget):
    def __init__(self, env):
        super().__init__()

        self._env_game_interface = env   #TODO: weirdly long name for ref of game logic
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
        qvalues = self._env_game_interface.get_Q_values(x, y)

        for i in range(4):
            self._q_labels[i].setText(f"{qvalues[i]:.2f}")

    def cell_left(self):
        for i in range(4):
            self._q_labels[i].setText("")


class AutomaticRL(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal(int, int, float)

    def _init_ui(self, env):
        self._command_layout = QVBoxLayout()

        # mode label
        self._label = QLabel()
        self._label.setText("Automatic RL mode")
        self._command_layout.addWidget(self._label)

        # q-values visualization
        self._qlabels = QLabelsVisualization(env)
        self._command_layout.addWidget(self._qlabels)

        # rl buttons
        self._buttons = QWidget()
        self._play_button = QPushButton("Play")
        self._next_step_button = QPushButton("Step")
        self._reset_button = QPushButton("Reset")

        self._buttons_layout = QVBoxLayout()
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

    def __init__(self, world, gamescreen, parent=None): # TODO world => logic
        super().__init__(parent)
        self._world = world
        self._env_game_interface = EnvGameInterface(self._world)
        self._playing = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._next_step)

        self._init_ui(self._env_game_interface)

        # connecting player buttons
        self._play_button.clicked.connect(self._play)
        self._next_step_button.clicked.connect(self._next_step)
        self._reset_button.clicked.connect(self._env_game_interface.reset)

        # connecting mouse hover from cells to our q-values visualization
        for cell in gamescreen.cells:
            cell.enter_signal.connect(self._qlabels.cell_entered)
            cell.leave_signal.connect(self._qlabels.cell_left)

        self.made_step_signal.connect(gamescreen.update_screen)

    def _next_step(self):
        reward, done, info = self._env_game_interface.next_step()
        x, y = self._env_game_interface.player_pos
        new_value = self._env_game_interface.get_value(x, y)
        self.made_step_signal.emit(x, y, new_value)

        action = info['actions'][-1]
        if done:
            self._reward_label.setText("Done!")
        else:
            self._reward_label.setText(f"Last reward: {reward}; Last action: {action}")

    def _play(self):
        if self._playing:
            self._playing = False
            self._timer.stop()
            self._play_button.setText("Play")
            return

        self._playing = True
        self._timer.start(500)  # TODO: move to settings
        self._play_button.setText("Stop")
