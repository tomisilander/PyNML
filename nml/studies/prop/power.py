import random

N=10
p0=0.5
bicot = None

p=0.7 # loop over this

def get_bicot(N):
    t=[[0L]*(N+1)]; t[0][0] = 1L
    for n in xrange(1,N+1):
        t.append([1])
        t[n].extend([t[n-1][k-1]+t[n-1][k]for k in xrange(1,n+1)])
        t[n].extend([0]*(N-n))
    return t[-1]
    
            

def sample(N, p):
    return [int(random.random()<p) for i in range(N)]
    
def prob(p, k, n):
    return bicot[k] * pow(p, k) * pow(1-p, n-k)
    
def power(N, p0, p, a, R):
    r = 0;
    p_avg = 0.0
    
    while r<R:
        s  = sample(N, p);
        n1 = sum(s)
        n0 = N - n1
        p_s = prob(p0, n1, N)

        p_avg = (r*p_avg + int(p_s<a))
        r += 1
        p_avg /= r

    return p_avg


bicot = get_bicot(N)
print power(N, p0, p, 0.011, 100000)
