#!/usr/bin/env python

from math import log, exp

def logml(frqs):
    N = sum(frqs)
    if N > 0:
        logN = log(N)
        return sum(frq*(log(frq)-logN) 
                   for frq in filter(None, frqs))
    else:
        return 0.0

def ml(frqs):
    return exp(logml(frqs))

if __name__ == '__main__':
    import sys
    print(logml([int(arg) for arg in sys.argv[1:]]))