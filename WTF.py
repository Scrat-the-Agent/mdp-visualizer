import numpy as np
import settings

from logic.q_learning import q_learning


class World:
    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._cells = [[0 for x in range(width)] for y in range(height)]
        self._init_rewards()

    def _init_rewards(self):
        for x, y in settings.REDS:
            self._cells[y][x] = settings.MIN_REWARD

        for x, y in settings.GREENS:
            self._cells[y][x] = settings.MAX_REWARD

    def reward_at(self, x, y):
        return self._cells[y][x]

    @property
    def pad_size(self):
        return self._height, self._width


class WorldEnv:
    def __init__(self, world):
        self.world = world
        self._episode_len = None
        self._player_x = None
        self._player_y = None
        self.reset()

    def _reward_at(self, x, y):
        return self.world.reward_at(x, y)

    def xy_to_state(self, x, y):
        _, w = self.world.pad_size
        return w * y + x

    def state_to_xy(self, state):
        _, w = self.world.pad_size
        x = state % w
        y = state // w
        return x, y

    @property
    def _state(self):
        return self.xy_to_state(self._player_x, self._player_y)

    def step(self, action):
        """
        :param action: number from 0 to 3
        0 -- right
        1 -- left
        2 -- down
        3 -- up
        :return:
        """
        if action not in {0, 1, 2, 3}:
            raise ValueError(f"Unknown action: {action}. Possible actions: [0, 1, 2, 3]")

        if action == 0 and self._player_x < settings.COLS - 1:
            self._player_x += 1
        if action == 1 and self._player_x > 0:
            self._player_x -= 1
        if action == 2 and self._player_y < settings.ROWS - 1:
            self._player_y += 1
        if action == 3 and self._player_y > 0:
            self._player_y -= 1

        # if action == 0 and self._player.x < COLS - 1:
        #     self._player.change_pos(1, 0)
        # if action == 1 and self._player.x > 0:
        #     self._player.change_pos(-1, 0)
        # if action == 2 and self._player.y < ROWS - 1:
        #     self._player.change_pos(0, 1)
        # if action == 3 and self._player.y > 0:
        #     self._player.change_pos(0, -1)

        reward = self._reward_at(self._player_x, self._player_y)
        done = self._episode_len >= 100
        return self._state, reward, done, {}

    def reset(self):
        self._player_x = 0
        self._player_y = 0
        # self._player.set_position(0, 0)
        self._episode_len = 0
        return self._state

    @property
    def n_states(self):
        height, width = self.world.pad_size
        return height * width

    @property
    def n_actions(self):
        return 4


class EnvGameInterface:
    def __init__(self, world):
        self._env = WorldEnv(world)
        self._state = self._env.reset()
        self._Q = np.zeros([self._env.n_states, self._env.n_actions])
        self._episode = 0

    def next_step(self):
        params = dict(lr=1.0, gamma=0.95, eps=1 / (self._episode + 1))
        r, self._Q, self._state, done, info = q_learning(self._env, self._state, self._episode, 1, Q=self._Q, **params)
        if done:
            self._episode += 1
            self.reset()
        return r, done, info

    @property
    def player_pos(self):
        return self._env.state_to_xy(self._state)

    def reset(self):
        self._state = self._env.reset()

    def get_Q_values(self, x, y):
        state = self._env.xy_to_state(x, y)
        return self._Q[state]

    def get_value(self, x, y):
        state = self._env.xy_to_state(x, y)
        return max(self._Q[state])
