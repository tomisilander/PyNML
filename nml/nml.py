#!/usr/bin/python

from math import log, exp
from ml import *
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
    print lognml(map(int,sys.argv[1:]))
