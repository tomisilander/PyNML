#!/usr/bin/python

import math
from nml import regtab, contab
import logmath

def xlogbinoms(n, logs):
    lb = 0.0
    yield lb
    
    for k in xrange(1,n):
        lb += logs[n-k+1] - logs[k]
        yield lb
    yield 0.0
    
def logpow(x,n):
    if n==0:
        return 0.0
    elif x==0:
        return None
    else:
        return n * math.log(x)

def lnom_p(p, f):
    t1 = logpow(p,f[1])
    t0 = logpow(1-p,f[0])
    if t1 == None or t0 == None :
        return None
    else:
        return t1 + t0

def in_p(a, b, f, N):
    fa = int(math.ceil (a*N)) # first f that is in
    fb = int(math.floor(b*N)) # last  f that is in

    if   f < fa       : return a
    elif f <= f <= fb : return float(f)/N
    else              : return b
    

def out_p(a, b, f, N):
    
    fa = int(math.ceil (a*N)) # first f that is in
    fb = int(math.floor(b*N)) # last  f that is in

    if   f < fa  or fb < f :
        return float(f)/N
    else :
        if a == 0 : return b
        if b == 1 : return a
        return (f*(math.log(a/b)) > (N-f)*math.log((1-b)/(1-a))) and a or b
            
def R_io(a, b, N, io_p):

    logs  = list(regtab.xlogs(N+1))
    lbs_N = list(xlogbinoms(N, logs))

    r  = 0.0
    for f1 in xrange(N+1):

        # print "RIO", f1, io_p(a,b,f1,N)
        t  = lnom_p(io_p(a,b,f1,N),(N-f1, f1))
        if t != None:
            r += math.exp(lbs_N[f1] + t)            

    return r


def proptest(frqs, mlines):

    N  = sum(frqs)
    f1 = frqs[1]

    if not N:
        raise Exception("Some data needed!")

    lprobs = []
    for mline in mlines:
	if not mline.strip(): continue

	ioab = mline.split()
        if len(ioab) != 3:
            raise Exception("Required model syntax (IN|OUT) a b")
        else:
            io,a,b = ioab[0].upper(), float(ioab[1]), float(ioab[2])

        if not 0<=a<=b<=1:
            raise Exception("Needs to be 0<=a<=b<=1")

        if io.startswith("O"):
            if a==0 and b==1:
                raise Exception("Model cannot be out of [0,1]")
            io_p = out_p
        else:
            io_p = in_p
            
        
        lnom_io = lnom_p(io_p(a,b,f1,N),frqs)
        reg_io  = R_io(a,b, N, io_p)
        lreg_io = math.log(reg_io)

        # print io_p(a,b,f1,N), lnom_io, reg_io, lreg_io
        lprobs.append((lnom_io != None) and (lnom_io - lreg_io) or None)

    if len(lprobs)<2:
        raise Exception("At least 2 models required to select among them!")
        
    return logmath.lognorm(lprobs)
        
if __name__ == '__main__':
    import coliche

    def main(f0, f1, mfile):
            print proptest((f0, f1), file(mfile))
        
    coliche.che(main,
                """
                f0 (int)  : number of zeros
                f1 (int)  : number of ones (successes)
                mfile     : modelfile with lines "[I|O] lower_limit upper_limit"
                """)
