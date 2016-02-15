import re

exec(open('parse.py').read())
exec(open('interpret.py').read())

string1 = "print 1;"
string2 = "print true;"
print (tokenizeAndParse(string2))
print(interpret(string1))
