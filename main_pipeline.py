################################################################################
#
# Main file for running experiments
#
################################################################################

import numpy as np
from scipy import stats
from functools import partial
import random

from edges import *
from feature_generation import *
from generation import *
from evolution import *
from measures import *

def one_attr(p):
    return lambda: (1,) if random.random() < p else (-1,)
def two_attr(p, q):
    def f():
        x = 1 if random.random() < p else -1
        y = 1 if random.random() < q else -1
        return (x, y)
    return f

def main():
    # quick placeholder code for testing
    G = generate(25, two_attr(0.5, 0.3), np.dot, partial(threshold_edge_gen, threshold=0.0))
    n_pos, n_neg = num_pos_neg_edges(G)
    print("Generated graph on 500 nodes with", n_pos, "positive edges and", n_neg, "negative edges")
    print("Evolving network:")
    for t in range(10000):
        evolve_step_LTD(G, 0.5)
        if t % 1000 == 0:
            print("Step {}. Triangle balance: {:.4f}".format(t,
                prop_balanced_triangles(G)))
    print(alliance_compositions(G))

if __name__ == '__main__':
    main()
