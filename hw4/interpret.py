#####################################################################
# David Wang
# CAS CS 320, Fall 2015
# Assignment 4
# interpret.py
#

exec(open('parse.py').read())

Node = dict
Leaf = str

def subst(s, a):
    if type(a) == Node:
        for label in a:
            children = a[label]
            if label == 'Variable':
                var = children[0]
                if var in s:
                    return s[var]
                else:
                    return a
            elif label == 'Number':
                return a
            elif label != 'Variable':
                new = []
                for args in children:
                    new.append(subst(s,args))
                return {label:new}
    return a

def unify(a, b):
    if type(a) == Leaf and type(b) == Leaf and a == b:
        return {}
    elif type(a) == Node and len(a) == 1 and 'Variable' in a:
        var = a['Variable'][0]
        #print({var:b})
        return {var:b}
    elif type(b) == Node and len(b) == 1 and 'Variable' in b:
        var = b['Variable'][0]
        #print({var:a})
        return {var:a}
    elif type(b) == Node and type(a) == Node:
        alabel = list(a.keys())[0]
        blabel = list(b.keys())[0]
        combined = {}
        if alabel == blabel and len(a[alabel]) == len(b[blabel]):
            for index in range(len(a[alabel])):
                matching = unify(a[alabel][index],b[blabel][index])
                if matching is None:
                    return None
                if matching:
                    for label in matching:
                        if label in combined:
                            return None
                    combined.update(matching)
        elif alabel != blabel:
            return None
        #print(combined)
        return combined

def build(m, d):
    if type(d) == Node:
        for label in d:
            children = d[label]
            if label == 'Function':
                name = children[0]['Variable'][0]
                patt = children[1]
                expr = children[2]
                decl = children[3]
                if name in m:
                    m[name].append((patt,expr))
                    m2 = build(m,decl)
                    return m2
                else:
                    m[name] = [(patt,expr)]
                    m2 = build(m,decl)
                    return m2
    elif type(d) == Leaf:
        if d == 'End':
            return m
  
def evaluate(m, env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number' or label == 'ConBase':
                return e
            elif label == 'Variable':
                var = children[0]
                if var in env:
                    return env[var]
                else:
                    print(x + " is unbound/not defined.")
                    exit()
            elif label == 'Mult':
                e1 = children[0]
                e2 = children[1]
                t1 = evaluate(m,env,e1)
                t2 = evaluate(m,env,e2)
                num1 = t1['Number'][0]
                num2 = t2['Number'][0]
                product = num1 * num2
                return {'Number':product}
            elif label == 'ConInd':
                c = children[0]
                e1 = children[1]
                e2 = children[2]
                v1 = evaluate(m,env,e1)
                v2 = evaluate(m,env,e2)
                return {'ConInd': [c,v1,v2]}
            elif label == 'Apply':
                func = children[0]['Variable'][0]
                expr = children[1]
                val = evaluate(m,env,expr)
                tuplist = m[func]
                sizes = []
                smallest = 'None'
                for index in range(len(tuplist)):
                    length = unify(tuplist[index][0],val)
                    if length is None:
                        sizes.append("None")
                    else:
                        sizes.append(len(length))
                for index in range(len(sizes)):
                    if sizes[index] == 'None':
                        continue
                    elif sizes[index] >= 0 and smallest == 'None':
                        smallest = index
                    elif sizes[index] < sizes[smallest]:
                        smallest = index
                sub = unify(tuplist[smallest][0],val)
                env.update(sub)
                val2 = evaluate(m,env,tuplist[smallest][1])
                return val2
                    #if (val == tuplist[index][0] and not sub) or sub: #sub can be None (AKA no unified matching between val and the pattern (AKA tup[0])), an empty dict {} (which means that the smallest substitution is 0), or a non-empty substitution
                    #    env.update(sub)
                    #    val2 = evaluate(m,env,tuplist[index][1])
                    #    return val2
                
def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof
