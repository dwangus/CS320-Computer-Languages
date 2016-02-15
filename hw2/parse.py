#David Wang
#CS320, Lapets
#Fall 2015
#Assignment 2, parse.py

#Collaborated with Leda Karadimou, Jennifer Tsui, Yiannis Sakkaris

import re

def tokenize(csyntax):
    toke = ["number", "variable", "parens", "plus", "if", "true", "false", "mult", "nonzero", "not", "and", "assign", "print", "until", "end", "{", "}", ";", "+", "*", "equal", "greater", "less", "(", ")"]
    #for the toke-array, must add or change it according to different abstract syntax trees w/ different keywords
    escape = (re.escape(x) for x in toke)
    regex = "(\s+|"
    regex += "|".join(escape)
    regex += ")"
    tokenlist = [t for t in re.split(regex, csyntax) if not t.isspace() and not t == "" and not t==None]
    return tokenlist



#1a variable() and number()
def variable(toke,top=True):
    if re.match(r"^[a-z]\w*$", toke[0]):
        return (str(toke[0]), toke[1:])
    else:
        return None
def number(toke,top=True):
    if re.match(r"^[0-9]+$", toke[0]):
        return (int(toke[0]), toke[1:])
    else:
        return (None)



#1b formula()
def formula(holder, top = True):
    toke = holder[0:]
    r = leftForm(toke)
    if not r is None:
        (expression1, toke) = r
        if len(toke) > 0:
            if toke[0] == 'and':
                toke = toke[1:]
                r = formula(toke, False)
                if not r is None:
                    (expression2, toke) = r
                    if not top or len(toke) == 0:
                        return ({'And':[expression1, expression2]}, toke)
    if not top or len(toke) == 0:
        return (r) 
    return (None)
#helper expression for left-recursion elimination on tree, solely for formula
def leftForm(toke):
    if toke[0] == 'true':
        return ('True', toke[1:])
    if toke[0] == 'false':
        return ('False', toke[1:])
    if len(toke)>1:
        if toke[0] == 'not'and toke[1] == '(':
            toke = toke[2:]
            r = formula(toke, False)
            if not r is None:
                (expression1, toke) = r
                if toke[0] == ')':
                    toke = toke[1:]
                    return ({'Not': [expression1]}, toke)
    if len(toke)>1:
        if toke[0] == 'nonzero' and toke[1] == '(':
            toke = toke[2:]
            r = term(toke, False)
            if not r is None:
                (expression1, toke) = r
                if toke[0] == ')':
                    toke = toke[1:]
                    return ({'Nonzero': [expression1]}, toke)
    #extra-credit option, extending parsing algorithm for tree node labels 'Greater', 'Lesser', and 'Equal'          
    if len(toke)>1:
        if toke[0] == '(':
            toke=toke[1:]
            r=term(toke,False)
            if not r is None:
                (expression1,toke)= r
                if toke[0]=='=':
                    toke=toke[1]
                    r=term(toke,False)
                    if not r is None:
                        (expression2,toke)=r
                        if toke[0]==')':
                            return({'Equal':[expression1,expression2]})
                if toke[0]=='>':
                    toke=toke[1]
                    r=term(toke,False)
                    if not r is None:
                        (expression2,toke)=r
                        if toke[0]==')':
                            return({'Greater':[expression1,expression2]})
                if toke[0]=='<':
                    toke=toke[1]
                    r=term(toke,False)
                    if not r is None:
                        (expression2,toke)=r
                        if toke[0]==')':
                            return({'Less':[expression1,expression2]})
                
    r = variable(toke)
    if re.match(r"^[a-z]\w*$", toke[0]):
        (expression1, toke)=variable(toke[0:], False)
        return ({"Variable":[expression1]}, toke[0:])
    else:
        return (None,toke[0:])



#1c term()
def term(holder, top = True):
    toke = holder[0:]
    r = factor(toke, False)
    if not r is None:
        (expression1, toke) = r
        if len(toke) > 0:
            if toke[0] == '+':
                toke = toke[1:]
                r = term(toke, False)
                if not r is None:
                    (expression2, toke) = r
                    if not top or len(toke) == 0:
                        return ({'Plus': [expression1, expression2]}, toke)
    if not top or len(toke) == 0:
        return (r)
    return (None)
#helper function for returning factor part of tree for term()
def factor(holder, top = True):
    toke = holder[0:]
    r = leftFact(toke)
    if not r is None:
        (expression1, toke) = r
        if len(toke) > 0:
            if toke[0] == '*':
                toke = toke[1:]
                r = factor(toke, False)
                if not r is None:
                    (expression2, toke) = r
                    if not top or len(toke) == 0:
                        return ({'Mult':[expression1, expression2]}, toke)
    if not top or len(toke) == 0:
        return (r)
    return (None)
