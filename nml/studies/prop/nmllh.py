import propreg

import sys
def main(N, H0):
    mlines = ("I %s %s" % (H0, H0),
              "O %s %s" % (H0, H0))
    h0 = float(H0)
    for f1 in xrange(N+1):
        p = float(f1)/N
        f0 = N-f1
        p0, p1 = propreg.proptest((f0, f1), mlines)
        print p, p0

if __name__ == '__main__':
    from coliche import che

    che(main,
        """ N (int); H0;
        """)
