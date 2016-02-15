#####################################################################
#
#David Wang
#CAS CS320, Lapets
#Fall 2015
#Assignment 3, compile.py

exec(open('parse.py').read())
exec(open('machine.py').read())

Node = dict
Leaf = str

#Potential Issues:
#NTI = Need To Implement
#1. What if memory addresses on the heap are used again to create multiple of the same labels?
#           Might need to find a way around that... Maybe a global counter? --> Yea, Lapets said it was ok to create a global fresh counter
#2. Might need a flag for evaluating expressions in compileFormula, as like in my interpret.py
#3. Where are the stack and heap pointers first initialized to?
#       You know what, since you only call compile(s) once, you can probably add initial instructions like
#       'set 7 -1', and pass into compileProgram(env, parse-tree, 8)
#(NTI)4. Why is compile(s) purple?
#5. I'm concerned about the changing environments...
#       For example:
#           x = 0
#           if (false):
#               x = 3
#           x = x + 1
#           print x
#       His response: "Keep in mind that the env for compile.py has a different purpose than the env in interpret. Make sure you read question #3 carefully."
#       Ahhh... you know what, I think it's because env is a mapping from variables to memory addresses -- it doesn't store procedures, as it did in interpret.py
#       The problem was in "Assign", fixed!
#6. Need to include the other files in compile.py -- or does he do it for us?
#       Yea, he does.
global fresh
fresh = 0

#'Plus', 'Number', 'Variable'
#function should return a tuple of (insts, addr, heap)
global count1
global count2
global flag
flag = False
def compileTerm(env, t, heap):
    global fresh, count1, count2, flag
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                (instsop1, addrop1, heap1) = compileTerm(env, t1, heap)
                (instsop2, addrop2, heap2) = compileTerm(env, t2, heap1)
                heap3 = heap2 + 1
                instsPlus = [copy(addrop1,1)
                + copy(addrop2,2)
                + ['add',]
                + copy(0,heap3)]
                addrPlus = heap3
                return ((instsop1 + instsop2 + sum(instsPlus,[])), addrPlus, heap3)
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return ([],str(env[x]),heap)
                else:
                    print(x + " is unbound/not defined.")
                    exit()
            elif label == 'Number':
                num = children[0]
                if flag == False and num > 0:
                    count1 = children[0]
                    flag = True
                else:
                    count2 = children[0]
                    flag == False
                heap = heap + 1
                inst = 'set ' + str(heap) + ' ' + str(num)
                addr1 = heap
                return ([inst], addr1, heap)

#"Variable", "True", "False", "Xor", "And", "Not"
def compileFormula(env, f, heap):
    global fresh, count1, count2
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return ([],str(env[x]),heap)
                else:
                    print(x + " is unbound/not defined.")
                    exit()
            elif label == 'Xor':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap1) = compileFormula(env, f1, heap)
                (insts2, addr2, heap2) = compileFormula(env, f2, heap1)
                heap3 = heap2 + 1
                instsXor = [copy(addr1,1) +
                copy(addr2,2) +
                ['add',
                 'set 2 -1',
                 'add',
                 'branch setFalse'+str(fresh)+' 0',
                 'set '+str(heap3)+' 1',
                 'goto finish'+str(fresh),
                 'label setFalse'+str(fresh),
                 'set '+str(heap3)+' 0',
                 'label finish'+str(fresh),]]
                instsXor = sum(instsXor,[])
                fresh += 1
                addr3 = heap3
                return (insts1 + insts2 + instsXor, addr3, heap3)
            elif label == 'And':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap1) = compileFormula(env, f1, heap)
                (insts2, addr2, heap2) = compileFormula(env, f2, heap1)
                heap3 = heap2 + 1
                instsAnd = ['branch secondOp'+str(fresh)+' '+str(addr1),
                 'set '+str(heap3)+' 0',
                 'goto finish'+str(fresh),
                 'label secondOp'+str(fresh),
                 'branch And'+str(fresh)+' '+str(addr2),
                 'set '+str(heap3)+' 0',
                 'goto finish'+str(fresh),
                 'label And'+str(fresh),
                 'set '+str(heap3)+' 1',
                 'label finish'+str(fresh),]
                fresh += 1
                addr3 = heap3
                return (insts1 + insts2 + instsAnd, addr3, heap3)
            #extra-credit option
            elif label == 'Equal':
                t1 = children[0]
                t2 = children[1]
                (insts1, addr1, heap1) = compileTerm(env, t1, heap)
                (insts2, addr2, heap2) = compileTerm(env, t2, heap1)
                heap3 = heap2 + 1
                instsEqual = ['set 1 -'+str(count1),
                'set 2 '+str(count2),
                'add',
                'branch notEqual'+str(fresh)+' 0',
                'set '+str(heap3)+' 1',
                'goto finish'+str(fresh),
                'label notEqual'+str(fresh),
                'set '+str(heap3)+' 0',
                'label finish'+str(fresh),]
                fresh += 1
                addr3 = heap3
                return (insts1 + insts2 + instsEqual, addr3, heap3)
            elif label == 'Not':
                f1 = children[0]
                (insts1, addr1, heap1) = compileFormula(env, f1, heap)
                instsNot = ['branch setFalse'+str(fresh)+' '+str(addr1),
                 'set '+str(addr1)+' 1',
                 'goto finish'+str(fresh),
                 'label setFalse'+str(fresh),
                 'set '+str(addr1)+' 0',
                 'label finish'+str(fresh),]
                fresh += 1
                return (insts1 + instsNot, addr1, heap1)
    elif type(f) == Leaf:
        flag = False
        if f == 'True':
            heap += 1
            inst = 'set '+str(heap)+' 1'
            addr1 = heap
            return([inst],addr1,heap)
        if f == 'False':
            heap += 1
            inst = 'set '+str(heap)+' 0'
            addr1 = heap
            return([inst],addr1,heap)
    return compileTerm(env, f, heap)

