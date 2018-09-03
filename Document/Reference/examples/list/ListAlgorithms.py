from List import List
from LinkedList import LinkedList

def find_max(lst):
    if lst.tail is None:
        return lst.head
    else:
        l = lst.head
        r = find_max(lst.tail)
        return max(l, r)
        
    
    
if __name__ == '__main__':
    lst = LinkedList()
    print(find_max(lst))
    lst.append(1)
    lst.append(2)
    lst.append(3)
    lst.append(4)
    lst.append(5)
    print(find_max(lst))
    print(dir(LinkedList))
    assert issubclass(LinkedList, List)
    