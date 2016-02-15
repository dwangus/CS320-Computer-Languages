#####################################################################
#
#David Wang
#CAS CS320, Lapets
#Fall 2015
#Assignment 3, machine.py

def simulate(s):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
    control = 0
    outputs = []
    while control < len(instructions):
        # Update the memory address for control.
        mem[6] = control 
        
        # Retrieve the current instruction.
        inst = instructions[control]
        
        # Handle the instruction.
        if inst[0] == 'label':
            pass
        if inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'branch' and mem[int(inst[2])]:
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        if inst[0] == 'set':
            mem[int(inst[1])] = int(inst[2])
        if inst[0] == 'copy':
            mem[mem[4]] = mem[mem[3]]
        if inst[0] == 'add':
            mem[0] = mem[1] + mem[2]

        # Push the output address's content to the output.
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1

        # Move control to the next instruction.
        control = control + 1

    print("memory: "+str(mem))
    return outputs

# Examples of useful helper functions from lecture.    
def copy(frm, to):
   return [\
      'set 3 ' + str(frm),\
      'set 4 ' + str(to),\
      'copy'\
   ]

#use negative memory addresses, starting at -1, for the stack;
#use memory address 7 to store the memory address of the top of the stack;
#use memory addresses 8 and higher for the heap (i.e., results of computations).

#return a list of instructions (in which each instruction is represented as a string in the list)
#instructions should correspond to machine level program that'd increment by 1 the integer stored in the memory location (addr)
#AND cleans up any memory addresses it used in the process by setting them back to 0
def increment(addr):
    inst = [copy(addr,1)        #copy what value is at address (addr) to memory-address-3 ==> @1: value@(addr)
    + [ 'set 2 1',              #memory-address-2 now has integer 1 ==> @2: (int)1 // so now, the value that we want to increment is now at memory-address-1, and the integer 1 is in memory address 2
        'add',]                 #the value @memory-address-0 now has the appropriate incremented value
    + copy(0,addr)              #copy what's in memory-address-0 (which is the appropriated incremented value) to the memory address of (addr)
    + [ 'set 0 0',
        'set 1 0',
        'set 2 0',
        'set 3 0',
        'set 4 0',]]
    return sum(inst,[])

def decrement(addr):
    inst = [copy(addr,1)
    + ['set 2 -1',
       'add',]
    + copy(0,addr)
    + ['set 0 0',
       'set 1 0',
       'set 2 0',
       'set 3 0',
       'set 4 0',
    ]]
    return sum(inst,[])

#unless the control index (memory address 6) is different from the way the simulator does it...
#I have no idea how else to go to the address in [7] and increment it directly
#...because you'd have to go [7]'s address (say addr1), then increment [addr1] ALL IN ONE GO before the control index changes again
#OHHHHHH, you skip the continually incremented control index of calling machine instructions IN procedure(name,body) -- which should be some
#   constant dependent upon the length of your code
#... actually, that part of procedure(name,body), where he chooses to implement this +constant in his pseudo-code, is instead specified to be done
#   in call(name)... either way, works... Welllll, if we want to use "jump a" right, it'd make more sense to do the adding in procedure().
def call(name):
    inst = [copy(7,1)
    + ['set 2 -1',
       'add',]
    + copy(0,7)
    + copy(7,4)
    + ['set 3 6',               #[6] = control index
       'copy',                  #top of stack now has THIS location, as per whatever was in the control index at this moment
       'goto '+str(name),]      #this instruction is @[top of stack]+1
    #+ copy(7,3)                -- what would have been the crucial "incrementing" step in call(name), is instead implemented in procedure()
    #+ ['set 4 1',               
    #   'set 2 #',               
    #   'copy',                  
    #   'add',]                   
    #+ copy(7,4)                 
    #+ ['set 3 0',               
    #   'copy',                  
    #   'goto '+str(name),]
    + copy(7,1)
    + ['set 2 1',
       'add',]
    + copy(0,7)]             #this instruction is@[top of stack]+2
    return sum(inst,[])

def procedure(name, body):
    inst = [['goto '+str(name)+'End',
            'label '+str(name),]
    + body
    + copy(7,3)                 #[7] = top-of-stack-address
    + ['set 4 1',               #to-address is 1 (first operand of sum operation)
       'copy',                  #whatever was in @[top-of-stack-address] (-- which was the ith instruction-location stored by call(name)) is now in @[1]
       'set 2 2',               #set 2 to some number -- which is (constant)2 in the call(name) function, directly to the increment(7) portion
       'add',                   #add @[1] to @[2] and store in [0]
       'jump 0',                #jump to @[0] -- which is 2 + where the last location that invoked this procedure was
       'label '+str(name)+'End',]]
    return sum(inst,[])
        

# eof
















































