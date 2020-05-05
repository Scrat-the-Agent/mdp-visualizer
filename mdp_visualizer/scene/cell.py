"""Cell module"""

from PyQt5.QtCore import pyqtSignal, Qt, QPointF, QTimer
from PyQt5.QtGui import QColor, QPixmap

from .. import settings
from ..utils import animate, value_update

from .roundRectItem import RoundRectItem
from ..logic.actions_objects_list import Modes


class Cell(RoundRectItem):
    """
    One cell of game field graphic visualization.
    """
    enter_signal = pyqtSignal()
    leave_signal = pyqtSignal()

    def __init__(self, x, y, pad, logic):
        """
        Args:
            x, y - ints, coordinates of cell
            pad - FlippablePad instance
            logic - GameLogic instance
        """
        self.x, self.y = x, y
        self.logic = logic

        if self.logic.game_mode == Modes.AUTOMATICRL:
            self.value = logic.game_board.cell_reward((self.x, self.y))
            self._timer = QTimer()
            self._timer.timeout.connect(self._update_value)
        else:
            self.value = None
        super().__init__(settings.ICON_RECT, self._compute_color(), parent=pad)

        self.setZValue(1)
        self.setOpacity(settings.BASE_CELL_OPACITY)

        pos = self.posForLocation(x, y)
        self.setPos(pos)

        self.setAcceptHoverEvents(True)

        self.reset_lava()

    def reset_lava(self):
        """
        Redraws lava after mode switch
        """
        if self.logic.game_mode == Modes.IAMRLAGENT:
            if self.logic.game_board.lava_is_here((self.x, self.y)):
                self._color = None
                self.setPixmap(settings.LAVA_IMAGE, True)
            else:
                self._pix = QPixmap()
                self._color = self._compute_color()

            self.update()

    def _compute_color(self):
        if self.value:
            mid = (settings.MIN_REWARD + settings.MAX_REWARD) / 2  # TODO: logic gameboard ref
            if self.value < mid:
                c = (self.value - settings.MIN_REWARD) / (mid - settings.MIN_REWARD)
                color2 = settings.RED_CELL
            else:
                c = (settings.MAX_REWARD - self.value) / (settings.MAX_REWARD - mid)
                color2 = settings.GREEN_CELL
        else:
            c = 1
            color2 = settings.RED_CELL  # not important because c = 1

        return QColor(
            c * settings.YELLOW_CELL.red() + (1 - c) * color2.red(),
            c * settings.YELLOW_CELL.green() + (1 - c) * color2.green(),
            c * settings.YELLOW_CELL.blue() + (1 - c) * color2.blue(),
            c * settings.YELLOW_CELL.alpha() + (1 - c) * color2.alpha()
        )

    def paint(self, painter, option, widget):
        """
        Qt paint event standard definition.
        """
        self._color = self._compute_color()
        super().paint(painter, option, widget)

        if self.value is not None:
            text_rect = self.boundingRect().adjusted(10, 10, -10, -10)
            flags = int(Qt.AlignCenter) | Qt.TextWordWrap

            painter.setPen(settings.REWARD_COLOR)
            painter.setFont(settings.REWARD_FONT)
            painter.drawText(text_rect, flags, f"{self.value:.1f}")

    def hoverEnterEvent(self, event):
        """
        Handler of mouse hover event

        Args:
          event - additional event information
        """
        self.anim = animate(self, "opacity", 100, 1)
        self.enter_signal.emit()

    def hoverLeaveEvent(self, event):
        """
        Handler of mouse leave event

        Args:
          event - additional event information
        """
        self.anim = animate(self, "opacity", 100, settings.BASE_CELL_OPACITY)
        self.leave_signal.emit()

    def set_value(self, new_value: float):
        """
        Starts animation of changing value to new_value

        Args:
          new_value: float
        """
        self._target_value = new_value
        self._timer.start(settings.VALUE_UPDATE_TIME)

    def _update_value(self):
        self.value, stop_timer = value_update(self.value, self._target_value)
        if stop_timer:
            self._timer.stop()

        self.update()

    def posForLocation(self, column: int, row: int):
        """
        Computes coordinates of the cell

        Args:
          column, row - ints

        Returns: QPointF
        """
        width, height = self.logic.game_size
        return QPointF(column * 150, row * 150) - QPointF((width - 1) * 75, (height - 1) * 75)
