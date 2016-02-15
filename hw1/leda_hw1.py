#Lida Karadimou
import re

#Exercise 1a
def regexp(tokens):
    string=''
    for i in range(0,len(tokens)):
        string=string+tokens[i]
        if i<(len(tokens)-1):
            string=string+'|'
    #string=''.join(tokens)
    #print(string)
    #print(string)
    return string

#Exercise 1b
def tokenize(terminals, csyntax):
    a = (re.escape(x) for x in terminals)
    regex = "(\s+|"
    regex += "|".join(a)
    regex += ")"
    return [t for t in re.split(regex, csyntax) if not t.isspace() and not t == "" and not t==None]
"""
def tokenize(tokens,syntax):
    return [t for t in re.split("(\s+|"+regexp(tokens)+")",syntax) if not t.isspace() and not t== "" and not t==None]
       
def regexp(tokens) :
        string=""
        for x in range(0,len(tokens)):
                if tokens [x] == ("*"):
                    string=string+"\\"
                if tokens [x] == ("+"):
                    string=string+"\\"
                if tokens [x] == ("("):
                    string=string+"\\"
                if tokens [x] == (")"):
                    string=string+"\\"
                string=string+tokens[x]
                if x<(len(tokens)-1):
                    string=string+"|"
        return string"""
"""def tokenize(terminals, csyntax):
    a = (re.escape(x) for x in terminals)
#    regex = "(\s+|"
#    regex += "|".join(a)
 #   regex += ")" 
    return [t for t in re.split("(\s+|"+regexp(terminals)+")", csyntax) if not t.isspace() and not t == "" and not t==None]"""

