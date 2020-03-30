# QDirIterator
# pyqtSignal
# pyqtProperty

import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QHBoxLayout, QLabel, QWidget, \
    QStackedWidget, QPushButton, QComboBox
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget

from settings import BACKGROUND_IMAGE
from splash import SplashItem
from world import World


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._central_widget = QStackedWidget()
        self._iAmRLAgent = IAmRLAgent()
        self._automaticRL = AutomaticRL()
        self._central_widget.addWidget(self._iAmRLAgent)
        self._central_widget.addWidget(self._automaticRL)
        self.setCentralWidget(self._central_widget)

        self._iAmRLAgent.clicked.connect(self._EnableAutomaticRLMode) # lambda: self._central_widget.setCurrentWidget(self._automaticRL))
        self._automaticRL.clicked.connect(self._EnableIAMRLAgentMode) # lambda: self._central_widget.setCurrentWidget(self._EnableIAMRLAgentMode()))

    def _EnableIAMRLAgentMode(self):
        print("Here")
        self._central_widget.setCurrentWidget(self._iAmRLAgent)
        self._iAmRLAgent = IAmRLAgent()

        # return self._iAmRLAgent

    def _EnableAutomaticRLMode(self):
        print("Here 2")
        # self._automaticRL = AutomaticRL()
        self._central_widget.setCurrentWidget(self._automaticRL)

        # return self._automaticRL


class IAmRLAgent(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(IAmRLAgent, self).__init__(parent)

        print("IAmRLAgent constructor")

        self._game = Game()
        self._label = QLabel()
        self._label.setText("FORTS AND MILLS 2.0")
        self._list_modes = ModesComboBox(0)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._game)
        self._layout.addWidget(self._list_modes)

        self.setLayout(self._layout)
        self._list_modes.currentIndexChanged.connect(self.clicked.emit)


class AutomaticRL(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(AutomaticRL, self).__init__(parent)

        print("AutomaticRL constructor")

        self._label = QLabel()
        self._label.setText("FORTS AND MILLS 3.0")
        self._list_modes = ModesComboBox(1)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._list_modes)

        self.setLayout(self._layout)
        self._list_modes.currentIndexChanged.connect(self.clicked.emit)


class ModesComboBox(QComboBox):
    def __init__(self, cur_mode=0):
        super().__init__()

        print("Combobox constructor")

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
