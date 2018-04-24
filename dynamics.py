import networkx as nx
import numpy as np
import random
from collections import defaultdict
import matplotlib.pyplot as plt

def friends(i, j, feats):
    epsilon = 0.01
    return np.abs(feats[i] - feats[j]) < epsilon#np.sign(feats[i]) == np.sign(feats[j])

N = 50
G = nx.complete_graph(N)
p = 0.5

feats = [0]*N
for i in range(N):
    feats[i] = np.random.normal()

for i in range(N):
    for j in range(i+1, N):
        G[i][j]["weight"] = 1 if random.random() < 0.5 else -1

counts_over_time = []
n_iter = 20000
for i in range(n_iter):
    a = random.randrange(0, N)
    b = random.sample(set(G.neighbors(a)), 1)[0]
    c = random.sample(set(G.neighbors(a)) & set(G.neighbors(b)), 1)[0]
    typ = tuple(sorted((G[a][b]["weight"], G[a][c]["weight"],
        G[b][c]["weight"])))
    triad = set([(a, b), (a, c), (b, c)])
    if typ == (-1, -1, -1):
        u, v = random.sample(triad, 1)[0]
        G[u][v]["weight"] = 1
    elif typ == (-1, 1, 1):
        for u, v in triad:
            if G[u][v]["weight"] == -1:
                enemy_u, enemy_v = u, v
                friends = triad - set((u, v))
        if random.random() < p:
            G[enemy_u][enemy_v]["weight"] = 1
        else:
            u, v = random.sample(friends, 1)[0]
            G[u][v]["weight"] = -1

    if i % 1000 == 0:
        print(i)
        counts = {(-1, -1, -1): 0, (-1, -1, 1): 0, (-1, 1, 1): 0, (1, 1, 1): 0}
        for a in range(N):
            for b in G.neighbors(a):
                for c in set(G.neighbors(a)) & set(G.neighbors(b)):
                    typ = tuple(sorted((G[a][b]["weight"], G[a][c]["weight"],
                        G[b][c]["weight"])))
                    counts[typ] += 1

        counts_over_time.append(counts)

xs = range(len(counts_over_time))
yss = defaultdict(list)
for x in xs:
    for k, v in counts_over_time[x].items():
        yss[k].append(v)

for k, ys in yss.items():
    plt.plot(xs, ys, label="{}/{}/{}".format(*[{-1: "-", 1: "+"}[s] for s in
        k]))
plt.legend()

plt.xlabel("Time")
plt.ylabel("Number of triangles")
plt.title("Triangle balance over time (n={}, p={})".format(N, p))
#plt.show()
plt.savefig("redner.png")