#1c
def tree(tmp, top = True):
    tokens = tmp[0:]
    if tokens[0] == 'zero' and tokens[1]=='children':
        tokens = tokens[2:]
        if not top or len(tokens) == 0:
            return ('Zero', tokens)

    tokens = tmp[0:]
    if tokens[0] == 'one' and tokens[1] == 'child' and tokens[2] == 'start':
        tokens = tokens[3:]
        r = tree(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == 'end':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return ({'One':[e1]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'two' and tokens[1]== 'children' and tokens[2]=='start':
        tokens = tokens[3:]
        r = tree(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ';':
                tokens = tokens[1:]
                r = tree(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == 'end':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Two':[e1,e2]}, tokens)#does not return unparsed tokens!!!

"""def number(tokens, top = True):
    if re.match(r"^([1-9][0-9]*|-[1-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])"""

def number(tokens, top): 
    if re.match(r"^([1-9][0-9]*|-[1-9][0-9]*)$", tokens[0]):
        return (({"Number": [int(tokens[0])]}, tokens[1:])) #used for the extension of negative numbers, required for exercise 3

def variable(tokens, top = True):
    if re.match(r"^([a-z]*)$", tokens[0]):
        return ({"Variable": [str(tokens[0])]}, tokens[1:])
"""
def term(tmp, top = True):
    seqs = [\
        ('Number', ['#',number]), \
        ('Variable',['$',variable])
        ('Plus',['plus','(',term,',',term,')']),\
        ('Plus',['(',term,'+',term,')']),\
        ('Max',['max','(',term,',',term,')']),\
        ('Max',['(',term,'max',term,')']),\
        ('If',['if','(',formula,',',term,',',term,')']),\
        ('If',[formula,'?',term,':',term,')'])\
        ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect formula trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.
        for x in seq:
            if type(x) == type(""): # Terminal.
                if tokens[0] == x: # Does terminal match token?
                    #print(tokens[0])
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        # Check that we got either a matched token
        # or a formula tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
"""

def term(tokens, top= True):

    if tokens[0] == '#':
        r=number(tokens[1:],False)
        if r is not None:
            (e1,tokens)=r
            return (e1,tokens)
    
    if tokens[0] == '$':
        r=number(tokens[1:],False)
        if r is not None:
            (e1,tokens)=r
            return (e1, tokens)
    
    if tokens[0] == 'plus' and tokens[1] == '(':
        #(e1, tokens) = term(tokens[2:], False)
        r=term(tokens[2:], False)
        if r is not None:
            (e1, tokens)=r
            if tokens[0] == ',':
                r=term(tokens[1:], False)
                #(e2, tokens) = term(tokens[1:], False)
                if r is not None:
                    (e2,tokens)=r
                    if tokens[0] == ')':
                        return ({'Plus':[e1, e2]}, tokens[1:])
                
    if tokens[0] == 'max' and tokens[1] == '(':
        r=term(tokens[2:], False)
        #(e1, tokens) = term(tokens[2:], False)
        if r is not None:
            (e1, tokens)=r
            if tokens[0] == ',':
                r=term(tokens[1:], False)
                #(e2, tokens) = term(tokens[1:], False)
                if r is not None:
                    (e2,tokens)=r
                    if tokens[0] == ')':
                        return ({'Max':[e1, e2]}, tokens[1:])

               
    if tokens[0] == 'if' and tokens[1] == '(':
        r=formula(tokens[2:], False)
        #(e1, tokens) = term(tokens[2:], False)
        if r is not None:
            (e1, tokens)=r
            if tokens[0] == ',':
                #(e2, tokens) = term(tokens[1:], False)
                r= term(tokens[1:], False)
                if r is not None:
                    (e2, tokens)=r
                    if tokens[0] == ',':
                        r=term(tokens[1:],False)
                        if not r is None:
                            (e3, tokens)=r
                        #(e3, tokens) = term(tokens[1:], False)
                        #(e2, tokens)=
                            if tokens[0]==')':
                                return ({'If':[e1, e2,e3]}, tokens[1:])
"""def term(tokens, top= True):
    if tokens[0] == '#':
        r=number(tokens[1:],False)
        if r is not None:
            (e1,tokens)=r
            return (e1,tokens)
    if tokens[0] == '$':
        return ({'Variable':[tokens[1]]}, tokens[2:])
    if tokens[0] == 'plus' and tokens[1] == '(':
        (e1, tokens) = term(tokens[2:], False)
        if tokens[0] == ',':
            (e2, tokens) = term(tokens[1:], False)
            if tokens[0] == ')':
                return ({'Plus':[e1, e2]}, tokens[1:])
    if tokens[0] == 'max' and tokens[1] == '(':
        (e1, tokens) = term(tokens[2:], False)
        if tokens[0] == ',':
            (e2, tokens) = term(tokens[1:], False)
            if tokens[0] == ')':
                return ({'Max':[e1, e2]}, tokens[1:])
    if tokens[0] == 'if' and tokens[1] == '(':
        (e1, tokens) = formula(tokens[2:], False)
        if tokens[0] == ',':
            (e2, tokens) = term(tokens[1:], False)
            if tokens[0] == ',':
                (e3, tokens) = term(tokens[1:], False)
                if tokens[0]==')':
                    return ({'If':[e1, e2]}, tokens[1:])"""
                        
def formula(tmp, top = True):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Not', ['not', '(', formula, ')']), \
        ('Xor', ['xor', '(', formula,',', formula, ')']), \
        ('Xor', ['(', formula, 'xor', formula, ')']),\
        ('Less',['less','(', term,',', term,')']),\
        ('Less',['(', term, '<', term, ')']),\
        ('Greater',['greater','(', term,',', term,')']),\
        ('Greater',['(', term, '>', term, ')']),\
        ('Equal', ['equal','(', term, ',', term, ')']),\
        ('Equal',['(',term,'=','=',term,')'])\
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.
        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)

def program(tmp,top=True):
    seqs=[\
        ('Print',['print',term,';',program]),\
        ('Input',['input','$',variable,';',program]),\
        ('Assign',['assign','$',variable,':','=',term,';',program]),\
        ('End',['end',';'])\
        ]
    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect formula trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.
        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x: # Does terminal match token?
                    #print('tokens[0]',tokens[0])
                    #print('x',x)
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
                
            #print(es)
        #print('label:', label)
        #print(ss)
        #print(es)
        #print(seq)
        # Check that we got either a matched token
        # or a formula tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    

        
def parse(s):
    gram=['print',';','input','$','assign',':','=',\
          'end','true','false','not','(',')','xor',\
          'equal','less','greater','<','>','#','+',\
          '?','if',',']
    a=tokenize(gram,s)
    #(b,c)=program(a)
    #(b,c)=program(a)
    #if a is None:
    #    (b,c)=program(a)
    #    return b
    #if not a is None:
    #    (b,c)=program(a)
    #(b,c)=program(a)
    """if not a is None:
        (b,c)=program(a)
        return b"""
    """if a is not(None):
        (b,c)=program(a)
        return b
    elif a is None:
        return None"""
    tupleRes=program(tokenize(gram,s))
    if not tupleRes is None:
        return tupleRes[0]

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
        except Exception as e:
            output = '<Error>'

        if output != '<Error>' and output == result:
            passed = passed + 1
        else:
            print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")
