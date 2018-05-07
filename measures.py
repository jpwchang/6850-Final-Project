# stats to test the network on
import networkx as nx
import numpy as np
from collections import Counter

# proportion of balanced triangles in whole network
def prop_balanced_triangles(G):
    counts = {(-1, -1, -1): 0, (-1, -1, 1): 0, (-1, 1, 1): 0, (1, 1, 1): 0}
    for a in range(len(G.nodes())):
        for b in G.neighbors(a):
            for c in set(G.neighbors(a)) & set(G.neighbors(b)):
                typ = tuple(sorted((G[a][b]["weight"], G[a][c]["weight"],
                    G[b][c]["weight"])))
                counts[typ] += 1
    return (counts[1, 1, 1] + counts[-1, -1, 1]) / sum(counts.values())

# proportion of positive/negative edges in network
def num_pos_neg_edges(G):
    n_pos = 0
    n_neg = 0
    for e in G.edges:
        if G[e[0]][e[1]]["weight"] == 1:
            n_pos += 1
        elif G[e[0]][e[1]]["weight"] == -1:
            n_neg += 1
    return n_pos, n_neg

# get connected components (dropping negative edges)
def get_alliances(G):
    Gp = G.copy()
    Gp.remove_edges_from([(u, v) for u, v in G.edges() if G[u][v]["weight"] < 0])
    return nx.connected_components(Gp)

# return sizes of all alliances in graph (including islands if graph isn't
#   fully connected)
def alliance_sizes(G):
    return list(sorted([len(cc) for cc in get_alliances(G)]))

# assuming network is balanced, what's the distribution of node types in each
#   alliance? returns a dict from factions to counters (each counter is from node
#   type to count). may have more than 2 entries if graph isn't fully connected
#   and there are islands
def alliance_compositions(G):
    ccs = list(get_alliances(G))
    print(ccs, len(ccs))
    d = {}
    for cc in ccs:
        d[tuple(cc)] = Counter([G.nodes[c]["latent"] for c in cc])
    return d
