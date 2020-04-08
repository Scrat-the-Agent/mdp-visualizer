from math import cos, sin, pi
from random import randint

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPixmap, QTransform

from settings import SCRAT_IMAGE
from settings import MOVE_TIME, ROTATION_TIME
from settings import SELECTION_COLOR
from utils import animate
from roundRectItem import RoundRectItem
from actions_objects_list import Actions, Objects


class GameObject:
    def __init__(self, scene, pad):
        self._x = 0
        self._y = 0
        self.pad = pad
        pos = self.pad.cellAt(0, 0).pos()

        # additional fields

        self.cur_speed = (0, 0)
        self.speed_limit = (0, 0)

        # selection underneath the cells!
        self.selection = RoundRectItem(QRectF(-60, -60, 120, 120), SELECTION_COLOR, pad)
        self.selection.setZValue(0.5)
        self.selection.setPos(pos)

        # picture!
        self.picture_path = None

        self.pic = RoundRectItem(QRectF(-50, -50, 100, 100))
        self.pic.setZValue(1.5)
        self.pic.setPos(pos)
        self.pic.setPixmap(QPixmap(SCRAT_IMAGE))
        scene.addItem(self.pic)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def cur_position(self):
        return self._x, self._y

    def set_position(self, x, y):
        self.pad.cellAt(self._x, self._y).leave()

        self._x = x
        self._y = y

        icon = self.pad.cellAt(self._x, self._y).visit()
        pos = self.pad.cellAt(self._x, self._y).pos()
        self.pic.setPos(pos)
        self.selection.setPos(pos)

    def change_position(self, dx, dy):
        self.pad.cellAt(self._x, self._y).leave()

        self._x += dx
        self._y += dy

        icon = self.pad.cellAt(self._x, self._y).visit()
        self.move(MOVE_TIME)

    def move(self, time):
        icon = self.pad.cellAt(self._x, self._y)

        # selection marker is inside the pad, so nothing complex here
        pos = icon.pos()
        self.sel_pos = animate(self.selection, "pos", 300, pos)

        # turning the Scrat picture turned out to be a quest:(
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

        # emperical (!) equation for size of marker
        coeff = cos(self.pad.goal_rotation * pi / 180)
        sc = (res.height() / original.height()) ** 0.5 / coeff

        # moving up to give illusion of "staying" on the platform
        new_pos_y += (res.height() - sc * original.height()) / 2

        # animation
        self.pic_pos_x = animate(self.pic, "x", time, new_pos_x)
        self.pic_pos_y = animate(self.pic, "y", time, new_pos_y)
        self.pic_sc = animate(self.pic, "scale", time, sc)

    def pad_rotated(self):
        self.move(ROTATION_TIME)
        

