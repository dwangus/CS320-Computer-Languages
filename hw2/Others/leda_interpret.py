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
                #print(t)
                #print(t[label])
                print(len(env))
                print(len(t))
                print(env)
                if env=={}:
                    return ({'Number':[children[0]]})
                else:
                    return (children[0])
            #return ({'Number':[children[0]]})
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
                v2 = evalTerm(env, t2)
                t1 = children[0]
                v1 = evalTerm(env, t1)
                return v1+v2
            elif label == 'Mult':
                t2 = children[1]
                v2 = evalTerm(env, t2)
                t1 = children[0]
                v1 = evalTerm(env, t1)
                return v1*v2
