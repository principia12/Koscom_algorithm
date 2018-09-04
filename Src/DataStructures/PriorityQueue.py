class PriorityQueue:
    def __init__(self, *elements):
        # elements must be a list of 2-tuple, containing element/priority pair. 
        for elem in elements:
            assert len(elem) == 2
        self.data = elements
    
    # return the element with highest priority
    def pop(self):
        import math
        max_idx, max_priority = 0, -math.inf # for initial value, must be lower than any value. 
        for idx, elem in enumerate(self.data):
            if max_priority < elem[1]:
                max_priority = elem[1]
                max_idx = idx
        res = self.data[max_idx]
        self.data = self.data[:idx] + self.data[idx+1:]
        return res     
    
    def push(self, element, priority):
        self.data.append((element, priority))
        
        
    