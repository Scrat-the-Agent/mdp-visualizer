# QDirIterator
# pyqtSignal
# pyqtProperty

import sys

from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    navigator = MainWindow()
    navigator.show()

    sys.exit(app.exec_())
