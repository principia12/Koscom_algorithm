from Tree import Tree
from PriorityQueue import PriorityQueue

def generate_freq_lst(input_string):
    freq_dict = {}
    for char in input_string:
        if char in freq_dict.keys():
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    
    res = []
    for key in freq_dict.keys():
        res.append((key, freq_dict[key]))
        
    return res

def assign_leaf_address(tree):
    addr = '0'
    if tree.children == []:
        yield tree.root, ''
    else:
        for idx, child in enumerate(tree.children):
            for l, l_addr in assign_leaf_address(child):
                yield l, str(idx) + l_addr
        
    
def huffman_encoding(input_string):
    freq_lst = generate_freq_lst(input_string)
    
    queue = PriorityQueue(*freq_lst)
    
    while len(queue.data) != 1:
        x = queue.pop()
        y = queue.pop()
        children = []
        if isinstance(x[0], Tree):
            children.append(x[0])
        else:
            children.append(Tree(x[0]))
        
        if isinstance(y[0], Tree):
            children.append(y[0])
        else:
            children.append(Tree(y[0]))    
            
        t = Tree(root = x[1] + y[1], children = children)
        queue.push(t, x[1] + y[1])
        
    res = queue.pop()[0] # huffman tree
    
    code_dict = {}
    for l, addr in assign_leaf_address(res):
        code_dict[l] = addr
    encoded_str = ''
    for char in input_string:
        encoded_str += code_dict[char]
    print(code_dict)
    print(encoded_str)
    return encoded_str, res
    
def huffman_decode(encoded_str, huffman_tree):
    res = ''
    idx = 0
    pos = huffman_tree
    while idx != len(encoded_str):
        
        char = encoded_str[idx]
        if char == '0':
            pos = pos.children[0]
        else:
            pos = pos.children[1]
        
        idx += 1
        if pos.children == []:
            res += pos.root
            pos = huffman_tree
        
    return res
        
    
    
print(huffman_decode(*huffman_encoding('abbcccddddeeeeeffffff')))
    
    
    
    