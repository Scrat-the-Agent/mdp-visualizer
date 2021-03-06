import pytest
import numpy as np
import gym

from mdp_visualizer.logic.q_learning import q_learning, QLearning


class TestEnv:
    """Testing environment for Q-learning
        Internally uses Gym for FrozenLake-v0.
    """

    def __init__(self):
        self.env = gym.make('FrozenLake-v0')

    def step(self, a):
        """Perform given action and update env accordingly

        Args:
            a (int): action to perform

        Returns:
            int: new state
        """
        return self.env.step(a)

    def reset(self):
        """Resets environment

        Returns:
            int: new state
        """
        return self.env.reset()

    @property
    def n_states(self):
        """
        Returns:
            int: number of states in environment
        """
        return self.env.observation_space.n

    @property
    def n_actions(self):
        """
        Returns:
            int: number of actions in environment
        """
        return self.env.action_space.n


def test_q_learning_frozen_lake():
    env = TestEnv()
    num_episodes = 5000
    q_table = None
    min_epsilon, max_epsilon = 0.001, 1.0
    decay_rate = 0.005

    r_all = []
    for e in range(num_episodes):
        s = env.reset()
        eps = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * e)
        # pylint: disable=W0612
        r, q_table, s, done, info = q_learning(env, s, n_steps=100, q_table=q_table, lr=0.3, gamma=0.95, eps=eps)
        r_all.append(r)

    mean_reward = np.mean(r_all)
    assert mean_reward >= 0.45


# pylint: disable=R0914
def test_q_learning_class():
    env = TestEnv()
    qlearning = QLearning(env)

    qlearning.reset()
    q_table = qlearning.get_q_values()
    assert (q_table == 0.).all()

    qlearning.step(lr=0.)

    q_table = qlearning.get_q_values()
    assert (q_table == 0.).all()

    num_episodes = 5000
    min_epsilon, max_epsilon = 0.001, 1.0
    decay_rate = 0.005
    n_steps = 100
    r_all = []

    for e in range(num_episodes):
        qlearning.reset()
        eps = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * e)
        total_r = 0.
        for s in range(n_steps):
            # pylint: disable=W0612
            r, done, info = qlearning.step(lr=0.3, gamma=0.95, eps=eps)
            total_r += r

        r_all.append(total_r)

    mean_reward = np.mean(r_all)
    assert mean_reward >= 0.45
