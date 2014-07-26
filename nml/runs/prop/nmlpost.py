import propreg

import sys
def main(N, p, nof_points=50, nof_reps=10000):
    h0 = float(H0)
    for f1 in xrange(N+1):
        f0 = N-f1
        pf1 = C(N,f1)*(p**f1)(1-p)**f0

        for 
        mlines = ("I %s %s" % (, H0), "O %s %s" % (H0, H0))
        p0, p1 = propreg.proptest((f0, f1), mlines)
        print p, p0

if __name__ == '__main__':
    from coliche import che
    
    che(main,
        """ N (int); p;
        """)
