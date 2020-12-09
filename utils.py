import numpy as np


def solution(lb, ub):
    x = []
    for l, u in zip(lb, ub):
        xi = np.random.uniform(l, u)
        x.append(xi)
    x = np.array(x).reshape(len(x), 1)
    s = np.sum(x)
    if s != 0:
        x = x / s
    else:
        x = solution(lb, ub)
    return x


def population(lb, ub, N):
    P = []
    for _ in range(N):
        P.append(solution(lb, ub))
    return P


def objective(P, f, r, s, c):
    objs = []
    for xi in P:
        M, V = f(xi, r, s, c)
        # TODO: objs.append(np.asarray([M, V])) ?
        objs.append(np.array([M, V]))
    return objs
