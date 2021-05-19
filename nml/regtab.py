#!/usr/bin/env python

import math
from itertools import islice

def gen_logfacs(logs):
    lf = 0.0
    yield lf
    
    for l in islice(logs,1,None):
        lf += l
        yield lf

def gen_logs(n):
    yield None
    for x in range(1,n):
        yield math.log(x)

def get_regs(rtbfile, kns):
    kns = list(kns)
    kns.sort()
    
    regs = {}
    for k_1, l in enumerate(open(rtbfile)):
        lt = None
        while kns[0][0] == k_1 + 1:
            (k,n) = kns.pop(0)
            if lt is None:
                lt = map(float, l.split())

            if n >= len(lt):
                raise MemoryError("Matrix entry too big to handle!")
            
            regs[(k,n)] = lt[n]
            if not kns:
                return regs
    if kns:
        raise Exception("Too many entries in the matrix!")
        
    
def R(k, n, Rs, l, lf):

    def rts(): # Always n>0, k > 1
        for r in range(n+1):
            n_r = n-r
            if r and n_r:
                log_mulco = lf[n] - lf[r] - lf[n_r]
                bnt = math.exp(log_mulco + r*(l[r]-l[n]) + n_r*(l[n_r]-l[n]))
            else :
                bnt = 1.0

            # print "n=%d k=%d r=%d" %(n, k, r)
            # print "Rs[r]", Rs[r]
            # print "Rs[n-r]",Rs[n-r]
                
            yield bnt * Rs[r]
                
    return sum(rts())

def Rs(N,K):
    l = list(gen_logs(N+1))
    lf = list(gen_logfacs(l))

    
    Rs = [1]*(N+1)
    yield Rs
    for k in range(2,K+1):
        Rs = [R(k,n,Rs,l,lf) for n in range(N+1)]
        yield Rs

if __name__ == '__main__':
    import coche

    def main(N,K,filename):
        f = open(filename, "w")
        for rk in Rs(N,K):
            #print >>f, " ".join(["%8.2f" % r for r in rk])    
            print(" ".join(map(str, rk)), file=f)    
        f.close()

    coche.che(main, "N (int); K (int); filename")
