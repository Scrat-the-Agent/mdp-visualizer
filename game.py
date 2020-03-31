import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget

from settings import BACKGROUND_IMAGE
from splash import SplashItem
from world import World


class Game(QGraphicsView):
    def __init__(self):
        super().__init__(parent=None)

        # background
        scene = QGraphicsScene(self)
        pix = QPixmap(BACKGROUND_IMAGE)
        scene.setBackgroundBrush(QBrush(pix))
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(scene.itemsBoundingRect())
        self.setScene(scene)

        # world
        self.world = World(scene)

        # splash
        self.splash = SplashItem()
        self.splash.setZValue(1)
        self.splash.setPos(-self.splash.boundingRect().width() / 2, scene.sceneRect().top() - 2)
        scene.addItem(self.splash)

        # general
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(50, 50)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        if QGLFormat.hasOpenGL():
            self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))

    def keyPressEvent(self, event):
        self.splash.disappear()
        self.world.keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)


class Interface(QWidget):
    def __init__(self):
        super().__init__()

        # Placeholder for mode switching
        self._label = QLabel()
        self._label.setText("FORTS AND MILLS 2.0")

        self._q_labels = [QLabel() for i in range(4)]
        self._q_layout = QHBoxLayout()
        for _q_label in self._q_labels:
            self._q_layout.addWidget(_q_label)
        self._q_labels_widget = QWidget()
        self._q_labels_widget.setLayout(self._q_layout)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._q_labels_widget)
        # ADD PLAYING WIDGETS
        #self._layout.addWidget(self._?!?)
        self.setLayout(self._layout)

    def cell_entered(self):
        cell = self.sender()
        values = cell.get_q_values()
        
        for i in range(4):
           self._q_labels[i].setText(str(values[i]))

    def cell_left(self):
        for i in range(4):
            self._q_labels[i].setText("")

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._interface = Interface()
        self._game = Game()        

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._interface)
        self._layout.addWidget(self._game)

        self._widget = QWidget()
        self._widget.setLayout(self._layout)
        self.setCentralWidget(self._widget)

        for cell_row in self._game.world.pad.iconGrid:
            for cell in cell_row:
                cell.enter_signal.connect(self._interface.cell_entered)
                cell.leave_signal.connect(self._interface.cell_left)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GameWindow()
    window.show()

    sys.exit(app.exec_())
