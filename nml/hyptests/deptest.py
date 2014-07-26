#!/usr/bin/python

import operator, math
import reg, contab, logmath

def lp(frqs):
    N, k = sum(frqs), len(frqs)
    return contab.lognom(frqs)  - math.log(reg.reg(N,k))

def deptest_ctb(ctb):
    frqsX  = map(sum, ctb)
    frqsY  = map(sum, zip(*ctb))
    frqsXY = reduce(operator.__concat__, ctb, [])
 
    lpX  = lp(frqsX)
    lpY  = lp(frqsY)
    lpXY = lp(frqsXY)
    # print lpXY - lpX
    return logmath.lognorm([lpX+lpY, lpXY])
    
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