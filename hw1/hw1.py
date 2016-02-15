import re

def regexp(tokenlist):
    newtok = tokenlist
    for index in range(len(newtok)):
        newtok[index] = re.escape(newtok[index])
    #sym = "((\s+)|(" + "|".join(newtok) + "))"
    sym = "(" + "|".join(newtok) + ")"
    return sym

def tokenize(tokens, s):
    r = regexp(tokens)
    if ('\ ' not in tokens):
        s = ''.join(s.split())
    split = re.split(r, s)
    tokensequence = []
    for item in split:
        if item != '' and item != None:
            tokensequence.append(item)
    return tokensequence

def tree(tokensequence):
    #for grammar choice 1:
    if tokens[0] == "two" and tokens[1] == "children" and tokens[2] == "start":
        (t, tokens) = tree(token[3:])
        if tokens[0] == 
        
    #for grammar choice 2:
    if tokens[0] == "one" and tokens[1] == "child" and tokens[2] == "start":
        (t, tokens) = tree(token[3:])
        if tokens[0] == "end":
            return ({"one": t}, tokens[1:])
    #backtracking refers to keeping track of previous nodes -- bsaically tree traversal

