
class Stack:
    def __init__(self, *initial_data, datastructure = 'list'):
        self.data = list(initial_data)
        
    def is_empty(self):
        return len(self.data) == 0
        
    def push(self, *elem):
        self.data.extend(elem)
        
    def pop(self):
        assert not self.is_empty()
        head, tail = self.data[:-1], self.data[-1]
        self.data = head
        
        return tail
        
    def top(self):
        if self.is_empty():
            return None
        return self.data[-1]
        
    def size(self):
        return len(self.data)
        
    def __str__(self):
        res = 'Stack'
        for elem in self.data:
            res += ' %s'%str(elem)
        return res