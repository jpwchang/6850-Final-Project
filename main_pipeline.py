################################################################################
#
# Main file for running experiments
#
################################################################################

import numpy as np
from scipy import stats
from functools import partial

from edges import *
from feature_generation import *
from generation import *

def main():
    # quick placeholder code for testing
    G = generate(500, random_vector(20, stats.uniform, loc=-0.5, scale=1), np.dot, partial(threshold_edge_gen, threshold=0.5))
    n_pos = 0
    n_neg = 0
    for e in G.edges:
        if G[e[0]][e[1]]["weight"] == 1:
            n_pos += 1
        elif G[e[0]][e[1]]["weight"] == -1:
            n_neg += 1
    print("Generated graph on 500 nodes with", n_pos, "positive edges and", n_neg, "negative edges")

if __name__ == '__main__':
    main()