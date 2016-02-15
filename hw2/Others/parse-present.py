#David Wang

#Collaborated with Leda Karadimou, Jennifer Tsui, Yiannis Sakkaris

import re

def tokennize(csyntax):
    token = ["number", "variable", "parens", "plus", "if", "true", "false", "mult", "nonzero", "not", "and", "assign", "print", "until", "end", "{", "}", ";", "+", "*", "equal", "greater", "less", "(", ")"]
    escape = (re.escape(x) for x in token)
    regex = "(\s+|"
    regex += "|".join(escape)
    regex += ")"
    tokennlist = [t for t in re.split(regex, csyntax) if not t.isspace() and not t == "" and not t==None]
    return tokennlist

def variable(token,top=True):
    if re.match(r"^[a-z]\w*$", token[0]):
        return (str(token[0]), token[1:])
    else:
        return None
def number(token,top=True):
    if re.match(r"^[0-9]+$", token[0]):
        return (int(token[0]), token[1:])
    else:
        return (None)

def formula(temp, top = True):
    token = temp[0:]
    r = lForm(token)
    if not r is None:
        (e1, token) = r
        if len(token) > 0:
            if token[0] == 'and':
                token = token[1:]
                r = formula(token, False)
                if not r is None:
                    (e2, token) = r
                    if not top or len(token) == 0:
                        return ({'And':[e1, e2]}, token)
    if not top or len(token) == 0:
        return (r) 
    return (None)
def lForm(token):
    if token[0] == 'true':
        return ('True', token[1:])
    if token[0] == 'false':
        return ('False', token[1:])
    if len(token)>1:
        if token[0] == 'not'and token[1] == '(':
            token = token[2:]
            r = formula(token, False)
            if not r is None:
                (e1, token) = r
                if token[0] == ')':
                    token = token[1:]
                    return ({'Not': [e1]}, token)
    if len(token)>1:
        if token[0] == 'nonzero' and token[1] == '(':
            token = token[2:]
            r = term(token, False)
            if not r is None:
                (e1, token) = r
                if token[0] == ')':
                    token = token[1:]
                    return ({'Nonzero': [e1]}, token)       
    if len(token)>1:
        if token[0] == '(':
            token=token[1:]
            r=term(token,False)
            if not r is None:
                (e1,token)= r
                if token[0]=='=':
                    token=token[1]
                    r=term(token,False)
                    if not r is None:
                        (e2,token)=r
                        if token[0]==')':
                            return({'Equal':[e1,e2]})
                if token[0]=='>':
                    token=token[1]
                    r=term(token,False)
                    if not r is None:
                        (e2,token)=r
                        if token[0]==')':
                            return({'Greater':[e1,e2]})
                if token[0]=='<':
                    token=token[1]
                    r=term(token,False)
                    if not r is None:
                        (e2,token)=r
                        if token[0]==')':
                            return({'Less':[e1,e2]})
                
    r = variable(token)
    if re.match(r"^[a-z]\w*$", token[0]):
        (e1, token)=variable(token[0:], False)
        return ({"Variable":[e1]}, token[0:])
    else:
        return (None,token[0:])

def term(temp, top = True):
    token = temp[0:]
    r = factor(token, False)
    if not r is None:
        (e1, token) = r
        if len(token) > 0:
            if token[0] == '+':
                token = token[1:]
                r = term(token, False)
                if not r is None:
                    (e2, token) = r
                    if not top or len(token) == 0:
                        return ({'Plus': [e1, e2]}, token)
    if not top or len(token) == 0:
        return (r)
    return (None)
def factor(temp, top = True):
    token = temp[0:]
    r = lFact(token)
    if not r is None:
        (e1, token) = r
        if len(token) > 0:
            if token[0] == '*':
                token = token[1:]
                r = factor(token, False)
                if not r is None:
                    (e2, token) = r
                    if not top or len(token) == 0:
                        return ({'Mult':[e1, e2]}, token)
    if not top or len(token) == 0:
        return (r)
    return (None)
