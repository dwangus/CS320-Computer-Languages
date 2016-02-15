#####################################################################
#
#David Wang
#CAS CS320, Lapets
#Fall 2015
#Assignment 3, interpret.py

exec(open('parse.py').read())

Node = dict
Leaf = str

#tokens to look for: "Plus", "Variable", "Number"
#the sole purpose of evalTerm is to return a Number-dict object
def evalTerm(env, t):
    if type(t) == Node:
        for token_label in t:
            children = t[token_label] #children is whatever (value, data structure, object, etc.) was associated with that token_label key in the dict
            if token_label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                num1 = evalTerm(env, t1)
                num2 = evalTerm(env, t2)
                v1 = num1['Number'][0]
                v2 = num2['Number'][0]
                v = [(v1 + v2)]
                return {'Number' : v}
            elif token_label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound/not defined.")
                    exit()
            elif token_label == 'Number':
                return t

#tokens to look for: "Variable", "True", "False", "Xor", "And", "Not"
#the sole purpose of evalFormula is to return a 'True' or a 'False'
def evalFormula(env, f):
    #flag to create an expression by nesting an evalTerm function call as a failsafe at the end of evalFormula
    #thus, essentially, formula == expression (it accounts for both formulas and terms)
    if type(f) == Node:
        for token_label in f:
            children = f[token_label]
            if token_label == 'Not':
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
            #extra-credit option
            elif token_label == 'Equal':
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                num1 = v1['Number'][0]
                num2 = v2['Number'][0]
                if (num1 == num2):
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
            elif token_label == 'Xor':
                t1 = children[0]
                t2 = children[1]
                v1 = evalFormula(env, t1)
                v2 = evalFormula(env, t2)
                if v1 == v2 :
                    return 'False'
                elif v1 != v2 :
                    return 'True'
    elif type(f) == Leaf:
        if f == 'True':
            return 'True'
        if f == 'False':
            return 'False'
    return evalTerm(env, f)			

#tokens to look for: "Print", "Assign", "If", "Until", "End", "Procedure", "Call"
#the sole purpose of evalFormula is to return a tuple-pair of (environment-dict{variable_name, value}, output-array of values [('True', 'False', or Number-dicts)])
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
            elif token_label == 'Until':
                [cond, body, rest] = s[token_label]
                env1 = env
                v = evalFormula(env1, cond)
                if v == 'True':
                    (env2, o1) = execProgram(env1, rest)
                    return (env2, o1)
                if v == 'False':
                    (env2, o1) = execProgram(env1, body)
                    (env3, o2) = execProgram(env2, {'Until':[cond, body, rest]})
                    return (env3, o1 + o2)
            elif token_label == 'Procedure':
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = p1
                return execProgram(env, p2)
            elif token_label == 'Call':
                x = children[0]['Variable'][0]
                xp1 = None
                if x in env:
                    xp1 = env[children[0]['Variable'][0]]
                else:
                    print(x + " is unbound/not defined.")
                    exit()
                p2 = children[1]
                env1 = env
                (env2, o1) = execProgram(env1, xp1)
                (env3, o2) = execProgram(env2, p2)
                return (env3, o1 + o2)
                    
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
