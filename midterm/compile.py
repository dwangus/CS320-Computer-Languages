#####################################################################
# David Wang
# CAS CS 320, Fall 2015
# Midterm
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                num = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(num)], heap, heap)
            elif label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                (instsop1, addrop1, heap1) = compileExpression(env, e1, heap)
                (instsop2, addrop2, heap2) = compileExpression(env, e2, heap1)
                heap3 = heap2 + 1
                instsPlus = [copy(addrop1,1)
                + copy(addrop2,2)
                + ['add',]
                + copy(0,heap3)]
                addrPlus = heap3
                return ((instsop1 + instsop2 + sum(instsPlus,[])), addrPlus, heap3)
            elif label == 'Element':
                varname = children[0]['Variable'][0]
                expr = children[1]
                (instsExpr, addrexpr, heap1) = compileExpression(env, expr, heap)
                varaddr = None
                if varname in env:
                    varaddr = env[varname]
                else:
                    print(varname + " is unbound/not defined.")
                    return None
                    #exit()
                heap2 = heap1 + 1
                addrEl = heap2
                instsOffset = [copy(addrexpr, 1) +
                ['set 2 '+str(varaddr),
                 'add',] +
                copyFromRef(0, heap2)]
                return ((instsExpr + sum(instsOffset,[])),addrEl, heap2)
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return ([], str(env[x]), heap)
                else:
                    print(x + " is unbound/not defined.")
                    return None
                    #exit()
    elif type(e) == Leaf:
        if e == 'True':
            heap += 1
            inst = 'set '+str(heap)+' 1'
            addr1 = heap
            return([inst],addr1,heap)
        if e == 'False':
            heap += 1
            inst = 'set '+str(heap)+' 0'
            addr1 = heap
            return([inst],addr1,heap)

def compileProgram(env, s, heap = 7):
    #if heap == 7:
    #    wellTyped = typeProgram({},s)
    #    if wellTyped == None:
    #        return({},None)
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            elif label == 'Loop':
                var = children[0]['Variable'][0]
                num = str(children[1]['Number'][0])
                pbody = children[2]
                prest = children[3]
                fresh = freshStr()
                heap2 = heap + 1
                
                instsSet = ['set '+str(heap2)+' '+num,]
                
                if var in env:
                    instsVar = copy(heap2, env[var])
                else:
                    env[var] = heap2
                    instsVar = []
                instsStart1 = ['label startLoop'+fresh,'branch startLoop2'+fresh+' '+str(env[var]),]
                #proginstructions
                instsStart2 = copy(env[var],1) + ['set 2 -1','add',] + copy(0,env[var]) + ['goto endLoop'+fresh,'label startLoop2'+fresh,]
                #goto endloop
                #label startLoop2
                (env2, instsBody, heap3) = compileProgram(env, pbody, heap2)
                #proginstructions
                iE1 = copy(env[var],1)  #<-- Decrement whatever's in the address of env[var]
                iE2 = ['set 2 -1','add',] #<-- THE FRUSTRATION OF SYNTAX
                iE3 = copy(0,env[var])
                #decrement
                iE4 = ['goto startLoop'+fresh,'label endLoop'+fresh,]
                #goto startLoop
                #label endLoop
                instsEnd = iE1 + iE2 + iE3 + iE4
                (env3, instsRest, heap4) = compileProgram(env2, prest, heap3)
                
                return (env3, instsSet + instsVar + instsStart1 + instsBody + instsStart2 + instsBody + instsEnd + instsRest, heap4)
            elif label == 'Assign':
                varname = children[0]['Variable'][0]
                e1 = children[1]
                e2 = children[2]
                e3 = children[3]
                prog = children[4]
                (instsE1, addr1, heap1) = compileExpression(env, e1, heap)
                (instsE2, addr2, heap2) = compileExpression(env, e2, heap1)
                (instsE3, addr3, heap3) = compileExpression(env, e3, heap2)
                heapE1 = heap3 + 1
                heapE2 = heap3 + 2
                heapE3 = heap3 + 3
                instsEle = copy(addr1,heapE1) + copy(addr2,heapE2) + copy(addr3,heapE3)
                if varname in env:
                    instsAssign = copy(heapE1, env[varname])
                else:
                    env[varname] = heapE1
                    instsAssign = []
                (env2, instsProg, heapP) = compileProgram(env, prog, heapE3)
                return (env2, instsE1 + instsE2 + instsE3 + instsEle + instsAssign + instsProg, heapP)

def compile(s):
    parseTree = tokenizeAndParse(s)
    wellTyped = typeProgram({},parseTree)
    if wellTyped == None:
        #print("It ain't well-typed! Fix yo shit!")
        #exit()
        return None
    alive = eliminateDeadCode(parseTree)
    folded = foldConstants(alive)
    (env, insts, heap) = compileProgram({}, folded)
    instsStackSet = ['set 7 -1',]
    finalInsts = instsStackSet + insts
    return finalInsts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
























