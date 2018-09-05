# This will be exam problems, so please take a time to solve these problems. 

'''
Problem 1. 

Write a function for calculating (num)th fibonacci number in O(2^n). Note that n denotes the number of bits for encoding num. 
'''

def fib(n):
    tmp = [1,1]
    
    # modify this part
    # range to what?
    for i in range(0): 
        # append what?  
        # note that a[-1] is the last element in the list
        # and a[-2] is the last element in the list
        tmp.append(1) 
        
    return tmp[-1]
    
'''
Problem 2. 

Write 3 different functions for sorting a list. 
'''

def sort1(lst):
    pass
    
def sort2(lst):
    pass
    
def sort3(lst):
    pass
    
'''
Problem 3. 

Write a function that gives solution to the problem of hanoi's tower in following format; 

Moved disk x from 1 to 3 

The problem of Hanoi will be explained before the test. 
....
'''

def hanoi(n):
    return '\n'.join(hanoi_tower(n, 1, 3, 2))
    
def hanoi_tower(n, from_rod, to_rod, passing_rod):
    res = []
    if n == 1:
        # move disk 1 to 3, and task is over. 
        res.append(move(1, 1, 3)) 
        return res
    else:
        # move disks 1~n-1 from 1 to 2
        res += hanoi_tower(None, None, None, None,)
        # move disks n from 1 to 3
        res += move(n, 1, 3)
        # move disks 1~n-1 from 2 to 3
        res += hanoi_tower(None, None, None, None,)
        # task is over, return the result. 
    
def move(disk_num, from_rod, to_rod):
    return 'Moved disk %d from %d to %d'%(disk_num, from_rod, to_rod)
    
'''
Problem 4. 

Write a function to check whether the paranthesis in the given string is correctly paired.
'''
def check_para(input_str):
    '''
    examples 
    (), (()), ()() returns True 
    )(, ((), )(()( returns False
    
    '''
    pass
   
    
    
    
