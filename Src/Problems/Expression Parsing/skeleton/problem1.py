import re
import math
from Stack import Stack
from Tree import Tree


'''
Parser Implementation

In this problem, you are given a grammar that expresses common mathematical expressions, but without (-) signed numbers. 

1. Grammar

IMPORTANT : IF YOU CAN UNDERSTAND THE GRAMMAR, DO NOT READ THIS PART.

Grammar is given as following; 

1) expr -> part (binary part)* ; 
2) part -> num | val | "(" expr ")" ; 
3) binary -> "+" | "-" | "*" | "/" | "^" ; 
4) num -> r"[1-9][0-9]*\.?[0-9]*|0" ; 
5) val -> r"[a-zA-Z]+"

Each line of grammar is called a rule. A rule can be seperated by '->', distinguishing left hand side and right hand side. Each rule means that the left hand side can be rewritten by one of the options - options are splited by | - on the left hand side. For example, binary can be replaced by "+". Input is always assumed to be the left hand side of the first rule, and parsed to the sequence of 'terminals', which are tokens that are wrapped by ". 

Your task is to write a parser that gets input string and return a tree-like structure expressing the meaning of this grammar. 

The grammar shown on the slide is NOT identical to the grammar you see in this text. However, it should not make a bit difference - unless you have passed all the tests till eq33. Even if so, it will not cause a significant error. 

On rule 1), '(binary part)*' means that 'binary part' will be finitely iterated. 0 iteration is also possible. So, 1) is just a shortened notation for  

1') expr -> part | part binary part | part binary part binary part | ... 

On rule 4 and 5, you might find the right hand side of the rule unfamiliar if you have not encounted a regular expression before. They imply as follows; 

4.r) r"[1-9][0-9]*\.?[0-9]*|0"

Firstly, [1-9] or [0-9] means from 1-9 or 0-9, respectively. * after the [] term means that token that is expressed in [] can be repeated zero or more times. Likewise, ? means it can be repeated zero or one times. \. represents dot itself. So, this regular expression means a string that starts with one of the numbers 1 to 9, and have few numbers afterward, allowing one dot in the middle; which is just a normal numbers, except 0. Since 0 is the only number that starts with 0, 0 is handled with care. 

5.r) r"[a-zA-Z]+"

Only new part is +. It means one or more iteration, not allowing zero iteration. 
 

2. Functions to implement and hints 

 
- tokenizer (optional. already implemented from the beginning.)

When implementing tokenizer, go through a given equation by iteratively checking whether the first part of equation matches with one of the tokens. If so, erase matching part and repeat again. For this, use re.match() function. 

re.match(pattern, string) checks whether the pattern is matched with the 'first part' of the string. (This is difference between re.find(); it searches through all the string.) Since it will return a match object, you can use m.start() and m.end() to locate the longest matching part. So the pseudocode will be as following; 

while eq !=  '':
    for pattern in tokens:
        if re.match(pattern, eq):
            yield (pattern_type, pattern)
            eq = erase_eq(...) 

Note that not all tokens are regular expression; some are just strings. Handle them accordingly. 

- parser

Two methods can be considered for implementing the parser for the given grammar. 

- Recursive implementation 

In the recursive implementation, 'expr' and 'part' will be a function that parses to that specific matching part and return the index of the matching part. For example, consider following expression; 

1+1 -> tokenized to ('num', 1), ('op', +), ('num', 1)

When you first call expr, it should call part twice; first part should return 1 or 2, since it will only parse the first token. You can either increment token, or make part function returns to the next index that parsing need to be started. 

- Iterative implementation 

Consider the type of current token and next token. Handle it accoridngly; use stack for handling the operators. 

'''
precedence = {\
    '+' : 1, 
    '-' : 1, 
    '*' : 2, 
    '/' : 2, 
    '^' : 3, }
    
