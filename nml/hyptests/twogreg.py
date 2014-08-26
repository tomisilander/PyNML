#!/usr/bin/python

import math
from nml import reg,  regtab, contab, ml
import logmath

def xlogbinoms(n, logs):
    lb = 0.0
    yield lb
    
    for k in xrange(1,n):
        lb += logs[n-k+1] - logs[k]
        yield lb
    yield 0.0
    
def R_eq(ctb):

    n1, n2 = map(sum, ctb)
    N      = n1 + n2
    logs   = list(regtab.xlogs(N+1))
    lbs_n1 = list(xlogbinoms(n1, logs))
    lbs_n2 = list(xlogbinoms(n2, logs))

    r = 0

    logN = logs[N]
    for f10 in xrange(n1+1):
        lbs_n1_f10 = lbs_n1[f10]
        for f20 in xrange(n2+1):
            m0 = f10 + f20
            m1 = N - m0
            if m0 == 0 or m1 == 0:
                t = 1.0
            else: 
                t = math.exp(lbs_n1_f10 + lbs_n2[f20]
                             + m1 * (logs[m1] - logN)
                             + m0 * (logs[m0] - logN))
            r += t
    return r

def twogtest(ctblines):
    ctb  = contab.get_ctb(ctblines)

    lnom_eq = ml.logml(map(sum, zip(*ctb)))

    reg_eq  = R_eq(ctb)
    lreg_eq = math.log(reg_eq)


    lnom_f  = sum(map(ml.logml, ctb))

    n1, n2 = map(sum, ctb)
    reg_f   = reg.reg(n1,2) * reg.reg(n2,2)
    lreg_f  = math.log(reg_f)


    lreg_ne = math.log((reg_f - reg_eq)/2)
        
    lnom_ge = (ctb[0][1] * n2 >= ctb[1][1] * n1) and lnom_f or lnom_eq
    
    return logmath.lognorm((lnom_eq - lreg_eq,
                            lnom_ge - lreg_ne,
                            lnom_f - lreg_f))
    
if __name__ == '__main__':
    import coliche

    def main(ctbfile):
            print " ".join(map(str, twogtest(file(ctbfile))))
        
    coliche.che(main, "ctbfile")


