from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QToolButton, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon


class Button(QToolButton):
    """ """
    def __init__(self, name):
        super().__init__()

        # transparent background
        self.setStyleSheet("QToolButton {border-style: outset; border-width: 0px; margin: 0px; padding: 0px;}")
        self.setAttribute(Qt.WA_TranslucentBackground)

        # picture change
        self.name = name
        self._pressed = False
        self.updatePic()

        self.pressed.connect(self._whenpressed)
        self.released.connect(self._whenreleased)

    # size kludges :/
    def resizeEvent(self, e):
        """

        Args:
          e: 

        Returns:

        """
        super().resizeEvent(e)
        self.setIconSize(self.size())

    def sizeHint(self):
        """:return:"""
        size = super().sizeHint()
        return QSize(size.width(), size.width())

    # changes picture of button
    def _whenpressed(self):
        """ """
        self._pressed = True
        self.updatePic()

    def _whenreleased(self):
        """ """
        self._pressed = False
        self.updatePic()

    def updatePic(self, name=None):
        """

        Args:
          name: Default value = None)

        Returns:

        """
        self.name = name or self.name
        pixmap = QPixmap(self.name + ("pr" if self._pressed else ""))
        self.setIcon(QIcon(pixmap))
