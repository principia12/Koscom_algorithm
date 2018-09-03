from List import List 

class ArrayList(List):
    def __init__(self):
        self.array = []
    
    def is_empty(self):
        return self.array == []
    
    def prepend(self, item):
        if self.is_empty():
            self.array.append(item)
            return self
        else:
            for elem in self.array:
                self.array.append(item)
        return self.
    
    def append(self, item):
        pass
    
    def head(self):
        pass
    
    def tail(self):
        pass