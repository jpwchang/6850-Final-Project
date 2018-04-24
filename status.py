import numpy as np
import math
import random
import networkx as nx
import matplotlib.pyplot as plt

N = 20
xs, ys = [], []
for p_status in range(1, 11):
    p_status /= 10
    p_lth = 0.2

    order = list(range(N))
    random.shuffle(order)

    balances = []
    balances_b = []
    for it in range(100):
        #print(it)
        G = nx.DiGraph()
        G_b = nx.Graph()
        for i in range(N):
            for j in range(i+1, N):
                if random.random() < p_lth:
                    G.add_edge(i, j, weight=1 if random.random() < p_status else -1)
                else:
                    G.add_edge(j, i, weight=-1 if random.random() < p_status else 1)
        p, n = 0, 0
        for i in range(N):
            for j in range(i+1, N):
                if G.has_edge(i, j):
                    if G[i][j]["weight"] > 0: p += 1
                    n += 1
                if G.has_edge(j, i):
                    if G[j][i]["weight"] > 0: p += 1
                    n += 1
        for i in range(N):
            for j in range(i+1, N):
                G_b.add_edge(i, j, weight=1 if random.random() < p/n else -1)

        counts = {(-1, -1, -1): 0, (-1, -1, 1): 0, (-1, 1, 1): 0, (1, 1, 1): 0}
        G_und = G.to_undirected()
        for a in range(N):
            for b in G_und.neighbors(a):
                for c in set(G_und.neighbors(a)) & set(G_und.neighbors(b)):
                    typ = tuple(sorted((G_und[a][b]["weight"], G_und[a][c]["weight"],
                        G_und[b][c]["weight"])))
                    counts[typ] += 1
        balance = (counts[-1, -1, 1] + counts[1, 1, 1]) / sum(counts.values())
        balances.append(balance)

        counts = {(-1, -1, -1): 0, (-1, -1, 1): 0, (-1, 1, 1): 0, (1, 1, 1): 0}
        G_und = G_b
        for a in range(N):
            for b in G_und.neighbors(a):
                for c in set(G_und.neighbors(a)) & set(G_und.neighbors(b)):
                    typ = tuple(sorted((G_und[a][b]["weight"], G_und[a][c]["weight"],
                        G_und[b][c]["weight"])))
                    counts[typ] += 1
        balance = (counts[-1, -1, 1] + counts[1, 1, 1]) / sum(counts.values())
        balances_b.append(balance)
    print(np.mean(balances) - np.mean(balances_b))
    xs.append(p_status)
    ys.append(np.mean(balances) - np.mean(balances_b))  # NB: should compare z-scores

plt.plot(xs, ys)
plt.xlabel("Degree to which status is respected")
plt.ylabel("Degree to which balance is respected")
plt.title("Balance vs status (q=0.2)")
plt.show()

