from random import shuffle

from .actions_objects_list import Actions, Objects, Modes
from .gameObject import Scrat, Hippo, Watermelon


class GameCell:
    def __init__(self, x, y, params):
        self._x = x
        self._y = y
        self.reward = params["reward"]
        self.is_terminal = params["is_terminal"]
        self.scrat_is_here = params["scrat_is_here"]
        self.hippo_is_here = params["hippo_is_here"]
        self.watermelon_is_here = params["watermelon_is_here"]
        self.lava_is_here = params["lava_is_here"]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class GameBoard:
    def __init__(self, params):
        self._board = []

        for y in range(params.game_height):
            cur_row = []
            for x in range(params.game_width):
                cell_params = dict(scrat_is_here=(params.scrat_start_position == (x, y)),
                                   hippo_is_here=(params.hippo_start_position == (x, y)),
                                   watermelon_is_here=(params.watermelon_start_position == (x, y)),
                                   lava_is_here=((x, y) in params.lava_cells),
                                   is_terminal=((x, y) in params.terminal_cells))
                reward = params.lava_reward if cell_params["lava_is_here"] else 0
                cell_params["reward"] = reward

                cur_row.append(GameCell(x, y, cell_params))
            self._board.append(cur_row)

    def move_object(self, obj, old_position, new_position):
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
        return self._board[position[1]][position[0]].reward

    def is_terminal(self, position):
        return self._board[position[1]][position[0]].is_terminal

    def scrat_is_here(self, position):
        return self._board[position[1]][position[0]].scrat_is_here

    def hippo_is_here(self, position):
        return self._board[position[1]][position[0]].hippo_is_here

    def watermelon_is_here(self, position):
        return self._board[position[1]][position[0]].watermelon_is_here

    def lava_is_here(self, position):
        return self._board[position[1]][position[0]].lava_is_here


class GameParams:
    def __init__(self, game_mode, game_height=5, game_width=5,
                 scrat_random=True, scrat_start_position=None,
                 hippo_random=False, hippo_start_position=None, hippo_move_prob=-1, hippo_fed_reward=100500,
                 watermelon_random=False, watermelon_start_position=None, watermelon_move_prob=-1,
                 lava_random=False, lava_cells=(), lava_reward=-100,
                 terminal_random=False, terminal_cells=()):
        # main
        self.game_mode = game_mode
        self.game_height = game_height
        self.game_width = game_width

        # rewards
        self.hippo_fed_reward = hippo_fed_reward
        self.lava_reward = lava_reward

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
        self.lava_cells = lava_cells

        # terminal
        self.terminal_random = terminal_random
        self.terminal_cells = terminal_cells


