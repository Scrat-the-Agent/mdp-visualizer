from random import randint

from .actions_objects_list import Actions


class GameObject:
    def __init__(self, params):
        self._x = 0
        self._y = 0
        self._game_height = params.game_height
        self._game_width = params.game_width

        # additional fields
        self._prev_x = 0
        self._prev_y = 0

        self._step_num = 0
        self._move_cooldown = -1

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def cur_position(self):
        return self._x, self._y

    @property
    def prev_position(self):
        return self._prev_x, self._prev_y

    @property
    def dx_dy(self):
        return self._x - self._prev_x, self._y - self._prev_y

    def change_position(self, dx, dy):
        self._prev_x = self._x
        self._prev_y = self._y
        self._x += dx
        self._y += dy

    def take_random_action(self):
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
                elif random_action == 2 and self.x < self._game_width - 1:
                    random_action = Actions.RIGHT.value
                    action_taken = True
                elif random_action == 3 and self.y < self._game_height - 1:
                    random_action = Actions.DOWN.value
                    action_taken = True

        return random_action


class Scrat(GameObject):
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.scrat_start_position[0]
        self._y = params.scrat_start_position[1]

        # specific properties
        self._carrying_watermelon = False

    def take_watermelon(self):
        self._carrying_watermelon = True

    def release_watermelon(self):
        self._carrying_watermelon = False

    @property
    def carrying_watermelon(self):
        return self._carrying_watermelon


class Hippo(GameObject):
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.hippo_start_position[0]
        self._y = params.hippo_start_position[1]
        self._move_cooldown = params.hippo_move_cooldown

        # specific properties
        self._is_fed = False

    def become_fed(self):
        self._is_fed = True

    def become_hungry(self):
        self._is_fed = False

    @property
    def is_fed(self):
        return self._is_fed


class Watermelon(GameObject):
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.watermelon_start_position[0]
        self._y = params.watermelon_start_position[1]
        self._move_cooldown = params.watermelon_move_cooldown

        # specific properties
        self._is_taken = False
        self._is_eaten = False

    def become_taken(self):
        self._is_taken = True

    def become_released(self):
        self._is_taken = False

    def become_eaten(self):
        self._is_eaten = True

    @property
    def is_taken(self):
        return self._is_taken
