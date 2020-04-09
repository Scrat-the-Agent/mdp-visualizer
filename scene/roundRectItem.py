from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QLinearGradient, QPalette, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsObject

class RoundRectItem(QGraphicsObject):
    def __init__(self, bounds, color=None, parent=None):
        super(RoundRectItem, self).__init__(parent)

        self.fillRect = False
        self.bounds = QRectF(bounds)
        self.pix = QPixmap()
        self.color = color            

        self.setCacheMode(QGraphicsItem.ItemCoordinateCache)

    def setFill(self, fill):
        self.fillRect = fill
        self.update()

    @property
    def gradient(self):
        gradient = QLinearGradient()
        gradient.setStart(self.bounds.topLeft())
        gradient.setFinalStop(self.bounds.bottomRight())
        gradient.setColorAt(0, self.color)
        gradient.setColorAt(1, self.color.darker(200))
        return gradient

    def paint(self, painter, option, widget):
        if self.color:
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