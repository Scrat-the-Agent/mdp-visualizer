from player import Scrat, Hippo, Watermelon


class GameCell:
    def __init__(self, x, y, params):
        self._x = x
        self._y = y
        self.scrat_is_here = params.scrat_is_here
        self.hippo_is_here = params.hippo_is_here
        self.watermelon_is_here = params.watermelon_is_here
        self.lava_is_here = params.lava_is_here

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class GameBoard:
    def __init__(self, params):
        self.board = []

        for y in range(params.game_height):
            cur_row = []
            for x in range(params.game_width):
                cell_params = dict(scrat_is_here=(params.scrat_start_position == (x, y)),
                                   hippo_is_here=(params.hippo_start_position == (x, y)),
                                   watermelon_is_here=(params.watermelon_start_position == (x, y)),
                                   lava_is_here=((x, y) in params.lava_cells))

                cur_row.append(GameCell(x, y, cell_params))
            self.board.append(cur_row)


class GameParams:
    def __init__(self, game_height=5, game_width=5,
                 scrat_start_position=(0, 0),
                 hippo_random=False, hippo_start_position=None, hippo_speed_limit=(0, 0),
                 watermelon_random=False, watermelon_start_position=None, watermelon_speed_limit=(0, 0),
                 lava_random=False, lava_cells=None):
        # main
        self.game_height = game_height
        self.game_width = game_width

        # scrat
        self.scrat_start_position = scrat_start_position

        # hippo
        self.hippo_random = hippo_random
        self.hippo_start_position = hippo_start_position
        self.hippo_speed_limit = hippo_speed_limit

        # watermelon
        self.watermelon_random = watermelon_random
        self.watermelon_start_position = watermelon_start_position
        self.watermelon_speed_limit = watermelon_speed_limit

        # lava
        self.lava_random = lava_random
        self.lava_cells = lava_cells


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

        self._scrat = None
        self._hippo = None
        self._watermelon = None

        self._generate_new_game()

    # generator
    def _generate_new_game(self):
        # game board
        self._game_board = GameBoard(self._start_params)

        # scrat
        self._scrat = Scrat(self._start_params)

        # hippo
        self._hippo = Hippo(self._start_params)

        # watermelon
        self._watermelon = Watermelon(self._start_params)

    # main properties
    @property
    def game_size(self):
        return self._start_params.game_height, self._start_params.game_width

    @property
    def start_params(self):
        return self._start_params

    @property
    def done(self):
        return self._done

    @property
    def n_actions(self):
        return self._n_actions

    # scrat
    @property
    def scrat_position(self):
        return self._scrat.cur_position

    # hippo
    @property
    def hippo_position(self):
        return self._hippo.cur_position

    # watermelon
    @property
    def watermelon_position(self):
        return self._watermelon.cur_position

    # other
    def step(self, action):
        """
        :param action: int from 0 to self.n_actions
        """
        pass

    def reset(self):  # with old start params
        self._generate_new_game()

    def full_reset(self, params):  # with new start params
        self._start_params = params
        self._generate_new_game()
