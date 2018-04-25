################################################################################
#
# Defines the main routine for generating signed networks from feature vectors,
# along with any and all required helpers
#
################################################################################

import networkx as nx
import itertools

def generate(n_nodes, get_vector, similarity_func, edge_func):
    """
    Generalized algorithm for generating a signed network with n_nodes nodes in
    which each node has an associated feature vector. Edges between nodes are
    produced with probability and sign determined by edge_func.
    Parameters:
    * n_nodes: number of nodes in the network
    * get_vector: callable that returns a feature vector
    * similarity_func: callable that computes the similarity between two vectors
                       Formally, it should be a function that takes two vectors
                       as input and produces a real value as output
    * edge_func: callable that takes as input the similarity between two edges,
                 and produces either 1 (positive edge), 0 (no edge), or -1
                 (negative edge)
    """

    # get a feature vector for each node in the graph. Nodes are indexed by
    # integer value, so the following will act as a map from node to vector.
    node_vecs = [get_vector() for _ in range(n_nodes)]

    # populate a networkX graph object to hold the result
    G = nx.Graph()
    for node in range(n_nodes):
        G.add_node(node)

    # For each pair of nodes, decide whether to draw an edge between them, and
    # what sign the edge should be
    for v1, v2 in itertools.combinations(range(n_nodes), 2):
        # compute similarity between nodes and use this to decide whether to
        # draw an edge
        sim = similarity_func(node_vecs[v1], node_vecs[v2])
        edge_wt = edge_func(sim)
        if edge_wt != 0:
            G.add_edge(v1, v2, weight=edge_wt)

    return G
