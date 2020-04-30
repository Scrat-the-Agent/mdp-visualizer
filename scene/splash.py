from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsObject

from utils import animate
from .roundRectItem import RoundRectItem


class SplashItem(RoundRectItem):
    """ 
    Information box to demonstrate on the screen.
    """
    def __init__(self):
        super().__init__(QRectF(0, 0, 500, 180), QColor(179, 179, 255, 235))

        self.setPos(-250, -90)
        self.setZValue(10)
        self.setOpacity(0)

    def paint(self, painter, option, widget):
        """

        Args:
          painter: param option:
          widget: 
          option: 

        Returns:

        """
        super().paint(painter, option, widget)

        # Text
        font = QFont()
        font.setPixelSize(32)
        painter.setPen(Qt.black)
        painter.setFont(font)
        textRect = self.boundingRect().adjusted(10, 10, -10, -10)
        painter.drawText(textRect, Qt.AlignCenter, self.text)

    def disappear(self):
        """ """
        self.disap = animate(self, 'opacity', 500, 0.0)

        self.move = animate(self, 'y', 500, -190)

    def appear(self, text):
        """ """
        self.text = text
        self.disap = animate(self, 'opacity', 500, 1.0)

        self.setY(-190)
        self.move = animate(self, 'y', 500, -90)
