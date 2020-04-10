from math import cos, sin, pi

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QTransform

import settings
from utils import animate

from .roundRectItem import RoundRectItem
from logic.gameObject import Scrat, Hippo, Watermelon


class ObjectPicture:
    def __init__(self, obj, scene, pad):
        self._obj = obj
        self.pad = pad
        pos = self.pad.cellAt(self.x, self.y).pos()

        # selection underneath the cells!
        self.selection = RoundRectItem(QRectF(-60, -60, 120, 120), settings.SELECTION_COLOR, self.pad)
        self.selection.setZValue(0.5)
        self.selection.setPos(pos)

        # picture!
        self.pic = RoundRectItem(QRectF(-50, -50, 100, 100))
        self.pic.setZValue(self.y)
        self.pic.setPos(pos)
        if isinstance(obj, Scrat):
            self.pic.setPixmap(QPixmap(settings.SCRAT_IMAGE))
        elif isinstance(obj, Hippo):
            self.pic.setPixmap(QPixmap(settings.HIPPO_IMAGE))
        elif isinstance(obj, Watermelon):
            self.pic.setPixmap(QPixmap(settings.WATERMELON_IMAGE))
        scene.addItem(self.pic)

        # for animation
        self.sel_pos = None
        self.pic_pos_x = None
        self.pic_pos_y = None
        self.pic_sc = None

    @property
    def x(self):
        return self._obj.x

    @property
    def y(self):
        return self._obj.y

    @property
    def dx_dy(self):
        return self._obj.dx_dy

    @property
    def cur_position(self):
        return self.x, self.y

    def change_position(self):
        self.pic.setZValue(self.y)
        self.move(settings.MOVE_TIME)

    def move(self, time):
        icon = self.pad.cellAt(self.x, self.y)

        # selection marker is inside the pad, so nothing complex here
        pos = icon.pos()
        self.sel_pos = animate(self.selection, "pos", 300, pos)

        # turning the Scrat picture turned out to be a quest :(
        trans = QTransform()
        trans.translate(pos.x() - self.pad.x(), pos.y() - self.pad.y())
        trans.rotate(-self.pad.goal_rotation, Qt.XAxis)
        trans.translate(self.pad.x() - pos.x(), self.pad.y() - pos.y())

        # rectangle of cell before rotation
        original = icon.boundingRect()
        # rectangle of cell after rotation, projected to screen!
        res = trans.mapRect(original)

        # correct center of cell after rotation
        new_pos_x = -res.x() - res.width() / 2 + pos.x()
        new_pos_y = -res.y() - res.height() / 2 + pos.y()

        # empirical (!) equation for size of marker
        coeff = cos(self.pad.goal_rotation * pi / 180)
        sc = (res.height() / original.height()) ** 0.5 / coeff

        # moving up to give illusion of "staying" on the platform
        new_pos_y += (res.height() - sc * original.height()) / 2

        # animation
        self.pic_pos_x = animate(self.pic, "x", time, new_pos_x)
        self.pic_pos_y = animate(self.pic, "y", time, new_pos_y)
        self.pic_sc = animate(self.pic, "scale", time, sc)

    def pad_rotated(self):
        self.move(settings.ROTATION_TIME)
