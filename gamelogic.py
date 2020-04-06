class GameCell:
    def __init__(self):
        pass


class GameBoard:
    def __init__(self):
        pass


class GameLogic:
    def __init__(self, game_height, game_width, hippo_start_pos, watermelon_start_pos, hippo_speed_limit,
                 watermelon_speed_limit):
        # main params
        self._game_height = game_height
        self._game_width = game_width
        self._scrat_cur_pos = None
        self._game_board = GameBoard()
        # game type
        self._game_type = dict(hippo_start_pos=hippo_start_pos, watermelon_start_pos=watermelon_start_pos,
                               hippo_speed_limit=hippo_speed_limit, watermelon_speed_limit=watermelon_speed_limit)

        # hippo
        self._hippo_cur_pos = hippo_start_pos
        self._hippo_cur_speed = None

        # watermelon
        self._hippo_cur_pos = hippo_start_pos
        self._hippo_cur_speed = None

        self._n_actions = None

    def _generate_new_game(self):
        pass

    @property
    def game_size(self):
        return self._game_height, self._game_width

    @property
    def game_type(self):
        return self._game_type

    @property
    def n_actions(self):
        return self._n_actions

    def step(self):
        pass

    def reset(self):
        pass

    def get_state(self):
        pass
