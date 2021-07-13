import grammar_ginger
import re
a='NIAID'
b=a.lower()
print(b)
string=grammar_ginger.main(b)
string = ''.join(e for e in string if e.isalnum())
if re.match("^[a-zA-Z0-9_]*$", string):
	print ("Valid")  
else:
	 print("Invalid")
string=string[:-2]
print(string)