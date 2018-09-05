import numpy as np

def argmax(lst):
    max_lst = max(lst)
    for idx, elem in enumerate(lst):
        if elem == max_lst:
            return idx, elem
            
def get_score(y, emission_scores,trans_scores, start_scores, end_scores):
    '''
    get y and return score of y
    '''
    N = len(y)
    
    score = 0.0
    score += start_scores[y[0]]
    for i in xrange(N-1):
        score += trans_scores[y[i]][y[i+1]]
        score += emission_scores[i][y[i]]
    score += emission_scores[N-1,y[N-1]]
    score += end_scores[y[N-1]]
    
    return score
    
    

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    '''Run the Viterbi algorithm.
    N - number of tokens (length of sentence)
    L - number of labels
    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array
    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is the size N array/seq of integers representing the best sequence.
    '''
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]
    
    # generate two L X N array T1, T2
    score = 0.0
    T1 = []
    T2 = []
    
    for i in range(L):
        T1.append([])
        T2.append([])
        for j in range(N):
            T1[i].append(0)
            T2[i].append(0)
    
    for i in range(L):
        T1[i][0] = [start_scores[i] + end_scores[i]+emission_scores[0,i]]
        T2[i][0] = [i]
        
        
    for j in range(1, N):
        for i in range(L): 
            max_val = -np.inf
            for elem in range(L):
                #print 'list', T2[elem][j-1]
                #print i-1, elem
                #print T2
                assert type(T2[elem][j-1])==list
                tmp_path = T2[elem][j-1] + [i]
                #print i, tmp_path
                tmp_val = get_score(tmp_path, emission_scores, trans_scores, start_scores, end_scores)
                if tmp_val > max_val:
                    max_path = [elem for elem in tmp_path]
                    max_val = tmp_val
            T1[i][j] = max_val
            T2[i][j] = max_path
            assert get_score(max_path, emission_scores, trans_scores, start_scores, end_scores) == max_val
            
            
    
    idx, score = argmax([T1[i][-1] for i in range(L)])
    y = T2[idx][-1]
    
    
    return (score, y)