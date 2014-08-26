#!/usr/bin/python

import operator, math
from nml import reg, contab, nml
import logmath

def logfnml_gi(ctb):
    frqsX  = map(sum, ctb)
    frqsY  = map(sum, zip(*ctb))
 
    lpX  = nml.lognml(frqsX)
    lpY  = nml.lognml(frqsY)

    return lpX + lpY

    
def logfnml_f(ctb):
    frqsX  = map(sum, ctb)

    lpX  = nml.lognml(frqsX)
    lpYifX = sum(nml.lognml(ctrow) for ctrow in ctb)

    return lpX + lpYifX

def fnml_gi(ctb):
	return math.exp(logfnml_gi(ctb))
	
def fnml_f(ctb):
	return math.exp(logfnml_f(ctb))


def deptest_ctb(ctb):
    frqsX  = map(sum, ctb)
    frqsY  = map(sum, zip(*ctb))
 
    lpX  = nml.lognml(frqsX)
    lpY  = nml.lognml(frqsY)
    lpYifX = sum(nml.lognml(ctrow) for ctrow in ctb)

    return logmath.lognorm([lpX+lpY, lpYifX+lpX])
    
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
