from settings import COLS, ROWS
from q_learning import q_learning


class WorldEnv:
    def __init__(self, world):
        self.world = world
        self._episode_len = None
        self.reset()

    def _value_at(self, x, y):
        return self.world.pad.iconAt(x, y).value

    @property
    def _player(self):
        return self.world.player

    def _xy_to_state(self, x, y):
        _, w = self._pad_size
        return w * y + x

    def _state_to_xy(self, state):
        _, w = self._pad_size
        x = state % w
        y = state // w
        return x, y

    @property
    def _player_pos(self):
        return self._player.x, self._player.y

    @property
    def _state(self):
        return self._xy_to_state(self._player.x, self._player.y)

    @property
    def _pad_size(self):
        height = len(self.world.pad.iconGrid)
        width = len(self.world.pad.iconGrid[0])
        return height, width

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

        if action == 0 and self._player.x < COLS - 1:
            self._player.change_pos(1, 0)
        if action == 1 and self._player.x > 0:
            self._player.change_pos(-1, 0)
        if action == 2 and self._player.y < ROWS - 1:
            self._player.change_pos(0, 1)
        if action == 3 and self._player.y > 0:
            self._player.change_pos(0, -1)

        reward = self._value_at(self._player_pos[0], self._player_pos[1])
        done = self._episode_len >= 100
        return self._state, reward, done, {}

    def reset(self):
        self._player.set_position(0, 0)
        self._episode_len = 0
        return self._state

    @property
    def n_states(self):
        height, width = self._pad_size
        return height * width

    @property
    def n_actions(self):
        return 4


class EnvGameInterface:
    def __init__(self, world):
        self._env = WorldEnv(world)
        self._state = self._env.reset()
        self._Q = None
        self._episode = 0

    def next_step(self):
        r, self._Q, done, info = q_learning(self._env, self._state, self._episode, 1, Q=self._Q, lr=1.0, gamma=0.95)
        if done:
            self._episode += 1
            self.reset()
        return r, done, info

    def reset(self):
        self._state = self._env.reset()

    @property
    def get_Q_table(self):
        return self._Q
