#!/usr/bin/env python

from math import log, exp
from ml import logml
from reg import reg

def lognml(frqs):
    return logml(frqs) - log(reg(sum(frqs),len(frqs)))

__log2 = log(2)

def log2nml(frqs):
	return lognml(frqs)/__log2

def nml(frqs):
    return exp(lognml(frqs))

if __name__ == '__main__':
    import sys
    print(lognml([int(arg) for arg in sys.argv[1:]]))
