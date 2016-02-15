#####################################################################
# David Wang
# CAS CS 320, Fall 2015
# Midterm
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open('parse.py').read())
exec(open('analyze.py').read())

Node = dict
Leaf = str

def evalExpression(env, e):
    if type(e) == Leaf:
        if e == 'True':
            return 'True'
        if e == 'False':
            return 'False'
    if type(e) == Node:
        for token_label in e:
            children = e[token_label]
            if token_label == 'Element':
                varf = children[0]
                exp = children[1]
                varname = evalExpression(env, varf)
                i = evalExpression(env, exp)
                index = i['Number'][0]
                if index >= 0 and index <= 2:
                    x = varname[index]
                    return (x)
                else:
                    print("Accessing out-of-bounds index in array.")
                    exit()
            elif token_label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                num1 = evalExpression(env, e1)
                num2 = evalExpression(env, e2)
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
                return e

def execProgram(env, s):
    #if not env:
    #    wellTyped = typeProgram({},s)
    #    if wellTyped == None:
    #        return({},[None])
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                e = children[0]
                p = children[1]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            elif label == 'Assign':
                var = children[0]['Variable'][0]
                e1 = children[1]
                e2 = children[2]
                e3 = children[3]
                p = children[4]
                num1 = evalExpression(env, e1)
                num2 = evalExpression(env, e2)
                num3 = evalExpression(env, e3)
                env[var] = [num1,num2,num3]
                return execProgram(env, p)
            elif label == 'Loop':
                var = children[0]
                varname = children[0]['Variable'][0]
                numdict = children[1]
                iterate = children[1]['Number'][0]
                pbody = children[2]
                prest = children[3]
                if iterate < 0:
                    env[varname] = {'Number':[iterate]}
                    (env2, o1) = execProgram(env, prest)
                    return (env2, o1)
                else:
                    env[varname] = numdict
                    (env2, o1) = execProgram(env,pbody)
                    iterate = env[varname]['Number'][0]
                    nprime = {'Number':[(iterate - 1)]}
                    nextloop = {'Loop': [var,nprime,pbody,prest]}
                    (env3, o2) = execProgram(env2, nextloop)
                    return (env3, o1 + o2)

def interpret(s):
    parseTree = tokenizeAndParse(s)
    wellTyped = typeProgram({},parseTree)
    if wellTyped == None:
        #print("It ain't well-typed! Fix yo shit!")
        #exit()
        return None
    (env,o) = execProgram({},parseTree)
    return (o)

#eof
