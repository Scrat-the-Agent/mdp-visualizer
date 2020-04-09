# QDirIterator
# pyqtSignal
# pyqtProperty

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from gui.mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    app.setApplicationName("Agent Scrat")

    app_icon = QIcon('./images/nut.png')
    app.setWindowIcon(app_icon)

    mainwindow = MainWindow()
    mainwindow.setWindowIcon(QIcon('./images/nut.png'))
    mainwindow.show()

    sys.exit(app.exec_())
