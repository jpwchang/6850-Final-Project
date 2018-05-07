import networkx as nx
import random

# LTD model of AKR paper
def evolve_step_LTD(G, p):
    N = len(G.nodes())
    a = random.randrange(0, N)
    if len(set(G.neighbors(a))) == 0: return # no change if no suitable triangle
    b = random.sample(set(G.neighbors(a)), 1)[0]
    if len(set(G.neighbors(a)) & set(G.neighbors(b))) == 0: return
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

