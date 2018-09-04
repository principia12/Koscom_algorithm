class Tree:
    def __init__(self, root, children = []):
        self.root = root 
        
        for idx, child in enumerate(children):
            assert isinstance(child, Tree), child
                
        self.children = children
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.root == other.root:
                if self.children == other.children == []:
                    return True
                return set(self.children) == set(other.children)
            return False
        return NotImplemented
    
    def __ne__(self, other):
        x = self.__eq__(other)
        if x is not NotImplemented:
            return not x
        return NotImplemented
    
    def __str__(self):
        res = str(self.root)
        for child in self.children:
            res += '\n\t' + str(child).replace('\n', '\n\t')
        return res
            
    def nodes(self):
        yield self
        for child in self.children:
            yield from child.nodes()
            
    def leaves(self):
        if self.children == []:
            yield self.root
        else:
            for child in self.children:
                yield from child.leaves()
    
    def internal_nodes(self):
        if not self.children == []:
            yield self.root
            for child in self.children:
                yield from child.internal_nodes()
    