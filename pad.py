from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsRotation

import settings
from cell import Cell
from roundRectItem import RoundRectItem
from utils import animate


class FlippablePad(RoundRectItem):
    def __init__(self, world, parent):
        super().__init__(self.boundsFromSize(), settings.PAD_COLOR, parent)
        self._world = world
        self._cells = []

        height, width = self._world.pad_size
        for y in range(height):
            row = []

            for x in range(width):
                rect = Cell(x, y, pad=self)
                row.append(rect)

            self._cells.append(row)

        # rotation
        self.goal_rotation = 0
        self.yRotation = QGraphicsRotation(self)
        self.yRotation.setAxis(Qt.XAxis)
        self.setTransformations([self.yRotation])

    def cellAt(self, column, row):
        return self.iconGrid[row][column]

    @property
    def cells(self):
        height, width = self._world.pad_size
        return (self._cells[y][x] for y in range(height) for x in range(width))

    @staticmethod
    def boundsFromSize():
        return QRectF((-settings.COLS / 2.0) * 150,
                      (-settings.ROWS / 2.0) * 150, settings.COLS * 150,
                      settings.ROWS * 150)

    def rotate(self):
        self.goal_rotation = settings.ROTATION_ANGLE if self.goal_rotation == 0 else 0
        self.rot = animate(self.yRotation, 'angle', settings.ROTATION_TIME, self.goal_rotation)