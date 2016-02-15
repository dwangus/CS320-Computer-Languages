Node = dict
Leaf = str

def evalTerm(env, t):
    if type(t) == Node:
        for token_label in t:
            children = t[token_label]
            if token_label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                num1 = evalTerm(env, t1)
                num2 = evalTerm(env, t2)
                v1 = num1['Number'][0]
                v2 = num2['Number'][0]
                v = [(v1 + v2)]
                return {'Number' : v}
            elif token_label == 'Mult':
                t1 = children[0]
                t2 = children[1]
                num1 = evalTerm(env, t1)
                num2 = evalTerm(env, t2)
                v1 = num1['Number'][0]
                v2 = num2['Number'][0]
                v = [(v1 * v2)]
                return {'Number' : v}
            elif token_label == 'Parens':
                t1 = children[0]
                return evalTerm(env, t1)
            elif token_label == 'If':
                var = children[0]   
                t1 = children[1]
                t2 = children[2]
                vvar = evalTerm(env, var)
                if (vvar == 'True'):
                    return evalTerm(env, t1)
                elif (vvar == 'False'):
                    return evalTerm(env, t2)
            elif token_label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound/not defined.")
                    exit()
            elif token_label == 'Number':
                return t

def evalFormula(env, f):
    flag = True
    if type(f) == Node:
        flag = False
        for token_label in f:
            children = f[token_label]
            if token_label == 'Nonzero':
                t1 = children[0]
                v1 = evalTerm(env, t1)
                if (v1['Number'][0] != 0):
                    return 'True'
                elif (v1['Number'][0] == 0):
                    return 'False'
            elif token_label == 'Not':
                f1 = children[0]
                v1 = evalFormula(env, f1)
                if v1 == 'True':
                    return 'False'
                elif v1 == 'False':
                    return 'True'
            elif token_label == 'And':
                f1 = children[0]
                f2 = children[1]
                v1 = evalFormula(env, f1)
                v2 = evalFormula(env, f2)
                if ((v1 == 'True') and (v2 == 'True')):
                    return 'True'
                else:
                    return 'False'
            elif token_label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound/not defined.")
                    exit()
    elif type(f) == Leaf:
        flag = False
        if f == 'True':
            return 'True'
        if f == 'False':
            return 'False'
    if (flag == False):
        return evalTerm(env, f)

def execProgram(env, s):
    if (type(s) == Leaf):
        if s == 'End':
            return (env, [])
    elif (type(s) == Node):
        for token_label in s:
            children = s[token_label]
            if token_label == 'Print':
                f = children[0]
                p = children[1]
                v1 = evalFormula(env, f)
                (env, o) = execProgram(env, p)
                return (env, [v1] + o)
            elif token_label == 'Assign':
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                v = evalFormula(env, f)
                env[x] = v
                return execProgram(env, p)
            elif token_label == 'If':
                f = children[0]
                body = children[1]
                rest = children[2]
                if (evalFormula(env, f) == 'False'):
                    (env2, o) = execProgram(env, rest)
                    return (env2, o)
                elif (evalFormula(env, f) == 'True'):
                    (env2, o1) = execProgram(env, body)
                    (env3, o2) = execProgram(env2, rest)
                    return (env3, o1 + o2)
            elif token_label == 'DoUntil':
                [body, condition, rest] = s[token_label]
                env1 = env
                (env2, o1) = execProgram(env1, body)
                v = evalFormula(env2, condition)
                if v == 'False':
                    (env3, o2) = execProgram(env2, {'DoUntil' : [body, condition, rest]})
                    return (env3, o1 + o2)
                if v == 'True':
                    (env3, o2) = execProgram(env2, rest)
                    return (env3, o1 + o2)
'''
def interpret(string):
    parse_tree = program(string)
    if parse_tree == None:
        return parse_tree
    else:
        output = execProgram(parse_tree)
        return output
'''
    





























