#!/usr/bin/python

import genctb, deptest

if __name__ == '__main__':

    import sys, coliche

    def main(pfile, N):
        try:
            ps = [map(float, l.split()) for l in file(pfile)]
            normalizer = sum(map(sum,ps))
            ps = [[p/normalizer for p in r] for r in ps]
            r = [0,0]
            while True:
                ctb = genctb.genctb(ps,N)
                dt = deptest.deptest_ctb(ctb)
                r[dt.index(max(dt))] += 1
                print r, float(r[0])/sum(r)
        except Exception, msg:
            raise
            sys.exit("ERROR: "+ str(msg))
            
    coliche.che(main, "pfile; N (int)")
