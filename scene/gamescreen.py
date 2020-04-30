"""
Game Screen module
=================

This module contains implementation of game screen with the graphical scene on it.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from .pad import FlippablePad
from .objectPicture import ObjectPicture
from .splash import SplashItem


class GameScreen(QGraphicsView):
    """Class GameScreen which manages the screen with the graphical scene and connection to the logic of the game.

    Attributes:
        logic: GameLogic object, the logic of the game which is being visualized.
        splash: SplashItem object, the splash message.
        pad: FlippablePad object, the game pad.
        objects_pictures: A list of ObjectPictures of game objects.
    """

    def _init_with_logic(self, logic):
        """Initializes the screen with game board and objects from the new logic.

        Args:
          logic: GameLogic object.
        """

        self.logic = logic

        scene = QGraphicsScene(self)
        # TODO: do we need this? scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("background: transparent")

        self.splash = SplashItem()
        scene.addItem(self.splash)

        # field with cells
        self.pad = FlippablePad(self.logic)
        scene.addItem(self.pad)

        # objects markers, in reverse order for equal zValues case
        self.objects_pictures = []
        if self.logic.watermelon:
            self.objects_pictures.append(ObjectPicture(self.logic.watermelon, scene, self.pad, self.logic))
        if self.logic.hippo:
            self.objects_pictures.append(ObjectPicture(self.logic.hippo, scene, self.pad, self.logic))
        self.objects_pictures.append(ObjectPicture(self.logic.scrat, scene, self.pad, self.logic))

        # general
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(50, 50)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        # # rotate if mode was switched
        # if self.rotated:
        #     self._make_rotated()

    def __init__(self):
        """A constructor. Only consturct base class object."""

        super().__init__()

        # # the fact the pad was rotated to pseudo-3d
        # self.rotated = False

    @property
    def cells(self):
        """List of lists of Cell objects corresponding to game cells."""

        return self.pad.cells

    def set_cell_value(self, column, row, value):
        """Set a specific value to the cell in specified position.

        Args:
          column: Column of the cell.
          row: Row of the cell.
          value: A value to set.
        """

        self.pad.set_cell_value(column, row, value)

    def change_logic(self, logic):
        """Changes the logic of the visualized game.

        Args:
          logic: A new GameLogic object.
        """

        self._init_with_logic(logic)

    def update_screen(self):
        """Resets cells and objects on the screen."""

        # cells
        for cell in self.cells:
            cell.reset_lava()

        # objects
        for obj in self.objects_pictures:
            obj.change_position()

        self.setFocus()

    def _make_rotated(self):
        """Rotate the pad and animate the objects during rotation."""

        self.pad.rotate()
        for obj in self.objects_pictures:
            obj.pad_rotated()

    def keyPressEvent(self, event):
        """Rotate the pad if T key is pressed. Overrides the base class method. See base class method."""

        if event.nativeVirtualKey() == Qt.Key_T:
            self._make_rotated()
            # self.rotated = not self.rotated

    def resizeEvent(self, event):
        """Resizes the screen. Overrides the base class method. See base class method."""

        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
