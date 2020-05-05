"""Splash module"""

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont

from ..utils import animate
from .roundRectItem import RoundRectItem


class SplashItem(RoundRectItem):
    """Information box to demonstrate on the screen."""

    def __init__(self):
        super().__init__(QRectF(0, 0, 500, 180), QColor(179, 179, 255, 235))

        self.setPos(-250, -90)
        self.setZValue(10)
        self.setOpacity(0)

    def paint(self, painter, option, widget):
        """Standard Qt paint event."""
        super().paint(painter, option, widget)

        # Text
        font = QFont()
        font.setPixelSize(26)
        painter.setPen(Qt.black)
        painter.setFont(font)
        text_rect = self.boundingRect().adjusted(10, 10, -10, -10)
        painter.drawText(text_rect, Qt.AlignCenter, self.text)

    def disappear(self):
        """animates disappearance of this screen"""
        self.disap = animate(self, 'opacity', 500, 0.0)

        self.move = animate(self, 'y', 500, -190)

    def appear(self, text: str):
        """
        Animates appearance of this screen and sets new text

        Args:
            text - str
        """
        self.text = text
        self.update()

        self.disap = animate(self, 'opacity', 500, 1.0)
        self.setY(-190)
        self.move = animate(self, 'y', 500, -90)
