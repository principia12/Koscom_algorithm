def insertion_sort(lst):
    if len(lst) == 1:
        return lst
    else:
        head, tail = lst[0], lst[1:]
        
        return insert(insertion_sort(tail), head) # recursive call to insertion_sort
        
def insert(lst, head):
    wanted_index = 0
    for idx, elem in enumerate(lst):
        if head > elem:
            wanted_index += 1
            
    return lst[:wanted_index] + [head] + lst[wanted_index:]
    
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
        if sorted(test) == insertion_sort(test):
            correct += 1
            
    assert correct == 100, '%d right out of 100'%correct
        
test()    