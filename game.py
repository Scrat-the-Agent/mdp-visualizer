# QDirIterator
# pyqtSignal
# pyqtProperty

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    app_icon = QIcon()
    app_icon.addFile('./images/nut.png')
    app_icon.addFile('./images/nut64x64.png', QSize(64,64))
    app.setWindowIcon(app_icon)

    mainwindow = MainWindow()
    mainwindow.setWindowIcon(QIcon('./images/nut.png'))
    mainwindow.show()

    sys.exit(app.exec_())
