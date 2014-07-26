#!/usr/bin/python

import sys, math, sets, coliche, operator, logmath

def lgamma(x):
    """
    Natural log of the gamma function (x > 0)
    Derived from "Numerical Receipes in C"
    """

    cof = (76.18009172947146,    -86.50532032941677,
           24.01409824083091,    -1.231739572450155,
           0.1208650973866179e-2,-0.5395239384953e-5)
    tmp = x + 5.5 - (x + 0.5) * math.log(x + 5.5);
    ser = 1.000000000190015 + sum([ c / (x + i + 1)
                                    for (i,c) in enumerate(cof)])
    return math.log(2.5066282746310005 * ser / x) - tmp


def vs(ssi, a):

    q = len(ssi)
    r  = len(ssi[0])

    vscore      = q * lgamma(r*a)

    for ssij in ssi:
        Nij = sum(ssij)
        vscore -= lgamma(r*a + Nij) + r * lgamma(a)
        for Nijk in ssij:
            vscore += lgamma(a + Nijk)

    return vscore


def var_score(ssi, N):

    q = len(ssi)
    r  = len(ssi[0])

    vscore = q * lgamma(N/q)

    for ssij in ssi:
        Nij = sum(ssij)
        vscore -= lgamma(N/q + Nij) + r * lgamma(N/r/q)
        for Nijk in ssij:
            vscore += lgamma(N/r/q + Nijk)

    return vscore


def read_ctb(ctbfile):
    
    ctb   = [map(int, l.split()) for l in file(ctbfile)]
    vcs   = (len(ctb), len(ctb[0]))

    return vcs, ctb


def deptest_BD(ctb, a):
    lpX     = vs([map(sum, ctb)], a)
    lpY     = vs([map(sum, zip(*ctb))], a)
    lpYifX  = vs(ctb, a)
    
    return logmath.lognorm([lpY, lpYifX])

def deptest_BDeu(ctb, ess):
    lpX     = var_score([map(sum, ctb)], ess)
    lpY     = var_score([map(sum, zip(*ctb))], ess)
    lpYifX  = var_score(ctb, ess)
    
    return logmath.lognorm([lpY, lpYifX])

def deptest_BD(ctb, ess):
    lpX     = var_score([map(sum, ctb)], ess)
    lpY     = var_score([map(sum, zip(*ctb))], ess)
    lpYifX  = var_score(ctb, ess)
    
    return logmath.lognorm([lpY, lpYifX])

def logratio(ctbfile, ess=1.0):

    vcs, ctb = read_ctb(ctbfile)
    
    scoreX   = var_score([map(sum, ctb)], ess)
    scoreY   = var_score([map(sum, zip(*ctb))], ess)
    scoreXY  = var_score(ctb, ess)

    return scoreY - scoreXY

def main(cbtfile, ess=1.0):
    r = math.exp(logratio(cbtfile, ess))
    d = 1 / (1+r)
    i = 1 - d
    
    print "%.4f %.4f" % (i, d)
    
if __name__ == "__main__":
    coliche.che(main,
                """
                cbtfile : contingency table
                -e --ess ess (float) : ess (default: 1.0)
                """)
