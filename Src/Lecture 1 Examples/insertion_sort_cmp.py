def insertion_sort(lst, cmp):
    if len(lst) == 1:
        return lst
    else:
        head, tail = lst[0], lst[1:]
        
        return insert(insertion_sort(tail, cmp), head, cmp)
        
def insert(lst, head, cmp):
    wanted_index = 0
    for idx, elem in enumerate(lst):
        if cmp(head, elem): # True if head > elem
            wanted_index += 1
            
    return lst[:wanted_index] + [head] + lst[wanted_index:]
    
def cmp_modulo(l,r):
    return l%4 > r%4
    
def test(): 
    import random    
    
    tests = []
    for i in range(100):
        l = random.randrange(20,300)
        tests.append([])
        for j in range(l):
            
            tests[-1].append(random.randrange(1,10000))

    correct = 0
    for test in tests:
        if insertion_sort(test, cmp_modulo) == sorted(insertion_sort(test, cmp_modulo), key = lambda x:x%4):
            correct += 1
            
    assert correct == 100, '%d right out of 100'%correct
        
test()    