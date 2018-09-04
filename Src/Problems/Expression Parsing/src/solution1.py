import re
import math
from Stack import Stack
from Tree import Tree


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
                    

    
def recursive_descent(tokens):
    
    operator = Stack()
    operand = Stack()
    idx = expr(operator, operand, tokens, 0)
    res = operand.pop()
    
    return res
    
def expr(operator, operand, tokens, idx):
    # expr := part (binary part)*
    idx = part(operator, operand, tokens, idx)
    idx += 1
    if idx != len(tokens):        
        next_tok = tokens[idx]
        
        while next_tok[1] in ['^', '+', '-', '*', '/']:
            push_operator(operator, operand, next_tok)
            idx += 1
            idx = part(operator, operand, tokens, idx)
            idx += 1
            try:
                next_tok = tokens[idx]
            except IndexError:
                next_tok = [None, None]
    
    while not operator.is_empty():
        pop_operator(operator, operand)
        
    return idx
        
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
    
def part(operator, operand, tokens, idx):
    # part := num | var 
    #      := "(" expr ")"
    #      := func "(" (expr ,)* expr ")"
    
    next_tok = tokens[idx]
    
    if next_tok[0] == 'num' or next_tok[0] == 'var':
        # part := num | var
        operand.push(Tree(root=next_tok))
    elif next_tok[1] == '(':
        # part := "(" expr ")"
        tokens_in_para = tokens[idx+1:find_match(tokens, idx)]
        e = recursive_descent(tokens_in_para)
        idx = find_match(tokens, idx) 
        operand.push(e)
        tokens = tokens[idx:]
    else:
        assert False, 'Something wrong at %s'%str(tokens[idx])
    return idx
    
def pop_operator(operator, operand):
    top = operator.pop()
    if top[1] in ['+', '*', '/', '^', '-']:
        arg1 = operand.pop()
        arg2 = operand.pop()
        operand.push(Tree(root = top, children = [arg2, arg1]))
    else:
        assert False, 'operator expected; not a valid operator %s'%str(top)

def push_operator(operator, operand, op):
    if not operator.is_empty():
        top = operator.top()
        while precedence[top[1]] > precedence[op[1]]:
            pop_operator(operator, operand)
            top = operator.top()
            if top is None:
                break
    operator.push(op)
    
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
    
    