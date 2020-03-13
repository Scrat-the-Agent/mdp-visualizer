from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QLinearGradient, QPalette, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsObject

from settings import MOVE_TIME
from settings import BASE_CELL_OPACITY
from settings import REWARD_COLOR, REWARD_FONT
from utils import animate
from roundRectItem import RoundRectItem

class Cell(RoundRectItem):
    def __init__(self, bounds, color, parent, reward):
        super().__init__(bounds, color, parent)

        self.reward = reward

    def visit(self):
        self.anim = animate(self, "opacity", MOVE_TIME, 1)

    def leave(self):
        self.anim = animate(self, "opacity", MOVE_TIME, BASE_CELL_OPACITY)

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)

        if self.reward != "0":
            textRect = self.boundingRect().adjusted(10, 10, -10, -10)
            flags = int(Qt.AlignCenter) | Qt.TextWordWrap

            painter.setPen(REWARD_COLOR)
            painter.setFont(REWARD_FONT)
            painter.drawText(textRect, flags, self.reward)