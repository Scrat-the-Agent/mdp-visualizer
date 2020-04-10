from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsRotation

import settings
from utils import animate

from .cell import Cell
from .roundRectItem import RoundRectItem


class FlippablePad(RoundRectItem):
    def __init__(self, logic):
        super().__init__(self.boundsFromSize(logic), settings.PAD_COLOR)
        self._logic = logic
        self._cells = []

        width, height = self._logic.game_size
        for y in range(height):
            row = []

            for x in range(width):
                rect = Cell(x, y, pad=self, logic=logic)
                row.append(rect)

            self._cells.append(row)

        # rotation
        self.goal_rotation = 0
        self.yRotation = QGraphicsRotation(self)
        self.yRotation.setAxis(Qt.XAxis)
        self.setTransformations([self.yRotation])

    def cellAt(self, column, row):
        return self._cells[row][column]

    @property
    def cells(self):
        width, height = self._logic.game_size
        return (self._cells[y][x] for y in range(height) for x in range(width))

    @staticmethod
    def boundsFromSize(logic):
        width, height = logic.game_size
        return QRectF((-width / 2.0) * 150,
                      (-height / 2.0) * 150, width * 150,
                      height * 150)

    def rotate(self):
        self.goal_rotation = settings.ROTATION_ANGLE if self.goal_rotation == 0 else 0
        self.rot = animate(self.yRotation, 'angle', settings.ROTATION_TIME, self.goal_rotation)
