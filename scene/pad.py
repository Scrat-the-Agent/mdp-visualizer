from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsRotation, QGraphicsScale

import settings
from utils import animate

from .cell import Cell
from .roundRectItem import RoundRectItem


class FlippablePad(RoundRectItem):
    """ """
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
        self.goal_scale = 1
        self.scaleTransform = QGraphicsScale(self)
        self.yRotation = QGraphicsRotation(self)
        self.yRotation.setAxis(Qt.XAxis)
        self.setTransformations([self.scaleTransform, self.yRotation])

    def set_cell_value(self, column, row, new_value):
        """

        Args:
          column: param row:
          new_value: 
          row: 

        Returns:

        """
        self.cellAt(column, row).set_value(new_value)

    def cellAt(self, column, row):
        """

        Args:
          column: param row:
          row: 

        Returns:

        """
        return self._cells[row][column]

    @property
    def cells(self):
        """:return:"""
        width, height = self._logic.game_size
        return (self._cells[y][x] for y in range(height) for x in range(width))

    @staticmethod
    def boundsFromSize(logic):
        """

        Args:
          logic: return:

        Returns:

        """
        width, height = logic.game_size
        return QRectF((-width / 2.0) * 150,
                      (-height / 2.0) * 150, width * 150,
                      height * 150)

    def rotate(self):
        """ """
        self.goal_rotation = settings.ROTATION_ANGLE if self.goal_rotation == 0 else 0
        self.rot = animate(self.yRotation, 'angle', settings.ROTATION_TIME, self.goal_rotation)
        
        self.goal_scale = 1 if self.goal_rotation == 0 else settings.SCALE_WHEN_ROTATED
        self.scx = animate(self.scaleTransform, 'xScale', settings.ROTATION_TIME, self.goal_scale)
        self.scy = animate(self.scaleTransform, 'yScale', settings.ROTATION_TIME, self.goal_scale)
        self.scz = animate(self.scaleTransform, 'zScale', settings.ROTATION_TIME, self.goal_scale)
