from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QLinearGradient, QPalette, QPen, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsObject


# noinspection PyArgumentEqualDefault
class RoundRectItem(QGraphicsObject):
    """ 
    Base class for most graphic objects in our scene
    """
    def __init__(self, bounds, color=None, parent=None):
        """ 
        Args:
            bounds - QRectF, geometry of object
            color - QColor or None
            parent - widget to contain this graphic item or None
        """
        super(RoundRectItem, self).__init__(parent)

        self._fillRect = False
        self._bounds = QRectF(bounds)
        self._pix = QPixmap()
        self._color = color

        self.setCacheMode(QGraphicsItem.ItemCoordinateCache)

    def setFill(self, fill : bool):
        """
        Changes the property of how the cell is filled.

        Args:
          fill: bool
        """
        self._fillRect = fill
        self.update()

    @property
    def _gradient(self):
        gradient = QLinearGradient()
        gradient.setStart((self._bounds.topLeft() + self._bounds.topRight()) / 2)
        gradient.setFinalStop((self._bounds.bottomLeft() + self._bounds.bottomRight()) / 2)
        gradient.setColorAt(0, self._color)
        gradient.setColorAt(1, self._color.darker(200))
        return gradient

    def paint(self, painter, option, widget):
        """Standard Qt paint event."""
        if self._color:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 64))
            painter.drawRoundedRect(self._bounds.translated(2, 2), 25.0, 25.0)

            if self._fillRect:
                painter.setBrush(QApplication.palette().brush(QPalette.Window))
            else:
                painter.setBrush(self._gradient)

            painter.setPen(QPen(Qt.black, 1))
            painter.drawRoundedRect(self._bounds, 25.0, 25.0)

        if not self._pix.isNull():
            if self._rounded_pixmap:
                painter.setRenderHint(QPainter.Antialiasing, True)
                brush = QBrush(self._pix.scaled(self._bounds.width(), self._bounds.height()))
                painter.setBrush(brush)
                painter.drawRoundedRect(self._bounds, 25.0, 25.0)
            else:
                painter.scale(self._bounds.width() / self._pix.width(), self._bounds.height() / self._pix.height())
                painter.drawPixmap(-self._pix.width() / 2, -self._pix.height() / 2, self._pix)

    def boundingRect(self):
        return self._bounds.adjusted(0, 0, 2, 2)

    def setPixmap(self, pixmap_path : str, rounded_pixmap=False):
        """
        Sets new pixmap for this graphic object.

        Args:
          pixmap_path: path to image for pixmap
          rounded_pixmap: make the picture rounded (used, e.g., for lava in the cells)
        """
        self._rounded_pixmap = rounded_pixmap
        self._pix = QPixmap(pixmap_path)
        self.update()
