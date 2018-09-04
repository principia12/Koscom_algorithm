import re
import math
from Stack import Stack
from Tree import Tree


FUNCTION_DICT = {\
    'cos' : (math.cos, math.sin, 
                      '-1*sin(placeholder)'),
    'sin' : (math.sin, lambda x:math.cos(x), 
                       'cos(placeholder)',),
    'tan' : (math.tan, lambda x:1/(math.cos(x)**2), 
                       '1/cos(placeholder)^2'),
    'ln' : (math.log, lambda x:1/x, 
                      '1/placeholder'),
    # constants are also considered as functions! 
    'e' : (lambda : math.e, lambda : 0, '0'),
    'pi' : (lambda : math.pi, lambda : 0, '0'),
    
    # custom functions 
    }

precedence = {\
    '+' : 1, 
    '-' : 1, 
    '*' : 2, 
    '/' : 2, 
    '^' : 3, 
    'unary -' : 4}
    
def tokenizer(equation):
    left = equation.replace(' ', '')
    tokens = {\
        'op' : ['^', '+', '-', '*', '+', '/'],
        'unary' :  ['-'],
        'para' : ['(', ')'],
        'num' : [r"[1-9][0-9]*\.?[0-9]*|0",],
        'var' : [r"[a-zA-Z]+_?[0-9]*",], 
        'comma' : [',']}
    
    #tok_strings = tokens['op'] + tokens['unary'] + \
    #    tokens['para'] + tokens['num'] + tokens['var'] 
    tok_strings = []
    for k in tokens.keys():
        tok_strings.extend(tokens[k])
    num_flag = False
    def find_key_from_elem(d, e):
        return None
    
    while left != '':
        for tok in tok_strings:
            if tok in tokens['num']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('num', left[m.start():m.end()]))
                    left = left[m.end():]
                    num_flag = True
            elif tok in tokens['comma']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('comma', left[m.start():m.end()]))
                    left = left[m.end():]
            elif tok in tokens['var']:
                if re.match(tok, left) is not None:
                    m = re.match(tok, left)
                    yield (('var', left[m.start():m.end()]))
                    left = left[m.end():]
                    num_flag = True
            else:
                if left.startswith(tok):
                    k = find_key_from_elem(tokens, tok)
                    
                    if len(k) == 1:
                        yield (k[0], left[0])
                    else:
                        if num_flag:
                            yield ('op', '+')
                            yield ('unary', 'unary %s'%left[0])
                        else:
                            yield ('unary', 'unary %s'%left[0])
                    left = left[1:]        
                    num_flag = False
                    
    
def compress_tok(tokenizer):
    for tok_type, tok in tokenizer:
        if tok_type == 'var' and tok in FUNCTION_DICT.keys():
                yield ('func', tok)
        else:
            yield (tok_type, tok)
            
    
def recursive_descent(tokens):
    
    operator = Stack()
    operand = Stack()
    idx = expr(operator, operand, tokens, 0)
    res = operand.pop()
    
    return res

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
    elif next_tok[0] == 'unary':
        # part := unary part
        pass
    elif next_tok[0] == 'func':
        # part := func "(" (expr ,)* expr ")"
        pass
    else:
        assert False, 'Something wrong at %s'%str(tokens[idx])
    
    return idx
    
def pop_operator(operator, operand):
    pass

def push_operator(operator, operand, op):
    pass
    
def parse(eq):
    return recursive_descent(list(compress_tok(tokenizer(eq))))
    

def differentiate(formula, variable = 'x', debug = False):
    
    args = [variable, debug]
    cur_tree = formula
    
    res = Tree(None, children = [])
    if cur_tree.root[0] == 'op':
        if cur_tree.root[1] in ['+', '-']:
            pass
        elif cur_tree.root[1] == '*':
            '''
            (f1*f2*...*fn)' = f1'*f2*f3*...*fn +
                              f1*f2'*f3*...*fn + 
                              ...
                              f1*f2*f3*...*fn'
            '''
            pass
        elif cur_tree.root[1] == '/':
            '''
            (f1/f2/f3/.../fn) = (f1*f3*...)/(f2*f4*...)
            (f/g)' = (f'g-g'f)/g^2
            '''
            pass        
        elif cur_tree.root[1] == '^':
            pass
    elif cur_tree.root[0] == 'func':
        pass
            
    elif cur_tree.root[0] == 'num':
        pass
    elif cur_tree.root[0] == 'var':
        if cur_tree.root[1] == variable:
            pass
        else:
            res = Tree(('num', '0'))
        
    
    return res
    

    
        
if __name__ == '__main__':
    
    # tests, tests, more tests! 
    
    # simple numbers
    eq1 = '(1)'
    eq2 = '3'
    eq3 = '-1'
    
    # +,- 
    eq4 = '1+1'
    eq5 = '1-1-2' # check
    eq6 = '-1-2-3-4-5'
    
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
    eq22 = '3*(-2+1)'
    eq23 = '-3-2^3'
    eq24 = '-3-2^(3+2)'
    eq25 = '-2^3'
    eq26 = '-2^-3'
    
    # +,-,*,/ with nested (,)
    eq27 = '-1+(-1-2)'
    eq28 = '-(2+2)'
    eq29 = '3+(2^(-(2+2)))'
    eq30 = '3*(2*2+1)'
    eq31 = '2-3*(2*2+1)'
    eq32 = '2-3*(2*(2+1))'
    eq33 = '((3+2)*4-(2*4+2^(2-5)))*(2+(3+2)*5^2)'
    eq34 = '2+(3+2)*5^2'
    eq35 = '1+2^2*1'
    
    eq36 = 'x/2'
    eq37 = '-x_0*z+y'
    eq40 = '1+3^3*c'
    eq45 = 'a+b+C+d+f+g+h'
    eq46 = '1'
    eq47 = '0'
    
    eq48 = 'sin(x+y)'
    
    
    for i in range(100):
        try:
            eq = eval('eq%d'%i)
        except NameError:
            continue
        print('=============')
        print(eq)
        for t, tok in compress_tok(tokenizer(eq)):
            print(t, tok)
        print(parse(eq))
        print('=============')
    print(differentiate(parse(eq36)))
    