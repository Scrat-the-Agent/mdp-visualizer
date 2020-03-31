from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QLinearGradient, QPalette, QPen, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsObject

from settings import MOVE_TIME
from settings import BASE_CELL_OPACITY
from settings import MIN_REWARD, MAX_REWARD, RED_CELL, YELLOW_CELL, GREEN_CELL
from settings import REWARD_COLOR, REWARD_FONT
from utils import animate
from roundRectItem import RoundRectItem

class Cell(RoundRectItem):
    enter_signal = pyqtSignal()
    leave_signal = pyqtSignal()

    def __init__(self, x, y, bounds, parent, value):
        self.value = value
        super().__init__(bounds, self.color(), parent)

        self.setAcceptHoverEvents(True)
        self.x, self.y = x, y

    def color(self):
        mid = (MIN_REWARD + MAX_REWARD) / 2
        if self.value < mid:
            c = (self.value - MIN_REWARD) / (mid - MIN_REWARD)
            color2 = RED_CELL
        else:
            c = (MAX_REWARD - self.value) / (MAX_REWARD - mid) 
            color2 = GREEN_CELL
        
        return QColor(
            c * YELLOW_CELL.red()   + (1 - c) * color2.red(),
            c * YELLOW_CELL.green() + (1 - c) * color2.green(),
            c * YELLOW_CELL.blue()  + (1 - c) * color2.blue(),
            c * YELLOW_CELL.alpha() + (1 - c) * color2.alpha()
        )

    def visit(self):
        pass

    def leave(self):
        pass

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)

        if self.value is not None:
            textRect = self.boundingRect().adjusted(10, 10, -10, -10)
            flags = int(Qt.AlignCenter) | Qt.TextWordWrap

            painter.setPen(REWARD_COLOR)
            painter.setFont(REWARD_FONT)
            painter.drawText(textRect, flags, str(self.value))

    def hoverEnterEvent(self, event):
        self.anim = animate(self, "opacity", 100, 1)
        self.enter_signal.emit()

    def hoverLeaveEvent(self, event):
        self.anim = animate(self, "opacity", 100, BASE_CELL_OPACITY)
        self.leave_signal.emit()

    def get_q_values(self):
        return [self.value]*4