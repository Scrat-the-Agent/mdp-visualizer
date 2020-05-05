"""
Game Logic module
==================================

This module contains backend logic of the game and GameParams class for setting initial params of the game.

Typical usage example:

    params = GameParams(game_mode)
    logic = GameLogic(params)
"""

from random import shuffle

from .actions_objects_list import Actions, Objects
from .gameObject import Scrat, Hippo, Watermelon


class GameCell:
    """GameCell class represents one cell of a game board.

    Attributes:
        reward: A float indicating the reward in the current cell.
        is_terminal: A boolean indicating if this cell is terminal.
        scrat_is_here: A boolean indicating if Scrat is standing on this cell.
        hippo_is_here: A boolean indicating if Hippo is standing on this cell.
        watermelon_is_here: A boolean indicating if Watermelon is lying on this cell.
        lava_is_here: A boolean indicating if there is lava on this cell.
        is_green: A boolean indicating if this cell is green (positive).
    """

    def __init__(self, x, y, params):
        """Constructs GameCell object.

        Args:
            x: Column.
            y: Row.
            params: A dictionary with keys 'reward', 'is_terminal', 'scrat_is_here', ' hippo_is_here',
                'watermelon_is_here', 'lava_is_here', 'is_green' representing properties of the current cell.
        """

        self._x = x
        self._y = y
        self.reward = params["reward"]
        self.is_terminal = params["is_terminal"]
        self.scrat_is_here = params["scrat_is_here"]
        self.hippo_is_here = params["hippo_is_here"]
        self.watermelon_is_here = params["watermelon_is_here"]
        self.lava_is_here = params["lava_is_here"]
        self.is_green = params["is_green"]

    @property
    def x(self):
        """Returns column."""

        return self._x

    @property
    def y(self):
        """Returns row."""

        return self._y


class GameBoard:
    """Represents the game board which consists of game cells."""

    def __init__(self, params):
        self._board = []

        for y in range(params.game_height):
            cur_row = []
            for x in range(params.game_width):
                cell_params = dict(scrat_is_here=(params.scrat_start_position == (x, y)),
                                   hippo_is_here=(params.hippo_start_position == (x, y)),
                                   watermelon_is_here=(params.watermelon_start_position == (x, y)),
                                   lava_is_here=((x, y) in params.lava_cells),
                                   is_terminal=((x, y) in params.terminal_cells),
                                   is_green=((x, y) in params.green_cells))
                if cell_params["lava_is_here"]:
                    reward = params.lava_reward
                elif cell_params["is_green"]:
                    reward = params.green_reward
                else:
                    reward = 0

                cell_params["reward"] = reward

                cur_row.append(GameCell(x, y, cell_params))
            self._board.append(cur_row)

    def move_object(self, obj, old_position, new_position):
        """Moves an object from the old position to the new position.

        Args:
          obj: A Scrat, Hippo or Watermelon object.
          old_position: A tuple representing the position to move the object from.
          new_position: A tuple representing the position to move the object to.
        """

        if obj == Objects.SCRAT:
            self._board[old_position[1]][old_position[0]].scrat_is_here = False
            self._board[new_position[1]][new_position[0]].scrat_is_here = True
        elif obj == Objects.HIPPO:
            self._board[old_position[1]][old_position[0]].hippo_is_here = False
            self._board[new_position[1]][new_position[0]].hippo_is_here = True
        elif obj == Objects.WATERMELON:
            self._board[old_position[1]][old_position[0]].watermelon_is_here = False
            self._board[new_position[1]][new_position[0]].watermelon_is_here = True

    def cell_reward(self, position):
        """Returns the reward of the cell in specified position.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].reward

    def is_terminal(self, position):
        """Returns True if the cell in specified position is terminal and False otherwise.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].is_terminal

    def is_green(self, position):
        """Returns True if the cell in specified position is green (positive) and False otherwise.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].is_green

    def scrat_is_here(self, position):
        """Returns True if Scrat stands in specified position and False otherwise.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].scrat_is_here

    def hippo_is_here(self, position):
        """Returns True if Hippo stands in specified position and False otherwise.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].hippo_is_here

    def watermelon_is_here(self, position):
        """Returns True if Watermelon lies in specified position and False otherwise.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].watermelon_is_here

    def lava_is_here(self, position):
        """Returns True if the cell in specified position contains lava and False otherwise.

        Args:
          position: A tuple representing position.
        """

        return self._board[position[1]][position[0]].lava_is_here


