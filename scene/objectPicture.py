from math import cos, sin, pi

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QTransform

import settings
from utils import animate

from .roundRectItem import RoundRectItem
from logic.gameObject import Scrat, Hippo, Watermelon
from logic.actions_objects_list import Actions


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
        self.pic2 = None
        if isinstance(obj, Scrat):
            self.pic.setPixmap(QPixmap(settings.SCRAT_IMAGE))

            self.pic2 = RoundRectItem(QRectF(-50, -50, 100, 100))
            self.pic2.setOpacity(0)
            self.pic2.setZValue(self.y)
            self.pic2.setPos(pos)
            self.pic2.setPixmap(QPixmap(settings.SCRAT_WITH_WATERMELON_IMAGE))
        elif isinstance(obj, Hippo):
            self.pic.setPixmap(QPixmap(settings.HIPPO_IMAGE))
        elif isinstance(obj, Watermelon):
            self.pic.setPixmap(QPixmap(settings.WATERMELON_IMAGE))
        scene.addItem(self.pic)
        if self.pic2:
            scene.addItem(self.pic2)

        # for animation
        self.sel_pos = None
        self.pic_pos_x = None
        self.pic_pos_y = None
        self.pic_sc = None
        self.pic2_pos_x = None
        self.pic2_pos_y = None
        self.pic2_sc = None

        self.anim = None
        self.anim2 = None

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

    def change_position(self, logic):
        self.pic.setZValue(self.y)
        if self.pic2:
            self.pic2.setZValue(self.y)
        self.move(settings.MOVE_TIME)

        if isinstance(self._obj, Scrat):
            if self._obj.carrying_watermelon and logic.last_action == Actions.TAKE.value:
                self.anim = animate(self.pic, "opacity", 100, 0)
                self.anim2 = animate(self.pic2, "opacity", 100, 1)
            elif self.cur_position == logic.watermelon_position and logic.last_action == Actions.PUT_FEED.value:
                if self.cur_position != logic.hippo_position:
                    self.anim = animate(self.pic, "opacity", 100, 1)
                    self.anim2 = animate(self.pic2, "opacity", 100, 0)
                else:
                    pass
        elif isinstance(self._obj, Hippo):
            pass
        elif isinstance(self._obj, Watermelon):
            if self.cur_position == logic.scrat_position and self.pic.opacity() > 0:
                self.anim = animate(self.pic, "opacity", 100, 0)
            elif self.cur_position != logic.scrat_position and self.pic.opacity() < 1:
                self.anim = animate(self.pic, "opacity", 100, 1)

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
        if self.pic2:
            self.pic2_pos_x = animate(self.pic2, "x", time, new_pos_x)
            self.pic2_pos_y = animate(self.pic2, "y", time, new_pos_y)
            self.pic2_sc = animate(self.pic2, "scale", time, sc)

    def pad_rotated(self):
        self.move(settings.ROTATION_TIME)
