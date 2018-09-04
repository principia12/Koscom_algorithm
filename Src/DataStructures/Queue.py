class Queue:
    def __init__(self, *initial_data):
        self.data = list(initial_data)
        
    def is_empty(self):
        return len(self.data) == 0
        
    def push(self, elem):
        self.data.append(elem)
        
    def pop(self):
        assert not self.is_empty()
        head, tail = self.data[0], self.data[1:]
        self.data = tail
        return head
    
    def __str__(self):
        res = 'Queue\nhead '
        for elem in self.data:
            res += '%s '%str(elem)
        return res            