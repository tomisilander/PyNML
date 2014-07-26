#!/usr/bin/python

def ct2s(N):
    for a in xrange(N+1):
        for b in xrange(N-a+1):
            for c in xrange(N-a-b+1):
                if a+b >= N/2:
                    yield [[a,b],
                           [c,N-(a+b+c)]]


import deptest, feptest, bn_deptest

for ctb in ct2s(10):
    print ctb
    print "NML : %.4f %.4f" % tuple(deptest.deptest_ctb(ctb))
    print "fNML: %.4f %.4f" % tuple(feptest.deptest_ctb(ctb))
    print "BDeu: %.4f %.4f" % tuple(bn_deptest.deptest_BDeu(ctb,1.0))
    print "BDJ : %.4f %.4f" % tuple(bn_deptest.deptest_BD(ctb,0.5))
    print
