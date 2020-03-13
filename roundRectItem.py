from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QLinearGradient, QPalette, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsObject

class RoundRectItem(QGraphicsObject):
    def __init__(self, bounds, color=None, parent=None):
        super(RoundRectItem, self).__init__(parent)

        self.fillRect = False
        self.bounds = QRectF(bounds)
        self.pix = QPixmap()

        if color is None: self.gradient = None
        else:
            self.gradient = QLinearGradient()
            self.gradient.setStart(self.bounds.topLeft())
            self.gradient.setFinalStop(self.bounds.bottomRight())
            self.gradient.setColorAt(0, color)
            self.gradient.setColorAt(1, color.darker(200))

        self.setCacheMode(QGraphicsItem.ItemCoordinateCache)

    def setFill(self, fill):
        self.fillRect = fill
        self.update()

    def paint(self, painter, option, widget):
        if self.gradient:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 64))
            painter.drawRoundedRect(self.bounds.translated(2, 2), 25.0, 25.0)

            if self.fillRect:
                painter.setBrush(QApplication.palette().brush(QPalette.Window))
            else:
                painter.setBrush(self.gradient)

            painter.setPen(QPen(Qt.black, 1))
            painter.drawRoundedRect(self.bounds, 25.0, 25.0)

        if not self.pix.isNull():
            painter.scale(self.bounds.width() / self.pix.width(), self.bounds.height() / self.pix.height())
            painter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)

    def boundingRect(self):
        return self.bounds.adjusted(0, 0, 2, 2)

    def pixmap(self):
        return QPixmap(self.pix)

    def setPixmap(self, pixmap):
        self.pix = QPixmap(pixmap)
        self.update()