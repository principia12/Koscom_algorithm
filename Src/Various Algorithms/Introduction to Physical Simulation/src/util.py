import math

def mean(lst):
    return sum(lst)/len(lst)

def var(lst):
    m = mean(lst)
    v = [(e - m)**2 for e in lst]
    return mean(v)
    
def dist(src, dest):
    return math.sqrt((src[0]-dest[0])**2 + (src[1]-dest[1])**2)
    
def dist_unitvec(src, dest):
    d = dist(src, dest)
    return [(dest[0] - src[0])/d, (dest[1] - src[1])/d]