# pylint: disable=R0902,R0903
class GameParams:
    """Stores game parameters required for game start.

    Attributes:
        game_mode: Game mode.
        game_height: Number of rows of the board.
        game_width: Number of columns of the board.
        scrat_random: Scrat position is generated randomly or not.
        scrat_start_position: A tuple representing Scrat starting position.
        hippo_random: Hippo position is generated randomly or not.
        hippo_start_position: A tuple representing Hippo starting position.
        hippo_move_prob: The probability of Hippo making a step.
        hippo_fed_reward: The reward for feeding the Hippo.
        watermelon_random: Watermelon position is generated randomly or not.
        watermelon_start_position: A tuple representing Watermelon starting position.
        watermelon_move_prob: The probability of Watermelon making a step.
        lava_random: The number of lava cells generated randomly.
        lava_cells: Explicitly specified positions of lava cells (tuple of tuples).
        lava_is_terminal: Lava cells are terminal or not.
        lava_reward: The reward of lava cells.
        terminal_random: The number of terminal cells generated randomly.
        terminal_cells: Explicitly specified terminal cells positions (tuple of tuples).
        green_random: The number of green (positive) cells generated randomly.
        green_cells: Explicitly specified green (positive) cells positions (tuple of tuples).
        green_is_terminal: Green (positive) cells are terminal or not.
        green_reward: The reward of green (positive) cells.
        tick_penalty: The penalty for each tick of time.
    """

    # pylint: disable=R0913,R0914
    def __init__(self, game_mode, game_height=4, game_width=6,
                 scrat_random=True, scrat_start_position=None,
                 hippo_random=False, hippo_start_position=None, hippo_move_prob=-1, hippo_fed_reward=100,
                 watermelon_random=False, watermelon_start_position=None, watermelon_move_prob=-1,
                 lava_random=False, lava_cells=None, lava_is_terminal=True, lava_reward=-10,
                 terminal_random=False, terminal_cells=None,
                 green_random=False, green_cells=None, green_is_terminal=True, green_reward=10,
                 tick_penalty=0):
        """Constructs GameParams object with game parameters."""

        # main
        self.game_mode = game_mode
        self.game_height = game_height
        self.game_width = game_width

        # rewards
        self.hippo_fed_reward = hippo_fed_reward
        self.lava_reward = lava_reward
        self.green_reward = green_reward

        # scrat
        self.scrat_random = scrat_random
        self.scrat_start_position = scrat_start_position

        # hippo
        self.hippo_random = hippo_random
        self.hippo_start_position = hippo_start_position
        self.hippo_move_prob = hippo_move_prob

        # watermelon
        self.watermelon_random = watermelon_random
        self.watermelon_start_position = watermelon_start_position
        self.watermelon_move_prob = watermelon_move_prob

        # lava
        self.lava_random = lava_random
        self.lava_cells = lava_cells or []
        self.lava_is_terminal = lava_is_terminal

        # green
        self.green_random = green_random
        self.green_cells = green_cells or []
        self.green_is_terminal = green_is_terminal

        # terminal
        self.terminal_random = terminal_random
        self.terminal_cells = terminal_cells or []
        self._initial_terminal_cells = self.terminal_cells.copy()

        # penalty
        self.tick_penalty = tick_penalty

    @property
    def initial_terminal_cells(self):
        """Terminal cells of the board which are specified explicitly."""

        return self._initial_terminal_cells


