from PyQt5.QtWidgets import QMainWindow, QComboBox, QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QBrush, QPalette, QFont, QFontDatabase

import settings
from utils import animate
from .automaticrl import AutomaticRL
from .iamrlagent import IAmRLAgent

from scene.gamescreen import GameScreen
from WTF import World

class ModeSwitcher(QWidget):
    def __init__(self, contents):
        super().__init__()
        self._contents = contents
        self._id = 0

        for content in self._contents:
            content.setParent(self)

    def resizeEvent(self, evt=None):
        for id, content in enumerate(self._contents):
            content.setGeometry(0 if id == self._id else -1.2 * self.width(), 0, self.width(), self.height())

    # TODO: WHYYYY IT DOES NOT WORK
    @property
    def sizeHint(self):
        return self._contents[self._id].sizeHint

    # TODO: WHYYYY IT DOES NOT WORK
    @property
    def minimumSizeHint(self):
        return self._contents[self._id].minimumSizeHint

    def turn(self, id):
        if id != self._id:
            self.disappear_anim = animate(self._contents[self._id], "geometry", 400, 
                                    QRectF(1.2 * -self.width(), 0, self.width(), self.height()))
            self.disappear_anim.finished.connect(self._animation_finish)
            
            self._id = id

            self._contents[self._id].setVisible(True)
            self._contents[self._id].setGeometry(1.2 * self.width(), 0, self.width(), self.height())
            self.appear_anim = animate(self._contents[self._id], "geometry", 400, 
                                    QRectF(0, 0, self.width(), self.height()))
    
    def _animation_finish(self):
        for id, content in enumerate(self._contents):
            if id != self._id:
                content.setVisible(False)

class MainWindow(QMainWindow):
    def _init_ui(self):
        # background image
        sh = f"background-image: url({settings.BACKGROUND_IMAGE})"
        self.setStyleSheet("MainWindow {" + sh + "}")

        # mode switcher
        self._combo_box = QComboBox()
        self._combo_box.setFont(QFont("Pacifico", 14, QFont.Normal))
        self._combo_box.addItems(["I Am RL Agent", "Automatic RL, Please"])
        for i in range(2):
            self._combo_box.setItemData(i, Qt.AlignCenter)

        # game screen
        self._game_screen = GameScreen(self._world)

        # widget for each mode
        self._iAmRLAgent = IAmRLAgent(self._world)
        self._automaticRL = AutomaticRL(self._world, self._game_screen)

        # mode widget
        self._mode_widget = ModeSwitcher([self._iAmRLAgent, self._automaticRL])

        # left widget
        self._left_layout = QVBoxLayout()
        self._left_layout.addWidget(self._combo_box)
        self._left_layout.addWidget(self._mode_widget)
        self._left_widget = QWidget()
        #self._left_widget.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred))
        self._left_widget.setLayout(self._left_layout)

        # central widget
        self._central_layout = QHBoxLayout()
        self._central_layout.addWidget(self._left_widget)
        self._central_layout.addWidget(self._game_screen)

        self._central_widget = QWidget() 
        self._central_widget.setLayout(self._central_layout)
        self.setCentralWidget(self._central_widget)        

    def __init__(self):
        super().__init__()
        self._world = World(settings.ROWS, settings.COLS)
        self._init_ui()
        self._combo_box.currentIndexChanged.connect(self._mode_widget.turn)

    # DEL
    # def _mode_change(self, mode):
    #     if mode == 0:
    #         self._automaticRL.setEnabled(False)
    #         self._iAmRLAgent.setEnabled(True)
    #         self._mode_widget.setCurrentWidget(self._iAmRLAgent)
    #     else:
    #         self._automaticRL.setEnabled(True)
    #         self._iAmRLAgent.setEnabled(False)
    #         self._mode_widget.setCurrentWidget(self._automaticRL)
