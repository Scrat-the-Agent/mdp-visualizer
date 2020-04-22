import numpy as np


class QLearning:
    def __init__(self, env):
        self.env = env
        self.Q = np.zeros([env.n_states, env.n_actions])
        self.state = self.env.reset()

    def step(self, lr=0.1, gamma=0.95, eps=0.9):
        params = dict(lr=lr, gamma=gamma, eps=eps, n_steps=1)
        r_all, self.Q, self.state, done, info = q_learning(self.env, self.state, Q=self.Q, **params)
        return r_all, done, info

    def reset(self):
        self.state = self.env.reset()

    def get_q_values(self, state=None):
        if state is None:
            return self.Q
        elif isinstance(state, tuple):
            state = self.env.start_params.game_width * state[1] + state[0]
            return self.Q[state]
        else:
            return self.Q[state]

    def get_value(self, state):
        return np.max(self.Q[state])


def q_learning(env, s, n_steps, Q=None, lr=0.1, gamma=0.95, eps=0.5):
    if Q is None:
        Q = np.zeros([env.n_states, env.n_actions])

    info = {
        'rewards': [],
        'actions': [],
        'states': [s]
    }

    r_all = 0.
    for i in range(n_steps):
        if np.random.rand() < eps:
            a = np.random.choice(env.n_actions)
            print(f"RANDOM: {a}")
        else:
            a = np.argmax(Q[s, :])
            print(s, Q.shape)
            print(f"STRAT: {a}")
        s1, r, done, _ = env.step(a)
        Q[s, a] = Q[s, a] + lr * (r + gamma * np.max(Q[s1, :]) - Q[s, a])

        info['states'].append(s1)
        info['rewards'].append(r)
        info['actions'].append(a)

        r_all += r
        s = s1

        if done:
            break

    return r_all, Q, s, done, info
