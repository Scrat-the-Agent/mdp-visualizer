"""Button module"""

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QPixmap, QIcon


class Button(QToolButton):
    """
    General class for buttons in GUI
    """

    def __init__(self, name: str):
        """
        Args:
            name - picture name
        """
        super().__init__()

        # transparent background
        self.setStyleSheet("QToolButton {border-style: outset; border-width: 0px; margin: 0px; padding: 0px;}")
        self.setAttribute(Qt.WA_TranslucentBackground)

        # picture change
        self._name = name
        self._pressed = False
        self.updatePic()

        self.pressed.connect(self._whenpressed)
        self.released.connect(self._whenreleased)

    # size kludges :/
    def resizeEvent(self, e):
        """Internal Qt method to processes resizing of this widget"""
        super().resizeEvent(e)
        self.setIconSize(self.size())

    def sizeHint(self):
        """
        Internal Qt method to imply this widget must be always a square

        returns: QSize
        """
        size = super().sizeHint()
        return QSize(size.width(), size.width())

    def _whenpressed(self):
        self._pressed = True
        self.updatePic()

    def _whenreleased(self):
        self._pressed = False
        self.updatePic()

    def updatePic(self, name=None):
        """
        Updates picture of this button.

        Args:
          name: new picture name or None (Default value = None)
        """
        self._name = name or self._name
        pixmap = QPixmap(self._name + ("pr" if self._pressed else ""))
        self.setIcon(QIcon(pixmap))
