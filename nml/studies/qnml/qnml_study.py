#!/usr/bin/env python
# coding: utf-8

from ast import parse
from itertools import product, combinations, permutations
from sympy.utilities.iterables import partitions

def gen_possible_data_vectors(rs):
    return product(*map(range,rs))

def gen_1(partitems, vixset):
    if len(partitems) == 0: 
        yield []
        return
    items = partitems[:]
    (count, mult) = items.pop(0)
    for vs in combinations(vixset, mult):
        vec0 = [(v,count) for v in vs]
        for vec_rest in gen_1(items, vixset - set(vs)):
            yield vec0 + vec_rest
    
def gen_datasets(vectors, N):
    Q = len(vectors)
    vixs = range(Q)
    for partition in partitions(N, m=Q):
        # print(partition)
        partitems = list(partition.items())
        
        counts = sum(([k]*n for k,n in partition.items()), [])
        # print('counts = ', counts)
        K = len(counts)
        for vixset in combinations(vixs, K):
            # print('c',vixset)
            for vec in gen_1(partitems, set(vixset)):
                # print(' ', vec)
                yield(vec)
            # print()


from scipy.special import binom
import numpy as np
from functools import lru_cache
@lru_cache
def mulco(ks): 
    ns = np.cumsum(ks)
    binoms = binom(ns,ks)
    return np.product(binoms)

def mulco_D(D):
    return mulco(tuple(count for _vix,count in D))


def gen_parents(g):
    for n in g:
        yield (n, g.predecessors(n))

def gen_counts(vectors, D, g):
    for (n,ps) in gen_parents(g): # go through nodes and their parents
        pset = frozenset(ps)
        for vix, count in D:      # go through the data
            d = vectors[vix]
            v = d[n]
            pcfg = frozenset((p,d[p]) for p in pset)
            yield ((n,v), pcfg, count)

from collections import defaultdict

def collect_counts(vectors, D, g): # could take N and rs
    N_vps = [defaultdict(lambda:defaultdict(int)) for _n in g]
    for ((n,v), pcfg, c) in gen_counts(vectors, D, g):
        N_vps[n][pcfg][v] += c
    return N_vps

from collections import Counter

def random_data(vectors, N):
    rng = np.random.default_rng()
    rints = rng.integers(low=0, high=len(vectors), size=N)
    return list(Counter(rints).items())                         

import networkx as nx
from scipy.stats import entropy

def log_ml(N_vps):
    res  = 0.0
    for N_vp in N_vps:
        for counts in N_vp.values():
            freqs = np.array(list(counts.values()))
            res -= freqs.sum() * entropy(freqs)
    return res

def gen_log_mls(vectors, N, g):
    for D in gen_datasets(vectors, N):
        N_vps = collect_counts(vectors, D, g)
        yield (log_ml(N_vps), mulco_D(D))

def log_mls_counts(vectors, N, g):
    log_mls = defaultdict(int)
    for lml, c in gen_log_mls(vectors, 4, g):
        log_mls[lml] += c
    return log_mls

from pprint import pprint

def log_nml_denom(vectors, N):
    denom = 0
    for lml,c in gen_log_mls(vectors, N, g):
        denom += np.exp(lml) * c
    return np.log(denom)

from itertools import chain
from nml import lognml
def log_qnml1(freqs, q):    
    freqs0 = [0]*(q-len(freqs)) + freqs
    return lognml(freqs0)

def log_qnml(N_vps, rs, g):
    qs = [int(np.product([rs[p] for p in g.predecessors(n)])) for n in range(len(g))]
    res = 0
    for N_vp, r, q in zip(N_vps, rs, qs):
        freqs_f = list(chain(*(counts.values() for counts in N_vp.values())))
        freqs_p = list(sum(counts.values()) for counts in N_vp.values())
        res += log_qnml1(freqs_f, q*r) 
        res -= log_qnml1(freqs_p,q)
    return res

def get_max_diffs(vectors, g):
    
    def gen_diffs():
        log_denom = log_nml_denom(vectors, N)
        for D in gen_datasets(vectors, N):
            N_vps = collect_counts(vectors, D, g)
            log_nml = log_ml(N_vps) - log_denom
            yield log_qnml(N_vps, rs, g) - log_nml
            
    difflist = np.array(list(gen_diffs()), dtype='float')
    return np.min(difflist), np.max(difflist)


def get_rss(n, max_r):
    rrange = range(2,max_r+1)
    return list(product(rrange, repeat=n))

def get_graph(*nodges):
    g = nx.DiGraph()
    for nodge in nodges:
        if isinstance(nodge, int):
            g.add_node(nodge)
        else:
            g.add_edge(*nodge)
    return g


if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('graph_filename')
    parser.add_argument('max_N', type=int)
    parser.add_argument('max_r', type=int)
    args = parser.parse_args()

    def load_graph(graph_filename):
        g = nx.DiGraph()
        f = open(graph_filename)
        n = int(f.readline())
        g.add_nodes_from(range(n))
        for l in f:
            src, dst = map(int, l.split())
            g.add_edge(src,dst)
        return g

    g = load_graph(args.graph_filename)
    rss = get_rss(g.number_of_nodes(), args.max_r)
    for N, rs in product(range(1,args.max_N+1), rss):
        vectors = list(gen_possible_data_vectors(rs))
        d = get_max_diffs(vectors, g)
        print(N, rs, d)