def lFact(token):
    if token[0] == 'if' and token[1] == '(':
        token= token[2:]
        r=formula(token,False)
        if not r is None:
            (e1,token)=r
            if token[0]==',':
                token=token[1:]
                r=term(token,False)
                if not r is None:
                    (e2,token)=r
                    if token[0]==',':
                        token=token[1:]
                        r=term(token,False)
                        if not r is None:
                            (e3,token)=r
                            if token[0]==')':
                                token=token[1:]
                                return ({'If': [e1,e2,e3]},token)
    if token[0] == '(':
        token = token[1:]
        r = term(token, False)
        if not r is None:
            (e1, token) = r
            if token[0] == ')':
                token = token[1:]
                return ({'Parens':[e1]}, token)
    r = variable(token)
    if not r is None:
        (e1, token) = r
        return ({'Variable':[e1]}, token)
    r = number(token)
    if not r is None:
        (e1, token) = r
        return ({'Number':[e1]}, token)

def program(temp, top = True):
    token = temp[0:]
    if len(token) > 0:
        if token[0] == 'print':
            token = token[1:]
            r = expression(token)
            if not r is None:
                (e1, token) = r
                if token[0] == ';':
                    token = token[1:]
                    r = program(token, False)
                    if not r is None:
                        (e2, token) = r
                        if not top or len(token) == 0:
                            return ({'Print':[e1, e2]}, token)

    token = temp[0:]
    if len(token) > 0:
        if token[0] == 'assign':
            token = token[1:]
            r = (variable(token))
            if not r is None:
                (e1, token) = r
                if token[0] == ':=':
                    token = token[1:]
                    r = expression(token,False)
                    if not r is None:
                        (e2, token) = r
                        if token[0] == ';':
                            token = token[1:]
                            r = program(token, False)
                            if not r is None:
                                (e3, token) = r
                                if not top or len(token) == 0:
                                    if e1==None:
                                        return None
                                    if e2==None:
                                        return None
                                    if e3==None:
                                        return None
                                    else:
                                        return ({'Assign':[{'Variable':[e1]}, e2, e3]}, token)

    token = temp[0:]
    if len(token) > 0:
        if token[0] == 'if':
            token = token[1:]
            r = expression(token,False)
            if not r is None:
                (e1, token) = r
                if token[0] == '{':
                    token = token[1:]
                    r = program(token, False)
                    if not r is None:
                        (e2, token) = r
                        if token[0] == '}':
                            token = token[1:]
                            r = program(token, False)
                            if not r is None:
                                (e3, token) = r
                                if not top or len(token) == 0:
                                    if e1==None:
                                        return None
                                    if e2==None:
                                        return None
                                    if e3==None:
                                        return None
                                    else:
                                        return ({'If':[e1, e2, e3]}, token)

                
                
            
    token = temp[0:]
    if len(token) > 0:
        if token[0] == 'do' and token[1]=='{':
            token = token[2:]
            r = program(token,False)
            if not r is None:
                (e1, token) = r
                if token[0] == '}' and token[1]=='until':
                    token = token[2:]
                    r = expression(token, False)
                    if not r is None:
                        (e2, token) = r
                        if token[0] == ';':
                            token = token[1:]
                            r = program(token, False)
                            if not r is None:
                                (e3, token) = r
                                if not top or len(token) == 0:
                                    if e1==None:
                                        return None
                                    if e2==None:
                                        return None
                                    if e3==None:
                                        return None
                                    else:
                                        return({'DoUntil':[e1, e2, e3]}, token)

   
    token = temp[:]
    if len(token) == 0 or token[0] == '}':
        return ('End', token)
    return (None)
def expression(temp,top=True):
    token = temp[0:]
    r = formula(token, False)
    if not r is None:
        (e1, token) = r
        if len(token) == 0 or token[0] == ';' or token[0] == '{':
            return (e1, token)
    
    token = temp[0:]
    r = term(token, False)
    if not r is None:
        (e1, token) = r
        if len(token) == 0 or token[0] == ';' or token[0] == '{':
            return (e1, token)
