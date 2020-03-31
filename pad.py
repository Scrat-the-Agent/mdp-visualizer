from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsRotation

from settings import PAD_COLOR, BASE_CELL_OPACITY
from settings import REDS, MIN_REWARD, GREENS, MAX_REWARD
from settings import ROTATION_TIME, ROTATION_ANGLE
from settings import ROWS, COLS
from utils import animate
from cell import Cell
from roundRectItem import RoundRectItem

class FlippablePad(RoundRectItem):
    def __init__(self, parent):
        super().__init__(self.boundsFromSize(), PAD_COLOR, parent)
        
        iconRect = QRectF(-54, -54, 108, 108)
        self.iconGrid = []

        for y in range(COLS):
            row = []

            for x in range(ROWS):
                if (x, y) in REDS:
                    rect = Cell(x, y, iconRect, self, MIN_REWARD)
                elif (x, y) in GREENS:
                    rect = Cell(x, y, iconRect, self, MAX_REWARD)
                else:
                    rect = Cell(x, y, iconRect, self, 0)

                rect.setZValue(1)
                rect.setOpacity(BASE_CELL_OPACITY)
                rect.setPos(self.posForLocation(x, y))

                row.append(rect)

            self.iconGrid.append(row)

        # rotation
        self.goal_rotation = 0
        self.yRotation = QGraphicsRotation(self)
        self.yRotation.setAxis(Qt.XAxis)
        self.setTransformations([self.yRotation])

    def iconAt(self, column, row):
        return self.iconGrid[row][column]

    @staticmethod
    def boundsFromSize():
        return QRectF((-ROWS / 2.0) * 150,
                (-COLS / 2.0) * 150, ROWS * 150,
                COLS * 150)

    @staticmethod
    def posForLocation(column, row):
        return QPointF(column * 150, row * 150) - QPointF((ROWS - 1) * 75, (COLS - 1) * 75)

    def rotate(self):
        self.goal_rotation = ROTATION_ANGLE if self.goal_rotation == 0 else 0
        self.rot = animate(self.yRotation, 'angle', ROTATION_TIME, self.goal_rotation)