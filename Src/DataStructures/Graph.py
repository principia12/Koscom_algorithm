class Graph:
    def __init__(self, V, E, is_directed = True):
        for from_node, to_node in E:
            assert from_node in V, from_node
            assert to_node in V, to_node
            
        self.V = V
        self.E = E
        self.is_directed = is_directed 
        
        # adjacency list generation 
        adj_list = {}
        for v in V:
            adj_list[v] = []
            
        for from_node, to_node in E:
            if from_node == v:
                adj_list[v].append(to_node)
        self.adjacency_list = adj_list
        
        # adjacency matrix generation 
        adj_mat = []
        for i, u in enumerate(V):
            adj_mat.append([])
            for j, v in enumerate(V):
                if v in adj_list[u]:
                    adj_mat[-1].append(1)
                else:
                    adj_mat[-1].append(0)
        
        self.adjacency_matrix = adj_mat
        
    def is_dag(self):
        try:
            self.topological_sort()
            return True
        except AssertionError:
            return False
    
    def get_adj(self, node):
        res = []
        
        for v,u in self.E:
            if node == v:
                res.append(u)
            elif node == u and not self.is_directed:
                res.append(v)
                
        return res
    
    def _dfs_util(self, start_node, visited, to_tree = True):
        if not to_tree:
            res  = []
            if visited[start_node]:
                return []
            visited[start_node] = True
            res.append(start_node)
            # get adj of start_node
            for node in self.get_adj(start_node):
                res.extend(self._dfs_util(node, visited, to_tree = to_tree))
        else:
            if visited[start_node]:
                return Tree(datum = start_node)
            visited[start_node] = True
            datum = start_node
            children = []
            for node in self.get_adj(start_node):
                if not visited[node]:
                    children.append(self._dfs_util(node, visited, to_tree = to_tree))
                    
            res = Tree(datum = datum, children = children)
        
        return res
    
    def dfs(self, start_node, to_tree = True):
        assert start_node in self.V
        visited = {}
        for v in self.V:
            visited[v] = False
            
        return self._dfs_util(start_node, visited, to_tree = to_tree)
    
    def bfs(self, start_node, to_tree = True):
        if not to_tree:
            res, queue = [], [start_node]
            while queue:
                v = queue.pop()
                if v not in res:
                    res.append(v)
                    queue.extend(list(set(self.V) - set(res)))
            return res
        else:
            queue = [start_node]
            res = Tree(datum = start_node, children = [])
            
            while queue:
                v = queue.pop()
                visited = [t.datum for t in res.nodes()]
                if v not in visited:
                    queue.extend(list(set(self.V) - set(visited)))
                    
            return res
            
            
    def topological_sort(self):
        # implementation of Kahn's algorithm for topological sort 
        res = []
        starting_nodes = []
        
        to_nodes = [e[1] for e in self.E]
        edges = [e for e in self.E]
        
        for v in self.V:
            if v not in to_nodes:  
                starting_nodes.append(v)
                
        while len(starting_nodes) != 0:
            n = starting_nodes.pop()
            
            res.append(n)
            for e in self.E:
                if e[0] == n:
                    m = e[1]
                    edges.remove(e)
                    if m not in [e[1] for e in edges]:
                        starting_nodes.append(m)
            
        if edges != []:
            print(res)
            assert False, 'Something Wrong! %s'%(edges)
            
        else:
            return res
