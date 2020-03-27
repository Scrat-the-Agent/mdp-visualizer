import pytest
import numpy as np
import gym

from q_learning import q_learning


class TestEnv:
    def __init__(self):
        self.env = gym.make('FrozenLake-v0')

    def step(self, a):
        return self.env.step(a)

    def reset(self):
        return self.env.reset()

    @property
    def n_states(self):
        return self.env.observation_space.n

    @property
    def n_actions(self):
        return self.env.action_space.n


def test_q_learning_frozen_lake():
    env = TestEnv()
    num_episodes = 5000
    Q = None

    r_all = []
    for e in range(num_episodes):
        s = env.reset()
        r, Q = q_learning(env, s, e, n_steps=100, Q=Q, lr=0.8, gamma=0.95)
        r_all.append(r)

    mean_reward = np.mean(r_all)
    assert mean_reward >= 0.5
