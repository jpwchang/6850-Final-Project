# stats to test the network on
import networkx as nx
import numpy as np
from collections import Counter
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

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

def bisect(G):
    Gp = G.copy()
    Gp.remove_edges_from([(u, v) for u, v in G.edges() if G[u][v]["weight"] < 0])
    partition = kernighan_lin_bisection(Gp)
    return partition

# return sizes of all alliances in graph (including islands if graph isn't
#   fully connected)
def alliance_sizes(G):
    return list(sorted([len(cc) for cc in get_alliances(G)]))

# assuming network is balanced, what's the distribution of node types in each
#   alliance? returns a dict from factions to counters (each counter is from node
#   type to count). may have more than 2 entries if graph isn't fully connected
#   and there are islands
def alliance_compositions(G):
    ccs = list(bisect(G))
    print(ccs, len(ccs))
    d = {}
    for cc in ccs:
        d[tuple(cc)] = Counter([G.nodes[c]["latent"] for c in cc])
    return d

# what fraction of edges have signs respecting the underlying node attribs?
def prop_node_respecting_edges(G):
    n, t = 0, 0
    for u, v in G.edges():
        w = G[u][v]["weight"]
        ul, vl = G.nodes[u]["latent"], G.nodes[v]["latent"]
        sim = G[u][v]["sim"]#sim_func(ul, vl)
        if sim != 0:
            n += int(w == np.sign(sim))
        #n += int((w > 0) == (ul[0] == vl[0]))
        t += 1
    return n / len(G.edges())

def gini_impurity(G):
    parts = bisect(G)
    g = 0
    for part in parts:
        composition = Counter([G.nodes[c]["latent"] for c in part])
        l = 0
        for k, v in composition.items():
            p = v / sum(composition.values())
            l += p*(1-p)
        g += len(part)/len(G.nodes()) * l
    return g
