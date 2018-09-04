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
        res = []
        for k in d.keys():
            if e in d[k]:
                res.append(k)
        return res
    
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
    #      := unary part 
    
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
    elif next_tok[0] == 'unary':
        # part := unary part
        push_operator(operator, operand, next_tok)
        idx += 1
        idx = part(operator, operand, tokens,  idx)
    elif next_tok[0] == 'func':
        # part := func "(" (expr ,)* expr ")"
        
        idx += 1
        tokens_in_para = tokens[idx+1:find_match(tokens, idx)]
        args = [[]]
        
        for tok_type, tok in tokens_in_para:
            if tok_type == 'comma':
                args.append([])
            else:
                args[-1].append((tok_type, tok))
        
        args = [recursive_descent(arg) for arg in args]
        idx = find_match(tokens, idx)
        
        operand.push(Tree(root=next_tok, children = args))
        
    else:
        assert False, 'Something wrong at %s'%str(tokens[idx])
    return idx
    
def pop_operator(operator, operand):
    top = operator.pop()
    if top[1] in ['+', '*', '/', '^', '-']:
        arg1 = operand.pop()
        arg2 = operand.pop()
        operand.push(Tree(root = top, children = [arg2, arg1]))
    elif top[1] in ['unary -',]:
        arg1 = operand.pop()

        if isinstance(arg1, Tree):
            if (arg1.children == [] and arg1.root[0] == 'num'):
                operand.push(Tree(root = ('num', '-%s'%arg1.root[1])))
            else:
                operand.push(Tree(root = ('op', '*'), \
                        children = [Tree(root = ('num', -1)), 
                                        arg1]))
        else:   
            operand.push(Tree(root = ('num', '-%s'%arg1[1])))
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
    return recursive_descent(list(compress_tok(tokenizer(eq))))
    
def calculate(equation):
    return 
    

def differentiate(formula, variable = 'x', debug = False):
    
    args = [variable, debug]
    cur_tree = formula
    if debug:
        print(cur_tree)
    
        res = Tree(None, children = [])
    if cur_tree.root[0] == 'op':
        if cur_tree.root[1] in ['+', '-']:
            res.root = cur_tree.root
            children = []
            for child in cur_tree.children:
                children.append(differentiate(child, *args))
            res.children = children
        elif cur_tree.root[1] == '*':
            res = Tree(None)
            '''
            (f1*f2*...*fn)' = f1'*f2*f3*...*fn +
                              f1*f2'*f3*...*fn + 
                              ...
                              f1*f2*f3*...*fn'
            '''
            res.root = ('op', '+')
            children = []
            for i in range(len(cur_tree.children)):
                tmp_children = []
                for j, child in enumerate(cur_tree.children):
                    if i == j:
                        tmp_children.append(differentiate(child, *args))
                    else:
                        tmp_children.append(child)
                children.append(Tree(('op', '*'), tmp_children))
            res.children = children            
        elif cur_tree.root[1] == '/':
            '''
            (f1/f2/f3/.../fn) = (f1*f3*...)/(f2*f4*...)
            (f/g)' = (f'g-g'f)/g^2
            '''
            top_children = []
            bottom_children = []
            for idx, child in enumerate(cur_tree.children):
                if idx%2==0:
                    top_children.append(child)
                else:
                    bottom_children.append(child)
            if len(top_children) != 1:
                top = Tree(('op', '*'), top_children)
            else:
                top = top_children[0]
            if len(bottom_children) != 1:    
                bottom = Tree(('op', '*'), bottom_children)
            else:
                bottom = bottom_children[0]
            top_diff = differentiate(top, *args) 
            bottom_diff = differentiate(bottom, *args) 
            
            
            res = Tree(('op', '/'), children = [\
                Tree(('op', '-'), [\
                    Tree(('op', '*'), [\
                        top_diff, 
                        bottom]), 
                    Tree(('op', '*'), [\
                        top, 
                        bottom_diff]),]),
                Tree(('op', '^'), [\
                    bottom, 
                    Tree(('num', '2'))])])
                    
                    
            
        elif cur_tree.root[1] == '^':
            if len(cur_tree.children) != 2:
                f = cur_tree.children[-1]
                g = Tree(('op', '^'), [cur_tree.children[:-1]])
                return differentiate(Tree(('op', '^'), [g,f]), *args)
            f = cur_tree.children[0]
            g = cur_tree.children[1]
            f_diff = differentiate(f, *args)
            g_diff = differentiate(g, *args)
            
            # (f^g)' = f^g ( g' ln f + gf'/f )
            res = Tree(('op', '*'), [\
                Tree(('op', '^'), [f ,g ]), 
                Tree(('op', '+'), [\
                    Tree(('op', '*'), [\
                        g_diff , 
                        Tree(('func', 'ln'), [f ]),]), 
                    Tree(('op', '/'), [\
                        Tree(('op', '*'), [\
                            g , 
                            f_diff , ],), 
                        f ,])])])
                        
            
            
    elif cur_tree.root[0] == 'func':
        NotImplemented
            
    elif cur_tree.root[0] == 'num':
        res = Tree(('num', '0'))
    elif cur_tree.root[0] == 'var':
        
        if cur_tree.root[1] == variable:
            res = Tree(('num', '1'))
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
    