# pylint: disable=R0904
class GameLogic:
    """Represents game logic. It is configured
    via `GameParams` object. Game consists of a board and
    objects on the board which can move.
    """

    def __init__(self, params: GameParams):
        """Constructs GameLogic object.

        Args:
            params (GameParams): An instance of class GameParams with game settings.
        """

        # params which define game type
        self._start_params = params

        # main params
        self._game_board = None
        self._done = False

        # actions
        self._n_actions = None
        self._last_action = None

        # rewards
        self._last_reward = 0
        self._full_reward = 0

        # objects
        self._scrat = None
        self._hippo = None
        self._watermelon = None

        # generate a new game with start params
        self._generate_new_game()

    # generator
    def _generate_random_positions(self, num_of_pos=1, exclude_cells=None):
        """Generate a number of positions on the game board excluding the specified cells.

        Args:
            num_of_pos:  Number of positions to generate. Default: 1.
            exclude_cells:  A tuple of tuples representing positions which shouldn't be generated. Default: None.

        Returns:
            A list of tuples with generated positions.
        """

        exclude_cells = set(exclude_cells or [])
        positions = [(x, y) for y in range(self.game_size[1]) for x in range(self.game_size[0])]
        shuffle(positions)

        out = []
        i = 0
        while len(out) < num_of_pos:
            if positions[i] not in exclude_cells:
                out.append(positions[i])
            i += 1

        return out

    # pylint: disable=R0912
    def _fill_start_params(self, resample=False):
        """Reverts the params to the initial condition with or without resampling before restart ot the game.

        Args:
            resample: Turn on resampling of random values or not. Default: False.
        """

        self._last_action = None
        self._last_reward = 0
        self._full_reward = 0

        # firstly lava cells not to set scrat, hippo and watermelon in lava
        if (len(self._start_params.lava_cells) == 0 or resample) and self._start_params.lava_random:
            self._start_params.lava_cells = self._generate_random_positions(int(self._start_params.lava_random))
            # print(self.lava_cells)

        # secondly green cells
        if (len(self._start_params.green_cells) == 0 or resample) and self._start_params.green_random:
            exclude = self._start_params.lava_cells
            self._start_params.green_cells = self._generate_random_positions(int(self._start_params.green_random),
                                                                             exclude_cells=exclude)

        # thirdly terminal cells not to set scrat or watermelon in terminal cell
        any_terminal_is_random = self._start_params.terminal_random or \
                                 self._start_params.lava_random and self._start_params.lava_is_terminal or \
                                 self._start_params.green_random and self._start_params.green_is_terminal
        if resample and any_terminal_is_random:
            # restore
            self._start_params.terminal_cells = self._start_params.initial_terminal_cells.copy()

        if (len(self._start_params.terminal_cells) == 0 or resample) and self._start_params.terminal_random:
            exclude = []

            # lava is terminal
            if self._start_params.lava_is_terminal:
                num_to_generate = self._start_params.terminal_random - len(self._start_params.lava_cells)
                exclude += self._start_params.lava_cells
            else:
                num_to_generate = self._start_params.terminal_random

            # green is terminal
            if self._start_params.green_is_terminal:
                num_to_generate -= len(self._start_params.green_cells)
                exclude += self._start_params.green_cells

            if num_to_generate > 0:
                self._start_params.terminal_cells = self._generate_random_positions(num_to_generate,
                                                                                    exclude_cells=exclude)
            else:
                self._start_params.terminal_cells = []

        if resample or not self._start_params.terminal_random and (len(self._start_params.terminal_cells) ==
                                                                   len(self._start_params.initial_terminal_cells)):
            if self._start_params.lava_is_terminal:
                self._start_params.terminal_cells += self.lava_cells
            if self._start_params.green_is_terminal:
                self._start_params.terminal_cells += self.green_cells

        # scrat: without lava and terminal cells
        if (not self._start_params.scrat_start_position or resample) and self._start_params.scrat_random:
            exclude = self._start_params.terminal_cells
            self._start_params.scrat_start_position = self._generate_random_positions(exclude_cells=exclude)[0]

        # hippo without lava cells
        if (not self._start_params.hippo_start_position or resample) and self._start_params.hippo_random:
            exclude = self._start_params.lava_cells
            self._start_params.hippo_start_position = self._generate_random_positions(exclude_cells=exclude)[0]

        # watermelon: without lava and terminal cells
        if (not self._start_params.watermelon_start_position or resample) and self._start_params.watermelon_random:
            exclude = self._start_params.lava_cells + self._start_params.terminal_cells
            self._start_params.watermelon_start_position = self._generate_random_positions(exclude_cells=exclude)[0]

    def _generate_new_game(self):
        """Initializes GameLogic inner objects at the start of the game."""

        # fill params
        self._fill_start_params()

        # create objects

        # game board
        self._game_board = GameBoard(self._start_params)

        # scrat
        self._scrat = Scrat(self._start_params)

        # hippo
        if self._start_params.hippo_start_position:
            self._hippo = Hippo(self._start_params)

        # watermelon
        if self._start_params.watermelon_start_position:
            self._watermelon = Watermelon(self._start_params)

        # actions!
        if self._watermelon:
            self._n_actions = 6  # Actions class
        else:
            self._n_actions = 4  # Actions class

    # other
    # pylint: disable=R0912
    def step(self, action):
        """Makes a game step with specified action.

        Args:
            action: int from 0 to self.n_actions.

        Returns:
            A tuple of (state, reward, done, info):

            state: An encoded Scrat position on the board.
            reward: Received reward.
            done: The game is finished or not.
            info: None.
        """

        assert 0 <= action <= self._n_actions, "Invalid action got into step function"

        # save last action
        self._last_action = action

        # save last hippo position
        last_hippo_position = self.hippo_position if self._hippo else None

        # move objects if they are present
        if self._hippo:
            direction = self._hippo.take_random_action()
            if direction:
                self._move_object(Objects.HIPPO, direction)

        if self._watermelon:
            if not (self._watermelon.is_taken or self._watermelon.is_eaten):
                direction = self._watermelon.take_random_action()
                if direction:
                    self._move_object(Objects.WATERMELON, direction)

        # make action
        action_reward = 0

        if action == 0 and self.scrat_position[0] > 0:
            self._move_object(Objects.SCRAT, Actions.LEFT.value)
        if action == 1 and self.scrat_position[1] > 0:
            self._move_object(Objects.SCRAT, Actions.UP.value)
        if action == 2 and self.scrat_position[0] < self.game_size[0] - 1:
            self._move_object(Objects.SCRAT, Actions.RIGHT.value)
        if action == 3 and self.scrat_position[1] < self.game_size[1] - 1:
            self._move_object(Objects.SCRAT, Actions.DOWN.value)
        if action == Actions.TAKE.value and self.scrat_position == self.watermelon_position:
            self._interact_with_watermelon(Actions.TAKE)
        if action == Actions.PUT_FEED.value and self.scrat_carrying_watermelon:
            if self.scrat_position == self.hippo_position and self.scrat_position == last_hippo_position:
                self._interact_with_watermelon(Actions.FEED)
                action_reward = self._interact_with_hippo(Actions.FEED)
            else:
                self._interact_with_watermelon(Actions.PUT)

        # penalty
        tick_penalty = self._start_params.tick_penalty

        # change cur game params
        cell_reward = self._game_board.cell_reward(self.scrat_position)
        self._last_reward = cell_reward + action_reward + tick_penalty
        self._full_reward += self._last_reward
        self._done = self._game_board.is_terminal(self.scrat_position) or (self._hippo and self.hippo_is_fed)

        state = self.scrat_position[1] * self._start_params.game_width + self.scrat_position[0]
        reward = self._last_reward
        done = self._done
        info = None

        return state, reward, done, info

    def _move_object(self, obj, direction):  # with watermelon if it is taken
        """Moves the specified object in specified direction.

        Args:
            obj: Scrat, Hippo or Watermelon object.
            direction: Value of one of LEFT, UP, RIGHT or DOWN actions of Actions class.
        """

        if obj == Objects.SCRAT:
            self._scrat.change_position(*direction)
            self._game_board.move_object(obj, self._scrat.prev_position, self.scrat_position)

            # with watermelon
            if self.scrat_carrying_watermelon:
                self._watermelon.change_position(*direction)
                self._game_board.move_object(self._watermelon, self._watermelon.prev_position, self.watermelon_position)
        elif obj == Objects.HIPPO:
            self._hippo.change_position(*direction)
            self._game_board.move_object(obj, self._hippo.prev_position, self.hippo_position)
        elif obj == Objects.WATERMELON:
            self._watermelon.change_position(*direction)
            self._game_board.move_object(obj, self._watermelon.prev_position, self.watermelon_position)

    def _interact_with_watermelon(self, action):
        """Updates objects' parameters which are connected to the Watermelon.

        Args:
          action: TAKE, PUT or FEED action of Actions class.
        """

        if action == Actions.TAKE:
            self._scrat.take_watermelon()
            self._watermelon.become_taken()
        elif action == Actions.PUT:
            self._scrat.release_watermelon()
            self._watermelon.become_released()
        elif action == Actions.FEED:
            self._scrat.release_watermelon()
            self._watermelon.become_released()
            self._watermelon.become_eaten()

    def _interact_with_hippo(self, action):
        """Updates objects' parameters which are connected to the Hippo.

        Args:
          action: FEED action of Actions class.
        """

        assert action == Actions.FEED

        if action == Actions.FEED:
            self._hippo.become_fed()

            return self._start_params.hippo_fed_reward

        return 0.

    # main properties
    @property
    def game_mode(self):
        """Game mode."""

        return self._start_params.game_mode

    @property
    def game_size(self):
        """A tuple with game size (width, height)."""

        return self._start_params.game_width, self._start_params.game_height

    @property
    def game_board(self):
        """Game board."""

        return self._game_board

    @property
    def start_params(self):
        """Start parameters of the game."""

        return self._start_params

    @property
    def done(self):
        """The game is finished or not."""
        return self._done

    # actions
    @property
    def n_actions(self):
        """Number of game actions."""

        return self._n_actions

    @property
    def last_action(self):
        """Last action made."""

        return self._last_action

    @property
    def n_states(self):
        """Number of game states."""

        return self._start_params.game_width * self._start_params.game_height

    # rewards
    @property
    def last_reward(self):
        """Last received reward."""

        return self._last_reward

    @property
    def full_reward(self):
        """Full received reward."""

        return self._full_reward

    # scrat
    @property
    def scrat(self):
        """Scrat object."""

        return self._scrat

    @property
    def scrat_position(self):
        """Scrat position."""

        return self._scrat.cur_position

    @property
    def scrat_carrying_watermelon(self):
        """Scrat is carrying the Watermelon or not."""

        return self._scrat.carrying_watermelon

    # hippo
    @property
    def hippo(self):
        """Hippo object."""

        return self._hippo

    @property
    def hippo_position(self):
        """Hippo position."""

        if self._hippo:
            return self._hippo.cur_position

        raise RuntimeError("No hippo")

    @property
    def hippo_is_fed(self):
        """Hippo is fed or not."""

        if self._hippo:
            return self._hippo.is_fed

        raise RuntimeError("No hippo")

    # watermelon
    @property
    def watermelon(self):
        """Watermelon object."""

        return self._watermelon

    @property
    def watermelon_position(self):
        """Watermelon position."""

        if self._watermelon:
            return self._watermelon.cur_position

        raise RuntimeError("No watermelon")

    # lava
    @property
    def lava_cells(self):
        """Tuple of lava cells."""

        return self._start_params.lava_cells

    # terminal
    @property
    def terminal_cells(self):
        """Tuple of terminal cells."""

        return self._start_params.terminal_cells

    # green
    @property
    def green_cells(self):
        """Tuple of green (positive) cells."""

        return self._start_params.green_cells

    # reset
    def _reset_objects(self):
        """Reset game logic objects to initial parameters."""

        # game board
        self._game_board = GameBoard(self._start_params)

        # scrat
        self._scrat.reset_position(self._start_params)
        self._scrat.update_params(self._start_params)
        self._scrat.release_watermelon()

        # hippo
        if self._start_params.hippo_start_position:
            self._hippo.reset_position(self._start_params)
            self._hippo.update_params(self._start_params)
            self._hippo.become_hungry()

        # watermelon
        if self._start_params.watermelon_start_position:
            self._watermelon.reset_position(self._start_params)
            self._watermelon.update_params(self._start_params)
            self._watermelon.become_released()
            self._watermelon.become_not_eaten()

    def reset(self):  # without resampling of random values
        """Reset game logic to initial parameters without resampling of random values."""

        self._fill_start_params()
        self._reset_objects()
        x, y = self.scrat_position
        self._done = self._game_board.is_terminal(self.scrat_position) or (self._hippo and self.hippo_is_fed)
        return self._start_params.game_width * y + x

    def full_reset(self):  # with resampling of random values
        """Reset game logic to initial parameters with resampling of random values."""

        self._fill_start_params(resample=True)
        self._reset_objects()