#use negative memory addresses, starting at -1, for the stack;
#use memory address 7 to store the memory address of the top of the stack;
#use memory addresses 8 and higher for the heap (i.e., results of computations).
#"Print", "Assign", "If", "Until", "End", "Procedure", "Call"
        #should be returning a tuple of (env, insts, heap)
def compileProgram(env, s, heap):
    global fresh
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                exprTree = children[0]
                progTree = children[1]
                (instsExpr, addr1, heap1) = compileFormula(env, exprTree, heap)
                instsPrint = copy(addr1,5)
                (env2, instsProg, heap2) = compileProgram(env, progTree, heap1)
                return (env2, instsExpr + instsPrint + instsProg, heap2)
            elif label == 'Assign':
                varname = children[0]['Variable'][0]
                exprTree = children[1]
                progTree = children[2]
                (instsExpr, addr1, heap1) = compileFormula(env, exprTree, heap)
                #my version to circumvent the updated assigned variable, but the other way works cleaner
                '''if varname in env:
                    heapx = heap + 1
                    (instsExpr, addr1, heap1) = compileFormula(env, exprTree, heapx)
                    env[varname] = heap
                    instsCopy = copy(addr1,heap)
                    (env2, instsProg, heap2) = compileProgram(env, progTree, heap1)
                    return (env2, instsExpr + instsCopy + instsProg, heap2)
                else:
                    (instsExpr, addr1, heap1) = compileFormula(env, exprTree, heap)
                    env[varname] = addr1
                    (env2, instsProg, heap2) = compileProgram(env, progTree, heap1)
                    return (env2, instsExpr + instsProg, heap2)'''
                if varname in env:
                    instsAssign = copy(addr1, env[varname])     #doesn't actually copy whatever's in addr1 into varname's memory address, just lists INSTRUCTIONS to do so
                else:
                    env[varname] = addr1
                    instsAssign = []
                (env2, instsProg, heap2) = compileProgram(env, progTree, heap1)
                return (env2, instsExpr + instsAssign + instsProg, heap2)
            elif label == 'If':
                exprTree = children[0]
                bodyTree = children[1]
                restTree = children[2]
                (instsExpr, addr1, heap1) = compileFormula(env, exprTree, heap)
                instsIfTrue = [copy(addr1,1) + 
                ['set 2 -1',
                 'add',
                 'branch IfFalse'+str(fresh)+' 0',]]
                instsIfTrue = sum(instsIfTrue,[])
                (env2, instsBody, heap2) = compileProgram(env, bodyTree, heap1)
                instsIfFalse = ['label IfFalse'+str(fresh),]
                (env3, instsRest, heap3) = compileProgram(env2, restTree, heap2)
                fresh += 1
                return (env3, instsExpr + instsIfTrue + instsBody + instsIfFalse + instsRest, heap3)
            elif label == 'Until':
                condition = children[0]
                body = children[1]
                rest = children[2]
                (instsCond, addr1, heap1) = compileFormula(env, condition, heap)
                (env2, instsBody, heap2) = compileProgram(env, body, heap1)
                instsUntil = ['label startUntilLoop'+str(fresh),
                 'branch endLoop'+str(fresh)+' '+str(addr1),]
                instsUntil2 = ['goto startUntilLoop'+str(fresh),
                 'label endLoop'+str(fresh),]
                fresh += 1
                (env3, instsRest, heap3) = compileProgram(env2, rest, heap2)
                return (env3, instsCond + instsUntil + instsBody + instsUntil2 + instsRest, heap3) 
            elif label == 'Call':
                varname = children[0]['Variable'][0]
                progTree = children[1]
                xp1 = []
                if varname in env:
                    xp1 = xp1 + call(varname)
                    (env2, instsProg, heap1) = compileProgram(env, progTree, heap)
                    return(env2, xp1 + instsProg, heap1)
                else:
                    print(varname + " is not defined in the environment, and thus did not compile.")
                    exit()
            #huh... procedures aren't stored in the environment. Well, then...
            #wait, then what if you call a procedure that doesn't exist? It will mess up the entire stack pointer...
            #maybe we store the procedure name in the environment? Such that, if it ever does get called yet doesn't exist,
            #   we simply don't compile those instructions...
            elif label == 'Procedure':
                x = children[0]['Variable'][0]
                pbody = children[1]
                prest = children[2]
                if x in env:
                    print(x + " is already defined.")
                    exit()
                else:
                    env[x] = 'hello' #store the variable name in the environment, so as to let Call() know whether or not the procedure has already been compiled somewhere in the program
                    (env2, instsBody, heap1) = compileProgram(env, pbody, heap)
                    (env3, instsRest, heap2) = compileProgram(env2, prest, heap1)
                    return(env3, procedure(x,instsBody) + instsRest, heap2)
                
def compile(s):     #uhhhh what, why is it purple
    parseTree = tokenizeAndParse(s)
    (env, insts, heap) = compileProgram({}, parseTree, 8)
    instsStackSet = ['set 7 -1',]
    finalInsts = instsStackSet + insts
    return finalInsts


#eof


































