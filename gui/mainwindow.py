from PyQt5.QtWidgets import QMainWindow, QComboBox, QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QBrush, QPalette, QFont, QFontDatabase

import settings
from utils import animate
from .automaticrl import AutomaticRL
from .iamrlagent import IAmRLAgent
from logic.actions_objects_list import Modes

from scene.gamescreen import GameScreen
from .button import Button

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

    @property
    def current_widget(self):
        return self._contents[self._id]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # background image
        sh = f"background-image: url({settings.BACKGROUND_IMAGE})"
        self.setStyleSheet("MainWindow {" + sh + "}")

        # mode switcher
        self._combo_box = QComboBox()
        self._combo_box.setFont(QFont("Pacifico", 14, QFont.Normal))
        self._combo_box.addItems(["I Am RL Agent", "Automatic RL, Please"])
        for i in range(2):
            self._combo_box.setItemData(i, Qt.AlignCenter)

        # Reset layout
        self._buttons = QWidget()
        self._reset_layout = QHBoxLayout()
        self._reset_button = Button(settings.RESET_BUTTON_IMAGE)
        self._full_reset_button = Button(settings.FULL_RESET_BUTTON_IMAGE)
        self._reset_layout.addWidget(self._reset_button)
        self._reset_layout.addWidget(self._full_reset_button)
        self._buttons.setLayout(self._reset_layout)
        self._buttons.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

        # widget for each mode
        self._game_screen = GameScreen()
        self._iAmRLAgent = IAmRLAgent(self._game_screen)
        self._automaticRL = AutomaticRL(self._game_screen)
        self._iAmRLAgent.enter_mode()

        # mode widget
        self._mode_widget = ModeSwitcher([self._iAmRLAgent, self._automaticRL])

        # left widget
        self._left_layout = QVBoxLayout()
        self._left_layout.addWidget(self._combo_box)
        self._left_layout.addWidget(self._buttons)
        self._left_layout.addWidget(self._mode_widget)
        self._left_widget = QWidget()
        self._left_widget.setFixedWidth(300)
        self._left_widget.setLayout(self._left_layout)

        # central widget
        self._central_layout = QHBoxLayout()
        self._central_layout.addWidget(self._left_widget)
        self._central_layout.addWidget(self._game_screen)

        self._central_widget = QWidget() 
        self._central_widget.setLayout(self._central_layout)
        self.setCentralWidget(self._central_widget)

        # focus
        self._game_screen.setFocus()
        self._reset_button.clicked.connect(self._reset)
        self._full_reset_button.clicked.connect(self._full_reset)
        self._combo_box.currentIndexChanged.connect(self._change_mode)

    def _change_mode(self, id):        
        self._mode_widget.current_widget.exit_mode()
        self._mode_widget.turn(id)
        self._mode_widget.current_widget.enter_mode()

        # focus!
        self._game_screen.setFocus()

    def _reset(self):
        self._mode_widget.current_widget.reset()

    def _full_reset(self):
        self._mode_widget.current_widget.full_reset()       
