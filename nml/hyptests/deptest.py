#!/usr/bin/python

import operator, math
from nml import contab
from nml.nml import lognml
import logmath

def lognml_gi(ctb):
    frqsX  = map(sum, ctb)
    frqsY  = map(sum, zip(*ctb))
 
    lpX  = lognml(frqsX)
    lpY  = lognml(frqsY)

    return lpX + lpY

    
def lognml_f(ctb):

    frqsXY = reduce(operator.__concat__, ctb, [])
    lpXY = lognml(frqsXY)

    return lpXY

def nml_gi(ctb):
	return math.exp(lognml_gi(ctb))
	
def nml_f(ctb):
	return math.exp(lognml_f(ctb))

def deptest_ctb(ctb):
    return logmath.lognorm([lognml_gi(ctb), lognml_f(ctb)])
    
def deptest(ctblines):
    return deptest_ctb(contab.get_ctb(ctblines))
        
if __name__ == '__main__':

    import sys, coliche

    def main(ctbfile):
        try:
            ps = deptest(file(ctbfile))
            print " ".join(["%.4f" % p for p in ps])
        except Exception, msg:
            sys.exit("ERROR: "+ str(msg))
            
    coliche.che(main, "ctbfile")