class GameLogic:
    def __init__(self, params: GameParams):
        """
        :param params: an instance of class GameParams with game settings
        """
        # params which define game type
        self._start_params = params

        # main params
        self._game_board = None
        self._done = False

        # actions
        self._n_actions = None

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
    def _generate_random_positions(self, num_of_pos=1):
        positions = [(x, y) for y in range(self.game_size[0]) for x in range(self.game_size[1])]
        shuffle(positions)
        return positions[:num_of_pos]

    def _fill_start_params(self, resample=False):
        if (not self._start_params.scrat_start_position or resample) and self._start_params.scrat_random:
            self._start_params.scrat_start_position = self._generate_random_positions()[0]

        if (not self._start_params.hippo_start_position or resample) and self._start_params.hippo_random:
            self._start_params.hippo_start_position = self._generate_random_positions()[0]

        if (not self._start_params.watermelon_start_position or resample) and self._start_params.watermelon_random:
            self._start_params.watermelon_start_position = self._generate_random_positions()[0]

        if (len(self._start_params.lava_cells) == 0 or resample) and self._start_params.lava_random:
            self._start_params.lava_cells = self._generate_random_positions(int(self._start_params.lava_random))

        if (len(self._start_params.terminal_cells) == 0 or resample) and self._start_params.terminal_random:
            self._start_params.terminal_cells = self._generate_random_positions(int(self._start_params.terminal_random))

    def _generate_new_game(self):
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
    def step(self, action):
        """
        :param action: int from 0 to self.n_actions
        """
        assert 0 <= action <= self._n_actions, "Invalid action got into step function"

        # move objects if they are present
        if self._hippo:
            direction = self._hippo.take_random_action()
            if direction:
                self._move_object(Objects.HIPPO, direction)

        if self._watermelon:
            direction = self._watermelon.take_random_action()
            if direction:
                self._move_object(Objects.WATERMELON, direction)

        # make action
        action_reward = 0

        if action == 0 and self.scrat_position[0] > 0:
            self._move_object(Objects.SCRAT, Actions.LEFT.value)
        elif action == 1 and self.scrat_position[1] > 0:
            self._move_object(Objects.SCRAT, Actions.UP.value)
        elif action == 2 and self.scrat_position[0] < self.game_size[0] - 1:
            self._move_object(Objects.SCRAT, Actions.RIGHT.value)
        elif action == 3 and self.scrat_position[1] < self.game_size[1] - 1:
            self._move_object(Objects.SCRAT, Actions.DOWN.value)
        elif action == Actions.TAKE and self.scrat_position == self.watermelon_position:
            self._interact_with_watermelon(Actions.TAKE)
        elif action == Actions.PUT_FEED and self.scrat_carrying_watermelon:
            if self.scrat_position == self.hippo_position:
                self._interact_with_watermelon(Actions.FEED)
                action_reward = self._interact_with_hippo(Actions.FEED)
            else:
                self._interact_with_watermelon(Actions.PUT)

        # change cur game params
        cell_reward = self._game_board.cell_reward(self.scrat_position)
        self._last_reward = cell_reward + action_reward
        self._full_reward += self._last_reward
        self._done = self._game_board.is_terminal(self.scrat_position) or (self._hippo and self.hippo_is_fed)

        state = self.scrat_position[1] * self._start_params.game_width + self.scrat_position[0]
        reward = self._last_reward
        done = self._done
        info = None

        return state, reward, done, info

    def _move_object(self, obj, direction):
        if obj == Objects.SCRAT:
            self._scrat.change_position(*direction)
            self._game_board.move_object(obj, self._scrat.prev_position, self.scrat_position)
        elif obj == Objects.HIPPO:
            self._hippo.change_position(*direction)
            self._game_board.move_object(obj, self._hippo.prev_position, self.hippo_position)
        elif obj == Objects.WATERMELON:
            self._watermelon.change_position(*direction)
            self._game_board.move_object(obj, self._watermelon.prev_position, self.watermelon_position)

    def _interact_with_watermelon(self, action):
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
        assert action == Actions.FEED

        if action == Actions.FEED:
            self._hippo.become_fed()

            return self._start_params.hippo_fed_reward

    # main properties
    @property
    def game_mode(self):
        return self._start_params.game_mode

    @property
    def game_size(self):
        """
        Returns a tuple of width, height
        """
        return self._start_params.game_width, self._start_params.game_height

    @property
    def game_board(self):
        return self._game_board

    @property
    def start_params(self):
        return self._start_params

    @property
    def done(self):
        return self._done

    @property
    def n_actions(self):
        return self._n_actions

    @property
    def n_states(self):
        return self._start_params.game_width * self._start_params.game_height

    @property
    def last_reward(self):
        return self._last_reward

    @property
    def full_reward(self):
        return self._full_reward

    # scrat
    @property
    def scrat(self):
        return self._scrat

    @property
    def scrat_position(self):
        return self._scrat.cur_position

    @property
    def scrat_carrying_watermelon(self):
        return self._scrat.carrying_watermelon

    # hippo
    @property
    def hippo(self):
        return self._hippo

    @property
    def hippo_position(self):
        if self._hippo:
            return self._hippo.cur_position

    @property
    def hippo_is_fed(self):
        if self._hippo:
            return self._hippo.is_fed

    # watermelon
    @property
    def watermelon(self):
        return self._watermelon

    @property
    def watermelon_position(self):
        if self._watermelon:
            return self._watermelon.cur_position

    # lava
    @property
    def lava_cells(self):
        return self._start_params.lava_cells

    # terminal
    @property
    def terminal_cells(self):
        return self._start_params.terminal_cells

    # reset
    def _reset_objects(self):
        # game board
        self._game_board = GameBoard(self._start_params)

        # scrat
        self._scrat.reset_position(self._start_params)

        # hippo
        if self._start_params.hippo_start_position:
            self._hippo.reset_position(self._start_params)

        # watermelon
        if self._start_params.watermelon_start_position:
            self._watermelon.reset_position(self._start_params)

    def reset(self):  # with old start params
        self._fill_start_params()
        self._reset_objects()

    def full_reset(self, params=None):  # with new start params
        self._fill_start_params(resample=True)
        self._reset_objects()