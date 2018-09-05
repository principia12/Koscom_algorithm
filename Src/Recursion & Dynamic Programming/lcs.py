from pprint import pprint 

def lcs(l,r):
    m = len(l)
    n = len(r)
    
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = []
    
    for i in range(m):
        for j in range(n):
            if l[i] == r[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = []
                    longest = c
                    lcs_set.append(l[i-c+1:i+1])
                elif c == longest:
                    lcs_set.append(l[i-c+1:i+1])
            else:
                counter[i+1][j+1] = \
                    max(counter[i+1][j], counter[i][j+1], counter[i][j])
    print(counter)
    
    for elem in counter:
        print(elem)
    return lcs_set
        
print(lcs('abc', 'badec'))