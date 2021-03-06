""" Compute the set of free variables of of a program. 
    Simple recursive functions over the AST
"""

def free_vars_exp(e):
    tag = e[0]
    if tag == 'INT':
        res = set()
    elif tag == 'IDENT':
        res = set([e[1]])
    elif tag == 'BINOP':
        res = free_vars_exp(e[2]).union(free_vars_exp(e[3]))
    else:
        print("don't know tag", tag, e)
        assert(False)
    return res

def free_vars_stm(p):
    tag = p[0]
    if tag == 'ASSIGN':
        res = free_vars_exp(p[2]).union(set([p[1]]))
    elif tag == 'WHILE':
        res = free_vars_exp(p[1]).union(_free_vars_block(p[2]))
    elif tag == 'IF':
        res = free_vars_exp(p[1])
        res = res.union(_free_vars_block(p[2])).union(_free_vars_block(p[3]))
    elif tag == 'SKIP':
        res = set()
    else:
        print("don't know tag", tag, p)
        assert(False)
    return res

def _free_vars_block(b):
    assert(b[0] == 'BLOCK')
    res = set()
    for s in b[1]:
        res = res.union(free_vars_stm(s))
    return res

def free_vars_prog(p):
    return _free_vars_block(p)
