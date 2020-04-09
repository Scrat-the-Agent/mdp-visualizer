from PyQt5.QtCore import QSize, Qt


from settings import COLS, ROWS
# from pad import FlippablePad
# from player import GameObject


        # player markers
        # self.player = GameObject(scene, self.pad)
        # self.pad.cellAt(0, 0).visit()

def keyPressEvent(self, event):
    if event.key() == Qt.Key_T:
        self.pad.rotate()
        self.player.pad_rotated()

    if event.key() == Qt.Key_Right and self.player.x < COLS - 1:
        self.player.change_position(1, 0)
    if event.key() == Qt.Key_Left and self.player.x > 0:
        self.player.change_position(-1, 0)
    if event.key() == Qt.Key_Down and self.player.y < ROWS - 1:
        self.player.change_position(0, 1)
    if event.key() == Qt.Key_Up and self.player.y > 0:
        self.player.change_position(0, -1)