"""
Object Picture module
=================

This module contains frontend implementations of game objects like Scrat, Hippo and Watermelon which are used on scene.
"""

from math import cos, pi

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QTransform

import settings
from utils import animate

from .roundRectItem import RoundRectItem
from logic.gameObject import Scrat, Hippo, Watermelon


class ObjectPicture:
    """Class ObjectPicture which contains graphical interface for a game object.

    Attributes:
        pad: FlippablePad object, the game pad.
        selection: RoundRectItem object, the selection rectangle under the object.
        pics: A list of pictures specified for the object.
        active_pic: Currently active picture.
        disappearing_pic: A picture which is now disappearing.
    """

    def __init__(self, obj, scene, pad, logic):
        """A constructor that saves object position and game logic and sets object specific pictures.

        Args:
            obj: Scrat, Hippo or Watermelon GameObject.
            scene: QGraphicsScene object.
            pad: FlippablePad object.
            logic: GameLogic object.
        """

        self._obj = obj
        self.pad = pad
        self._logic = logic
        pos = self.pad.cellAt(self.x, self.y).pos()

        # selection underneath the cells!
        self.selection = RoundRectItem(QRectF(-60, -60, 120, 120), settings.SELECTION_COLOR, self.pad)
        self.selection.setZValue(0.5)
        self.selection.setPos(pos)

        # pictures!
        self.pics = []

        pic = RoundRectItem(QRectF(-50, -50, 100, 100))
        pic.setZValue(self.y)
        pic.setPos(pos)
        self.pics.append(pic)

        self.active_pic = self.pics[0]
        self.disappearing_pic = None

        # pic2 = None
        if isinstance(obj, Scrat):
            self.active_pic.setPixmap(QPixmap(settings.SCRAT_IMAGE))

            # 1 -- near watermelon
            pic2 = RoundRectItem(QRectF(-50, -50, 100, 100))
            pic2.setOpacity(0)
            pic2.setZValue(self.y)
            pic2.setPos(pos)
            pic2.setPixmap(QPixmap(settings.SCRAT_AND_WATERMELON_IMAGE))

            # 2 -- with watermelon
            pic3 = RoundRectItem(QRectF(-50, -50, 100, 100))
            pic3.setOpacity(0)
            pic3.setZValue(self.y)
            pic3.setPos(pos)
            pic3.setPixmap(QPixmap(settings.SCRAT_WITH_WATERMELON_IMAGE))

            # 3 -- near hippo without watermelon
            pic4 = RoundRectItem(QRectF(-100, -50, 200, 100))
            pic4.setOpacity(0)
            pic4.setZValue(self.y)
            pic4.setPos(pos)
            pic4.setPixmap(QPixmap(settings.SCRAT_HIPPO_IMAGE))

            # 4 -- near hippo and watermelon
            pic5 = RoundRectItem(QRectF(-100, -50, 200, 100))
            pic5.setOpacity(0)
            pic5.setZValue(self.y)
            pic5.setPos(pos)
            pic5.setPixmap(QPixmap(settings.SCRAT_HIPPO_AND_WATERMELON_IMAGE))

            # 5 -- near hippo carrying watermelon
            pic6 = RoundRectItem(QRectF(-100, -50, 200, 100))
            pic6.setOpacity(0)
            pic6.setZValue(self.y)
            pic6.setPos(pos)
            pic6.setPixmap(QPixmap(settings.SCRAT_WITH_WATERMELON_HIPPO_IMAGE))

            # 6 -- near hippo, hippo is fed
            pic7 = RoundRectItem(QRectF(-100, -50, 200, 100))
            pic7.setOpacity(0)
            pic7.setZValue(self.y)
            pic7.setPos(pos)
            pic7.setPixmap(QPixmap(settings.SCRAT_HIPPO_FED_IMAGE))

            self.pics.append(pic2)
            self.pics.append(pic3)
            self.pics.append(pic4)
            self.pics.append(pic5)
            self.pics.append(pic6)
            self.pics.append(pic7)

            if self.cur_position == self._logic.watermelon_position:  # near watermelon at start
                if self.cur_position == self._logic.hippo_position:
                    if self._logic.hippo_is_fed:
                        self.pics[6].setOpacity(1)  # 6 -- near hippo, hippo is fed
                        self.active_pic.setOpacity(0)
                        self.active_pic = self.pics[6]
                    elif self._logic.scrat_carrying_watermelon:
                        self.pics[5].setOpacity(1)  # 5 -- near hippo carrying watermelon
                        self.active_pic.setOpacity(0)
                        self.active_pic = self.pics[5]
                    else:
                        self.pics[4].setOpacity(1)  # 4 -- near hippo and watermelon
                        self.active_pic.setOpacity(0)
                        self.active_pic = self.pics[4]
                else:
                    self.pics[1].setOpacity(1)  # 1 -- near watermelon
                    self.active_pic.setOpacity(0)
                    self.active_pic = self.pics[1]
            elif self.cur_position == self._logic.hippo_position:  # near hippo at start
                self.pics[3].setOpacity(1)  # 3 -- near hippo without watermelon
                self.active_pic.setOpacity(0)
                self.active_pic = self.pics[3]
        elif isinstance(obj, Hippo):
            self.active_pic.setPixmap(QPixmap(settings.HIPPO_IMAGE))

            # 1 -- near watermelon
            pic2 = RoundRectItem(QRectF(-50, -50, 100, 100))
            pic2.setOpacity(0)
            pic2.setZValue(self.y)
            pic2.setPos(pos)
            pic2.setPixmap(QPixmap(settings.HIPPO_AND_WATERMELON_IMAGE))

            self.pics.append(pic2)  # 0 -- far from watermelon, 1 -- near watermelon

            if self.cur_position == self._logic.scrat_position:
                self.active_pic.setOpacity(0)
            elif self.cur_position == self._logic.watermelon_position:
                self.pics[1].setOpacity(1)  # 1 -- near watermelon
                self.active_pic.setOpacity(0)
                self.active_pic = self.pics[1]
        elif isinstance(obj, Watermelon):
            if self.cur_position == self._logic.scrat_position or self.cur_position == self._logic.hippo_position:
                self.active_pic.setOpacity(0)

            self.active_pic.setPixmap(QPixmap(settings.WATERMELON_IMAGE))

        self._update_neighborhood_params()

        for pic in self.pics:
            scene.addItem(pic)

        # for animation
        self.sel_pos = None
        self.anim_list = []
        self.anim = None
        self.anim2 = None

    @property
    def x(self):
        """X coordinate of the object."""

        return self._obj.x

    @property
    def y(self):
        """Y coordinate of the object."""

        return self._obj.y

    @property
    def dx_dy(self):
        """Tuple with the last differences in X and Y coordinates."""

        return self._obj.dx_dy

    @property
    def cur_position(self):
        """Tuple with current position of the object."""

        return self.x, self.y

    def _update_neighborhood_params(self):
        """Updates the neighborhood properties between the objects of the game."""

        if isinstance(self._obj, Scrat):
            self.is_near_watermelon = self.cur_position == self._logic.watermelon_position
            self.is_near_hippo = self.cur_position == self._logic.hippo_position
        elif isinstance(self._obj, Hippo):
            self.is_near_scrat = self.cur_position == self._logic.scrat_position
            self.is_near_watermelon = self.cur_position == self._logic.watermelon_position
        elif isinstance(self._obj, Watermelon):
            self.is_near_scrat = self.cur_position == self._logic.scrat_position
            self.is_near_hippo = self.cur_position == self._logic.hippo_position

    def _set_active_pic(self, num):
        """Sets another active picture with animation of opacity changing.

        Args:
          num: A number of picture to set.
        """

        self.disappearing_pic = self.active_pic
        self.active_pic = self.pics[num]
        self.anim = animate(self.active_pic, "opacity", 100, 1)
        self.anim2 = animate(self.disappearing_pic, "opacity", 100, 0)

    def change_position(self):
        """Change the position of the object and update the neighborhood properties and active picture if needed."""

        for pic in self.pics:
            pic.setZValue(self.y)

        self.disappearing_pic = None

        self.move(settings.MOVE_TIME)

        # is_near params --- for previous step!!! Update is only made after changing position (see below)

        if isinstance(self._obj, Scrat):
            if self.cur_position == self._logic.hippo_position and self._logic.hippo_is_fed:  # hippo became fed
                self._set_active_pic(6)  # 6 -- near hippo, hippo is fed

            elif not self.is_near_hippo and self.cur_position == self._logic.hippo_position:  # became near hippo
                if not self._obj.carrying_watermelon and self.cur_position != self._logic.watermelon_position:
                    self._set_active_pic(3)  # 3 -- near hippo without watermelon
                elif self._obj.carrying_watermelon:
                    self._set_active_pic(5)  # 5 -- near hippo carrying watermelon
                elif self.cur_position == self._logic.watermelon_position:
                    self._set_active_pic(4)  # 4 -- near hippo and watermelon

            elif self.is_near_hippo and self.cur_position != self._logic.hippo_position:  # became far from hippo
                if self.cur_position != self._logic.watermelon_position:  # became near
                    self._set_active_pic(0)  # 0 -- without watermelon
                elif self._obj.carrying_watermelon:
                    self._set_active_pic(2)  # 2 -- with watermelon
                elif self.cur_position == self._logic.watermelon_position:
                    self._set_active_pic(1)  # 1 -- near watermelon

            elif self.is_near_hippo and self.is_near_watermelon and self.cur_position == self._logic.hippo_position and\
                    self.cur_position != self._logic.watermelon_position:  # stay near hippo but now far from watermelon
                self._set_active_pic(3)  # near hippo without watermelon

            elif self.is_near_hippo and self.cur_position == self._logic.hippo_position:
                # stay near hippo but now near watermelon
                if not self.is_near_watermelon and self.cur_position == self._logic.watermelon_position:
                    self._set_active_pic(4)  # 4 -- near hippo and watermelon
                # take watermelon near hippo
                elif self._obj.carrying_watermelon and self.active_pic is not self.pics[5]:
                    self._set_active_pic(5)  # 5 -- near hippo carrying watermelon

            elif not self.is_near_watermelon and self.cur_position == self._logic.watermelon_position:  # became near
                self._set_active_pic(1)  # 1 -- near watermelon
            elif self.is_near_watermelon and self.cur_position != self._logic.watermelon_position:  # became not near
                self._set_active_pic(0)  # 0 -- without watermelon

            elif self._obj.carrying_watermelon and self.cur_position != self._logic.hippo_position and\
                    self.active_pic is not self.pics[2]:  # took watermelon
                self._set_active_pic(2)  # 2 -- with watermelon
            elif not self._obj.carrying_watermelon and self.cur_position != self._logic.hippo_position and\
                    self.active_pic is self.pics[2]:  # put watermelon
                self._set_active_pic(1)  # 1 -- near watermelon

        elif isinstance(self._obj, Hippo):
            if self.cur_position == self._logic.scrat_position and self.active_pic.opacity() > 0:  # near Scrat
                self.anim = animate(self.active_pic, "opacity", 100, 0)
            elif self.cur_position != self._logic.scrat_position and self.active_pic.opacity() < 1:  # far from Scrat
                if self.cur_position == self._logic.watermelon_position:  # near watermelon
                    self.active_pic = self.pics[1]  # 1 -- near watermelon
                else:
                    self.active_pic = self.pics[0]  # 0 -- without watermelon
                self.anim = animate(self.active_pic, "opacity", 100, 1)

            elif not self.is_near_watermelon and self.cur_position == self._logic.watermelon_position and\
                    self.cur_position != self._logic.scrat_position:  # became near
                self._set_active_pic(1)  # 1 -- near watermelon
            elif self.is_near_watermelon and self.cur_position != self._logic.watermelon_position and\
                    self.cur_position != self._logic.scrat_position:  # became not near
                self._set_active_pic(0)  # 0 -- without watermelon

        elif isinstance(self._obj, Watermelon):
            if self.active_pic.opacity() > 0 and (self.cur_position == self._logic.scrat_position or
                                                  self.cur_position == self._logic.hippo_position):  # near object
                self.anim = animate(self.active_pic, "opacity", 100, 0)
            elif self.active_pic.opacity() < 1 and self.cur_position != self._logic.scrat_position and\
                    self.cur_position != self._logic.hippo_position:  # far from object
                self.anim = animate(self.active_pic, "opacity", 100, 1)

        self._update_neighborhood_params()

    def move(self, time):
        """An utility function for animation of moving the object on the board.

        Args:
          time: Time of animation.
        """

        icon = self.pad.cellAt(self.x, self.y)

        # selection marker is inside the pad, so nothing complex here
        pos = icon.pos()
        self.sel_pos = animate(self.selection, "pos", time, pos)

        # turning the Scrat picture turned out to be a quest :(
        trans = QTransform()        
        trans.translate(pos.x() - self.pad.x(), pos.y() - self.pad.y())
        trans.scale(self.pad.goal_scale, self.pad.goal_scale)
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
        sc = (res.height() / original.height()) ** 0.5 / coeff * self.pad.goal_scale

        # moving up to give illusion of "staying" on the platform
        new_pos_y += (res.height() - sc * original.height()) / 2

        # animation
        for pic in self.pics:
            if pic is self.active_pic:
                self.anim_list.append(animate(self.active_pic, "x", time, new_pos_x))
                self.anim_list.append(animate(self.active_pic, "y", time, new_pos_y))
                self.anim_list.append(animate(self.active_pic, "scale", time, sc))
            elif pic is self.disappearing_pic:
                self.anim_list.append(animate(self.disappearing_pic, "x", time, new_pos_x))
                self.anim_list.append(animate(self.disappearing_pic, "y", time, new_pos_y))
                self.anim_list.append(animate(self.disappearing_pic, "scale", time, sc))
            else:
                self.anim_list.append(animate(pic, "x", time, new_pos_x))
                self.anim_list.append(animate(pic, "y", time, new_pos_y))
                self.anim_list.append(animate(pic, "scale", time, sc))

    def pad_rotated(self):
        """Moves the picture during rotation of the pad."""

        self.move(settings.ROTATION_TIME)
