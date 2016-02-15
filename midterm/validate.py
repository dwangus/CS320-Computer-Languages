#####################################################################
# David Wang
# CAS CS 320, Fall 2015
# Midterm
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#

exec(open('analyze.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())

def convertValue(v):
    if type(v) == Leaf:
        if v == 'True':
            return 1
        elif v == 'False':
            return 0
    elif type(v) == Node:
        for label in v:
            children = v[label]
            if label == 'Number':
                return children[0]
    elif type(v) == None:
        return None

# Converts an output (a list of values) from the
# value representation to the machine representation
def convert(o):
    return [convertValue(v) for v in o]

def expressions(n):
    if n <= 0:
        []
    elif n == 1:
        return ['True', 'False',{'Number':[1]}]
    else:
        es = expressions(n-1)
        esN = []
        esN += [{'Element':[{'Variable':['a']},e]} for e in es]
        esf = es + esN
        esF = []
        for e in esf:
            wellTyped = typeExpression({},e)
            if wellTyped != None:
                esF.append(e)
        return esF

def programs(n):
    if n <= 0:
        []
    elif n == 1:
        return ['End']
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{'Print':[e,p]} for e in es for p in ps]
        psN += [{'Assign':[{'Variable':['a']},e1,e2,e3,p]} for e1 in es for e2 in es for e3 in es for p in ps]
        psN += [{'Loop':[{'Variable':['x']},n,p1,p2]} for n in es for p1 in ps for p2 in ps]
        psf = ps + psN
        psF = []
        for p in psf:
            wellTyped = typeProgram({},p)
            if wellTyped != None:
                psF.append(p)
        return psF
   
# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most k.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def exhaustive(k):
    for p in programs(k):
        try:
            if simulate(compileProgram({}, p)[1]) != convert(execProgram({}, p)[1]):
                print('\nIncorrect behavior on: ' + str(p))
        except:
            print('\nError on: ' + str(p))
print

#eof
