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
    pass
    
def huffman_decode(encoded_str, huffman_tree):
    pass    
    
    
print(huffman_decode(*huffman_encoding('abbcccddddeeeeeffffff')))
    
    
    
    