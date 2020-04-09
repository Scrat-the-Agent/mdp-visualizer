from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBrush, QPainter
from PyQt5.QtOpenGL import QGLFormat, QGLWidget, QGL
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

import settings
from .pad import FlippablePad
from .objectPicture import ObjectPicture


class GameScreen(QGraphicsView):
    def __init__(self, world, parent=None):
        super().__init__(parent=None)

        # background
        scene = QGraphicsScene(self)
        pix = QPixmap(settings.BACKGROUND_IMAGE)
        scene.setBackgroundBrush(QBrush(pix))
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)

        # field with cells
        self.pad = FlippablePad(world, parent=parent)
        scene.addItem(self.pad)

        # player markers
        self.player = ObjectPicture(scene, self.pad)
        self.pad.cellAt(0, 0).visit()

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

    @property
    def cells(self):
        return self.pad.cells

    def update_screen(self, x, y, value):
        self.player.change_pos(x - self.player.x, y - self.player.y)
        self.pad.cellAt(x, y).set_value(value)

    def keyPressEvent(self, event):
        self.splash.disappear()
        if event.key() == Qt.Key_T:
            self.pad.rotate()
            self.player.pad_rotated()

        if event.key() == Qt.Key_Right and self.player.x < settings.COLS - 1:
            self.player.change_pos(1, 0)
        if event.key() == Qt.Key_Left and self.player.x > 0:
            self.player.change_pos(-1, 0)
        if event.key() == Qt.Key_Down and self.player.y < settings.ROWS - 1:
            self.player.change_pos(0, 1)
        if event.key() == Qt.Key_Up and self.player.y > 0:
            self.player.change_pos(0, -1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)


