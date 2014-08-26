#!/usr/bin/python

from math import log, exp
from itertools import ifilter

def logml(frqs):
    N = sum(frqs)
    if N > 0:
        logN = log(N)
        return sum(frq*(log(frq)-logN) 
                   for frq in ifilter(None, frqs))
    else:
        return 0.0

def ml(frqs):
    return exp(logml(frqs))

if __name__ == '__main__':
    import sys
    print logml(map(int,sys.argv[1:]))
