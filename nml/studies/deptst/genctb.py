#!/usr/bin/python

import operator, random

def wheel(ps):
    su = 0.0;
    r = random.random()
    for i,p in enumerate(ps):
        su += p
        if r<=su: return i
    return len(ps) - 1 


def genctb(ps,N):

    nof_rows = len(ps)
    nof_cols = len(ps[0])
    ps = reduce(operator.__concat__, ps)
    ctb = [[0]*nof_cols for i in xrange(nof_rows)]

    for i in xrange(N):
        r,c = divmod(wheel(ps),nof_cols)
        ctb[r][c]+=1
    return ctb   

        
if __name__ == '__main__':

    import sys, coliche

    def main(ctbfile, N):
        try:
            ps = [map(float, l.split()) for l in file(ctbfile)]
            normalizer = sum(map(sum,ps))
            ps = [[p/normalizer for p in r] for r in ps]
            ctb = genctb(ps,N)
            for r in ctb:
                print " ".join(map(str,r))
        except Exception, msg:
            raise
            sys.exit("ERROR: "+ str(msg))
            
    coliche.che(main, "pfile; N (int)")
