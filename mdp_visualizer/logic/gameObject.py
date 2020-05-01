"""
Game Object module
=================

This module contains backend implementations of game objects like Scrat, Hippo and Watermelon.
"""

from random import randint, random

from .actions_objects_list import Actions


class GameObject:
    """A class that implements backend logic of game objects like Scrat, Hippo and Watermelon."""

    def __init__(self, params):
        """A constructor which initializes object parameters.

        Args:
            params: A GameParams object with game parameters.
        """

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
        """X position of the object."""

        return self._x

    @property
    def y(self):
        """Y position of the object."""

        return self._y

    @property
    def cur_position(self):
        """Tuple with current position of the object."""

        return self._x, self._y

    @property
    def prev_position(self):
        """Tuple with previous position of the object."""

        return self._prev_x, self._prev_y

    @property
    def dx_dy(self):
        """Tuple with the last differences in X and Y coordinates."""

        return self._x - self._prev_x, self._y - self._prev_y

    def reset_position(self, params):
        """An abstract method for resetting object params

        Args:
          params: GameParams object with game parameters.
        """

        pass

    def change_position(self, dx, dy):
        """Move the object by dx in x and dy in y.

        Args:
          dx: Difference in x coordinate.
          dy: Difference in y coordinate.
        """

        self._prev_x = self._x
        self._prev_y = self._y
        self._x += dx
        self._y += dy

    def take_random_action(self):
        """Returns a random action number with specified probability."""

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
        """Updates game height, width and lava cells saved parameters of the object.

        Args:
          params: GameParams object with game parameters.
        """

        self._game_height = params.game_height
        self._game_width = params.game_width

        # additional fields
        self._lava_cells = params.lava_cells


class Scrat(GameObject):
    """A class that implements specific Scrat object details."""

    def __init__(self, params):
        """"A constructor. Also saves the fact Scrat is carrying the Watermelon or not."""

        super().__init__(params)

        # base
        self._x = params.scrat_start_position[0]
        self._y = params.scrat_start_position[1]

        # specific properties
        self._carrying_watermelon = False

    def reset_position(self, params):
        """Overrides base class method and resets Scrat position to the position in parameters list.

        Args:
          params: GameParams object with game parameters.
        """

        self._x = params.scrat_start_position[0]
        self._y = params.scrat_start_position[1]
        self._prev_x = -1
        self._prev_y = -1

    def take_watermelon(self):
        """Saves the fact Scrat is carrying the Watermelon now."""

        self._carrying_watermelon = True

    def release_watermelon(self):
        """Saves the fact Scrat is not carrying the Watermelon now."""

        self._carrying_watermelon = False

    @property
    def carrying_watermelon(self):
        """Scrat is carrying the Watermelon or not."""

        return self._carrying_watermelon


class Hippo(GameObject):
    """A class that implements specific Hippo object details."""

    def __init__(self, params):
        """"A constructor. Also saves Hippo move probability and his/her fed state.

        Args:
            params: GameParams object with game parameters.
        """

        super().__init__(params)

        # base
        self._x = params.hippo_start_position[0]
        self._y = params.hippo_start_position[1]
        self._move_prob = params.hippo_move_prob

        # specific properties
        self._is_fed = False

    def reset_position(self, params):
        """Overrides base class method and resets Hippo position to the position in parameters list.

        Args:
          params: GameParams object with game parameters.
        """

        self._x = params.hippo_start_position[0]
        self._y = params.hippo_start_position[1]
        self._prev_x = -1
        self._prev_y = -1

    def become_fed(self):
        """Saves the fact Hippo is fed now."""

        self._is_fed = True

    def become_hungry(self):
        """Saves the fact Hippo is hungry again now."""

        self._is_fed = False

    @property
    def is_fed(self):
        """Hippo is fed or not."""

        return self._is_fed


class Watermelon(GameObject):
    """A class that implements specific Watermelon object details."""

    def __init__(self, params):
        """"A constructor. Also saves Watermelon move probability and its eaten and taken states.

        Args:
            params: GameParams object with game parameters.
        """

        super().__init__(params)

        # base
        self._x = params.watermelon_start_position[0]
        self._y = params.watermelon_start_position[1]
        self._move_prob = params.watermelon_move_prob

        # specific properties
        self._is_taken = False
        self._is_eaten = False

    def reset_position(self, params):
        """Overrides base class method and resets Watermelon position to the position in parameters list.

        Args:
          params: GameParams object with game parameters.
        """

        self._x = params.watermelon_start_position[0]
        self._y = params.watermelon_start_position[1]
        self._prev_x = -1
        self._prev_y = -1

    def become_taken(self):
        """Saves the fact Watermelon is taken now."""

        self._is_taken = True

    def become_released(self):
        """Saves the fact Watermelon is not taken now."""

        self._is_taken = False

    def become_eaten(self):
        """Saves the fact Watermelon is eaten now."""

        self._is_eaten = True

    def become_not_eaten(self):
        """Saves the fact Watermelon is not eaten now."""

        self._is_eaten = False

    @property
    def is_taken(self):
        """Watermelon is taken or not."""

        return self._is_taken

    @property
    def is_eaten(self):
        """Watermelon is eaten or not."""

        return self._is_eaten
