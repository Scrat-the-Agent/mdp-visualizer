"""
Q-learning module
=================

This module contains Q-learning in two forms:
    1. ``q_learning`` functional interface which is more flexible
    2. ``QLearning`` class interface which encapsulates environment and Q-values
"""

import numpy as np
from .. import settings

__all__ = ('QLearning', 'q_learning')


class QLearning:
    """
    Implements Q-learning. Encapsulates environment and provides
    more convenient interface.
    """

    def __init__(self, env):
        """Constructs QLearning object.

        Args:
            env: Environment to train on.
        """
        self.env = env
        self.Q = np.zeros([self.env.n_states, self.env.n_actions])
        self.state = self.env.reset()

    def reset_q(self, env=None):
        """Resets Q-values and environment if needed.

        Args:
            env: New environment.
        """
        env = env or self.env
        self.Q = np.zeros([env.n_states, env.n_actions])
        self.state = self.env.reset()

    def step(self, lr=0.1, gamma=0.95, eps=0.1):
        """Iterates one step of Q-learning.

        Args:
            lr (float): Learning rate.
            gamma (float): Discount coefficient.
            eps (float): Epsilon from eps-greedy.

        Returns:
            tuple: (cumulative reward, done, info about states, actions and rewards)
        """
        params = dict(lr=lr, gamma=gamma, eps=eps, n_steps=1)
        r_all, self.Q, self.state, done, info = q_learning(self.env, self.state, q_table=self.Q, **params)
        return r_all, done, info

    def reset(self):
        """Resets environment to start new episode."""
        self.state = self.env.reset()

    def get_q_values(self, state=None):
        """Returns all Q-values or for specific state.

        Args:
            state: Optional state to take Q-values from.

        Returns:
            np.array: Q-values for all states or for the given state.
        """
        if state is None:
            return self.Q
        elif isinstance(state, tuple):
            state = self.env.start_params.game_width * state[1] + state[0]
            return self.Q[state]
        else:
            return self.Q[state]

    def get_value(self, state):
        """Computes V function of state `state`.

        Args:
            state: The state, value of which we want to know.

        Returns:
            float: V(`state`)
        """
        return np.max(self.Q[state])


def q_learning(env, s, n_steps, q_table=None, lr=0.1, gamma=0.95, eps=0.5):
    """Implements Q-learning.

    Args:
        env: Environment to train on.
        s: Initial state.
        n_steps (int): Maximum number of steps.
        q_table (np.array): Initial Q-values.
        lr (float): Learning rate.
        gamma (float): Discount coefficient.
        eps (float): Epsilon from eps-greedy.

    Returns:
        tuple: (Cumulative reward, new Q-values, last state, done, info about rewards, actions, states)
    """
    if q_table is None:
        q_table = np.zeros([env.n_states, env.n_actions])

    info = {
        'rewards': [],
        'actions': [],
        'states': [s]
    }

    r_all = 0.
    done = False

    for i in range(n_steps):
        if np.random.rand() < eps:
            a = np.random.choice(env.n_actions)
        else:
            qvalues = q_table[s, :]
            value = max(qvalues)
            a = np.random.choice(np.where(np.abs(qvalues - value) < settings.MAX_FLOAT_DIFF)[0])
        s1, r, done, _ = env.step(a)
        q_table[s, a] = q_table[s, a] + lr * (r + gamma * np.max(q_table[s1, :]) - q_table[s, a])

        info['states'].append(s1)
        info['rewards'].append(r)
        info['actions'].append(a)

        r_all += r
        s = s1

        if done:
            break

    return r_all, q_table, s, done, info
