import random, propreg, math, logmath, lgamma

def lfac(n):
    f = 0.0;
    for x in xrange(1,n+1):
        f += math.log(x)
    return f

def lmgprob(f0,f1,a,b):
    lg = lgamma.lgamma
    return lg(a+b) - (lg(a)+lg(b)) + lg(a+f0) + lg(b+f1) - lg(f0+f1+a+b)

def sample(N, p):
    return [int(random.random()<p) for i in range(N)]

import sys
def main(N, H0, nof_points=50, nof_reps=10000):
    mlines = ("I %s %s" % (H0, H0), "O %s %s" % (H0, H0))
    h0 = float(H0)
    for i in xrange(nof_points+1):
        p = float(i)/nof_points
        p0_avg, p1_avg = 0.0, 0.0
        b0_avg, b1_avg = 0.0, 0.0
        for r in xrange(nof_reps):
            s = sample(N,p)
            f1 = sum(s)
            f0 = N-f1

            p0, p1 = propreg.proptest((f0, f1), mlines)
            p0_avg = (r*p0_avg + p0) / (r+1)
            p1_avg = (r*p1_avg + p1) / (r+1)

            lb0 =   f1 * (h0>0.0 and math.log(h0)   or 0.0) \
                  + f0 * (h0<1.0 and math.log(1-h0) or 0.0)
            # lb1 = lfac(f1)+lfac(f0)-lfac(N+1)
            # lb1 = lmgprob(f0, f1, 1.0, 1.0)
            lb1 = lmgprob(f0, f1, 0.5, 0.5)

            b0, b1 = logmath.lognorm((lb0, lb1))
            b0_avg = (r*b0_avg + b0) / (r+1)
            b1_avg = (r*b1_avg + b1) / (r+1)
            
            
        print p, p0_avg, b0_avg

if __name__ == '__main__':
    from coliche import che
    
    che(main,
        """ N (int); H0;
        -n --nof-points nof-points (int)
        -r --nof-reps nof-reps (int)
        """)
    
        
