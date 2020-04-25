from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from .pad import FlippablePad
from .objectPicture import ObjectPicture


class GameScreen(QGraphicsView):
    def _init_with_logic(self, logic):
        self.logic = logic

        scene = QGraphicsScene(self)
        # TODO: do we need this? scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("background: transparent")

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
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        # # rotate if mode was switched
        # if self.rotated:
        #     self._make_rotated()

    def __init__(self):
        super().__init__()

        # # the fact the pad was rotated to pseudo-3d
        # self.rotated = False

    @property
    def cells(self):
        return self.pad.cells

    def set_cell_value(self, column, row, value):
        self.pad.set_cell_value(column, row, value)

    def change_logic(self, logic):
        self._init_with_logic(logic)

    def update_screen(self):
        # cells
        for cell in self.cells:
            cell.reset_lava()

        # objects
        for obj in self.objects_pictures:
            obj.change_position()

        self.setFocus()

    def _make_rotated(self):
        self.pad.rotate()
        for obj in self.objects_pictures:
            obj.pad_rotated()

    def keyPressEvent(self, event):
        if event.nativeVirtualKey() == Qt.Key_T:
            self._make_rotated()
            # self.rotated = not self.rotated

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
