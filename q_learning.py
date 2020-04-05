import numpy as np


def q_learning(env, s, e, n_steps, Q=None, lr=0.1, gamma=0.95, eps=0.5):
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
        else:
            a = np.argmax(Q[s, :])
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
