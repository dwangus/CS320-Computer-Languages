#####################################################################
# David Wang
# CAS CS 320, Fall 2015
# Midterm
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

exec(open('parse.py').read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'TyBoolean'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'TyNumber'
            
            elif label == 'Variable':
                varname = children[0]
                if varname not in env:
                    return None
                    #print("Variable name not initialized.")
                    #exit()
                if env[varname] == 'TyNumber':
                    return env[varname]
                else:
                    #print("Loop-iterator must be of type Number.")
                    #print("Ain't using loop-numbers right!")
                    return None

            elif label == 'Element':
                varname = children[0]['Variable'][0]
                expr = children[1]
                if varname not in env:
                    return None
                    #print("Variable name not initialized.")
                    #exit()
                exprtype = typeExpression(env, expr)
                if env[varname] == 'TyArray' and exprtype == 'TyNumber':
                    return 'TyNumber'
                else:
                    #print("Variable-name %s not associated with type Array; element-index must be of type Number.") %(varname)
                    #print("Ain't accessing arrays right!")
                    return None

            elif label == 'Plus':
                expr1 = children[0]
                expr2 = children[1]
                exptype1 = typeExpression(env, expr1)
                exptype2 = typeExpression(env, expr2)
                if exptype1 == 'TyNumber' and exptype2 == 'TyNumber':
                    return 'TyNumber'
                else:
                    #print("+ requires arguments of type Number.")
                    #print("Ain't adding right!")
                    return None

def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'TyVoid'
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                expr = children[0]
                prog = children[1]
                exptype = typeExpression(env, expr)
                ptype = typeProgram(env, prog)
                if ptype == 'TyVoid' and (exptype == 'TyBoolean' or exptype == 'TyNumber'):
                    return 'TyVoid'
                else:
                    #print("Expression must be of either type Boolean or Number; subsequent program must be of type Void.")
                    #print("Ain't printing right!")
                    return None

            if label == 'Assign':
                [xTree, e0, e1, e2, p] = s[label]
                x = xTree['Variable'][0]
                e0t = typeExpression(env, e0)
                e1t = typeExpression(env, e1)
                e2t = typeExpression(env, e2)
                env[x] = 'TyArray'
                ptype = typeProgram(env, p)
                if ptype == 'TyVoid' and e0t == 'TyNumber' and e1t == 'TyNumber' and e2t == 'TyNumber':
                    return 'TyVoid'
                else:
                    #print("Array-expressions must be of type Number; subsequent program must be of type Void.")
                    #print("Ain't assigning right!")
                    return None

            if label == 'Loop':
                [xTree, nTree, body, rest] = s[label]
                x = xTree['Variable'][0]
                env[x] = 'TyNumber'
                ntype = typeExpression(env, nTree)
                if ntype != 'TyNumber':
                    #print("Must iterate with Numbers.")
                    #print("Ain't looping right!")
                    return None
                bodytype = typeProgram(env, body)
                resttype = typeProgram(env, rest)
                if bodytype == 'TyVoid' and resttype == 'TyVoid':
                    return 'TyVoid'
                else:
                    #print("Programs must return Void.")
                    #print("Ain't looping programs right!")
                    return None

#eof