#helper function for implementing left-recursion elimination, solely for term()
def leftFact(toke):
    if toke[0] == 'if' and toke[1] == '(':
        toke= toke[2:]
        r=formula(toke,False)
        if not r is None:
            (expression1,toke)=r
            if toke[0]==',':
                toke=toke[1:]
                r=term(toke,False)
                if not r is None:
                    (expression2,toke)=r
                    if toke[0]==',':
                        toke=toke[1:]
                        r=term(toke,False)
                        if not r is None:
                            (expression3,toke)=r
                            if toke[0]==')':
                                toke=toke[1:]
                                return ({'If': [expression1,expression2,expression3]},toke)
    if toke[0] == '(':
        toke = toke[1:]
        r = term(toke, False)
        if not r is None:
            (expression1, toke) = r
            if toke[0] == ')':
                toke = toke[1:]
                return ({'Parens':[expression1]}, toke)
    r = variable(toke)
    if not r is None:
        (expression1, toke) = r
        return ({'Variable':[expression1]}, toke)
    r = number(toke)
    if not r is None:
        (expression1, toke) = r
        return ({'Number':[expression1]}, toke)



#1d program()    
def program(holder, top = True):
    toke = holder[0:]
    if len(toke) > 0:
        if toke[0] == 'print':
            toke = toke[1:]
            r = expr(toke)
            if not r is None:
                (expression1, toke) = r
                if toke[0] == ';':
                    toke = toke[1:]
                    r = program(toke, False)
                    if not r is None:
                        (expression2, toke) = r
                        if not top or len(toke) == 0:
                            return ({'Print':[expression1, expression2]}, toke)

    toke = holder[0:]
    if len(toke) > 0:
        if toke[0] == 'assign':
            toke = toke[1:]
            r = (variable(toke))
            if not r is None:
                (expression1, toke) = r
                if toke[0] == ':=':
                    toke = toke[1:]
                    r = expr(toke,False)
                    if not r is None:
                        (expression2, toke) = r
                        if toke[0] == ';':
                            toke = toke[1:]
                            r = program(toke, False)
                            if not r is None:
                                (expression3, toke) = r
                                if not top or len(toke) == 0:
                                    if expression1==None:
                                        return None
                                    if expression2==None:
                                        return None
                                    if expression3==None:
                                        return None
                                    else:
                                        return ({'Assign':[{'Variable':[expression1]}, expression2, expression3]}, toke)

    toke = holder[0:]
    if len(toke) > 0:
        if toke[0] == 'if':
            toke = toke[1:]
            r = expr(toke,False)
            if not r is None:
                (expression1, toke) = r
                if toke[0] == '{':
                    toke = toke[1:]
                    r = program(toke, False)
                    if not r is None:
                        (expression2, toke) = r
                        if toke[0] == '}':
                            toke = toke[1:]
                            r = program(toke, False)
                            if not r is None:
                                (expression3, toke) = r
                                if not top or len(toke) == 0:
                                    if expression1==None:
                                        return None
                                    if expression2==None:
                                        return None
                                    if expression3==None:
                                        return None
                                    else:
                                        return ({'If':[expression1, expression2, expression3]}, toke)

                
                
            
    toke = holder[0:]
    if len(toke) > 0:
        if toke[0] == 'do' and toke[1]=='{':
            toke = toke[2:]
            r = program(toke,False)
            if not r is None:
                (expression1, toke) = r
                if toke[0] == '}' and toke[1]=='until':
                    toke = toke[2:]
                    r = expr(toke, False)
                    if not r is None:
                        (expression2, toke) = r
                        if toke[0] == ';':
                            toke = toke[1:]
                            r = program(toke, False)
                            if not r is None:
                                (expression3, toke) = r
                                if not top or len(toke) == 0:
                                    if expression1==None:
                                        return None
                                    if expression2==None:
                                        return None
                                    if expression3==None:
                                        return None
                                    else:
                                        return({'DoUntil':[expression1, expression2, expression3]}, toke)

   
    toke = holder[:]
    if len(toke) == 0 or toke[0] == '}':
        return ('End', toke)
    return (None)
#helper function expr for differentiating between formula() and term() function calls
def expr(holder,top=True):
    toke = holder[0:]
    r = formula(toke, False)
    if not r is None:
        (expression1, toke) = r
        if len(toke) == 0 or toke[0] == ';' or toke[0] == '{':
            return (expression1, toke)
    
    toke = holder[0:]
    r = term(toke, False)
    if not r is None:
        (expression1, toke) = r
        if len(toke) == 0 or toke[0] == ';' or toke[0] == '{':
            return (expression1, toke)
#eof
