import numpy as np


def q_learning(env, s, e, n_steps, Q=None, lr=0.1, gamma=0.95):
    if Q is None:
        Q = np.zeros([env.n_states, env.n_actions])

    r_all = 0.
    for i in range(n_steps):
        a = np.argmax(Q[s, :] + np.random.randn(1, env.n_actions) / (e + 1))
        s1, r, done, _ = env.step(a)
        Q[s, a] = Q[s, a] + lr * (r + gamma * np.max(Q[s1, :]) - Q[s, a])

        r_all += r
        s = s1

        if done:
            break

    return r_all, Q
