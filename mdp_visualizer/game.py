# QDirIterator
# pyqtSignal
# pyqtProperty

import sys
import ctypes
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFontDatabase

from .gui.mainwindow import MainWindow
from .utils import path

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    app.setApplicationName("Agent Scrat")

    app_icon = QIcon(path('images/nut.png'))
    app.setWindowIcon(app_icon)

    # windows taskbar icon issues
    # solution from https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    if os.name == 'nt':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Agent Scrat')

    # must be done after application initialization
    QFontDatabase.addApplicationFont(path("fonts/Pacifico-Regular.ttf"))

    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())
