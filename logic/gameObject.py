from random import randint, random

from .actions_objects_list import Actions


class GameObject:
    """ """
    def __init__(self, params):
        self._x = 0
        self._y = 0
        self._game_height = params.game_height
        self._game_width = params.game_width

        # additional fields
        self._prev_x = -1
        self._prev_y = -1
        self._lava_cells = params.lava_cells

        self._move_prob = 0

    @property
    def x(self):
        """:return:"""
        return self._x

    @property
    def y(self):
        """:return:"""
        return self._y

    @property
    def cur_position(self):
        """:return:"""
        return self._x, self._y

    @property
    def prev_position(self):
        """:return:"""
        return self._prev_x, self._prev_y

    @property
    def dx_dy(self):
        """:return:"""
        return self._x - self._prev_x, self._y - self._prev_y

    def reset_position(self, params):
        """

        Args:
          params: 

        Returns:

        """
        pass

    def change_position(self, dx, dy):
        """

        Args:
          dx: param dy:
          dy: 

        Returns:

        """
        self._prev_x = self._x
        self._prev_y = self._y
        self._x += dx
        self._y += dy

    def take_random_action(self):
        """:return:"""
        random_action = None

        if self._move_prob > 0:
            take_action = random() < self._move_prob
            if take_action:
                action_taken = False
                num_samples = 0
                while not action_taken and num_samples < 4:
                    random_action = randint(0, 3)
                    if random_action == 0 and self.x > 0 and (self.x - 1, self.y) not in self._lava_cells:
                        random_action = Actions.LEFT.value
                        action_taken = True
                    elif random_action == 1 and self.y > 0 and (self.x, self.y - 1) not in self._lava_cells:
                        random_action = Actions.UP.value
                        action_taken = True
                    elif random_action == 2 and self.x < self._game_width - 1 and (
                                                                            self.x + 1, self.y) not in self._lava_cells:
                        random_action = Actions.RIGHT.value
                        action_taken = True
                    elif random_action == 3 and self.y < self._game_height - 1 and (
                                                                            self.x, self.y + 1) not in self._lava_cells:
                        random_action = Actions.DOWN.value
                        action_taken = True

                    num_samples += 1

                if num_samples == 4 and not action_taken:
                    random_action = None

        return random_action

    def update_params(self, params):
        """

        Args:
          params: 

        Returns:

        """
        self._game_height = params.game_height
        self._game_width = params.game_width

        # additional fields
        self._lava_cells = params.lava_cells


class Scrat(GameObject):
    """ """
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.scrat_start_position[0]
        self._y = params.scrat_start_position[1]

        # specific properties
        self._carrying_watermelon = False

    def reset_position(self, params):
        """

        Args:
          params: 

        Returns:

        """
        self._x = params.scrat_start_position[0]
        self._y = params.scrat_start_position[1]
        self._prev_x = -1
        self._prev_y = -1

    def take_watermelon(self):
        """ """
        self._carrying_watermelon = True

    def release_watermelon(self):
        """ """
        self._carrying_watermelon = False

    @property
    def carrying_watermelon(self):
        """:return:"""
        return self._carrying_watermelon


class Hippo(GameObject):
    """ """
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.hippo_start_position[0]
        self._y = params.hippo_start_position[1]
        self._move_prob = params.hippo_move_prob

        # specific properties
        self._is_fed = False

    def reset_position(self, params):
        """

        Args:
          params: 

        Returns:

        """
        self._x = params.hippo_start_position[0]
        self._y = params.hippo_start_position[1]
        self._prev_x = -1
        self._prev_y = -1

    def become_fed(self):
        """ """
        self._is_fed = True

    def become_hungry(self):
        """ """
        self._is_fed = False

    @property
    def is_fed(self):
        """:return:"""
        return self._is_fed


class Watermelon(GameObject):
    """ """
    def __init__(self, params):
        super().__init__(params)

        # base
        self._x = params.watermelon_start_position[0]
        self._y = params.watermelon_start_position[1]
        self._move_prob = params.watermelon_move_prob

        # specific properties
        self._is_taken = False
        self._is_eaten = False

    def reset_position(self, params):
        """

        Args:
          params: 

        Returns:

        """
        self._x = params.watermelon_start_position[0]
        self._y = params.watermelon_start_position[1]
        self._prev_x = -1
        self._prev_y = -1

    def become_taken(self):
        """ """
        self._is_taken = True

    def become_released(self):
        """ """
        self._is_taken = False

    def become_eaten(self):
        """ """
        self._is_eaten = True

    def become_not_eaten(self):
        """ """
        self._is_eaten = False

    @property
    def is_taken(self):
        """:return:"""
        return self._is_taken

    @property
    def is_eaten(self):
        """:return:"""
        return self._is_eaten
