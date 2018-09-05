class Tree:
    def __init__(self, root = None, children = []):
        self.root = root
        
        for child in children:
            assert isinstance(child, Tree), \
                    'child is not a tree'
        self.children = children
        
    def __str__(self):
        res = str(self.root)
        for child in self.children:
            res += ('\n' + str(child)).replace('\n', '\n\t')
        return res
        
    def nodes(self):
        yield self.root
        for child in self.children:
            yield from child.nodes()
            
    def _nodes(self):
        res = []
        res.append(self.root)
        for child in self.children:
            res = res + child._nodes()
        return res
        
    def leaves(self):
        if self.children == []:
            yield self.root
        else:
            for child in self.children:
                yield from child.leaves()
    
    def prefix(self):
        res = []
        res.append(str(self.root))
        
        for child in self.children:
            res.append(child.prefix())
            
        return ' '.join(res)
        
    def iter_with_address(self):
        res = []
        addr = ''
        res.append((self.root, addr))
        for idx, child in enumerate(self.children):
            for elem, addr in child.iter_with_address():
                res.append((elem, str(idx) + addr))
        return res
        
    def find_subtree(self, elem):
        '''
        return subtree with root elem if elem is in tree. 
        else, return -1 
        '''
        if self.root == elem:
            return self
        for idx, child in enumerate(self.children):
            cand = child.find_subtree(elem)
            if cand != -1:
                return cand
        
        return -1
        
    def find_subtree_addr(self, elem):
        '''
        return address with node elem if elem is in tree. 
        else, return -1 
        '''
        if self.root == elem:
            return ''
        for idx, child in enumerate(self.children):
            cand = child.find_subtree_addr(elem)
            if cand == -1:
                pass
            else:
                return str(idx) + cand
        
        return -1
        
    def find_subtree_addr2(self, elem):
        for node, addr in self.iter_with_address():
            if node == elem:
                return addr
    
    def find_subtree_addrs(self, elem):
        for node, addr in self.iter_with_address():
            if node == elem:
                yield addr

    def equals(self, other, is_ordered):
        res = True 
        res = res and self.root == other.root
        if not is_ordered:
            for child in self.children:
                tmp = False
                for o_child in other.children:
                    tmp = tmp or child.equals(o_child)
                res = res and tmp 
            for child in other.children:
                tmp = False
                for o_child in self.children:
                    tmp = tmp or child.equals(o_child)
                res = res and tmp 
        else:
            res = res and len(self.children) == len(other.children)
            for l, r in zip(self.children, other.children):
                res = res and l.equals(r)
        return res
    
    def substitute(self, src, dest):
        pass
    
    
    
t = Tree(1, 
            [Tree(2, 
                [Tree(4), 
                Tree(5)]), 
             Tree(3, 
                [Tree(6)])])
print(t)
for n in t.nodes():
    print(n)    
print('----------------')
for l in t.leaves():
    print(l)
    
print('----------------')
print(t.prefix())

print('----------------')
for elem, addr in t.iter_with_address():
    print(elem, addr)
print('----------------')
print(t.find_subtree_addr(3))
print('----------------')
print(t.find_subtree(3))

