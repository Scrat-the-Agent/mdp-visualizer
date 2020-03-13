from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsObject

from utils import animate

class SplashItem(QGraphicsObject):
    def __init__(self, parent=None):
        super(SplashItem, self).__init__(parent)

        self.text = "Press T to rotate field.\nPress arrows to play.\nPress any key to begin."
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self):
        return QRectF(0, 0, 400, 175)

    def paint(self, painter, option, widget):
        # Rectangle
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QColor(245, 245, 255, 220))
        painter.setClipRect(self.boundingRect())
        painter.drawRoundedRect(3, -100 + 3, 400 - 6, 250 - 6, 25.0, 25.0)

        # Text
        font = QFont()
        font.setPixelSize(18)
        painter.setPen(Qt.black)
        painter.setFont(font)
        textRect = self.boundingRect().adjusted(10, 10, -10, -10)
        painter.drawText(textRect, Qt.AlignCenter, self.text)

    def disappear(self):
        self.disap = animate(self, 'opacity', 500, 0.0)
        
        # issues with scene rectangle after that!
        #self.move = animate(self, 'y', 500, self.y() - 100.0)