def tokenizer(equation):
    left = equation.replace(' ', '')
    tokens = {\
        'op' : ['^', '+', '-', '*', '+', '/'],
        'para' : ['(', ')'],
        'num' : [r"[1-9][0-9]*\.?[0-9]*|0",],
        'var' : [r"[a-zA-Z]+_?[0-9]*",], }
    
    tok_strings = []
    for k in tokens.keys():
        tok_strings.extend(tokens[k])
    
    while left != '':
        for tok in tok_strings:
            if tok in tokens['num']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('num', left[m.start():m.end()]))
                    left = left[m.end():]
            elif tok in tokens['var']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('var', left[m.start():m.end()]))
                    left = left[m.end():]
                    
            else:
                if left.startswith(tok):
                    if tok in tokens['para']:
                        yield ('para', left[0])
                        left = left[1:]        
                    elif tok in tokens['op']:
                        yield ('op', left[0])
                        left = left[1:]        
                    
def find_match(tokens, t_idx):
    tok_type, tok = tokens[t_idx]
    
    assert tok_type == 'para' and tok == '(', \
            'Should find for paranthesis matching, %s.'%(str(tokens)) 
    cnt = 0 
    
    for idx, elem in enumerate(tokens[t_idx:]):
        token_type, token = elem
        if token == tok:
            cnt += 1
        elif token == ')':
            cnt -= 1
        
        if cnt < 0:
            assert False, 'Paranthesis matching error!'
        if cnt == 0:
            return idx + t_idx
    return len(tokens)+1

    
def recursive_descent(tokens):
    
    operator = Stack()
    operand = Stack()
    idx = expr(operator, operand, tokens, 0)
    res = operand.pop()
    
    return res
    
def expr(operator, operand, tokens, idx):
    return idx
        
    
def part(operator, operand, tokens, idx):
    
    next_tok = tokens[idx]
    
    if next_tok[0] == 'num' or next_tok[0] == 'var':
        # part := num | var
        pass
    elif next_tok[1] == '(':
        # part := "(" expr ")"
        pass
    else:
        assert False, 'Something wrong at %s'%str(tokens[idx])
    return idx
    
def pop_operator(operator, operand):
    pass
    
def push_operator(operator, operand, op):
    pass
    
def parse(eq):
    return recursive_descent(list(tokenizer(eq)))
    

    
        
if __name__ == '__main__':
    
    # tests, tests, more tests! 
    
    # simple numbers
    eq1 = '(1)'
    eq2 = '3'
    #eq3 = '-1'
    
    # +,- 
    eq4 = '1+1'
    eq5 = '1-1-2' # check
    #eq6 = '-1-2-3-4-5'
    
    # +,-,*,/ 
    eq7 = '1+2/3+2'
    eq8 = '3*4+2'
    eq9 = '4/2'
    eq10 = '3+4*2'
    eq11 = '3+4/2'
    eq12 = '3/4/2'
    eq13 = '(3/4)/2' # check
    eq14 = '3/(4/2)'
    eq15 = '1+2/3'
    
    # +,-,*,/,^ with (,)
    eq16 = '(1+2)/3'
    eq17 = '(1*2)/3'
    eq18 = '(1+2)*3'
    eq19 = '3*(1+2)'
    eq20 = '3*(2-1)'
    eq21 = '3*(1-2)'
    # eq22 = '3*(-2+1)'
    # eq23 = '-3-2^3'
    # eq24 = '-3-2^(3+2)'
    # eq25 = '-2^3'
    # eq26 = '-2^-3'
    
    # +,-,*,/ with nested (,)
    # eq27 = '-1+(-1-2)'
    # eq28 = '-(2+2)'
    # eq29 = '3+(2^(-(2+2)))'
    # eq30 = '3*(2*2+1)'
    eq31 = '2-3*(2*2+1)'
    eq32 = '2-3*(2*(2+1))'
    eq33 = '((3+2)*4-(2*4+2^(2-5)))*(2+(3+2)*5^2)'
    eq34 = '2+(3+2)*5^2'
    eq35 = '1+2^2*1'
    
    eq36 = 'x/2'
    # eq37 = '-x_0*z+y'
    eq40 = '1+3^3*c'
    eq45 = 'a+b+C+d+f+g+h'
    eq46 = '1'
    eq47 = '0'
    
    # eq48 = 'sin(x+y)'
    
    
    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        print('=============')
        print(eq)
        for t, tok in tokenizer(eq):
            print(t, tok)
        print(parse(eq))
        print('=============')
    
    