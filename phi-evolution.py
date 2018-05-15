# stats as a function of time for various phi

import numpy as np
from scipy import stats
from functools import partial
import random

from edges import *
from feature_generation import *
from generation import *
from evolution import *
from measures import *

import matplotlib.pyplot as plt

def one_attr(p):
    return lambda: (1,) if random.random() < p else (-1,)
def two_attr(p, q):
    def f():
        x = 1 if random.random() < p else -1
        y = 1 if random.random() < q else -1
        return (x, y)
    return f
def n_types(lst):
    def f():
        c = 0
        r = random.random()
        for i, l in enumerate(lst):
            c += l
            if r < c:
                return (i,)
    return f#lambda: (random.randrange(0, n), )
def types_equal(a, b):
    return 1 if a == b else -1

def noisy_edges(q):
    def f(sim):
        if sim == 0:  # if tie, randomly set edge sign
            return 1 if random.random() < 0.5 else -1
        else:
            return np.sign(sim) if random.random() < q else -np.sign(sim)
    return f

def main():
    G1 = lambda: generate(30, one_attr(0.5), np.dot, noisy_edges(0.75))
    G2 = lambda: generate(30, two_attr(0.5, 0.5), np.dot, noisy_edges(0.75))
    G3 = lambda: generate(30, n_types([0.333, 0.333, 0.334]), types_equal, noisy_edges(0.75))
    for G_gen, name in [(G1, "1-attribute"), (G2, "2-attribute"), (G3, "3-types")]:
        #orig_G = G.copy()
        G = G_gen()

        n_pos, n_neg = num_pos_neg_edges(G)
        print(name)
        print("Generated graph with", n_pos, "positive edges and", n_neg, "negative edges")
        ys_node_resp, ys_gini, ys_tri_bal = [], [], []
        for i, phi in enumerate([0, 0.25, 0.5, 0.75, 1]):
            print(phi)
            #print("Evolving network:")

            xs = []
            y1s, y2s, y3s = [], [], []
            for samp in range(1):
                for t in range(5000 if abs(phi-0.5)>0.01 else 5000):
                    evolve_step_LTD_phi(G, phi, 0.75)
                    if t % 100 == 0:
                        xs.append(t)
                        y1s.append(prop_node_respecting_edges(G))
                #y2s.append(gini_impurity(G))
                #y3s.append(prop_balanced_triangles(G))
                G = G_gen()
            #ys_node_resp.append(np.mean(y1s))
            #ys_gini.append(np.mean(y2s))
            #ys_tri_bal.append(np.mean(y3s))

            plt.xlabel("time step")
            plt.ylabel("fraction of edges that respect node attributes")
            plt.title("{} (phi={:.2f})".format(name, phi))
            plt.plot(xs, y1s)
            plt.savefig("fig/evol-{}-node-resp-{}".format(name, i))
            plt.close()

if __name__ == '__main__':
    main()

