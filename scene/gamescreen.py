from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBrush, QPainter, QColor, QPalette
from PyQt5.QtOpenGL import QGLFormat, QGLWidget, QGL
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

import settings
from .pad import FlippablePad
from .objectPicture import ObjectPicture


class GameScreen(QGraphicsView):
    def __init__(self, logic):
        super().__init__()

        self.logic = logic

        scene = QGraphicsScene(self)
        #TODO: do we need this? scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("background: transparent")

        # field with cells
        self.pad = FlippablePad(self.logic)
        scene.addItem(self.pad)

        # objects markers, in reverse order for equal zValues case
        self.objects_pictures = []
        if self.logic.watermelon:
            self.objects_pictures.append(ObjectPicture(self.logic.watermelon, scene, self.pad))
        if self.logic.hippo:
            self.objects_pictures.append(ObjectPicture(self.logic.hippo, scene, self.pad))
        self.objects_pictures.append(ObjectPicture(self.logic.scrat, scene, self.pad))

        # general
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(50, 50)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

    @property
    def cells(self):
        return self.pad.cells

    def update_screen(self):
        for obj in self.objects_pictures:
            obj.change_position()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_T:
            self.pad.rotate()
            for obj in self.objects_pictures:
                obj.pad_rotated()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
