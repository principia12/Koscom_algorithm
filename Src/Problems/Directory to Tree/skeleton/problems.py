import os 
from util import * 
from Tree import *

def dir2tree(path_to_root):
    return Tree()
    
def files(path_to_root, cond):
    pass
    
def directories(path_to_root):
    pass
    
if __name__ == '__main__':
    print(dir2tree('.'))
    for f in files('..', lambda x:x.endswith('.hwp')):
        print(f)
    for d in directories('..'):
        print(d)

