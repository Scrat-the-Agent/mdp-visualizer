from PyQt5.QtCore import pyqtSignal, Qt, QPointF, QTimer
from PyQt5.QtGui import QColor

import settings
from utils import animate

from .roundRectItem import RoundRectItem


class Cell(RoundRectItem):
    enter_signal = pyqtSignal()
    leave_signal = pyqtSignal()

    def __init__(self, x, y, pad, logic):
        self.x, self.y = x, y
        self.pad = pad

        self.value = 0   # TODO: gamelogic ref!
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_value)
        super().__init__(settings.ICON_RECT, self._compute_color(), parent=pad)
        
        self.setZValue(1)
        self.setOpacity(settings.BASE_CELL_OPACITY)

        pos = self.posForLocation(x, y)
        self.setPos(pos)

        self.setAcceptHoverEvents(True)

    def _compute_color(self):
        mid = (settings.MIN_REWARD + settings.MAX_REWARD) / 2
        if self.value < mid:
            c = (self.value - settings.MIN_REWARD) / (mid - settings.MIN_REWARD)
            color2 = settings.RED_CELL
        else:
            c = (settings.MAX_REWARD - self.value) / (settings.MAX_REWARD - mid)
            color2 = settings.GREEN_CELL

        return QColor(
            c * settings.YELLOW_CELL.red() + (1 - c) * color2.red(),
            c * settings.YELLOW_CELL.green() + (1 - c) * color2.green(),
            c * settings.YELLOW_CELL.blue() + (1 - c) * color2.blue(),
            c * settings.YELLOW_CELL.alpha() + (1 - c) * color2.alpha()
        )

    def visit(self):
        pass

    def leave(self):
        pass

    def paint(self, painter, option, widget):
        self.color = self._compute_color()
        super().paint(painter, option, widget)

        if self.value is not None:
            text_rect = self.boundingRect().adjusted(10, 10, -10, -10)
            flags = int(Qt.AlignCenter) | Qt.TextWordWrap

            painter.setPen(settings.REWARD_COLOR)
            painter.setFont(settings.REWARD_FONT)
            painter.drawText(text_rect, flags, f"{self.value:.1f}")

    def hoverEnterEvent(self, event):
        self.anim = animate(self, "opacity", 100, 1)
        self.enter_signal.emit()

    def hoverLeaveEvent(self, event):
        self.anim = animate(self, "opacity", 100, settings.BASE_CELL_OPACITY)
        self.leave_signal.emit()

    def set_value(self, new_value):
        self._target_value = new_value
        self._timer.start(10)  # TODO: settings!

    def _update_value(self):
        diff = abs(self._target_value - self.value)
        step = max(0.1, diff / 20)

        if diff < 0.1:
            self.value = self._target_value
            self._timer.stop()
        elif self._target_value > self.value:
            self.value += 0.1
        else:
            self.value -= 0.1

        self.update()

    @staticmethod
    def posForLocation(column, row):
        return QPointF(column * 150, row * 150) - QPointF((settings.COLS - 1) * 75, (settings.ROWS - 1) * 75)