# QDirIterator
# pyqtSignal
# pyqtProperty

import sys

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QHBoxLayout, QLabel, QWidget, \
    QStackedWidget, QPushButton, QComboBox, QVBoxLayout, QGridLayout
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget

from settings import BACKGROUND_IMAGE
from splash import SplashItem
from world import World
from env_game_interface import EnvGameInterface


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._central_widget = QStackedWidget()
        self._iAmRLAgent = IAmRLAgent()
        self._automaticRL = AutomaticRL()
        self._central_widget.addWidget(self._iAmRLAgent)
        self._central_widget.addWidget(self._automaticRL)
        self.setCentralWidget(self._central_widget)

        self._iAmRLAgent.clicked_mode.connect(self._enableAutomaticRLMode)
        self._automaticRL.clicked_mode.connect(self._enableIAMRLAgentMode)

    def _enableIAMRLAgentMode(self):
        self._central_widget.removeWidget(self._iAmRLAgent)
        self._iAmRLAgent = IAmRLAgent()
        self._central_widget.addWidget(self._iAmRLAgent)
        self._central_widget.setCurrentWidget(self._iAmRLAgent)
        self._iAmRLAgent.clicked_mode.connect(self._enableAutomaticRLMode)
        self._iAmRLAgent._game.setFocus()  # protected member ?

    def _enableAutomaticRLMode(self):
        self._central_widget.removeWidget(self._automaticRL)
        self._automaticRL = AutomaticRL()
        self._central_widget.addWidget(self._automaticRL)
        self._central_widget.setCurrentWidget(self._automaticRL)
        self._automaticRL.clicked_mode.connect(self._enableIAMRLAgentMode)
        self._automaticRL._game.setFocus()  # protected member ?


class IAmRLAgent(QWidget):
    clicked_mode = pyqtSignal()

    def _init_ui(self):
        # game
        self._game = Game()

        # mode switcher
        self._list_modes = ModesComboBox(0)

        # reward label
        self._reward_label = QLabel()
        self._reward_label.setText("Your last reward: 5")

        # hint for buttons
        self._actions_label = QLabel()
        self._actions_label.setText("Choose your next action")

        # buttons layout
        self._actions_layout = QGridLayout()
        self._actions_layout.setColumnStretch(0, 10)
        self._actions_layout.setColumnStretch(1, 10)
        self._actions_layout.setColumnStretch(2, 10)
        self._actions_layout.setRowStretch(0, 10)
        self._actions_layout.setRowStretch(1, 10)

        self._action_1 = QPushButton("1")
        self._action_2 = QPushButton("2")
        self._action_3 = QPushButton("3")
        self._action_4 = QPushButton("4")
        self._action_5 = QPushButton("5")
        self._action_6 = QPushButton("6")

        self._actions_layout.addWidget(self._action_1, 0, 0)
        self._actions_layout.addWidget(self._action_2, 0, 1)
        self._actions_layout.addWidget(self._action_3, 0, 2)
        self._actions_layout.addWidget(self._action_4, 1, 0)
        self._actions_layout.addWidget(self._action_5, 1, 1)
        self._actions_layout.addWidget(self._action_6, 1, 2)

        # overall layout
        self._command_layout = QVBoxLayout()
        self._command_layout.addWidget(self._list_modes)
        self._command_layout.addWidget(self._actions_label)
        self._command_layout.addLayout(self._actions_layout)
        self._command_layout.addWidget(self._reward_label)

        self._layout = QHBoxLayout()
        self._layout.addLayout(self._command_layout)
        self._layout.addWidget(self._game)

        self.setLayout(self._layout)
        self._list_modes.currentIndexChanged.connect(self.clicked_mode.emit)

    def __init__(self, parent=None):
        super(IAmRLAgent, self).__init__(parent)
        self._init_ui()


class AutomaticRL(QWidget):
    clicked_mode = pyqtSignal()

    def _init_ui(self):
        # left layout
        self._command_layout = QVBoxLayout()

        # mode switcher
        self._list_modes = ModesComboBox(1)
        self._command_layout.addWidget(self._list_modes)

        # mode label
        self._label = QLabel()
        self._label.setText("Automatic RL mode")
        self._command_layout.addWidget(self._label)

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

        # main layout and game widgets
        self._layout = QHBoxLayout()
        self._game = Game()
        self._layout.addLayout(self._command_layout)
        self._layout.addWidget(self._game)

        self.setLayout(self._layout)
        self._list_modes.currentIndexChanged.connect(self.clicked_mode.emit)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._env_game_interface = EnvGameInterface(self._game.world)
        self._playing = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._next_step)

        self._play_button.clicked.connect(self._play)
        self._next_step_button.clicked.connect(self._next_step)
        self._reset_button.clicked.connect(self._env_game_interface.reset)

    def _next_step(self):
        reward, done, info = self._env_game_interface.next_step()
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
        self._timer.start(500)
        self._play_button.setText("Stop")


class ModesComboBox(QComboBox):
    def __init__(self, cur_mode=0):
        super().__init__()

        self.addItems(["I Am RL Agent", "Automatic RL, Please"])
        self.setCurrentIndex(cur_mode)


class Game(QGraphicsView):
    def __init__(self):
        super().__init__(parent=None)

        # background
        scene = QGraphicsScene(self)
        pix = QPixmap(BACKGROUND_IMAGE)
        scene.setBackgroundBrush(QBrush(pix))
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)

        # world
        self.world = World(scene)

        # splash
        self.splash = SplashItem()
        self.splash.setZValue(1)
        self.splash.setPos(-self.splash.boundingRect().width() / 2, scene.sceneRect().top() - 2)
        scene.addItem(self.splash)

        # general
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(50, 50)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        if QGLFormat.hasOpenGL():
            self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))

    def keyPressEvent(self, event):
        self.splash.disappear()
        self.world.keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    navigator = GameWindow()
    navigator.show()

    sys.exit(app.exec_())
