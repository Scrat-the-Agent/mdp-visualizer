from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from env_game_interface import EnvGameInterface


class AutomaticRL(QWidget):
    clicked_mode = pyqtSignal()
    made_step_signal = pyqtSignal(int, int, float)

    def _init_ui(self):
        self._command_layout = QVBoxLayout()

        # mode label
        self._label = QLabel()
        self._label.setText("Automatic RL mode")
        self._command_layout.addWidget(self._label)

        # q-values visualization
        self._q_labels = [QLabel() for i in range(4)]
        self._q_layout = QHBoxLayout()
        for _q_label in self._q_labels:
            self._q_layout.addWidget(_q_label)
        self._q_labels_widget = QWidget()
        self._q_labels_widget.setLayout(self._q_layout)
        self._command_layout.addWidget(self._q_labels_widget)

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

    def __init__(self, world, gamescreen, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._world = world
        self._env_game_interface = EnvGameInterface(self._world)
        self._playing = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._next_step)

        # connecting player buttons
        self._play_button.clicked.connect(self._play)
        self._next_step_button.clicked.connect(self._next_step)
        self._reset_button.clicked.connect(self._env_game_interface.reset)

        # connecting mouse hover from cells to our q-values visualization
        for cell in gamescreen.cells:
            cell.enter_signal.connect(self._cell_entered)
            cell.leave_signal.connect(self._cell_left)

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

    def _cell_entered(self):
        cell = self.sender()
        x, y = cell.x, cell.y
        qvalues = self._env_game_interface.get_Q_values(x, y)

        for i in range(4):
            # self._q_labels[i].setText(str(qvalues[i]))
            self._q_labels[i].setText(f"{qvalues[i]:.1f}")

    def _cell_left(self):
        for i in range(4):
            self._q_labels[i].setText("")
