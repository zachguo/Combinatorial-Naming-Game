def intersect(a, b):
     return list(set(a) & set(b))

def setdiff(a, b):
    return list(set(a) - set(b))

def unique(l):
    return list(set(l))

def deepvalues(d):
    return sum(d.values(),[])

def countHomophones(l):
    return len(l)-len(unique(l))
