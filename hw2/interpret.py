#David Wang
#CS320, Lapets
#Fall 2015
#Assignment 2, interpret.py

#Collaborated with Leda Karadimou, Jennifer Tsui, Yiannis Sakkaris

# How the check function works:
#   It executes the test-function with an array of test cases
#       Each test case comes in a tuple-pair of (inputs, outputs/results)
#           For execProgram, each input/output data structure comes in a tuple-pair of itself
#               Each tuple-pair contains (environment, output)
#                   Each environment data structure is, itself, a dict of (key,value) pairs -- of (variable_name, value)
#                   Each output data structure is an array of previously outputted values of varying types/tokens
#                       Outputted values can be 'True'/'False' string or a 'Number' dict
#                           'Number' dict data structures associate simply the string-key 'Number' with the specific value-integer (that is, Number(key,value) ==> (string 'Number',int some_token_number))

#Issues to work out:
#   - should probably substitute in, under the evalTerm's 'If' token_label, to evaluate the first child as a formula rather than just straight-assume it's a variable
#   - also worried about expression ::= formula | term ...
#           - there is no way to decide between the two, and all the test cases for execProgram::= ... only ever solicit evalFormula recursive calls...
#             (and also, evalFormula and evalTerm recursive functions calls call two separate functions -- there are no tokens distinguishing between the two, and you can't get to a Number-dict
#             through evalFormula... so what to do?)
#           - Maybe I have to replace evalFormula() calls in execProgram with a new function choosing either evalFormula() or evalTerm()... but how?
#           - Alright, so at least I know that the 'If' and 'DoUntil' token_lavels for execProgram will ALWAYS use formula expressions...
#             The vulnerable parts are with 'Print' and 'Assign'... Alright, so print can directly access a variable through formula regardless of its type, so that's good. But print can't 
#             directly access a Number-dict otherwise, that'd only be returned/recognized from evalTerm... The same problem exists with assign...
#           - POSSIBLE SOLUTION: at the end of evalFormula, as a trigger, if it executes and returns no matching tokens, it immediately runs evalTerm (nested function call)

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
                varf = children[0]   
                t1 = children[1]
                t2 = children[2]
                vvarf = evalFormula(env, varf)
                if (vvarf == 'True'):
                    return evalTerm(env, t1)
                elif (vvarf == 'False'):
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

#tokens to look for: "Variable", "True", "False", "Nonzero", "And", "Not"
#the sole purpose of evalFormula is to return a 'True' or a 'False'
def evalFormula(env, f):
    #flag to create an expression by nesting an evalTerm function call as a failsafe at the end of evalFormula
    #thus, essentially, formula == expression (it accounts for both formulas and terms)
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
            #extra-credit option, extending evaluation algorithms (for just evalFormula) for token-labels 'Greater', 'Lesser', and 'Equal'
            elif token_label == 'Greater':  # term > term
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                num1 = v1['Number'][0]
                num2 = v2['Number'][0]
                if num1 > num2 :
                    return 'True'
                elif num1 <= num2 :
                    return 'False'
            elif token_label == 'Lesser':   # term < term
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                num1 = v1['Number'][0]
                num2 = v2['Number'][0]
                if num1 < num2 :
                    return 'True'
                elif num1 >= num2 :
                    return 'False'
            elif token_label == 'Equal':    # term = term
                t1 = children[0]
                t2 = children[1]
                v1 = evalTerm(env, t1)
                v2 = evalTerm(env, t2)
                num1 = v1['Number'][0]
                num2 = v2['Number'][0]
                if num1 == num2 :
                    return 'True'
                elif num1 != num2 :
                    return 'False'
    elif type(f) == Leaf:
        flag = False
        if f == 'True':
            return 'True'
        if f == 'False':
            return 'False'
    if (flag == False):
        return evalTerm(env, f)

#tokens to look for: "Print", "Assign", "If", "DoUntil", "End"
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

def interpret(string):
    parse_tree = program(tokenize(string))
    if parse_tree[1] == None:
        return None
    else:
        (env, output) = execProgram({}, parse_tree[0])
        return output

#eof
























