import re
exec(open('parse.py').read())

def check(name, function, inputs_result_pairs):
    def str_(s):
        return '"'+str(s)+'"' if type(s) == str else str(s)
    if type(name) == tuple:
        prefix = name[0]
        suffix = name[1]
    if type(name) == str:
        prefix = name + '('
        suffix = ')'

    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            output = function(inputs[0], inputs[1]) if len(inputs) == 2  else function(inputs[0])
        except:
            output = '<Error>'

        if output != '<Error>' and output == result:
            passed = passed + 1
        else:
            print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str_(result)+"\n\n"+"  Returned:\n    "+str_(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

Node = dict
Leaf = str
#2a
"""
def evalTerm(env, t):
    if type(t) == Node:
        v = evalTerm2(env, t)
    return {'Number':[v]}

def evalTerm2(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                return children[0]
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return evalTerm2(env, env[x])
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Parens':
                f = children[0]
                return evalTerm2(env, f)
            elif label == 'If':
                f = evalTerm2(env, children[0])
                if f == "True":
                    return evalTerm2(env, children[1])
                if f == "False":
                    return evalTerm2(env, children[2])
            elif label == 'Plus':
                f1 = children[0]
                f2 = children[1]
                # Implement without helper method such that values are taken out
                # for Plus and Mult and then added together
                v1 = evalTerm2(env, f1)
                v2 = evalTerm2(env, f2)
                return v1 + v2
            elif label == 'Mult':
                f1 = children[0]
                f2 = children[1]
                v1 = evalTerm2(env, f1)
                v2 = evalTerm2(env, f2)
                return v1 * v2
    elif type(t) == Leaf:
        if t == 'True':
            return 'True'
        if t == 'False':
            return 'False'
"""
def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]

            if label == 'Number':
                print(({'Number':[children[0]]}))
                return ({'Number':[children[0]]})
                #print(t)
                #print(t[label])
                """print(len(env))
                print(len(t))
                print(env)
                if env=={}:
                    return ({'Number':[children[0]]})
                else:
                    return (children[0])
                #return ({'Number':[children[0]]})"""
            elif label == 'Variable':
                t = children[0]
                v = env[t]
                return v
            elif label == 'Parens':
                t = children[0]
                v = evalTerm(env, t)
                return v
            elif label == 'If':
                [cond, body, rest] = s[label]
                env1 = env
                v = evaluate(env1, cond)
                if v == 'False':
                    #(env2, o1) = execute(env1, rest)
                    (env2, o1) = execProgram(env1, rest)
                    return (env2, o1)
                if v == 'True':
                    #(env2, o1) = execute(env1, rest)
                    (env2, o1) = execProgram(env1, rest)
                    return (env2, o1)
            elif label == 'Plus':
                t2 = children[1]
                v2=evalTerm(env,t2[1])
                #v2 = evalTerm(env, t2)
                t1 = children[0]
                v1=evalTerm(env,t1[1])
                #v1 = evalTerm(env, t1)
                return v1+v2
            elif label == 'Mult':
                t2 = children[1]
                v2=evalTerm(env,t2[1])
                #v2 = evalTerm(env, t2)
                t1 = children[0]
                v1=evalTerm(env,t1[1])
                #v1 = evalTerm(env, t1)
                return v1*v2



#2b
def vand(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True':  return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'

def vnot(v):
    if v == 'True':  return 'False'
    if v == 'False': return 'True'
    
def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                m = children[0]
                return env[m]
            elif label == 'Not':
                m = children[0]
                n = evalFormula(env, m)
                #return not n
                return vnot(n)
            elif label == 'And':
                f1 = children[0]
                f2 = children[1]
                v1 = evalFormula(env, f1)
                v2 = evalFormula(env, f2)
                return vand(v1,v2)
            elif label == 'Nonzero':
                m = children[0]
                v = evalTerm(env, m)
                if v == 0:
                    return 'False'
                else:
                    return 'True'
            
    elif type(f) == Leaf:
        if f == 'True':
            return 'True'
        elif f == 'False':
            return 'False'

def execProgram(env,s):
    if type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                m = children[0]
                n = children[1]
                eval = evalTerm(env, m)
                if eval is None:
                    eval = evalFormula(env, m)
                (env, o) = execProgram(env, n)
                return (env,[eval] + o)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                m = children[1]
                n = children[2]
                eval = evalFormula(env, m)
                if eval is None:
                    eval = evalTerm(env, m)
                env[x] = eval
                return execProgram(env, n)
            elif label == 'If':
                children = s[label]
                m = children[0]
                n1 = children[1]
                n2 = children[2]
                eval = evalTerm(env, m)
                if eval is None:
                    eval = evalFormula(env, m)
                if eval == False:
                    (env2, o1) = execProgram(env, n2)
                    return (env2 , o1)
                if eval == True:
                    (env2, o1) = execProgram(env, n1)
                    (env3, o2) = execProgram(env2, n2)
                    return (env3, o1 + o2)
            elif label == 'DoUntil':
                [cond, body, rest] = s[label]
                env1 = env
                v = evaluate(env1, cond)
                if v == 'False':
                    #(env2, o1) = execute(env1, rest)
                    (env2, o1) = execProgram(env1, rest)
                    return (env2, o1)
                if v == 'True':
                    #(env2, o1) = execute(env1, body)
                    #(env3, o2) = execute(env2, {'DoUntil':[cond, body, rest]})
                    (env2, o1) = execProgram(env1, body)
                    (env3, o2) = execProgram(env2, {'DoUntil':[cond, body, rest]})
                    return (env3, o1 + o2)

    elif type(s) == Leaf:
        if s == 'End':
            return (env, [])

           
def interpret(s):
    keywords = ["number", "variable", "parens", "plus", "if", "true", "false", "mult", "nonzero", "not", "and", "assign", "print", "until", "end", "{", "}", ";", "+", "*"]
    t = program(tokenize(keywords, s))
    (e1, tokens) = t
    if not t is None:
        (e1, tokens) = t
        r = execProgram({}, e1)
        if not r is None:
            (env, o) = r
            return o
    return (None)

