class GameObject_test:
    def __init__(self, params):
        self._x = 0
        self._y = 0
        self._game_height = params.game_height
        self._game_width = params.game_width

        # self.pad = pad
        # pos = self.pad.cellAt(0, 0).pos()

        # additional fields
        self._step_num = 0
        self._move_cooldown = -1

        # selection underneath the cells!
        # self.selection = RoundRectItem(QRectF(-60, -60, 120, 120), SELECTION_COLOR, pad)
        # self.selection.setZValue(0.5)
        # self.selection.setPos(pos)

        # picture!
        self.picture_path = None

        # self.pic = RoundRectItem(QRectF(-50, -50, 100, 100))
        # self.pic.setZValue(1.5)
        # self.pic.setPos(pos)
        # self.pic.setPixmap(QPixmap(SCRAT_IMAGE))
        # scene.addItem(self.pic)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def cur_position(self):
        return self._x, self._y

    def make_step(self):
        self._step_num += 1
        random_action = None

        if self._move_cooldown > 0 and not (self._step_num % self._move_cooldown):
            action_taken = False
            while not action_taken:
                random_action = randint(0, 3)
                if random_action == 0 and self.x > 0:
                    random_action = Actions.LEFT.value
                    action_taken = True
                elif random_action == 1 and self.y > 0:
                    random_action = Actions.UP.value
                    action_taken = True
                elif random_action == 2 and self.x < self._game_width:
                    random_action = Actions.RIGHT.value
                    action_taken = True
                elif random_action == 3 and self.y < self._game_height:
                    random_action = Actions.DOWN.value
                    action_taken = True

        return random_action

    def set_position(self, x, y):
        pass
    #     self.pad.cellAt(self._x, self._y).leave()
    #
    #     self._x = x
    #     self._y = y
    #
    #     icon = self.pad.cellAt(self._x, self._y).visit()
    #     pos = self.pad.cellAt(self._x, self._y).pos()
    #     self.pic.setPos(pos)
    #     self.selection.setPos(pos)

    def change_position(self, dx, dy):
        # self.pad.cellAt(self._x, self._y).leave()

        self._x += dx
        self._y += dy

        # icon = self.pad.cellAt(self._x, self._y).visit()
        # self.move(MOVE_TIME)

    def move(self, time):
        pass
    #     icon = self.pad.cellAt(self._x, self._y)
    #
    #     # selection marker is inside the pad, so nothing complex here
    #     pos = icon.pos()
    #     self.sel_pos = animate(self.selection, "pos", 300, pos)
    #
    #     # turning the Scrat picture turned out to be a quest:(
    #     trans = QTransform()
    #     trans.translate(pos.x() - self.pad.x(), pos.y() - self.pad.y())
    #     trans.rotate(-self.pad.goal_rotation, Qt.XAxis)
    #     trans.translate(self.pad.x() - pos.x(), self.pad.y() - pos.y())
    #
    #     # rectangle of cell before rotation
    #     original = icon.boundingRect()
    #     # rectangle of cell after rotation, projected to screen!
    #     res = trans.mapRect(original)
    #
    #     # correct center of cell after rotation
    #     new_pos_x = -res.x() - res.width() / 2 + pos.x()
    #     new_pos_y = -res.y() - res.height() / 2 + pos.y()
    #
    #     # emperical (!) equation for size of marker
    #     coeff = cos(self.pad.goal_rotation * pi / 180)
    #     sc = (res.height() / original.height()) ** 0.5 / coeff
    #
    #     # moving up to give illusion of "staying" on the platform
    #     new_pos_y += (res.height() - sc * original.height()) / 2
    #
    #     # animation
    #     self.pic_pos_x = animate(self.pic, "x", time, new_pos_x)
    #     self.pic_pos_y = animate(self.pic, "y", time, new_pos_y)
    #     self.pic_sc = animate(self.pic, "scale", time, sc)

    def pad_rotated(self):
        self.move(ROTATION_TIME)


class Scrat(GameObject_test):
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.scrat_start_position[0]
        self._y = params.scrat_start_position[1]

        # specific properties
        self._carrying_watermelon = False

        # picture
        self.picture_path = SCRAT_IMAGE

    def take_watermelon(self):
        self._carrying_watermelon = True

    def release_watermelon(self):
        self._carrying_watermelon = False

    @property
    def carrying_watermelon(self):
        return self._carrying_watermelon


class Hippo(GameObject_test):
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.hippo_start_position[0]
        self._y = params.hippo_start_position[1]
        self._move_cooldown = params.hippo_move_cooldown

        # specific properties
        self._is_fed = False

        # picture
        self.picture_path = SCRAT_IMAGE  # HIPPO_IMAGE

    def become_fed(self):
        self._is_fed = True

    def become_hungry(self):
        self._is_fed = False

    @property
    def is_fed(self):
        return self._is_fed


class Watermelon(GameObject_test):
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.watermelon_start_position[0]
        self._y = params.watermelon_start_position[1]
        self._move_cooldown = params.watermelon_move_cooldown

        # specific properties
        self._is_taken = False
        self._is_eaten = False

        # picture
        self.picture_path = SCRAT_IMAGE  # WATERMELON_IMAGE

    def become_taken(self):
        self._is_taken = True

    def become_released(self):
        self._is_taken = False

    def become_eaten(self):
        self._is_eaten = True

    @property
    def is_taken(self):
        return self._is_taken
