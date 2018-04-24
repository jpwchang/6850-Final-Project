import networkx as nx
import numpy as np
import random
from collections import defaultdict
import matplotlib.pyplot as plt
import math

def friends(i, j, feats):
    epsilon = 0.01
    return np.dot(feats[i], feats[j])

N = 100
G = nx.complete_graph(N)
k = 30

feats = np.zeros((N, 2))
for i in range(N):
    feats[i][:] = np.array([random.random(), random.random()])

counts_over_time = []
n_iter = 100
for it in range(n_iter):
    print(it)
    xs, ys = zip(*feats)
    plt.scatter(xs, ys)
    plt.title("Iteration {}".format(it))
    plt.savefig("it-{}".format(it))
    plt.close()

    for i in range(N):
        for j in range(i+1, N):
            G[i][j]["weight"] = 1 if friends(i, j, feats) else -1
    #new_feats = np.array(feats)
    for i in range(N):
        feats[i] = np.mean(list(sorted(feats, key=lambda f: np.linalg.norm(f -
            feats[i])))[:k], axis=0)
    #feats = new_feats

