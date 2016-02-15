import re

exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())
exec(open('validate.py').read())

#remember, have a couple of print statements strewn about, as well as in parse at the end

string1 = "@ a := [1+2,4,6];"
string2 = "loop $ hello from 3 {print true ;} print false ;"
string3 = "@ a := [1+2,4,6]; print @ a[0];"

string4 = "@ a := [true,4,6];"
string5 = "loop $ hello from 3 {} print @ hello [2];"
string6 = "print 6 + true;"
string7 = "@ a := [1,2,3]; print $ a;"

string8 = "loop $ hello from -1 {print true;} print false;"
string9 = "loop $ hello from 0 {print 4;} print -1;"
string10 = "print false; print true; print false;"
string11 = "loop $ hello from 3 {print $ hello;} print $ hello;"

tree = {'Assign': [{'Variable': ['a']}, 'True', 'True', 'True', 'End']}
tree1 = {'Loop': [{'Variable': ['x']}, {'Number': [1]}, {'Loop': [{'Variable': ['x']}, {'Number': [1]}, {'Loop': [{'Variable': ['x']}, {'Number': [1]}, 'End', 'End']}, {'Print': [{'Number': [1]}, 'End']}]}, {'Loop': [{'Variable': ['x']}, {'Number': [1]}, {'Loop': [{'Variable': ['x']}, {'Number': [1]}, 'End', 'End']}, {'Loop': [{'Variable': ['x']}, {'Number': [1]}, 'End', 'End']}]}]}
tree2 = {'Loop': [{'Variable': ['x']}, {'Number': [1]}, 
	{'Loop': [{'Variable': ['x']}, {'Number': [1]}, 
		'End', 
		{'Print': [{'Number': [1]}, 'End']}]}, 
	'End']}
'''
print (tokenizeAndParse(string1))
#{'Assign': [{'Variable': ['a']}, {'Plus': [{'Number': [1]}, {'Number': [2]}]}, {'Number': [4]}, {'Number': [6]}, 'End']}

print (tokenizeAndParse(string2))
#{'Loop': [{'Variable': ['hello']}, {'Number': [3]}, {'Print': ['True', 'End']}, {'Print': ['False', 'End']}]}

print(tokenizeAndParse(string3))
#{'Assign': [{'Variable': ['a']}, {'Plus': [{'Number': [1]}, {'Number': [2]}]}, {'Number': [4]}, {'Number': [6]}, {'Print': [{'Element': [{'Variable': ['a']}, {'Number': [0]}]}, 'End']}]}

print(interpret(string2))
#['True', 'True', 'True', 'True', 'False']

print(interpret(string3))
#[{'Number': [3]}]

print(interpret(string4))
#Ain't assigning right!

print(interpret(string5))
#Ain't accessing arrays right! // Ain't printing right! // Ain't looping programs right!

print(interpret(string6))
#Ain't adding right! // Ain't printing right!

print(interpret(string7))
#Ain't using loop-numbers right! // Ain't printing right! // Ain't assigning right!

print(compileAndSimulate(string3))
#[3]

print(compileAndSimulate(string2))
#[1,1,1,1,0]

print(compileAndSimulate(string8))
#[0]

print(compileAndSimulate(string9))
#[4,-1]

print(compileAndSimulate(string10))
#[0,1,0]

print(compileAndSimulate(string11))
#[3,2,1,0,-1]

print(interpret(string11))
#[{'Number': [3]}, {'Number': [2]}, {'Number': [1]}, {'Number': [0]}, {'Number': [-1]}]

print(interpret(string8))
#['False']
'''
exhaustive(4)
#print(tree2)
#print(simulate(compileProgram({}, tree2)[1]))
#print(execProgram({}, tree2)[1])
#













































