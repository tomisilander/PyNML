#!/usr/bin/python

from math import log, exp
from ml import *
from reg import reg

def lognml(frqs):
    return logml(frqs) - log(reg(sum/frqs),len(frqs)))

def nml(frqs):
    return exp(lognml(frqs))

if __name__ == '__main__':
    import sys
    print lognml(*map(int,sys.argv[1:]))
