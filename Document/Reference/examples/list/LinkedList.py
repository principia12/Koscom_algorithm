from List import List
from copy import deepcopy

class LinkedList(List):
    def __init__(self):
        self.head = None
        self.tail = None 
        
    def set_head(self, h):
        self.head = h
    
    def set_tail(self, t):
        self.tail = t
        
    def is_empty(self):
        return self.head is None and self.tail is None
        
    def prepend(self, item):
        if self.is_empty():
            self.head = item
        else:
            self.set_tail(deepcopy(self))
            self.set_head(item)
            
    def append(self, item):
        if self.is_empty():
            self.head = item 
        else:
            tmp = LinkedList()
            tmp.head = item 
            cur = self
            while cur.tail is not None:
                cur = cur.tail
            cur.tail = tmp
        
    def head(self):
        return self.head
        
    def tail(self):
        return self.tail
        
    def iter(self, option):
        return range(option)
        
        
    def __str__(self):
        if self.is_empty():
            return ''
        else:
            res = []
            res.append(str(self.head))
            if self.tail is not None:
                res.append(str(self.tail))
            
            return '->'.join(res)
            
if __name__ == '__main__':
    a = LinkedList()
    '''
    print(a)
    a = a.prepend(1) 
    print(a)
    a = a.prepend(2)
    print(a)
    a = a.prepend(3)
    print(a)
    '''
    a.prepend(1)
    a.prepend(2)
    a.prepend(3)
    print(a.head)
    print(a.tail.head)
    print(a)
    
    print(a)
    a.append(4)
    a.append(5)
    print(a)
    
    b = LinkedList()
    b.append(1)
    print(b)
    b.append(2)
    print(b)
    b.prepend(1)
    b.prepend(2)
    b.prepend(3)
    print(b)
    
    for elem in a.iter(2):
        print(elem)
    
    