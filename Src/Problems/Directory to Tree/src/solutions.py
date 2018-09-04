import os 
from Tree import Tree

def dir2tree(path_to_root):
    if os.path.isdir(path_to_root):
        root = path_to_root
        children = []
        for elem in os.listdir(path_to_root):
            sub = os.path.join(path_to_root, elem)
            if os.path.isdir(sub):
                children.append(dir2tree(sub))
            else:
                children.append(Tree(sub))
        return Tree(root = root, children = children)
    else:
        return Tree(root = path_to_root)
    
def files(path_to_root, cond):
    tree = dir2tree(path_to_root)
    for elem in tree.leaves():
        if cond(elem):
            yield elem
    
def directories(path_to_root):
    tree = dir2tree(path_to_root)
    for elem in tree.internal_nodes():
        yield elem
    
if __name__ == '__main__':
    print(dir2tree('.'))
    for f in files('..', lambda x:x.endswith('.hwp')):
        print(f)
    for d in directories('..'):
        print(d)

