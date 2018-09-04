# Three functions for calculating fibonacci numbers 

# O(2^2^n) algorithm
def fib1(n):
    assert n > -1
    
    if n in [0,1]:
        return 1
    else:
        return fib1(n-1) + fib1(n-2)

# O(2^n) algorithm        
def fib2(n):
    assert n > -1 
    
    tmp = [1,1]
    
    while len(tmp) < n+1:
        tmp.append(tmp[-1] + tmp[-2])
     
    return tmp[-1]
    
# O(n) algorithm
def fib3(n):
    assert n > -1 
    
    # auxillary class Matrix 
    class Matrix:
        def __init__(self, lst):
            # assert 2 by 2 matrix
            assert len(lst) == 2
            for elem in lst:
                assert len(lst) == 2
            self.lst = lst
            
            
        # magic method __mul__ for matrix multiplication 
        def __mul__(self, other):
            l = self.lst
            r = other.lst
            res = [[l[0][0]*r[0][0] + l[0][1]*r[1][0], 
                    l[0][0]*r[0][1] + l[0][1]*r[1][1]], 
                   [l[1][0]*r[0][0] + l[1][1]*r[1][0], 
                    l[1][0]*r[0][1] + l[1][1]*r[1][1]],]
            return Matrix(res)
            
    # auxillary function multiply        
    def multiply(a, n, one):
        # one : 곱셈에 대한 항등원 
        if n == 0:
            return one
        elif n == 1:
            return a
        elif n%2 == 1:
            tmp = multiply(a, n//2, one)
            return a*tmp*tmp # think of why not using multiply(a, n//2, one) * multiply(a, n//2, one) * as
        else:
            tmp = multiply(a, n//2, one)
            return tmp*tmp
    
    if n in [0,1]:
        return 1
    else:
        res = multiply(Matrix([[1,1], [1,0]]), n-1, Matrix([[1,0], [0,1]]))
    
    return sum(res.lst[0])
    
# tests and runtime analysis
    
for i in range(5):
    print(fib1(i), fib2(i), fib3(i))
    assert fib1(i) == fib2(i) == fib3(i)
    
for i in range(5, 100):
    print(fib2(i), fib3(i))
    assert fib2(i) == fib3(i)
    
from time import time
begin = time()
for i in range(1000, 10000):
    fib2(i)
end = time()
print(end-begin) # about 30s

begin = time()
for i in range(1000, 10000):
    fib3(i)
end = time()
print(end-begin) # about 2s, much better!    