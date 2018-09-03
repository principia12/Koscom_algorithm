class Test:
    def __init__(self, a):
        self.a = a
    
    def seta(self, b):
        self.a = b
    
    def f(self, b):
        #self = Test(b)
        self.seta(b)
        
t = Test(1)
t.f(2)
print(t.a)
    